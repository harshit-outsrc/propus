"""
This module contains helper functions for working with Canvas, which combine other services (such as the Calbright
database) to perform operations.
"""

import asyncio

import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from typing import Literal, Optional, Union

from .exceptions import MissingCourseLmsId, MissingCanvasUserId, NoEnrollmentFound, NoCourseEnrollmentsFound

from propus.calbright_sql.course_version_section import CourseVersionSection
from propus.calbright_sql.enrollment import LMS, Enrollment
from propus.calbright_sql.enrollment_status import EnrollmentStatus
from propus.calbright_sql.user import User
from propus.calbright_sql.user_lms import UserLms

from propus.canvas import Canvas

from propus.logging_utility import Logging

logger = Logging.get_logger("propus/helpers/canvas")


def create_canvas_user(
    user_type: Literal["student", "staff"],
    first_name: str,
    last_name: str,
    email_address: str,
    sis_user_id: str,
    session: Session,
    canvas: Canvas,
    user_object: Optional[User] = None,
):
    """
    Create a user in Canvas and insert a record in the user_lms table in the database
    Params:
        user_type (str): Either "student" or "staff"
        first_name (str): The user's first name
        last_name (str): The user's last name
        email_address (str): The user's email address
        sis_user_id (str): The user's SIS ID - For students this should be CCC_ID, for staff this should be
            the email address
        session (Session): The Calbright session object
        canvas (Canvas): The Canvas object
        user_object (User): An optional User object
    Returns:
        dict: A dictionary containing the Canvas ID (str), e.g. {"canvas_id": "12345"}

    Raises:
        UserIdTaken: If the user already exists in Canvas and for some reason there is not a record in
            the user_lms table
    """
    logger.info(f"Creating Canvas user for {sis_user_id}...")
    if user_object:
        user_response = user_object
    elif user_type == "student":
        user_response = session.execute(select(User).filter_by(ccc_id=sis_user_id)).scalar_one()
    elif user_type == "staff":
        user_response = session.execute(select(User).filter_by(email=email_address)).scalar_one()

    for user_lms in user_response.user_lms:
        if user_lms.lms == LMS("Canvas"):
            return {"canvas_id": user_lms.lms_id}
    # Create the user in Canvas if no existing Canvas ID is found in the database
    created_user = asyncio.run(
        canvas.create_user(
            user_type=user_type,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            sis_user_id=sis_user_id,
        )
    )

    # Insert a record for the user_lms table in the database
    canvas_id = created_user["id"]
    lms_record = UserLms(lms=LMS("Canvas"), lms_id=canvas_id, user=user_response)
    session.add(lms_record)
    session.commit()

    return {"canvas_id": canvas_id}


def create_course_sections(session: Session, canvas: Canvas):
    """
    Create sections in Canvas for courses that don't have a section created yet.
    - This operates by finding any course sections in the course_version_section table that don't have an LMS ID
    - After it creates the section it will write back the section ID to the course_version_section table
    - This function is intended to be run on a schedule (or db trigger) to create sections for new courses
    :param session: A Propus Calbright session object. E.g. Calbright.build().session
    :param canvas: A Propus Canvas object.
    :return: bool: True if sections were created, False if no sections were created
    """
    logger.info("Creating course sections...")
    sections_to_create = session.execute(select(CourseVersionSection).filter_by(lms=LMS("Canvas"), lms_id=None)).all()
    sections_created = False
    if not sections_to_create:
        return sections_created
    for section in sections_to_create:
        section_data = section[0]
        section_name = section_data.section_name
        program_version_course = section_data.program_version_course
        course_lms_id = program_version_course.course_version.lms_id
        if not course_lms_id:
            raise MissingCourseLmsId(course_version_id=program_version_course.course_version.id)

        created_section = asyncio.run(
            canvas.create_section(course_id=course_lms_id, name=section_name, sis_section_id=section_name)
        )
        logger.debug(f"Created section: {section_name} for course_id: {course_lms_id}")
        # Write the newly created section ID back to the section in the db
        section_data.lms_id = created_section.get("id")
        session.commit()
        sections_created = True

    return sections_created


def get_canvas_id_from_user_lms_list(user_lms_list: list[UserLms]):
    """
    This is a helper function to get the Canvas ID from a list of UserLms objects.
    :param user_lms_list: A list of UserLms objects
    :return: str: The Canvas ID if found, None if not found
    """
    for user_lms in user_lms_list:
        if user_lms.lms == LMS("Canvas"):
            logger.debug(f"Found canvas user ID {user_lms.lms_id}")
            return user_lms.lms_id
    return None


def get_student_enrollment(ccc_id: str, session):
    """
    This function will get the student's active enrollment record from the database.
    :param ccc_id: The student's CCC_ID
    :param session: A Propus Calbright session object. E.g. Calbright.build().session
    :return: Enrollment: The student's enrollment record
    """
    # TODO: can I get a re-check on this?
    try:
        student_enrollment = session.execute(
            select(Enrollment)
            .join(EnrollmentStatus, Enrollment.enrollment_status_id == EnrollmentStatus.id)
            .filter(Enrollment.ccc_id == ccc_id)
            .filter(EnrollmentStatus.status.in_(["Enrolled", "Started"]))
        ).scalar_one()
    except sqlalchemy.exc.NoResultFound:
        raise NoEnrollmentFound(ccc_id=ccc_id)

    return student_enrollment


def create_initial_course_enrollment(
    ccc_id: str,
    session: Session,
    canvas: Canvas,
    orientation_course_section_id: Union[int, None] = None,
):
    """
    Create initial course enrollment for a student.
    - This function should be called when a student is first enrolled.
    - It will find the student's Canvas user ID and enroll them in the first course in their program.
    - The first course is determined by the is_first_course_in_program flag on the ProgramVersionCourse record.
    - It will also create an account in Canvas for the student if one doesn't exist.

    :param ccc_id: The student's CCC_ID
    :param session: A Propus Calbright session object. E.g. Calbright.build().session
    :param canvas: A Propus Canvas object.
    :param orientation_course_section_id: The LMS ID of the orientation course section. If provided, the student will
        be enrolled in this section as well.
    :return: bool: True if the student was enrolled in a course, False if no course enrollment was created
    """
    logger.info(f"Creating initial course enrollment for {ccc_id}...")
    student_enrollment = get_student_enrollment(ccc_id=ccc_id, session=session)

    canvas_user_id = get_canvas_id_from_user_lms_list(student_enrollment.student.user.user_lms)

    if not canvas_user_id:
        logger.info("No canvas user ID found - creating user...")
        # If we don't find a Canvas ID, create a new user in Canvas (and store the ID in the user_lms table)
        created_user = create_canvas_user(
            user_type="student",
            first_name=student_enrollment.student.user.first_name,
            last_name=student_enrollment.student.user.last_name,
            email_address=student_enrollment.student.user.calbright_email,
            sis_user_id=ccc_id,
            session=session,
            canvas=canvas,
        )

        canvas_user_id = created_user["canvas_id"]

    # Get the students enrollments from the enrollment_course_term table in the database
    course_enrollments = student_enrollment.enrollment_enrollment_course_term
    if not course_enrollments:
        raise NoCourseEnrollmentsFound(ccc_id=ccc_id)

    enrolled = False
    # Go through the enrollments and get the first course in the program
    for course_enrollment in course_enrollments:
        if course_enrollment.course_version_section.program_version_course.is_first_course_in_program:
            section_id = course_enrollment.course_version_section.lms_id
            # TODO: I figured we can check to make sure the section exists and create it if for some reason it doesn't
            if not section_id:
                logger.info("no section ID found, creating section...")
                create_course_sections(session, canvas)
                # Get the newly committed section ID back from the DB...
                section_id = session.execute(
                    select(CourseVersionSection.lms_id).filter_by(id=course_enrollment.course_version_section.id)
                ).scalar_one()
            logger.info("creating enrollment for first course...")
            created_enrollment = asyncio.run(
                canvas.create_enrollment(
                    section_id=section_id, user_id=canvas_user_id, enrollment_type="StudentEnrollment"
                )
            )
            logger.debug(f"Created enrollment: {created_enrollment}")
            enrolled = True
            # TODO: we should find a place to store the created enrollment canvas ID.
            #   I don't think the enrollment_course_term table is the right place, tbd...

    if orientation_course_section_id:
        logger.info("Enrolling in orientation course...")
        orientation_enrollment = asyncio.run(
            canvas.create_enrollment(
                section_id=orientation_course_section_id, user_id=canvas_user_id, enrollment_type="StudentEnrollment"
            )
        )
        logger.debug(f"Created enrollment for orientation course: {orientation_enrollment}")
    return enrolled


def create_subsequent_course_enrollment(
    current_course_id: str, ccc_id: str, canvas_user_id: str, session: Session, canvas: Canvas
):
    """
    Create subsequent course enrollment for a student.
    - This function should be called when a student submits their last summative assignment.
    - It will find the student's Canvas user ID and enroll them in the next course in their program.
    - The next course is determined by the next_program_version_course_record field on the ProgramVersionCourse record.
    :param current_course_id: The LMS ID of the course the student just completed
    :param ccc_id: The student's CCC_ID
    :param canvas_user_id: The student's Canvas user ID
    :param session: A Propus Calbright session object. E.g. Calbright.build().session
    :param canvas: A Propus Canvas object.
    :return: bool: True if the student was enrolled in a course, False if no course enrollment was created
    """
    logger.info(f"Creating subsequent course enrollment for {ccc_id=}...")
    student_enrollment = get_student_enrollment(ccc_id=ccc_id, session=session)
    course_enrollments = student_enrollment.enrollment_enrollment_course_term
    next_course = None
    # Go through course term enrollments and see if there is a next course
    for course_enrollment in course_enrollments:
        if current_course_id == course_enrollment.course_version_section.program_version_course.course_version.lms_id:
            next_course = (
                course_enrollment.course_version_section.program_version_course.next_program_version_course_record
            )
            break
    # If there is a next course, go through course term enrollments and find the course section for the next course
    if next_course:
        for course_enrollment in course_enrollments:
            if course_enrollment.course_version_section.program_version_course == next_course:
                section_id = course_enrollment.course_version_section.lms_id
                created_enrollment = asyncio.run(
                    canvas.create_enrollment(
                        section_id=section_id, user_id=canvas_user_id, enrollment_type="StudentEnrollment"
                    )
                )
                logger.debug(f"Created enrollment: {created_enrollment}")
                # TODO: same as the initial enrollment, we should store the created enrollment ID somewhere...
                return True
    return False


def enroll_instructors_in_sections(session: Session, canvas: Canvas):
    """
    This function will enroll instructors in sections that have been created in Canvas, but for which the instructor
    has not been enrolled yet.
    - It will find the instructor's Canvas user ID and enroll them in the section.
    - It will write the Canvas enrollment ID back to the section in the database.
    - It will create a Canvas account for the instructor if one doesn't exist.
    :param session: A Propus Calbright session object. E.g. Calbright.build().session
    :param canvas: A Propus Canvas object.
    :return:
    """
    logger.info("Enrolling instructors in sections...")
    # Get all sections that have a canvas LMS ID (section has been created), but don't have an instructor enrolled yet
    enrollments_to_create = session.execute(
        select(CourseVersionSection)
        .filter_by(
            lms=LMS("Canvas"),
            instructor_enrollment_lms_id=None,
        )
        .filter(CourseVersionSection.lms_id.isnot(None))
    ).all()
    enrollments_created = False
    if not enrollments_to_create:
        return enrollments_created
    for enrollment in enrollments_to_create:
        section = enrollment[0]

        canvas_user_id = get_canvas_id_from_user_lms_list(section.instructor.user.user_lms)
        if not canvas_user_id:
            logger.info("No canvas user ID found - creating user...")
            created_user = create_canvas_user(
                user_type="staff",
                first_name=section.instructor.user.first_name,
                last_name=section.instructor.user.last_name,
                email_address=section.instructor.user.calbright_email,
                sis_user_id=section.instructor.user.calbright_email,
                session=session,
                canvas=canvas,
                user_object=section.instructor.user,
            )
            canvas_user_id = created_user["canvas_id"]

        # Enroll the instructor in the section
        section_id = section.lms_id
        logger.debug(f"Creating enrollment for section {section_id} and user {canvas_user_id}...")
        created_enrollment = asyncio.run(
            canvas.create_enrollment(section_id=section_id, user_id=canvas_user_id, enrollment_type="TeacherEnrollment")
        )

        # Add the Canvas enrollment ID to the section in the database
        section.instructor_enrollment_lms_id = created_enrollment["id"]
        session.commit()
        enrollments_created = True

    return enrollments_created

    # TODO: Note: If an instructor for a section _changes_ - then we should set the instructor_enrollment_lms_id to NULL
    #   so that it picks up the new instructor on the next run


def conclude_student_enrollments(ccc_id: str, session: Session, canvas: Canvas):
    """
    This function will conclude all of a student's enrollments in Canvas.
    Currently, it works by fetching all current enrollments from Canvas and then concluding all of those.
    If needed it can be adjusted to only conclude specific enrollments.
    :param ccc_id: The student's CCC_ID
    :param session: A Propus Calbright session object. E.g. Calbright.build().session
    :param canvas: A Propus Canvas object.
    :return: bool: True if the student's enrollments were concluded, False if no enrollments were concluded
    """
    logger.info(f"Concluding student enrollments for {ccc_id}...")
    # Get the student's enrollments from the enrollment_course_term table in the database
    student_enrollment = get_student_enrollment(ccc_id=ccc_id, session=session)
    canvas_user_id = get_canvas_id_from_user_lms_list(student_enrollment.student.user.user_lms)
    if not canvas_user_id:
        raise MissingCanvasUserId(ccc_id=ccc_id)

    # TODO: Note - for now I'm just concluding all of their Canvas enrollments. We may want to be more specific about
    #  which enrollments we're concluding, but we will need to store the Canvas enrollment ID somewhere to do that.
    canvas_enrollments = asyncio.run(canvas.list_enrollments(object_type="user", object_id=canvas_user_id))
    if not canvas_enrollments:
        return False
    for enrollment in canvas_enrollments:
        course_id = enrollment["course_id"]
        enrollment_id = enrollment["id"]
        logger.debug(f"concluding enrollment {enrollment_id} in course {course_id} for ccc_id {ccc_id}")
        asyncio.run(
            canvas.conclude_delete_deactivate_enrollment(
                course_id=course_id, enrollment_id=enrollment_id, task="conclude"
            )
        )
    return True
