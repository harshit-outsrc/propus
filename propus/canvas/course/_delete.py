import json
from typing import Literal, Union


async def delete_or_conclude_course(self, course_id: Union[str, int], event: Literal["conclude", "delete"]) -> dict:
    """
    Delete or conclude a course.
    :param self:
    :param course_id: The ID of the course.
    :param event: The event to perform on the course. It can be either "conclude" or "delete".
    :return: The status of the course after the event, e.g. {'conclude': True}
    """
    payload = {"event": event}
    return self.make_request(
        req_type="delete",
        url=self._get_endpoint("delete_or_conclude_course", {"<course_id>": course_id}),
        data=json.dumps(payload),
    )


async def delete_section(self, section_id: Union[str, int]) -> dict:
    """
    Delete a section.
    :param self:
    :param section_id: The ID of the section.
    :return: The deleted section object.
    """
    return self.make_request(
        req_type="delete",
        url=self._get_endpoint("delete_section", {"<section_id>": section_id}),
    )
