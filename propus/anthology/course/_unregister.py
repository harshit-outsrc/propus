import json
from typing import AnyStr, Dict


async def unregister_course(self, student_course_id: int, reason: AnyStr, description: AnyStr = None) -> Dict:
    """
    API wrapper to unregister a student for a course

    Args:
        student_course_id (int): anthology student course id. Can be retrieved with fetch_all_courses
        reason (AnyStr): String reason of why the student was unregistered. It is the "Name" field from the below
            fetch_unregister_reason function
        description (AnyStr): (Optional) String description of why the student was unregistered

    Returns:
        Dict: direct response from anthology course drop
    """
    unregister_payload = {
        "IsUnregisterCall": True,
        "IsMultipleUnregisterEnabled": True,
        "StudentCourseId": student_course_id,
        "Comments": reason,
    }
    if description:
        unregister_payload["Description"] = description

    return self.make_request(
        req_type="post", url=self._get_endpoint("unregister_course"), data=json.dumps({"payload": unregister_payload})
    )
