from typing import Literal, Union
import json


async def conclude_delete_deactivate_enrollment(
    self,
    course_id: Union[str, int],
    enrollment_id: Union[str, int],
    task: Literal["conclude", "delete", "deactivate", "inactivate"],
) -> dict:
    """
    Conclude, delete, or deactivate an enrollment.
    :param self:
    :param course_id: The ID of the course.
    :param enrollment_id: The ID of the enrollment.
    :param task: The action to take on the enrollment. When inactive, a user will still appear in the course roster
        to admins, but be unable to participate. (“inactivate” and “deactivate” are equivalent tasks)
    :return: The concluded, deleted, or deactivated enrollment object.
    """
    payload = {"task": task}
    return self.make_request(
        req_type="delete",
        url=self._get_endpoint(
            "conclude_delete_deactivate_enrollment",
            {"<course_id>": course_id, "<enrollment_id>": enrollment_id},
        ),
        data=json.dumps(payload),
    )
