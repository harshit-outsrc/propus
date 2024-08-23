from datetime import datetime
import json
from typing import AnyStr, Dict


async def post_final_grade(
    self, course_id: int, letter_grade: AnyStr, date_completed: datetime = datetime.now().strftime("%Y-%m-%d")
) -> Dict:
    """_summary_

    API wrapper that will be used to create a new final grade record

    Args:
        course_id (int): anthology course id
        letter_grade (AnyStr): letter grade to be added
        date_completed (datetime, optional): date to add to completion
            Defaults to datetime.now()

    Returns:
        Dict: if a 200 status code is returned the json response payload from anthology is returned
    """
    required_keys = [
        "studentEnrollmentDpaCourseCategoryId",
        "campusId",
        "id",
        "academicYear",
        "classSectionId",
        "clockHours",
        "clockHoursAttempted",
        "clockHoursEarned",
        "consecutiveMinutesAbsent",
        "cost",
        "courseId",
        "courseName",
        "createdDateTime",
        "creditHours",
        "creditHoursAttempted",
        "creditHoursEarned",
        "endDate",
        "enrollmentStatusClockHours",
        "enrollmentStatusCreditHours",
        "expectedEndDate",
        "gradePoints",
        "gradePostedDate",
        "gradeScaleId",
        "lda",
        "letterGrade",
        "lmsExtractStatus",
        "makeUpMinutes",
        "minutesAbsent",
        "minutesAttended",
        "modFlag",
        "note",
        "outsideCourseWorkHours",
        "payStatus",
        "previousStatus",
        "retakeFeeWaived",
        "startDate",
        "status",
        "studentEnrollmentPeriodId",
        "studentId",
        "termId",
        "transferTypeId",
    ]

    # First go fetch needed course data
    course_data = await self.fetch_course(course_id)

    # Second assemble the post data to create the letter grade
    course_payload = {k: v for k, v in course_data.items() if k in required_keys}
    course_payload["endDate"] = f"{date_completed}T00:00:00"
    course_payload["gradePostedDate"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    course_payload["letterGrade"] = letter_grade
    course_payload["isPassFail"] = True

    grade_payload = {
        "PostFinalGradeForExistingGrade": True,
        "AllowOverrideExpectedDeadlineDate": True,
        "CampusId": self._campus_id,
        "StudentCourse": course_payload,
    }

    return self.make_request(
        req_type="post", url=self._get_endpoint("post_final_grade"), data=json.dumps({"payload": grade_payload})
    )


async def fetch_grade(self, filters: Dict = {}) -> Dict:
    """
    API wrapper to retrieve possible grades from Anthology

    Args:
        filters (Dict, optional): Dictionary of possible filters for grade responses. Possible responses are:
            - drop (must be set to True or False)
            - pass_fail (must be set to True or False)
            Defaults to {}.

    Returns:
        Dict: direct response from anthology drop grades request
    """

    filter_string = (
        self.format_anthology_filters({f"grade_{k}": "true" if v else "false" for k, v in filters.items()})
        if filters
        else ""
    )

    return self.make_request(
        url=self._get_endpoint("fetch_grade"), params={"$filter": filter_string} if filter_string else None
    )
