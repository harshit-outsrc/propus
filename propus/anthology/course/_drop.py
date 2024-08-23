import json
from datetime import datetime
from typing import AnyStr, Dict


async def drop_course(
    self, student_course_id: int, drop_date: datetime, drop_reason_id: int, letter_grade: AnyStr = None
) -> Dict:
    """
    API wrapper to drop a student for a course

    Args:
        student_course_id (int): anthology student course id. Can be retrieved with fetch_all_courses
        drop_date (datetime): drop date
        drop_reason_id (int): anthology drop reason id. Can be retrieved with fetch_drop_reason
        letter_grade (AnyStr): anthology letter grade. Can be retrieved with fetch_drop_letter_grades

    Returns:
        Dict: direct response from anthology course drop
    """
    drop_payload = {
        "StudentEnrollmentScheduleId": student_course_id,
        "DropDate": drop_date.strftime("%Y/%m/%d %H:%M:%S"),
        "DropReasonId": drop_reason_id,
        "AllowLdwOverride": True,
    }
    if letter_grade:
        drop_payload["LetterGrade"] = letter_grade

    return self.make_request(
        req_type="post", url=self._get_endpoint("drop_course"), data=json.dumps({"payload": drop_payload})
    )


async def fetch_drop_reason(self) -> Dict:
    """
    API wrapper to retrieve drop reasons from Anthology

    Returns:
        Dict: direct response from anthology drop reasons request
    """
    return self.make_request(url=self._get_endpoint("fetch_drop_reason"))
