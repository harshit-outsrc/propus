import datetime
import urllib.parse
from typing import Literal, Union, Optional


async def list_assignment_submissions_for_single_assignment(
    self,
    object_type: Literal["course", "section"],
    object_id: Union[int, str],
    assignment_id: Union[int, str],
    include: Optional[
        list[
            Literal[
                "submission_history",
                "submission_comments",
                "rubric_assessment",
                "assignment",
                "visibility",
                "course",
                "user",
                "group",
                "read_status",
            ]
        ]
    ] = None,
    grouped: Optional[bool] = None,
) -> list[dict]:
    """
    Returns the list of submissions for the specified assignment.
    :param self:
    :param object_type: The type of object to list submissions for. Either 'course' or 'section'.
    :param object_id: The id of the object to list submissions for. This is the course or section id.
    :param assignment_id: The id of the assignment to list submissions for.
    :param include: Associations to include with the group. “group” will add group_id and group_name.
    :param grouped: If this argument is true, the response will be grouped by student groups.
    :return: The list of submissions for the specified assignment.
    """
    payload = {}
    if include is not None:
        payload["include[]"] = include
    if grouped is not None:
        payload["grouped"] = grouped

    if object_type == "course":
        url = self._get_endpoint(
            "list_assignment_submissions_by_course_single_assignment",
            {"<course_id>": object_id, "<assignment_id>": assignment_id},
        )
    elif object_type == "section":
        url = self._get_endpoint(
            "list_assignment_submissions_by_section_single_assignment",
            {"<section_id>": object_id, "<assignment_id>": assignment_id},
        )

    query_params = urllib.parse.urlencode(payload, doseq=True)
    url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)


async def list_assignment_submissions_for_multiple_assignments(
    self,
    object_type: Literal["course", "section"],
    object_id: Union[int, str],
    student_ids: Union[list[str], str] = "all",
    assignment_ids: Optional[list[str]] = None,
    grouped: Optional[bool] = None,
    post_to_sis: Optional[bool] = None,
    submitted_since: Optional[datetime.datetime] = None,
    graded_since: Optional[datetime.datetime] = None,
    grading_period_id: Optional[int] = None,
    workflow_state: Optional[Literal["submitted", "unsubmitted", "graded", "pending_review"]] = None,
    enrollment_state: Optional[Literal["active", "concluded"]] = None,
    state_based_on_date: Optional[bool] = None,
    order: Optional[Literal["id", "graded_at"]] = None,
    order_direction: Optional[Literal["ascending", "descending"]] = None,
    include: Optional[
        list[
            Literal[
                "submission_history",
                "submission_comments",
                "rubric_assessment",
                "assignment",
                "total_scores",
                "visibility",
                "course",
                "user",
            ]
        ]
    ] = None,
) -> list[dict]:
    """
    Returns a list of submissions for multiple assignments.
    :param self:
    :param object_type: The type of object to list submissions for. Either 'course' or 'section'.
    :param object_id: The id of the object to list submissions for. This is the course or section id.
    :param student_ids: List of student ids to return submissions for. If this argument is omitted, return submissions
        for the calling user. Students may only list their own submissions. Observers may only list those of associated
         students. The special id “all” will return submissions for all students in the course/section as appropriate.
    :param assignment_ids: List of assignments to return submissions for. If none are given, submissions for all
        assignments are returned.
    :param grouped: If this argument is present, the response will be grouped by student, rather than a flat
        array of submissions.
    :param post_to_sis: If this argument is set to true, the response will only include submissions for assignments
        that have the post_to_sis flag set to true and user enrollments that were added through sis.
    :param submitted_since: If this argument is set, the response will only include submissions that were submitted
        after the specified date_time. This will exclude submissions that do not have a submitted_at which will exclude
         unsubmitted submissions. The value must be formatted as ISO 8601 YYYY-MM-DDTHH:MM:SSZ.
    :param graded_since: If this argument is set, the response will only include submissions that were graded after
        the specified date_time. This will exclude submissions that have not been graded. The value must be formatted
        as ISO 8601 YYYY-MM-DDTHH:MM:SSZ.
    :param grading_period_id: The id of the grading period in which submissions are being requested
        (Requires grading periods to exist on the account)
    :param workflow_state: The current status of the submission
    :param enrollment_state: The current state of the enrollments. If omitted will include all enrollments
        that are not deleted.
    :param state_based_on_date: If omitted it is set to true. When set to false it will ignore the effective state of
        the student enrollments and use the workflow_state for the enrollments. The argument is ignored unless
         enrollment_state argument is also passed.
    :param order: The order submissions will be returned in. Defaults to “id”. Doesn’t affect results for
        “grouped” mode.
    :param order_direction: Determines whether ordered results are returned in ascending or descending order.
        Defaults to “ascending”. Doesn’t affect results for “grouped” mode.
    :param include: Associations to include with the group. ‘total_scores` requires the `grouped` argument.
    :return: A list of submissions for multiple assignments.
    """
    payload = {"student_ids[]": student_ids}
    if assignment_ids is not None:
        payload["assignment_ids[]"] = assignment_ids
    if grouped is not None:
        payload["grouped"] = grouped
    if post_to_sis is not None:
        payload["post_to_sis"] = post_to_sis
    if submitted_since is not None:
        payload["submitted_since"] = submitted_since.isoformat()
    if graded_since is not None:
        payload["graded_since"] = graded_since.isoformat()
    if grading_period_id is not None:
        payload["grading_period_id"] = grading_period_id
    if workflow_state is not None:
        payload["workflow_state"] = workflow_state
    if enrollment_state is not None:
        payload["enrollment_state"] = enrollment_state
    if state_based_on_date is not None:
        payload["state_based_on_date"] = state_based_on_date
    if order is not None:
        payload["order"] = order
    if order_direction is not None:
        payload["order_direction"] = order_direction
    if include is not None:
        payload["include[]"] = include

    if object_type == "course":
        url = self._get_endpoint(
            "list_assignment_submissions_by_course_multiple_assignments",
            {"<course_id>": object_id},
        )
    elif object_type == "section":
        url = self._get_endpoint(
            "list_assignment_submissions_by_section_multiple_assignments",
            {"<section_id>": object_id},
        )

    query_params = urllib.parse.urlencode(payload, doseq=True)
    url = f"{url}?{query_params}"
    return self.make_request(req_type="get", url=url)


async def get_single_submission(
    self,
    object_type: Literal["course", "section"],
    object_id: Union[int, str],
    assignment_id: Union[int, str],
    user_id: Union[int, str],
    include: Optional[
        list[
            Literal[
                "submission_history",
                "submission_comments",
                "rubric_assessment",
                "full_rubric_assessment",
                "visibility",
                "course",
                "user",
                "read_status",
            ]
        ]
    ] = None,
) -> dict:
    """
    Returns a single submission based on the submission id and user id. Can be used on either course or section.
    :param self:
    :param object_type: The type of object to list submissions for. Either 'course' or 'section'.
    :param object_id: The id of the object to list submissions for. This is the course or section id.
    :param assignment_id: The id of the assignment to list submissions for.
    :param user_id: The id of the user to list submissions for.
    :param include: Associations to include with the group.
    :return: A single submission object.
    """
    payload = {}
    if include is not None:
        payload["include[]"] = include

    if object_type == "course":
        url = self._get_endpoint(
            "get_single_submission_by_course_and_user",
            {
                "<course_id>": object_id,
                "<assignment_id>": assignment_id,
                "<user_id>": user_id,
            },
        )
    elif object_type == "section":
        url = self._get_endpoint(
            "get_single_submission_by_section_and_user",
            {
                "<section_id>": object_id,
                "<assignment_id>": assignment_id,
                "<user_id>": user_id,
            },
        )

    query_params = urllib.parse.urlencode(payload, doseq=True)
    url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)


async def get_submission_summary(
    self,
    object_type: Literal["course", "section"],
    object_id: Union[int, str],
    assignment_id: Union[int, str],
    grouped: bool = False,
) -> dict:
    """
    Returns the number of submissions for the given assignment based on gradeable students that fall into three
        categories: graded, ungraded, not submitted.
    :param self:
    :param object_type: The type of object to list submissions for. Either 'course' or 'section'.
    :param object_id: The id of the object to list submissions for. This is the course or section id.
    :param assignment_id: The id of the assignment to list submissions for.
    :param grouped: If this argument is true, the response will take into account student groups.
    :return: a summary of the number of submissions for the given assignment. For example:
        {
          "graded": 5,
          "ungraded": 10,
          "not_submitted": 42
        }
    """
    payload = {"grouped": grouped}
    if object_type == "course":
        url = self._get_endpoint(
            "get_submission_summary_by_course",
            {
                "<course_id>": object_id,
                "<assignment_id>": assignment_id,
            },
        )
    elif object_type == "section":
        url = self._get_endpoint(
            "get_submission_summary_by_section",
            {
                "<section_id>": object_id,
                "<assignment_id>": assignment_id,
            },
        )

    query_params = urllib.parse.urlencode(payload, doseq=True)
    url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)


async def list_missing_submissions_for_user(
    self,
    user_id: Union[str, int],
    observed_user_id: Optional[str] = None,
    include: Optional[list[Literal["planner_overrides", "course"]]] = None,
    filter: Optional[list[Literal["submittable", "current_grading_period"]]] = None,
    course_ids: Optional[list[Union[str, int]]] = None,
) -> list[dict]:
    """
    Returns a list of assignments the user has not submitted and the due date has passed.
    :param self:
    :param user_id: The id of the user to list missing submissions for.
    :param observed_user_id: Return missing submissions for the given observed user. Must be accompanied by
        course_ids[]. The user making the request must be observing the observed user in all the courses specified
        by course_ids[].
    :param include: “planner_overrides” Optionally include the assignment’s associated planner override, if it exists,
        for the current user. These will be returned under a planner_override key.
        "course" Optionally include the assignments’ courses
    :param filter: submittable” Only return assignments that the current user can submit (filter out locked assignments)
        “current_grading_period” Only return missing assignments that are in the current grading period
    :param course_ids: Optionally restricts the list of past-due assignments to only those associated with the
        specified course IDs. Required if observed_user_id is passed.

    :return: A list of missing assignments.
    """
    payload = {}
    if observed_user_id is not None:
        payload["observed_user_id"] = observed_user_id
    if include is not None:
        payload["include[]"] = include
    if filter is not None:
        payload["filter[]"] = filter
    if course_ids is not None:
        payload["course_ids[]"] = course_ids

    url = self._get_endpoint(
        "list_missing_submissions_by_user",
        {"<user_id>": user_id},
    )
    query_params = urllib.parse.urlencode(payload, doseq=True)
    url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)
