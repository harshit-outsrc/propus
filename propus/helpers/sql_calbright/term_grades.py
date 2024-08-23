from datetime import datetime
import json
from sqlalchemy import select
from zoneinfo import ZoneInfo

from propus.helpers.sql_alchemy import update_or_create
from propus.helpers.sql_calbright.enrollment import fetch_matching_enrollment, fetch_course_version
from propus.calbright_sql.course import Course
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.enrollment_course_term import EnrollmentCourseTerm, GradeStatus
from propus.calbright_sql.staff import Staff
from propus.calbright_sql.user import User


def upsert_eotg_records(
    session,
    term_id: str,
    sf_grade_id: str,
    course: Course,
    instructor_id: Staff.id,
    grade_status: GradeStatus = GradeStatus.not_graded,
    is_sp_grade: bool = False,
    certified_by_id: Staff.id = None,
    grade_id: str = None,
    grade_date: datetime = None,
    drop_date: datetime = None,
    withdrawn_date: datetime = None,
    certified_date: datetime = None,
    term_start_date: str = None,
    user: User = None,
    enrollment: Enrollment = None,
    modified_at: datetime = datetime.now(tz=ZoneInfo("UTC")),
    created_at: str = None,
):
    """Upserts EnrollmentCourseTerm records for a user's grade.

    This function takes a database session, user, grade details and creates
    EnrollmentCourseTerm records to link the user's enrollment to their grade
    for a given term and course.

    It first finds the matching enrollment for the user, term and course. Then
    it builds a dictionary with details to create the EnrollmentCourseTerm object.

    Optionally, it will populate created_at and modified_at fields if provided.

    The data is passed to update_or_create to upsert the records, linking them
    by the enrollment and course version IDs.

    Args:
    session: Database session
    term_id: Calbright DB Term ID
    sf_grade_id: Grade Salesforce ID
    course: Course object
    instructor_id: Staff ID for Instructor
    grade_status: Optional Grade status, defaults to NOT GRADED
    is_sp_grade: Optional boolean, set true if grade is an SP grade
    events_queue: Optional string, events queue to drop possible event into
    certified_by_id: Optional Staff ID for certifier
    grade_id: Optional DB Grade ID
    grade_date: Optional date grade submitted
    drop_date: Optional date drop grade submitted
    withdrawn_date: Optional date withdrawn grade submitted
    certified_date: Optional date grade certified
    user: Optional User object  Used for enrollment lookup
    term_start_date: Optional: Used for enrollment lookup. Term start date
    enrollment: Optional Enrollment object if known. If none we will fetch an enrollment from DB
    modified_at: Optional modified datetime, defaults to current UTC timestamp
    created_at: Optional created datetime
    sqs: SQS Client to drop messages onto the events queue
    """
    if not enrollment:
        enrollment = fetch_matching_enrollment(
            user=user,
            term_start_date=term_start_date,
            grade_id=sf_grade_id,
            course_versions=course.course_version_course,
        )

    course_version_id = None
    for ect in enrollment.enrollment_enrollment_course_term:
        if ect.term_id == term_id and ect.course_version.course.course_code == course.course_code:
            course_version_id = ect.course_version_id

    if course_version_id is None:
        course_version_id = fetch_course_version(session, course, enrollment.salesforce_course_version)

    enrollment_course_term = {
        "grade_salesforce_id": sf_grade_id,
        "term_id": term_id,
        "grade_status": grade_status,
        "enrollment_id": enrollment.id,
        "course_version_id": course_version_id,
        "instructor_id": instructor_id,
    }
    optionals = {
        "grade_id": grade_id,
        "grade_date": grade_date,
        "drop_date": drop_date,
        "withdraw_date": withdrawn_date,
        "modified_at": modified_at,
        "created_at": created_at,
        "certified_by_id": certified_by_id,
        "certified_date": certified_date,
    }

    enrollment_course_term |= {key: value for key, value in optionals.items() if value}

    should_create_next_terms = False
    if is_sp_grade and enrollment_course_term.get("grade_status").value == "Certified":
        ect_resp = session.execute(
            select(EnrollmentCourseTerm).filter_by(
                enrollment_id=enrollment_course_term.get("enrollment_id"),
                course_version_id=enrollment_course_term.get("course_version_id"),
                term_id=enrollment_course_term.get("term_id"),
            )
        ).one_or_none()
        if ect_resp and (
            not ect_resp[0].grade
            or ect_resp[0].grade.grade != "SP"
            or ect_resp[0].grade_status != GradeStatus("Certified")
        ):
            should_create_next_terms = True

    obj, created = update_or_create(
        session,
        EnrollmentCourseTerm,
        enrollment_course_term,
        enrollment_id=enrollment_course_term.get("enrollment_id"),
        course_version_id=enrollment_course_term.get("course_version_id"),
        term_id=enrollment_course_term.get("term_id"),
    )

    return (
        obj,
        created,
        (
            json.dumps(
                {
                    "event_type": "sp_term_grade_certified",
                    "event_data": {
                        "salesforce_grade_id": enrollment_course_term.get("grade_salesforce_id"),
                        "enrollment_course_term_id": str(obj.id),
                    },
                }
            )
            if should_create_next_terms
            else None
        ),
    )
