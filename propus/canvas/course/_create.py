import datetime
import json
from typing import Literal, Union, Optional


async def create_course(
    self,
    account_id: Union[str, int],
    course_name: str,
    course_code: str,
    term_id: Union[str, int],
    sis_course_id: str,
    start_at: Optional[datetime.datetime] = None,
    end_at: Optional[datetime.datetime] = None,
    license: Optional[
        Literal[
            "private",
            "cc_by_nc_nd",
            "cc_by_nc_sa",
            "cc_by_nc",
            "cc_by_nd",
            "cc_by_sa",
            "cc_by",
            "public_domain",
        ]
    ] = "private",
    is_public: bool = False,
    is_public_to_auth_users: bool = False,
    public_syallbus: bool = False,
    public_syllabus_to_auth: bool = False,
    public_description: Optional[str] = None,
    allow_student_wiki_edits: bool = False,
    allow_wiki_comments: bool = False,
    allow_student_forum_attachments: bool = True,
    open_enrollment: bool = False,
    self_enrollment: bool = False,
    restrict_enrollments_to_course_dates: bool = False,
    integration_id: Optional[str] = None,
    hide_final_grades: bool = False,
    apply_assignment_group_weights: bool = True,
    time_zone: str = "America/Los_Angeles",
    default_view: Literal["feed", "wiki", "modules", "syllabus", "assignments"] = "syllabus",
    syllabus_body: Optional[str] = None,
    grading_standard_id: Optional[str] = None,
    grade_passback_setting: Optional[Literal["nightly_sync", "disabled", ""]] = None,
    course_format: Literal["online", "on_campus", "blended"] = "online",
    offer: bool = False,
    enroll_me: bool = False,
    enable_sis_reactivation: bool = True,
) -> dict:
    """
    Create a course. This is a wrapper around the Canvas API endpoint for creating a course.
    :param self:
    :param account_id:
    :param course_name: The name of the course. If omitted, the course will be named “Unnamed Course.”
    :param course_code: The course code for the course.
    :param term_id: The unique ID of the term to create to course in.
    :param sis_course_id: The unique SIS identifier.
    :param start_at: Course start date in ISO8601 format, e.g. 2011-01-01T01:00Z
        This value is ignored unless ‘restrict_enrollments_to_course_dates’ is set to true.
    :param end_at: Course end date in ISO8601 format. e.g. 2011-01-01T01:00Z
        This value is ignored unless ‘restrict_enrollments_to_course_dates’ is set to true.
    :param license: The name of the licensing. Options are: 'private' (Private Copyrighted),
        'cc_by_nc_nd' (CC Attribution Non-Commercial No Derivatives),
        'cc_by_nc_sa' (CC Attribution Non-Commercial Share Alike),
        'cc_by_nc' (CC Attribution Non-Commercial), 'cc_by_nd' (CC Attribution No Derivatives),
        'cc_by_sa' (CC Attribution Share Alike), 'cc_by' (CC Attribution),
        'public_domain' (Public Domain).,
    :param is_public: Set to true if course is public to both authenticated and unauthenticated users.
    :param is_public_to_auth_users: Set to true if course is public only to authenticated users.
    :param public_syallbus: Set to true to make the course syllabus public.
    :param public_syllabus_to_auth: Set to true to make the course syllabus public for authenticated users.
    :param public_description: A publicly visible description of the course.
    :param allow_student_wiki_edits: If true, students will be able to modify the course wiki.
    :param allow_wiki_comments: If true, course members will be able to comment on wiki pages.
    :param allow_student_forum_attachments: If true, students can attach files to forum posts.
    :param open_enrollment: Set to true if the course is open enrollment.
    :param self_enrollment: Set to true if the course is self enrollment.
    :param restrict_enrollments_to_course_dates: Set to true to restrict user enrollments to the start and end dates
        of the course. This value must be set to true in order to specify a course start date and/or end date.
    :param integration_id: The unique Integration identifier.
    :param hide_final_grades: If this option is set to true, the totals in student grades summary will be hidden.
    :param apply_assignment_group_weights: Set to true to weight final grade based on assignment groups percentages.
    :param time_zone: The time zone for the course. Allowed time zones are IANA time zones or friendlier
        Ruby on Rails time zones.
    :param default_view: The type of page that users will see when they first visit the course.
        Options are: 'feed' (Recent Activity Dashboard), 'modules' (Course Modules/Sections Page),
        'assignments' (Course Assignments List), 'syllabus' (Course Syllabus Page)
        Note: other types may be added in the future
    :param syllabus_body: The syllabus body for the course
    :param grading_standard_id: The grading standard id to set for the course. If no value is provided for this
        argument the current grading_standard will be un-set from this course.
    :param grade_passback_setting: Optional. The grade_passback_setting for the course.
        Only ‘nightly_sync’, ‘disabled’, and ” are allowed
    :param course_format: Optional. Specifies the format of the course. (Should be ‘on_campus’, ‘online’, or ‘blended’)
    :param offer: If this option is set to true, the course will be available to students immediately.
    :param enroll_me: Set to true to enroll the current user as the teacher.
    :param enable_sis_reactivation: When true, will first try to re-activate a deleted course with matching
        sis_course_id if possible.
    :return: The created course object
    """

    payload = {
        "course": {
            "name": course_name,
            "course_code": course_code,
            "is_public": is_public,
            "is_public_to_auth_users": is_public_to_auth_users,
            "public_syllabus": public_syallbus,
            "public_syllabus_to_auth": public_syllabus_to_auth,
            "allow_student_wiki_edits": allow_student_wiki_edits,
            "allow_wiki_comments": allow_wiki_comments,
            "allow_student_forum_attachments": allow_student_forum_attachments,
            "open_enrollment": open_enrollment,
            "self_enrollment": self_enrollment,
            "term_id": term_id,
            "sis_course_id": sis_course_id,
            "hide_final_grades": hide_final_grades,
            "apply_assignment_group_weights": apply_assignment_group_weights,
            "time_zone": time_zone,
            "default_view": default_view,
            "course_format": course_format,
        },
        "offer": offer,
        "enroll_me": enroll_me,
        "enable_sis_reactivation": enable_sis_reactivation,
    }

    if start_at is not None and restrict_enrollments_to_course_dates:
        payload["course"]["start_at"] = start_at.isoformat()
    if end_at is not None and restrict_enrollments_to_course_dates:
        payload["course"]["end_at"] = end_at.isoformat()
    if restrict_enrollments_to_course_dates:
        payload["course"]["restrict_enrollments_to_course_dates"] = True
    if license is not None:
        payload["course"]["license"] = license
    if public_description is not None:
        payload["course"]["public_description"] = public_description
    if integration_id is not None:
        payload["course"]["integration_id"] = integration_id
    if syllabus_body is not None:
        payload["course"]["syllabus_body"] = syllabus_body
    if grading_standard_id is not None:
        payload["course"]["grading_standard_id"] = grading_standard_id
    if grade_passback_setting is not None:
        payload["course"]["grade_passback_setting"] = grade_passback_setting

    return self.make_request(
        req_type="post",
        url=self._get_endpoint("create_course", {"<account_id>": account_id}),
        data=json.dumps(payload),
    )


async def create_section(
    self,
    course_id: Union[str, int],
    name: str,
    sis_section_id: str,
    integration_id: Optional[str] = None,
    start_at: Optional[datetime.datetime] = None,
    end_at: Optional[datetime.datetime] = None,
    restrict_enrollments_to_section_dates: bool = False,
    enable_sis_reactivation: bool = True,
) -> dict:
    """
    Create a section. This is a wrapper around the Canvas API endpoint for creating a section.
    :param self:
    :param course_id: The course ID to create the section in
    :param name: The name of the section
    :param sis_section_id: The sis ID of the section. Must have manage_sis permission to set.
        This is ignored if caller does not have permission to set.
    :param integration_id: The integration_id of the section. Must have manage_sis permission to set.
        This is ignored if caller does not have permission to set.
    :param start_at: Section start date in ISO8601 format, e.g. 2011-01-01T01:00Z
    :param end_at: Section end date in ISO8601 format. e.g. 2011-01-01T01:00Z
    :param restrict_enrollments_to_section_dates: Set to true to restrict user enrollments to the start
        and end dates of the section.
    :param enable_sis_reactivation: When true, will first try to re-activate a deleted section with
        matching sis_section_id if possible.
    :return: The created section object
    """

    payload = {
        "course_section": {
            "name": name,
            "sis_section_id": sis_section_id,
        },
        "enable_sis_reactivation": enable_sis_reactivation,
    }

    if integration_id is not None:
        payload["course_section"]["integration_id"] = integration_id
    if start_at is not None and restrict_enrollments_to_section_dates:
        payload["course_section"]["start_at"] = start_at.isoformat()
    if end_at is not None and restrict_enrollments_to_section_dates:
        payload["course_section"]["end_at"] = end_at.isoformat()
    if restrict_enrollments_to_section_dates:
        payload["course_section"]["restrict_enrollments_to_section_dates"] = True

    return self.make_request(
        req_type="post",
        url=self._get_endpoint("create_section", {"<course_id>": course_id}),
        data=json.dumps(payload),
    )
