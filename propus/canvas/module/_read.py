import urllib.parse
from typing import Union, Literal


async def get_course_modules(
    self,
    course_id: Union[str, int],
    include: Union[
        Literal[
            "items",
            "content_details",
        ],
        None,
    ] = None,
    search_term: Union[str, None] = None,
    student_id: Union[str, None] = None,
) -> dict:
    payload = {}
    if include is not None:
        payload["include[]"] = include
    if search_term is not None:
        payload["search_term"] = search_term
    if student_id is not None:
        payload["student_id"] = student_id

    url = self._get_endpoint("get_course_modules", {"<course_id>": course_id})

    if payload:
        query_params = urllib.parse.urlencode(payload, doseq=True)
        url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)


async def get_module(self):
    # TODO: Implement this method
    pass


async def get_module_items(self):
    # TODO: Implement this method
    pass


async def get_module_item(self):
    # TODO: Implement this method
    pass
