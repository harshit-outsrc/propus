from typing import Union


async def reactivate_enrollment(self, course_id: Union[str, int], enrollment_id: Union[str, int]) -> dict:
    """
    Reactivate a deactivated enrollment.
    :param self:
    :param course_id: The ID of the course.
    :param enrollment_id: The ID of the enrollment.
    :return: The reactivated enrollment object.
    """
    return self.make_request(
        req_type="put",
        url=self._get_endpoint(
            "reactivate_enrollment",
            {"<course_id>": course_id, "<enrollment_id>": enrollment_id},
        ),
    )
