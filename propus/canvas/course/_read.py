from typing import Union


async def get_course(self, course_id: Union[str, int]) -> dict:
    """
    Get a course by its ID.
    :param self:
    :param course_id: The ID of the course.
    :return: A course object.
    """
    return self.make_request(
        req_type="get",
        url=self._get_endpoint("get_course", {"<course_id>": course_id}),
    )


async def get_section(self, course_id: Union[str, int], section_id: Union[str, int]) -> dict:
    """
    Get a section by its ID.
    :param self:
    :param course_id: The ID of the course.
    :param section_id: The ID of the section.
    :return: A section object.
    """
    return self.make_request(
        req_type="get",
        url=self._get_endpoint("get_section", {"<course_id>": course_id, "<section_id>": section_id}),
    )
