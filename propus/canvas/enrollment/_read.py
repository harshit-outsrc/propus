from typing import Literal, Union, Optional

import urllib.parse


async def list_enrollments(
    self,
    object_type: Literal["user", "section", "course"],
    object_id: Union[str, int],
    enrollment_type: Optional[
        Literal[
            "StudentEnrollment",
            "TeacherEnrollment",
            "TaEnrollment",
            "ObserverEnrollment",
            "DesignerEnrollment",
        ]
    ] = None,
    role: Optional[str] = None,
    state: Optional[
        Literal[
            "active",
            "invited",
            "creation_pending",
            "deleted",
            "rejected",
            "completed",
            "inactive",
            "current_and_invited",
            "current_and_future",
            "current_and_concluded",
        ]
    ] = None,
    include: Optional[
        list[
            Literal[
                "avatar_url",
                "group_ids",
                "locked",
                "observed_users",
                "can_be_removed",
                "uuid",
                "current_points",
            ]
        ]
    ] = None,
    user_id: Optional[str] = None,
    grading_period_id: Optional[int] = None,
    enrollment_term_id: Optional[int] = None,
    sis_account_id: Optional[Union[str, list[str]]] = None,
    sis_course_id: Optional[Union[str, list[str]]] = None,
    sis_section_id: Optional[Union[str, list[str]]] = None,
    sis_user_id: Optional[Union[str, list[str]]] = None,
    created_for_sis_id: Optional[bool] = None,
) -> list[dict]:
    """
    List enrollments for a user, section, or course.
    :param self:
    :param list_type: This function can list enrollments for a user, section, or course.
    :param object_id: The ID of the user, section, or course.
    :param enrollment_type: A list of enrollment types to return. If omitted, all enrollment types are returned.
        This argument is ignored if ‘role` is given
    :param role: A list of enrollment roles to return. Accepted values include course-level roles created by the
        Add Role API as well as the base enrollment types accepted by the ‘type` argument above.
    :param state: Filter by enrollment state. If omitted, ‘active’ and ‘invited’ enrollments are returned.
        The following synthetic states are supported only when querying a user’s enrollments (either via user_id
        argument or via user enrollments endpoint) - current_and_invited, current_and_future, current_and_concluded
    :param include: Array of additional information to include on the enrollment or user records. “avatar_url” and
        “group_ids” will be returned on the user record. If “current_points” is specified, the fields “current_points”
        and (if the caller has permissions to manage grades) “unposted_current_points” will be included in the
        “grades” hash for student enrollments.
    :param user_id: Filter by user_id (only valid for course or section enrollment queries).
        If set to the current user’s id, this is a way to determine if the user has any enrollments in the course or
        section, independent of whether the user has permission to view other people on the roster.
    :param grading_period_id: Return grades for the given grading_period. If this parameter is not specified,
        the returned grades will be for the whole course.
    :param enrollment_term_id: Returns only enrollments for the specified enrollment term. This parameter only applies
        to the user enrollments path. May pass the ID from the enrollment terms api or the SIS id prepended
        with ‘sis_term_id:’.
    :param sis_account_id: Returns only enrollments for the specified SIS account ID(s).
        Does not look into sub_accounts. May pass in array or string.
    :param sis_course_id: Returns only enrollments matching the specified SIS course ID(s).
        May pass in array or string.
    :param sis_section_id: Returns only section enrollments matching the specified SIS section ID(s).
        May pass in array or string.
    :param sis_user_id: Returns only enrollments for the specified SIS user ID(s). May pass in array or string.
    :param created_for_sis_id: If sis_user_id is present and created_for_sis_id is true, Returns only enrollments for
        the specified SIS ID(s). If a user has two sis_id’s, one enrollment may be created using one of the two ids.
        This would limit the enrollments returned from the endpoint to enrollments that were created from a sis_import
        with that sis_user_id
    :return: A list of enrollments
    """
    payload = {}

    if enrollment_type is not None:
        payload["type[]"] = enrollment_type
    if role is not None:
        payload["role[]"] = role
    if state is not None:
        payload["state[]"] = state
    if include is not None:
        payload["include[]"] = include
    if user_id is not None:
        payload["user_id"] = user_id
    if grading_period_id is not None:
        payload["grading_period_id"] = grading_period_id
    if enrollment_term_id is not None:
        payload["enrollment_term_id"] = enrollment_term_id
    if sis_account_id is not None:
        payload["sis_account_id[]"] = sis_account_id
    if sis_course_id is not None:
        payload["sis_course_id[]"] = sis_course_id
    if sis_section_id is not None:
        payload["sis_section_id[]"] = sis_section_id
    if sis_user_id is not None:
        payload["sis_user_id[]"] = sis_user_id
    if created_for_sis_id is not None:
        payload["created_for_sis_id[]"] = created_for_sis_id

    if object_type == "user":
        url = self._get_endpoint("list_user_enrollments", {"<user_id>": object_id})
    elif object_type == "section":
        url = self._get_endpoint("list_section_enrollments", {"<section_id>": object_id})
    elif object_type == "course":
        url = self._get_endpoint("list_course_enrollments", {"<course_id>": object_id})
    if payload:
        query_params = urllib.parse.urlencode(payload, doseq=True)
        url = f"{url}?{query_params}"
    return self.make_request(req_type="get", url=url)


async def list_students_in_course(self, course_id: Union[str, int]) -> list[dict]:
    """
    List student enrollments in a course.
    :param self:
    :param course_id: The ID of the course.
    :return: A list of student enrollments in the course.
    """
    return self.make_request(
        req_type="get",
        url=self._get_endpoint("list_students_in_course", {"<course_id>": course_id}),
    )


async def get_single_enrollment(self, enrollment_id: Union[str, int]) -> dict:
    """
    Get a single enrollment by ID
    :param self:
    :param enrollment_id: The ID of the enrollment.
    :return: The enrollment object
    """
    return self.make_request(
        req_type="get", url=self._get_endpoint("get_single_enrollment", {"<enrollment_id>": enrollment_id})
    )
