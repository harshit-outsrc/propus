import json
from dataclasses import dataclass
from typing import Literal, Optional, Union
import datetime


@dataclass
class BlueprintRestriction:
    content: bool  # Restriction on main content (e.g. title, description).
    points: bool  # Restriction on points possible for assignments and graded learning objects
    due_date: bool  # Restriction on due dates for assignments and graded learning objects
    availability_dates: bool  # Restriction on availability dates for an object


async def update_course(
    self,
    course_id: Union[str, int],
    account_id: Optional[int] = None,
    name: Optional[str] = None,
    course_code: Optional[str] = None,
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
    ] = None,
    is_public: Optional[bool] = None,
    is_public_to_auth_users: Optional[bool] = None,
    public_syllabus: Optional[bool] = None,
    public_syllabus_to_auth: Optional[bool] = None,
    public_description: Optional[str] = None,
    allow_student_wiki_edits: Optional[bool] = None,
    allow_wiki_comments: Optional[bool] = None,
    allow_student_forum_attachments: Optional[bool] = None,
    open_enrollment: Optional[bool] = None,
    self_enrollment: Optional[bool] = None,
    restrict_enrollments_to_course_dates: Optional[bool] = None,
    term_id: Optional[int] = None,
    sis_course_id: Optional[str] = None,
    integration_id: Optional[str] = None,
    hide_final_grades: Optional[bool] = None,
    time_zone: Optional[str] = None,
    apply_assignment_group_weights: Optional[bool] = None,
    storage_quota_mb: Optional[int] = None,
    event: Optional[Literal["claim", "offer", "conclude", "delete", "undelete"]] = None,
    default_view: Optional[Literal["feed", "wiki", "modules", "syllabus", "assignments"]] = None,
    syllabus_body: Optional[str] = None,
    syllabus_course_summary: Optional[bool] = None,
    grading_standard_id: Optional[int] = None,
    grade_passback_setting: Optional[Literal["nightly_sync", ""]] = None,
    course_format: Optional[Literal["online", "on_campus"]] = None,
    image_id: Optional[int] = None,
    image_url: Optional[str] = None,
    remove_image: Optional[bool] = None,
    remove_banner_image: Optional[bool] = None,
    blueprint: Optional[bool] = None,
    blueprint_restrictions: Optional[BlueprintRestriction] = None,
    use_blueprint_restrictions_by_object_type: Optional[bool] = None,
    blueprint_restrictions_by_object_type_assignment: Optional[BlueprintRestriction] = None,
    blueprint_restrictions_by_object_type_attachment: Optional[BlueprintRestriction] = None,
    blueprint_restrictions_by_object_type_discussion_topic: Optional[BlueprintRestriction] = None,
    blueprint_restrictions_by_object_type_quiz: Optional[BlueprintRestriction] = None,
    blueprint_restrictions_by_object_type_wiki_page: Optional[BlueprintRestriction] = None,
    template: Optional[bool] = None,
    enable_course_paces: Optional[bool] = None,
    conditional_release: Optional[bool] = None,
    offer: Optional[bool] = None,
    override_sis_stickiness: bool = True,
) -> dict:
    """
    Update a course in Canvas. This method is a wrapper for the Canvas API endpoint.
    :param self:
    :param course_id:
    :param account_id: The unique ID of the account to move the course to.
    :param name: The name of the course. If omitted, the course will be named “Unnamed Course.”
    :param course_code: The course code for the course.
    :param start_at: Course start date in ISO8601 format, e.g. 2011-01-01T01:00Z This value is ignored unless
        ‘restrict_enrollments_to_course_dates’ is set to true, or the course is already published.
    :param end_at: Course end date in ISO8601 format. e.g. 2011-01-01T01:00Z This value is ignored unless
        ‘restrict_enrollments_to_course_dates’ is set to true.
    :param license:  The name of the licensing. Options are: 'private' (Private Copyrighted),
        'cc_by_nc_nd' (CC Attribution Non-Commercial No Derivatives),
        'cc_by_nc_sa' (CC Attribution Non-Commercial Share Alike),
        'cc_by_nc' (CC Attribution Non-Commercial), 'cc_by_nd' (CC Attribution No Derivatives),
        'cc_by_sa' (CC Attribution Share Alike), 'cc_by' (CC Attribution),
        'public_domain' (Public Domain).,
    :param is_public: Set to true if course is public to both authenticated and unauthenticated users.
    :param is_public_to_auth_users: Set to true if course is public only to authenticated users.
    :param public_syllabus: Set to true to make the course syllabus public.
    :param public_syllabus_to_auth: Set to true to make the course syllabus to public for authenticated users.
    :param public_description: A publicly visible description of the course.
    :param allow_student_wiki_edits: If true, students will be able to modify the course wiki.
    :param allow_wiki_comments: If true, course members will be able to comment on wiki pages.
    :param allow_student_forum_attachments: If true, students can attach files to forum posts.
    :param open_enrollment: Set to true if the course is open enrollment.
    :param self_enrollment: Set to true if the course is self enrollment.
    :param restrict_enrollments_to_course_dates: Set to true to restrict user enrollments to the start and end dates
        of the course. Setting this value to false will remove the course end date (if it exists),
         as well as the course start date (if the course is unpublished).
    :param term_id: The unique ID of the term to create to course in.
    :param sis_course_id: The unique SIS identifier.
    :param integration_id: The unique Integration identifier.
    :param hide_final_grades: If this option is set to true, the totals in student grades summary will be hidden.
    :param time_zone: The time zone for the course. Allowed time zones are IANA time zones or friendlier
        Ruby on Rails time zones.
    :param apply_assignment_group_weights: Set to true to weight final grade based on assignment groups percentages.
    :param storage_quota_mb: Set the storage quota for the course, in megabytes. The caller must have the
        “Manage storage quotas” account permission.
    :param event: The action to take on each course.
        - "claim" makes a course no longer visible to students. This action is also called “unpublish” on the web site.
         A course cannot be unpublished if students have received graded submissions.
        - "offer" makes a course visible to students. This action is also called “publish” on the web site.
        - "conclude" prevents future enrollments and makes a course read-only for all participants.
        The course still appears in prior-enrollment lists.
        - "delete" completely removes the course from the web site (including course menus and prior-enrollment lists).
        All enrollments are deleted. Course content may be physically deleted at a future date.
        - "undelete" attempts to recover a course that has been deleted. This action requires account administrative
         rights. (Recovery is not guaranteed; please conclude rather than delete a course if there is any possibility
          the course will be used again.) The recovered course will be unpublished.
          Deleted enrollments will not be recovered.
    :param default_view: The type of page that users will see when they first visit the course.
        Options are: 'feed' (Recent Activity Dashboard), 'modules' (Course Modules/Sections Page),
        'assignments' (Course Assignments List), 'syllabus' (Course Syllabus Page)
        Note: other types may be added in the future
    :param syllabus_body: The syllabus body for the course
    :param syllabus_course_summary: Optional. Indicates whether the Course Summary (consisting of the course’s
        assignments and calendar events) is displayed on the syllabus page. Defaults to true.
    :param grading_standard_id: The grading standard id to set for the course. If no value is provided for this
        argument the current grading_standard will be un-set from this course.
    :param grade_passback_setting: Optional. The grade_passback_setting for the course.
        Only ‘nightly_sync’ and ” are allowed #
    :param course_format: Optional. Specifies the format of the course. (Should be either ‘on_campus’ or ‘online’)
    :param image_id: This is a file ID corresponding to an image file in the course that will be used as the course
        image. This will clear the course’s image_url setting if set.
        If you attempt to provide image_url and image_id in a request it will fail.
    :param image_url: This is a URL to an image to be used as the course image. This will clear the course’s
        image_id setting if set. If you attempt to provide image_url and image_id in a request it will fail.
    :param remove_image: If this option is set to true, the course image url and course image ID are both set to nil
    :param remove_banner_image: If this option is set to true, the course banner image url and course banner
        image ID are both set to nil
    :param blueprint: Sets the course as a blueprint course.
    :param blueprint_restrictions: Sets a default set to apply to blueprint course objects when restricted,
        unless use_blueprint_restrictions_by_object_type is enabled. See the Blueprint Restriction documentation
    :param use_blueprint_restrictions_by_object_type: When enabled, the blueprint_restrictions parameter will be
        ignored in favor of the blueprint_restrictions_by_object_type parameter
    :param blueprint_restrictions_by_object_type_assignment: Allows setting multiple Blueprint Restriction to apply to
        blueprint course objects of the matching type when restricted.
    :param blueprint_restrictions_by_object_type_attachment: Allows setting multiple Blueprint Restriction to apply to
        blueprint course objects of the matching type when restricted.
    :param blueprint_restrictions_by_object_type_discussion_topic: Allows setting multiple Blueprint Restriction
        to apply to blueprint course objects of the matching type when restricted.
    :param blueprint_restrictions_by_object_type_quiz: Allows setting multiple Blueprint Restriction to apply to
        blueprint course objects of the matching type when restricted.
    :param blueprint_restrictions_by_object_type_wiki_page: Allows setting multiple Blueprint Restriction to apply to
        blueprint course objects of the matching type when restricted.
    :param template: Enable or disable the course as a template that can be selected by an account
    :param enable_course_paces: Enable or disable Course Pacing for the course. This setting only has an effect when
        the Course Pacing feature flag is enabled for the sub-account. Otherwise, Course Pacing are always disabled.
    :param conditional_release: Enable or disable individual learning paths for students based on assessment
    :param offer: If this option is set to true, the course will be available to students immediately.
    :param override_sis_stickiness: Default is true. If false, any fields containing “sticky” changes will not be
        updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness
    :return: The updated course object
    """
    payload = {"course": {}, "override_sis_stickiness": override_sis_stickiness}

    if (
        blueprint_restrictions_by_object_type_assignment
        or blueprint_restrictions_by_object_type_attachment
        or blueprint_restrictions_by_object_type_discussion_topic
        or blueprint_restrictions_by_object_type_quiz
        or blueprint_restrictions_by_object_type_wiki_page
    ):
        payload["course"]["blueprint_restrictions_by_object_type"] = {}

    if account_id is not None:
        payload["course"]["account_id"] = account_id
    if name is not None:
        payload["course"]["name"] = name
    if course_code is not None:
        payload["course"]["course_code"] = course_code
    if start_at is not None:
        payload["course"]["start_at"] = start_at.isoformat()
    if end_at is not None:
        payload["course"]["end_at"] = end_at.isoformat()
    if license is not None:
        payload["course"]["license"] = license
    if is_public is not None:
        payload["course"]["is_public"] = is_public
    if is_public_to_auth_users is not None:
        payload["course"]["is_public_to_auth_users"] = is_public_to_auth_users
    if public_syllabus is not None:
        payload["course"]["public_syllabus"] = public_syllabus
    if public_syllabus_to_auth is not None:
        payload["course"]["public_syllabus_to_auth"] = public_syllabus_to_auth
    if public_description is not None:
        payload["course"]["public_description"] = public_description
    if allow_student_wiki_edits is not None:
        payload["course"]["allow_student_wiki_edits"] = allow_student_wiki_edits
    if allow_wiki_comments is not None:
        payload["course"]["allow_wiki_comments"] = allow_wiki_comments
    if allow_student_forum_attachments is not None:
        payload["course"]["allow_student_forum_attachments"] = allow_student_forum_attachments
    if open_enrollment is not None:
        payload["course"]["open_enrollment"] = open_enrollment
    if self_enrollment is not None:
        payload["course"]["self_enrollment"] = self_enrollment
    if restrict_enrollments_to_course_dates is not None:
        payload["course"]["restrict_enrollments_to_course_dates"] = restrict_enrollments_to_course_dates
    if term_id is not None:
        payload["course"]["term_id"] = term_id
    if sis_course_id is not None:
        payload["course"]["sis_course_id"] = sis_course_id
    if integration_id is not None:
        payload["course"]["integration_id"] = integration_id
    if hide_final_grades is not None:
        payload["course"]["hide_final_grades"] = hide_final_grades
    if time_zone is not None:
        payload["course"]["time_zone"] = time_zone
    if apply_assignment_group_weights is not None:
        payload["course"]["apply_assignment_group_weights"] = apply_assignment_group_weights
    if storage_quota_mb is not None:
        payload["course"]["storage_quota_mb"] = storage_quota_mb
    if event is not None:
        payload["course"]["event"] = event
    if default_view is not None:
        payload["course"]["default_view"] = default_view
    if syllabus_body is not None:
        payload["course"]["syllabus_body"] = syllabus_body
    if syllabus_course_summary is not None:
        payload["course"]["syllabus_course_summary"] = syllabus_course_summary
    if grading_standard_id is not None:
        payload["course"]["grading_standard_id"] = grading_standard_id
    if grade_passback_setting is not None:
        payload["course"]["grade_passback_setting"] = grade_passback_setting
    if course_format is not None:
        payload["course"]["course_format"] = course_format
    if image_id is not None:
        payload["course"]["image_id"] = image_id
    if image_url is not None:
        payload["course"]["image_url"] = image_url
    if remove_image is not None:
        payload["course"]["remove_image"] = remove_image
    if remove_banner_image is not None:
        payload["course"]["remove_banner_image"] = remove_banner_image
    if blueprint is not None:
        payload["course"]["blueprint"] = blueprint
    if blueprint_restrictions is not None:
        payload["course"]["blueprint_restrictions"] = blueprint_restrictions
    if use_blueprint_restrictions_by_object_type is not None:
        payload["course"]["use_blueprint_restrictions_by_object_type"] = use_blueprint_restrictions_by_object_type
    if blueprint_restrictions_by_object_type_assignment is not None:
        payload["course"]["blueprint_restrictions_by_object_type"][
            "assignment"
        ] = blueprint_restrictions_by_object_type_assignment
    if blueprint_restrictions_by_object_type_attachment is not None:
        payload["course"]["blueprint_restrictions_by_object_type"][
            "attachment"
        ] = blueprint_restrictions_by_object_type_attachment
    if blueprint_restrictions_by_object_type_discussion_topic is not None:
        payload["course"]["blueprint_restrictions_by_object_type"][
            "discussion_topic"
        ] = blueprint_restrictions_by_object_type_discussion_topic
    if blueprint_restrictions_by_object_type_quiz is not None:
        payload["course"]["blueprint_restrictions_by_object_type"]["quiz"] = blueprint_restrictions_by_object_type_quiz
    if blueprint_restrictions_by_object_type_wiki_page is not None:
        payload["course"]["blueprint_restrictions_by_object_type"][
            "wiki_page"
        ] = blueprint_restrictions_by_object_type_wiki_page
    if template is not None:
        payload["course"]["template"] = template
    if enable_course_paces is not None:
        payload["course"]["enable_course_paces"] = enable_course_paces
    if conditional_release is not None:
        payload["course"]["conditional_release"] = conditional_release
    if offer is not None:
        payload["offer"] = offer

    return self.make_request(
        req_type="put",
        url=self._get_endpoint("update_course", {"<course_id>": course_id}),
        data=json.dumps(payload),
    )


async def update_course_settings(
    self,
    course_id: Union[str, int],
    allow_student_discussion_topics: Optional[bool] = None,
    allow_student_forum_attachments: Optional[bool] = None,
    allow_student_discussion_editing: Optional[bool] = None,
    allow_student_organized_groups: Optional[bool] = None,
    allow_student_discussion_reporting: Optional[bool] = None,
    allow_student_anonymous_discussion_topics: Optional[bool] = None,
    filter_speed_grader_by_student_group: Optional[bool] = None,
    hide_final_grades: Optional[bool] = None,
    hide_distribution_graphs: Optional[bool] = None,
    hide_sections_on_course_users_page: Optional[bool] = None,
    lock_all_announcements: Optional[bool] = None,
    usage_rights_required: Optional[bool] = None,
    restrict_student_past_view: Optional[bool] = None,
    restrict_student_future_view: Optional[bool] = None,
    show_announcements_on_home_page: Optional[bool] = None,
    home_page_announcement_limit: Optional[int] = None,
    syllabus_course_summary: Optional[bool] = None,
    default_due_time: Optional[datetime.time] = None,
    conditional_release: Optional[bool] = None,
) -> dict:
    """
    Update course settings.
    :param self:
    :param course_id: The ID of the course.
    :param allow_student_discussion_topics: Let students create discussion topics
    :param allow_student_forum_attachments: Let students attach files to discussions
    :param allow_student_discussion_editing: Let students edit or delete their own discussion replies
    :param allow_student_organized_groups: Let students organize their own groups
    :param allow_student_discussion_reporting: Let students report offensive discussion content
    :param allow_student_anonymous_discussion_topics: Let students create anonymous discussion topics
    :param filter_speed_grader_by_student_group: Filter SpeedGrader to only the selected student group
    :param hide_final_grades: Hide totals in student grades summary
    :param hide_distribution_graphs: Hide grade distribution graphs from students
    :param hide_sections_on_course_users_page: Disallow students from viewing students in sections they don't belong to
    :param lock_all_announcements: Disable comments on announcements
    :param usage_rights_required: Copyright and license information must be provided for files before being published.
    :param restrict_student_past_view: Restrict students from viewing courses after end date
    :param restrict_student_future_view: Restrict students from viewing courses before start date
    :param show_announcements_on_home_page: Show the most recent announcements on the Course home page (if a Wiki,
        defaults to five announcements, configurable via home_page_announcement_limit).
        Canvas for Elementary subjects ignore this setting
    :param home_page_announcement_limit: Limit the number of announcements on the home page if enabled via
        show_announcements_on_home_page
    :param syllabus_course_summary: Limit the number of announcements on the home page if enabled via
        show_announcements_on_home_page
    :param default_due_time: Set the default due time for assignments. This is the time that will be pre-selected in
        the Canvas user interface when setting a due date for an assignment. It does not change when any existing
        assignment is due. It should be given in 24-hour HH:MM:SS format. The default is “23:59:59”.
         Use “inherit” to inherit the account setting.
    :param conditional_release: Enable or disable individual learning paths for students based on assessment
    :return: The updated course settings
    """
    payload = {}
    if allow_student_discussion_topics is not None:
        payload["allow_student_discussion_topics"] = allow_student_discussion_topics
    if allow_student_forum_attachments is not None:
        payload["allow_student_forum_attachments"] = allow_student_forum_attachments
    if allow_student_discussion_editing is not None:
        payload["allow_student_discussion_editing"] = allow_student_discussion_editing
    if allow_student_organized_groups is not None:
        payload["allow_student_organized_groups"] = allow_student_organized_groups
    if allow_student_discussion_reporting is not None:
        payload["allow_student_discussion_reporting"] = allow_student_discussion_reporting
    if allow_student_anonymous_discussion_topics is not None:
        payload["allow_student_anonymous_discussion_topics"] = allow_student_anonymous_discussion_topics
    if filter_speed_grader_by_student_group is not None:
        payload["filter_speed_grader_by_student_group"] = filter_speed_grader_by_student_group
    if hide_final_grades is not None:
        payload["hide_final_grades"] = hide_final_grades
    if hide_distribution_graphs is not None:
        payload["hide_distribution_graphs"] = hide_distribution_graphs
    if hide_sections_on_course_users_page is not None:
        payload["hide_sections_on_course_users_page"] = hide_sections_on_course_users_page
    if lock_all_announcements is not None:
        payload["lock_all_announcements"] = lock_all_announcements
    if usage_rights_required is not None:
        payload["usage_rights_required"] = usage_rights_required
    if restrict_student_past_view is not None:
        payload["restrict_student_past_view"] = restrict_student_past_view
    if restrict_student_future_view is not None:
        payload["restrict_student_future_view"] = restrict_student_future_view
    if show_announcements_on_home_page is not None:
        payload["show_announcements_on_home_page"] = show_announcements_on_home_page
    if home_page_announcement_limit is not None:
        payload["home_page_announcement_limit"] = home_page_announcement_limit
    if syllabus_course_summary is not None:
        payload["syllabus_course_summary"] = syllabus_course_summary
    if default_due_time is not None:
        payload["default_due_time"] = default_due_time.strftime("%H:%M:%S")
    if conditional_release is not None:
        payload["conditional_release"] = conditional_release

    return self.make_request(
        req_type="put",
        url=self._get_endpoint("update_course_settings", {"<course_id>": course_id}),
        data=json.dumps(payload),
    )


async def update_section(
    self,
    section_id: Union[str, int],
    name: Optional[str] = None,
    sis_section_id: Optional[str] = None,
    integration_id: Optional[str] = None,
    start_at: Optional[datetime.datetime] = None,
    end_at: Optional[datetime.datetime] = None,
    restrict_enrollments_to_section_dates: Optional[bool] = None,
    override_sis_stickiness: bool = True,
) -> dict:
    """
    Update a section.
    :param self:
    :param section_id: The ID of the section.
    :param name: The name of the section.
    :param sis_section_id: The unique SIS identifier.
    :param integration_id: The unique Integration identifier.
    :param start_at: The start date of the section.
    :param end_at: The end date of the section.
    :param restrict_enrollments_to_section_dates: Set to true to restrict user enrollments to the start and end
        dates of the section.
    :param override_sis_stickiness: Default is true. If false, any fields containing “sticky” changes will not be
        updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness

    :return: The updated section object
    """
    payload = {"course_section": {}, "override_sis_stickiness": override_sis_stickiness}
    if name is not None:
        payload["course_section"]["name"] = name
    if sis_section_id is not None:
        payload["course_section"]["sis_section_id"] = sis_section_id
    if integration_id is not None:
        payload["course_section"]["integration_id"] = integration_id
    if start_at is not None:
        payload["course_section"]["start_at"] = start_at.isoformat()
    if end_at is not None:
        payload["course_section"]["end_at"] = end_at.isoformat()
    if restrict_enrollments_to_section_dates is not None:
        payload["course_section"]["restrict_enrollments_to_section_dates"] = restrict_enrollments_to_section_dates

    return self.make_request(
        req_type="put",
        url=self._get_endpoint("update_section", {"<section_id>": section_id}),
        data=json.dumps(payload),
    )
