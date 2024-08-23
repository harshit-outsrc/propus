import urllib.parse
from typing import Union, Literal


async def get_course_assignments(
    self,
    course_id: Union[str, int],
    include: Union[
        Literal[
            "submission",
            "assignment_visibility",
            "all_dates",
            "overrides",
            "observed_users",
            "can_edit",
            "score_statistics",
            "ab_guid",
        ],
        None,
    ] = None,
    search_term: Union[str, None] = None,
    override_assignment_dates: bool = True,
    needs_grading_count_by_section: bool = False,
    bucket: Union[Literal["past", "overdue", "undated", "ungraded", "unsubmitted", "upcoming", "future"], None] = None,
    assignment_ids: Union[list[Union[str, int]], None] = None,
    order_by: Union[Literal["position", "name", "due_at"], None] = None,
    post_to_sis: bool = False,
    new_quizzes: bool = False,
) -> dict:
    payload = {}
    if include is not None:
        payload["include[]"] = include  # TODO: can prob change this to be a list of multiple include...
    if search_term is not None:
        payload["search_term"] = search_term
    if override_assignment_dates is not None:
        payload["override_assignment_dates"] = override_assignment_dates
    if needs_grading_count_by_section is not None:
        payload["needs_grading_count_by_section"] = needs_grading_count_by_section
    if bucket is not None:
        payload["bucket"] = bucket
    if assignment_ids is not None:
        payload["assignment_ids[]"] = assignment_ids
    if order_by is not None:
        payload["order_by"] = order_by
    if post_to_sis is not None:
        payload["post_to_sis"] = post_to_sis
    if new_quizzes is not None:
        payload["new_quizzes"] = new_quizzes

    url = self._get_endpoint("get_course_assignments", {"<course_id>": course_id})
    if payload:
        query_params = urllib.parse.urlencode(payload, doseq=True)
        url = f"{url}?{query_params}"
    return self.make_request(req_type="get", url=url)


async def get_assignment(
    self,
    course_id: Union[str, int],
    assignment_id: Union[str, int],
    include: Union[
        Literal[
            "submission",
            "assignment_visibility",
            "overrides",
            "observed_users",
            "can_edit",
            "score_statistics",
            "ab_guid",
        ],
        None,
    ] = None,
    override_assignment_dates: bool = True,
    needs_grading_count_by_section: bool = False,
    all_dates: bool = False,
) -> dict:
    payload = {}

    if include is not None:
        payload["include[]"] = include
    if override_assignment_dates is not None:
        payload["override_assignment_dates"] = override_assignment_dates
    if needs_grading_count_by_section is not None:
        payload["needs_grading_count_by_section"] = needs_grading_count_by_section
    if all_dates is not None:
        payload["all_dates"] = all_dates

    url = self._get_endpoint("get_assignment", {"<course_id>": course_id, "<assignment_id>": assignment_id})
    if payload:
        query_params = urllib.parse.urlencode(payload, doseq=True)
        url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)


async def get_course_assignment_groups(
    self,
    course_id: Union[str, int],
    include: Union[
        list[
            Literal[
                "assignments",
                "discussion_topic",
                "all_dates",
                "assignment_visibility",
                "overrides",
                "submission",
                "observed_users",
                "can_edit",
                "score_statistics",
            ]
        ],
        None,
    ] = None,
    assignment_ids: Union[list[Union[str, int]], None] = None,
    exclude_assignment_submission_types: Union[
        list[Literal["online_quiz", "discussion_topic", "wiki_page", "external_tool"]],
        None,
    ] = None,
    override_assignment_dates: bool = True,
    grading_period_id: Union[int, None] = None,
    scope_assignments_to_student: bool = False,
) -> dict:
    payload = {}
    if include is not None:
        payload["include[]"] = include
    if assignment_ids is not None:
        payload["assignment_ids[]"] = assignment_ids
    if exclude_assignment_submission_types is not None:
        payload["exclude_assignment_submission_types[]"] = exclude_assignment_submission_types
    if override_assignment_dates is not None:
        payload["override_assignment_dates"] = override_assignment_dates
    if grading_period_id is not None:
        payload["grading_period_id"] = grading_period_id
    if scope_assignments_to_student is not None:
        payload["scope_assignments_to_student"] = scope_assignments_to_student

    url = self._get_endpoint("get_course_assignment_groups", {"<course_id>": course_id})

    if payload:
        query_params = urllib.parse.urlencode(payload, doseq=True)
        url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)


async def get_assignment_group(
    self,
    course_id: Union[str, int],
    assignment_group_id: Union[str, int],
    include: Union[
        Literal[
            "assignments",
            "discussion_topic",
            "assignment_visibility",
            "submission",
            "score_statistics",
        ],
        None,
    ] = None,
    override_assignment_dates=True,
    grading_period_id: Union[int, None] = None,
) -> dict:

    payload = {}
    if include is not None:
        payload["include[]"] = include
    if override_assignment_dates is not None:
        payload["override_assignment_dates"] = override_assignment_dates
    if grading_period_id is not None:
        payload["grading_period_id"] = grading_period_id

    url = self._get_endpoint(
        "get_assignment_group", {"<course_id>": course_id, "<assignment_group_id>": assignment_group_id}
    )
    if payload:
        query_params = urllib.parse.urlencode(payload, doseq=True)
        url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)
