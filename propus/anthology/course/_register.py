from datetime import datetime
import json
from typing import Dict


async def register_course(
    self,
    student_course_id: int,
    enrollment_id: int,
    class_section_id: int,
    course_id: int,
    term_id: int,
    hours: int,
    start_date: datetime,
    end_date: datetime,
) -> Dict:
    """
    API wrapper to register a student for a course

    Args:
        student_course_id (int): anthology student course id. Can be retrieved with fetch_all_courses
        enrollment_id (int): anthology enrollment id. Can be retrieved with fetch_all_courses
        class_section_id (int): anthology class section id. Can be retrieved with fetch_student_classes
        course_id (int): anthology course id. Can be retrieved with fetch_terms_for_classes
        term_id (int): anthology term id. Can be retrieved with fetch_terms_for_classes
        hours (int): hours for course. Can be retrieved with fetch_all_courses
        start_date (datetime): start date of term. Can be retrieved with fetch_terms_for_classes
        end_date (datetime): end date of term. Can be retrieved with fetch_terms_for_classes

    Returns:
        Dict: direct response from anthology course register
    """
    register_payload = {
        "StudentCourseId": student_course_id,
        "StudentEnrollmentPeriodId": enrollment_id,
        "CampusId": self._campus_id,
        "ClassSectionId": class_section_id,
        "CourseId": course_id,
        "TermId": term_id,
        "Hours": hours,
        "Comments": "Registered Via API",
        "Credits": 0,
        "Action": 2,
        "AllowOverrideRegistrationHold": True,
        "IsAllowedToOverrideLockedTermSequence": True,
        "IsAllowedPostCourseStartDateRegistration": True,
        "Description": "",
        "StartDate": start_date if isinstance(start_date, str) else start_date.strftime("%Y-%m-%dT00:00:00"),
        "EndDate": end_date if isinstance(end_date, str) else end_date.strftime("%Y-%m-%dT00:00:00"),
        "RetakeID": 0,
        "ReturnCode": 0,
        "IsPassFail": 1,
        "RetakeFee": "O",
        "IsAddDropPeriodClassSectionAllowed": True,
        "IsAllowedToOverrideClosedTerm": True,
        "IsAllowedToOverrideRegistrationGroup": True,
        "IsPreCoRequisiteValidationSkipped": True,
        "IsAllowedToWaitListStudent": True,
        "IsAllowedToOverrideRetakeAttempts": True,
        "IsRetakeOverride": True,
    }

    return self.make_request(
        req_type="post", url=self._get_endpoint("register_course"), data=json.dumps({"payload": register_payload})
    )


async def add_new_course(
    self,
    student_id: int,
    enrollment_id: int,
    class_section_id: int,
    course_id: int,
    course_name: str,
    term_id: int,
    start_date: datetime,
    end_date: datetime,
) -> Dict:
    """API wrapper to add a student to a new course

    Args:
        student_id (int): anthology student id.
        enrollment_id (int): anthology enrollment id. Can be retrieved with fetch_all_courses
        class_section_id (int): anthology class section id. Can be retrieved with fetch_student_classes
        course_id (int): anthology course id. Can be retrieved with fetch_terms_for_classes
        course_name (str): anthology course name. Can be retrieved with fetch_terms_for_classes
        term_id (int): anthology term id. Can be retrieved with fetch_terms_for_classes
        start_date (datetime): start date of term. Can be retrieved with fetch_terms_for_classes
        end_date (datetime): end date of term. Can be retrieved with fetch_terms_for_classes

    Returns:
        Dict: direct response from anthology course adding
    """

    course_payload = {
        "campusId": self._campus_id,
        "classSectionId": class_section_id,
        "courseId": course_id,
        "courseName": course_name,
        "createdDateTime": datetime.now().strftime("%Y-%m-%dT00:00:00"),
        "endDate": end_date if isinstance(end_date, str) else end_date.strftime("%Y-%m-%dT00:00:00"),
        "isPassFail": 1,
        "letterGrade": "",
        "modFlag": "A",
        "note": "Created via API",
        "retakeFeeWaived": "0",
        "retakeOverride": False,
        "rosterFlag": "",
        "startDate": start_date if isinstance(start_date, str) else start_date.strftime("%Y-%m-%dT00:00:00"),
        "status": "F",
        "studentEnrollmentPeriodId": enrollment_id,
        "studentId": student_id,
        "termId": term_id,
    }

    return self.make_request(
        req_type="post",
        url=self._get_endpoint("add_new_course"),
        data=json.dumps({"payload": course_payload}),
    )


async def add_attendance(
    self,
    student_id: int,
    class_section_id: int,
    start_date: datetime,
    end_date: datetime,
    student_course_id: int,
    student_enrollment_id: int,
    minutes_to_add: int = 60,
) -> Dict:
    """API wrapper around Anthology's add attendance API. This "attendance" is not actually used by Calbright but is
    required to change the student into EPP status.

    Args:
        student_id (int): anthology's student id
        class_section_id (int): anthology class section id. Can be retrieved with fetch_student_classes
        start_date (datetime): start date of class or any date
        end_date (datetime): end date of class or any date
        student_course_id (int): anthology course id. Can be retrieved with fetch_terms_for_classes
        student_enrollment_id (int): anthology enrollment id. Can be retrieved with fetch_all_courses
        minutes_to_add (int, optional): Any number for minutes of attendance. Defaults to 60.

    Returns:
        Dict: Anthology Response
    """
    attendance_payload = {
        "StudentId": student_id,
        "ClassSectionId": class_section_id,
        "StartDate": start_date.strftime("%Y-%m-%dT00:00:00"),
        "EndDate": end_date.strftime("%Y-%m-%dT00:00:00"),
        "AllowClosedTerm": True,
        "IsPostExternshipOnline": True,
        "Entity": {
            "Id": -1,
            "ClassSectionMeetingDateId": 0,
            "AttendanceDate": f"{datetime.now().strftime('%Y-%m-%d')}T00:00:00.000",
            "Attended": minutes_to_add,
            "Absent": 0,
            "Status": "A",
            "AttendedStatus": "A",
            "Type": "O",
            "UnitType": "M",
            "Note": "",
            "StudentCourseId": student_course_id,
            "StudentEnrollmentPeriodId": student_enrollment_id,
            "EntityState": 0,
        },
    }

    return self.make_request(
        req_type="post", url=self._get_endpoint("add_attendance"), data=json.dumps({"payload": attendance_payload})
    )
