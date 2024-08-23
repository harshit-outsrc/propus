import json
from typing import Dict


async def reinstate_course(self, student_course_id: int) -> Dict:
    """
    API wrapper to reinstate a student for a course

    Args:
        student_course_id (int): anthology student course id. Can be retrieved with fetch_all_courses

    Returns:
        Dict: direct response from anthology course reinstate
    """
    return self.make_request(
        req_type="post",
        url=self._get_endpoint("reinstate_course"),
        data=json.dumps({"payload": {"StudentCourseId": student_course_id}}),
    )
