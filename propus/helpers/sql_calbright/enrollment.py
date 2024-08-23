from datetime import timedelta
from dateutil.parser import parse as parse_date
from sqlalchemy import and_, select, or_, func
from zoneinfo import ZoneInfo

from propus.helpers.calbright import PROGRAM_TO_COURSE_VERSION_MAP, CURRENT_COURSE_VERSION_MAP
from propus.helpers.sql_alchemy import update_or_create

from propus.calbright_sql.course import Course
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.course_version_section import CourseVersionSection
from propus.calbright_sql.enrollment import Enrollment, LMS
from propus.calbright_sql.enrollment_course_term import EnrollmentCourseTerm
from propus.calbright_sql.enrollment_status import EnrollmentStatus
from propus.calbright_sql.program import Program
from propus.calbright_sql.program_version import ProgramVersion
from propus.calbright_sql.program_version_course import ProgramVersionCourse
from propus.calbright_sql.term import Term

from propus.logging_utility import Logging

logger = Logging.get_logger("propus/helpers/sql_calbright/enrollment.py", debug=True)


class NoMatchingProgramVersion(Exception):
    pass


class MultipleInProgressEnrollments(Exception):
    pass


class NoMatchingFirstTerm(Exception):
    pass


class MissingEnrollment(Exception):
    pass


class MissingCourseVersion(Exception):
    pass


class EnrollmentClosingWithOpenGrade(Exception):
    pass


class EnrollmentClosingWithDifferentGrades(Exception):
    pass


def fetch_program_version_by_course_versions(session, program_name: str, program_version: str = None):
    """
    Fetch the program version associated with a list of course versions.

    This function queries the database to find the program version that
    contains the given courses. It first maps the course codes and versions
    from the program version string. Then it builds a SQL query with AND
    statements to filter on each course version.

    Args:
        session (SQLAlchemy Session): Database Session
        program_name (str): The name of the program
        program_version (str) [Optional]: The program version string
    Returns:
        The program version ID if a single match is found.

    Raises:
        NoMatchingProgramVersion: If no single program version contains all the given course versions

    Example Function Call:
         - fetch_program_version_by_course_versions("Data Analysis")
         - fetch_program_version_by_course_versions("Data Analysis", "BUS500 - v2.0, BUS501 - v2.0")
    """

    def fetch_course_versions_for_program(program, program_version):
        if program_version:
            course_list = program_version.split(", ")
            if len(course_list) == 2:
                return {k.split(" - v")[0]: k.split(" - v")[1] for k in course_list if len(k.split(" - v")) >= 2}
        return PROGRAM_TO_COURSE_VERSION_MAP.get(program, {})

    and_stmts = []
    course_version_map = fetch_course_versions_for_program(program_name, program_version)
    for course_code, version_id in course_version_map.items():
        and_stmts.append(
            and_(
                Course.course_code == course_code,
                CourseVersion.version_id == float(version_id),
            ),
        )
    stmt = (
        select(ProgramVersionCourse.program_version_id)
        .outerjoin(ProgramVersion)
        .join(Program)
        .outerjoin(CourseVersion)
        .join(Course)
        .where(or_(*and_stmts), Program.short_name == program_name)
    )
    program_version_ids = session.scalars(stmt).unique().all()
    if program_version_ids:
        if len(program_version_ids) > 1:
            logger.warn(f"Multiple Program Version IDs for {program_name} - {program_version}")
        return program_version_ids.pop()
    raise NoMatchingProgramVersion(f"No matching program version found for {program_name} and {course_version_map}")


def check_enrollment_before_upsert(enrollment, new_data):
    """
    Check an enrollment record before upserting.

    Checks that an enrollment's status is not being changed to a final
    status if there are open grades or inconsistent grades. Raises
    exceptions in those cases.

    Args:
        enrollment: The enrollment record to check
        new_data: A dict of new data to upsert

    Raises:
        EnrollmentClosingWithOpenGrade: If enrollment is closing but
            has courses with no grade
        EnrollmentClosingWithDifferentGrades: If enrollment has courses
            with different grades
    """

    if new_data.get("enrollment_status").status not in ["Started", "Enrolled"]:
        term_to_grades = {}
        for course_term in enrollment.enrollment_enrollment_course_term:
            if not course_term.grade:
                raise EnrollmentClosingWithOpenGrade(
                    f"Enrollment for user {enrollment.ccc_id} (enrollment {enrollment.enrollment_salesforce_id}) "
                    "closing with open grade",
                )
            term_to_grades[course_term.term.term_name] = term_to_grades.get(course_term.term.term_name, []) + [
                course_term.grade.grade
            ]
        for _, grades in term_to_grades.items():
            if len(set(grades)) > 1:
                raise EnrollmentClosingWithDifferentGrades(
                    f"Enrollment for user {enrollment.ccc_id} (enrollment {enrollment.enrollment_salesforce_id}) "
                    "closing with different grade",
                )


def upsert_enrollment(session, user, enrollment_data: dict):
    """
    Upsert an enrollment record.
    This function checks if an enrollment record already exists for the given user
    and enrollment data. If so, it updates the existing record. Otherwise, it will
    create a new enrollment record. It also handles assigning the first term and
    raising exceptions if needed.

    Args:
        session: The database session.
        user: The user object.
        enrollment_data: A dictionary containing enrollment data.

    Raises:
        MultipleInProgressEnrollments: If the user already has an active enrollment.
        NoMatchingFirstTerm: If no matching term is found for the enrollment date.
    """
    existing_enrollment = None
    active_enrollment = False
    for enrollment in user.student.enrollment_student:
        if enrollment.enrollment_status.status in ["Started", "Enrolled"]:
            active_enrollment = True
        if enrollment.enrollment_salesforce_id:
            if enrollment.enrollment_salesforce_id == enrollment_data.get("enrollment_salesforce_id"):
                existing_enrollment = enrollment
                break
        elif (
            enrollment.program_version_id == enrollment_data.get("program_version_id")
            and (
                parse_date(enrollment_data.get("enrollment_date")).replace(tzinfo=None) - enrollment.enrollment_date
            ).days
            <= 1
        ):
            # Check if the program versions are the same and the enrollment dates are within 1 day of each other
            existing_enrollment = enrollment
            break

    if enrollment_data.get("enrollment_status"):
        enrollment_data["enrollment_status_id"] = enrollment_data.get("enrollment_status").id
    if existing_enrollment:
        enrollment_data["first_term_id"] = existing_enrollment.first_term_id
        try:
            check_enrollment_before_upsert(existing_enrollment, enrollment_data)
        except Exception as err:
            logger.warning(err)
            pass
        update_or_create(session, Enrollment, enrollment_data, id=existing_enrollment.id)
        logger.info(f"Record with ccc_id = {enrollment_data.get('ccc_id')} updated successfully")
        return existing_enrollment

    if active_enrollment:
        raise MultipleInProgressEnrollments(f"Multiple In Progress Enrollments for student {user.student.ccc_id}")
    first_term = session.scalars(
        select(Term).filter(Term.start_date >= enrollment_data.get("enrollment_date")).order_by(Term.start_date)
    ).first()
    if not first_term:
        raise NoMatchingFirstTerm(
            f"No Matching Term for enrollment of  {enrollment_data.get('enrollment_date')} - {user.student.ccc_id}"
        )
    enrollment_data["first_term"] = first_term
    enrollment = Enrollment(**enrollment_data)
    session.add(enrollment)
    return enrollment


def fetch_course_version(session, course: Course, sf_course_versions: str = None):
    """
        Fetch the CourseVersion object for a course.

        This function takes a database session, optional string of Salesforce
        course versions, and a Course object. It first checks a map to get the
        default course version.

        If Salesforce versions are provided, it parses the string to extract the
        version for the given course code.

        A query is made to the database to get the matching CourseVersion object
        by course ID and version ID.

        If no object is found, a MissingCourseVersion exception is raised.

        Otherwise, the CourseVersion ID is returned.

    Args:
        session: The database session.
        sf_course_versions: Salesforce course versions string.
        course: The Course object.

    Returns:
        The CourseVersion ID.

    Raises:
        MissingCourseVersion: If no matching object is found.
    """
    course_version = CURRENT_COURSE_VERSION_MAP.get(course.course_code)
    if sf_course_versions and course.course_code in sf_course_versions:
        course_version_list = [c for c in sf_course_versions.split(", ") if course.course_code in c].pop()
        course_version = course_version_list.split(" - v")[1]
    cv = session.scalars(
        select(CourseVersion).filter(
            CourseVersion.course_id == course.id, CourseVersion.version_id == float(course_version)
        )
    ).first()
    if not cv:
        raise MissingCourseVersion(
            f"MissingCourseVersion: Could not identify {course.course_code} with version {course_version}"
        )
    return cv.id


def fetch_matching_enrollment(user, term_start_date: str, grade_id: str, course_versions: list):
    """
    Fetch the matching enrollment for a user, term, grade, and course versions.

    This function takes a user object, term start date, grade ID, and list of course
    versions. It checks the user's enrollments to find one that matches:

    - The program version is in the list of matching programs for the course versions
    - The enrollment date is before the term start date
    - The status date (drop/withdraw/complete) is before the term start date

    If no matching enrollment is found, a MissingEnrollment exception is raised.

    Args:
        user: The user object.
        term_start_date: Start date of the term.
        grade_id: The grade ID.
        course_versions: List of CourseVersion objects

    Returns:
        The matching Enrollment object.

    Raises:
        MissingEnrollment: If no matching enrollment is found.
    """
    enrollments = user.student.enrollment_student
    if not enrollments:
        raise MissingEnrollment(f"EnrollmentNotFound: {user.student.ccc_id} - GradeId: {grade_id}")

    matching_programs = set(
        [cpv.program_version.program_id for i in course_versions for cpv in i.course_program_version]
    )

    term_start_date = term_start_date.replace(tzinfo=ZoneInfo("America/Los_Angeles"))

    for e in enrollments:
        if e.program_version.program_id not in matching_programs:
            # if the program version is not in the matching programs it is not the right grade
            continue
        utc_enrollment_date = e.enrollment_date.replace(tzinfo=ZoneInfo("UTC"))
        if utc_enrollment_date.astimezone(ZoneInfo("America/Los_Angeles")) > term_start_date + timedelta(days=1):
            # if the grade start date is before the enrollment_date it is not the right grade
            continue
        status_date = e.drop_date if e.drop_date else e.withdrawn_date if e.withdrawn_date else e.completion_date
        if status_date:
            utc_status_date = status_date.replace(tzinfo=ZoneInfo("UTC"))
            pst_status_date = utc_status_date.astimezone(ZoneInfo("America/Los_Angeles"))
            if term_start_date > pst_status_date:
                # if the grade start date is after the status date it is not the right grade
                # this sometimes breaks because students are occasionally dropped before the term start date (no fix)
                # we cannot just extend out term_start_date because then previous enrollments that happen days
                # before the next enrollment will get selected
                continue
        return e
    raise MissingEnrollment(f"NoMatchingEnrollmentFound: {user.student.ccc_id} - GradeId: {grade_id}")


def get_instructor_loads(session):
    """
    Get the number of distinct enrollment IDs for each instructor.
    - This only selects enrollments that are either in the "Enrolled" or "Started" status.
    :param session: A Calbright database session
    :return: A dictionary of instructor ID to enrollment count
    """
    query = (
        session.query(
            CourseVersionSection.instructor_id,
            func.coalesce(func.count(func.distinct(EnrollmentCourseTerm.enrollment_id)), 0).label("enrollment_count"),
        )
        .outerjoin(EnrollmentCourseTerm, CourseVersionSection.id == EnrollmentCourseTerm.course_version_section_id)
        .outerjoin(Enrollment, EnrollmentCourseTerm.enrollment_id == Enrollment.id)
        .outerjoin(
            EnrollmentStatus,
            (Enrollment.enrollment_status_id == EnrollmentStatus.id)
            & (EnrollmentStatus.status.in_(["Enrolled", "Started"])),
        )
        .group_by(CourseVersionSection.instructor_id)
    )
    logger.debug("Fetching instructor loads...")

    return {r.instructor_id: r.enrollment_count for r in query.all()}


def get_instructors_to_assign(session):
    """
    Get the section to assign for each program version course.
    - This function gets the instructor loads and then assigns the instructor with the lowest load to each course.
    - This can then be used to assign the instructor to the course version section.
    :param session:
    :return: A dictionary of program version course ID to course version section
    """
    instructor_loads = get_instructor_loads(session=session)
    program_version_courses = (
        session.query(ProgramVersionCourse)
        .join(CourseVersion, ProgramVersionCourse.course_version_id == CourseVersion.id)
        .filter(CourseVersion.lms == LMS("Canvas"))
        .all()
    )
    section_to_assign_for_each_program_version_course = {}
    logger.debug("Calculating the section to assign for each program version course...")
    for program_version_course in program_version_courses:
        course_instructors = program_version_course.course_version.course.course_instructor
        min_count = float("inf")
        selected_instructor = None
        for course_instructor in course_instructors:
            if course_instructor.instructor.id in instructor_loads:
                count = instructor_loads[course_instructor.instructor.id]
                if count < min_count:
                    min_count = count
                    selected_instructor = course_instructor.instructor
        if selected_instructor:
            course_version_section = (
                session.query(CourseVersionSection)
                .filter(
                    CourseVersionSection.program_version_course_id == program_version_course.id,
                    CourseVersionSection.instructor_id == selected_instructor.id,
                )
                .first()
            )
            section_to_assign_for_each_program_version_course[program_version_course.id] = course_version_section
        else:
            raise Exception("No instructor found for course")  # TODO: custom exception
    logger.debug(f"Sections to assign: {section_to_assign_for_each_program_version_course}")
    return section_to_assign_for_each_program_version_course


def assign_enrollment_course_term_sections(
    session, enrollment_course_term_list: list[EnrollmentCourseTerm], commit=True
):
    """
    This function assigns sections to enrollment course terms.
    - It expects the enrollment course term list to be a list of EnrollmentCourseTerm objects for a single student
    - It calculates the instructor load at the start of the function
    :param session: A Calbright database session
    :param enrollment_course_term_list: A list of EnrollmentCourseTerm objects
    :param commit: Whether to commit the transaction
    :return: bool: True if sections were assigned
    """
    logger.debug(f"Assigning sections to enrollment_course_term_list: {enrollment_course_term_list}")
    assigned_sections = False
    sections_to_assign = get_instructors_to_assign(session=session)
    # TODO: Need to add logic to also assign the instructor to ALL courses if possible.
    #    E.g. - if the instructor is assigned to BUS501, then they should also be assigned to BUS502
    #    Right now it is assigning to the instructor with the lowest enrollment, but that could be different by course.
    #    This should also check to see IF the instructor is assigned to teach the course.
    for enrollment_course_term in enrollment_course_term_list:
        program_course_versions = enrollment_course_term.enrollment.program_version.program_course_version
        logger.debug(f"Program Course Versions: {program_course_versions}")
        for program_course_version in program_course_versions:
            logger.debug(
                f"Checking Course Version: {program_course_version.course_version_id} "
                f"against {enrollment_course_term.course_version_id}"
            )
            if program_course_version.course_version_id == enrollment_course_term.course_version_id:
                if program_course_version.id not in sections_to_assign:
                    raise Exception("No section found for course")
                if enrollment_course_term.course_version_section:
                    logger.info("Section already assigned to enrollment_course_term. Skipping...")
                    continue
                section = sections_to_assign.get(program_course_version.id)
                enrollment_course_term.course_version_section = section
                assigned_sections = True
                logger.info(f"Assigned section {section} to enrollment_course_term {enrollment_course_term}")

    if commit and assigned_sections:
        session.commit()

    return assigned_sections
