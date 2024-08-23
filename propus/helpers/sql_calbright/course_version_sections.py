from sqlalchemy import func
from propus.calbright_sql.course import Course
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.course_version_section import CourseVersionSection
from propus.calbright_sql.enrollment import LMS
from propus.calbright_sql.program_version_course import ProgramVersionCourse

from propus.logging_utility import Logging

logger = Logging.get_logger("propus/helpers/sql_calbright/course_version_sections.py", debug=True)


def create_course_version_section_records(session):
    """
    This function will create course_version_section records for each instructor associated with a course_version
    - This will only create sections for course_versions that are associated with the LMS "Canvas"
    - The section name will be the course_code and the section_id, e.g. "BUS500-1"
    - The section_id will increment for each new section created for a course_code, e.g. BUS500-2, BUS500-3, etc.
    :param session:
    :return: bool: True if sections were created, False if no sections were created
    """
    logger.info("Creating course version sections...")
    # Get the max section_id for each course_code, we will use this to increment the section_id for each new section
    max_section_id_by_course = (
        session.query(Course.course_code, func.max(CourseVersionSection.section_id).label("max_section_id"))
        .join(ProgramVersionCourse, CourseVersionSection.program_version_course_id == ProgramVersionCourse.id)
        .join(CourseVersion, ProgramVersionCourse.course_version_id == CourseVersion.id)
        .join(Course, CourseVersion.course_id == Course.id)
        .group_by(Course.course_code)
        .all()
    )
    course_section_ids = {result.course_code: int(result.max_section_id) for result in max_section_id_by_course}

    # Get all course_versions that are associated with Canvas, go through each course and check the instructors
    # associated with the course, if a course_version_section does not exist for the instructor, create one
    sections_created = False
    course_versions = session.query(CourseVersion).filter(CourseVersion.lms == "canvas").all()
    for course_version in course_versions:
        logger.debug(f"course_version: {course_version}")
        program_version_courses = course_version.course_program_version
        logger.debug(f"program_version_courses: {program_version_courses}")
        for program_version_course in program_version_courses:
            course_code = program_version_course.course_version.course.course_code
            logger.debug(f"Instructor course: {course_version.course.course_instructor}")
            for instructor_course in course_version.course.course_instructor:
                # TODO: This is what I did to skip instructors who aren't set as Canvas instructors... Review?
                if not instructor_course.canvas_instructor:
                    logger.debug(f"Skipping instructor {instructor_course.instructor}")
                    continue
                instructor = instructor_course.instructor
                course_version_section = (
                    session.query(CourseVersionSection)
                    .join(
                        ProgramVersionCourse, CourseVersionSection.program_version_course_id == ProgramVersionCourse.id
                    )
                    .filter(
                        ProgramVersionCourse.course_version_id == course_version.id,
                        CourseVersionSection.instructor_id == instructor.id,
                    )
                    .first()
                )
                if not course_version_section:
                    logger.debug(
                        f"creating section for course_version: {course_version.id} and instructor: {instructor.id}"
                    )
                    course_section_id = course_section_ids[course_code] = course_section_ids.get(course_code, 0) + 1
                    course_version_section = CourseVersionSection(
                        program_version_course_id=program_version_course.id,
                        instructor_id=instructor.id,
                        lms=LMS("Canvas"),
                        section_id=course_section_id,
                        section_name=f"{course_code}-{course_section_id}",
                    )
                    session.add(course_version_section)
                    sections_created = True

                else:
                    logger.debug(
                        f"course version section found for {course_version.id} and {instructor.id}, skipping..."
                    )
                    continue

    session.commit()
    return sections_created
