import json
from typing import Dict, List, AnyStr


async def fetch_classes_for_courses(self, student_id: int, term_id: int, course_ids: List[int]) -> Dict:
    """
    API Wrapper to fetch student classes from Anthology. Returned is the direct response from Anthology

    Args:
        student_id (int): anthology student id
        term_id (int): anthology term id
        course_ids (List[int]): list of course ids to retrieve class data for

    Returns:
        Dict: direct response from anthology student class query
    """
    fields_to_return = [
        "Id",
        "CourseCode",
        "CourseName",
        "SectionCode",
        "SectionName",
        "CourseId",
        "CampusId",
        "StartDate",
        "EndDate",
        "IsActive",
        "DeliveryMethodName",
        "InstructorName",
    ]
    return self.make_request(
        url=self._get_endpoint(
            "fetch_classes_for_courses",
            parameters={
                "<campus_id>": self._campus_id,
                "<term_id>": term_id,
                "<course_ids>": ",".join([str(c) for c in course_ids]),
                "<student_id>": student_id,
                "<fields_to_return>": ",".join(fields_to_return),
            },
        )
    )


async def fetch_course_for_enrollment(self, student_id: int, enrollment_id: int) -> Dict:
    """
    Query Anthology for all Student Courses by Enrollment ID

    Args:
        student_id (int): anthology's student ID
        enrollment_id (int): anthology enrollment ID

    Returns:
        Dict: Course Payload from Anthology. Example:
            {
            "Items": [
                {
                "Entity": {
                    "TranscripNote": null,
                    "IsCrsg": false,
                    "StudentEnrollmentPeriodIdList": null,
                    "StudentEnrollmentDpaCourseCategoryId": 13837,
                    "CampusId": 5,
                    "StudentTransferCreditMultipleCourseAssociationId": null,
                    "StudentTransferCreditMultipleId": null,
                    "Id": 6933,
                    "AcademicYear": 0,
                    "AdEnrollRegistrationId": null,
                    "AdvisedDate": null,
                    "AppealType": null,
                    "AuditEffectiveDate": null,
                    "AverageBestOfPercentFinal": null,
                    "BilledDate": null,
                    "ClassSectionId": 0,
                    "ClockHours": 30,
                    "ClockHoursAttempted": 0,
    """
    return self.make_request(
        url=self._get_endpoint(
            "fetch_course_for_enrollment", parameters={"<student_id>": student_id, "<enrollment_id>": enrollment_id}
        )
    )


async def fetch_all_courses(self):
    """
    Query Anthology to return all course data
    """

    return self.make_request(url=self._get_endpoint("fetch_all_courses"))


async def fetch_course(self, course_id: int):
    """
    Query Anthology for a specific course's details and metadata

    Args:
        course_id (int): Course ID
    """

    return self.make_request(
        req_type="post", url=self._get_endpoint("fetch_course"), data=json.dumps({"payload": {"id": course_id}})
    )


async def fetch_term_for_courses(self, course_ids: List[int]) -> Dict:
    """
    API Wrapper to fetch terms for a specific list of Course Ids

    Args:
        course_ids (List[int]): list of ints that are course ids to be retrieved from Anthology

    Returns:
        Dict: direct response from anthology term query
    """
    fields_to_return = [
        "TermName",
        "TermCode",
        "Id",
        "TermStartDate",
        "TermEndDate",
        "CodeAndName",
    ]
    return self.make_request(
        url=self._get_endpoint(
            "fetch_term_for_courses",
            parameters={
                "<campus_id>": self._campus_id,
                "<course_ids>": ",".join([str(c) for c in course_ids]),
                "<fields_to_return>": ",".join(fields_to_return),
            },
        )
    )


async def fetch_all_enrolled_courses(self) -> Dict:
    """
    API Wrapper to fetch all courses that students are enrolled in

    Returns:
        Dict: direct response from anthology term query
    """
    return self.make_request(
        url=self._get_endpoint("course_search"), params={"$expand": "Student,Enrollment,Course,Term"}
    )


async def fetch_course_by_cccid(self, ccc_id: AnyStr, enrollment_id=None) -> Dict:
    """
    API Wrapper to fetch courses for a specific student and optional enrollment_id

    Args:
        ccc_id (str): student ccc id
        enrollment_id (int, optional): student enrollment id. Defaults to None.

    Returns:
        Dict: direct response from anthology term query
    """
    filter_param = f"Student/StudentNumber eq '{ccc_id}'"
    if enrollment_id:
        filter_param += f" and Enrollment/Id eq {enrollment_id}"
    return self.make_request(
        url=self._get_endpoint("course_search"),
        params={"$filter": filter_param, "$expand": "Student,Enrollment,Course,Term"},
    )
