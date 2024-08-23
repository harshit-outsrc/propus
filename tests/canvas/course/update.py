import asyncio
import unittest
import datetime
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasCourseUpdate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(application_key=self.application_key, base_url=self.url, auth_providers=auth_providers)
        self.canvas.request_service = self._req_mock
        self.blueprint_restriction_object = {
            "content": True,
            "points": True,
            "due_date": False,
            "availability_dates": True,
        }

        self.test_data = {
            "course": {
                "course_id": 1234,
                "account_id": 1,
                "name": "Introduction to Testology 101 - Updated",
                "course_code": "TEST101-1-1",
                "start_at": datetime.datetime(2023, 3, 13),
                "end_at": datetime.datetime(2023, 6, 13),
                "license": "private",
                "is_public": False,
                "is_public_to_auth_users": False,
                "public_syllabus": True,
                "public_syllabus_to_auth": False,
                "public_description": "This is a test course. Please do not enroll.",
                "allow_student_wiki_edits": False,
                "allow_wiki_comments": False,
                "allow_student_forum_attachments": True,
                "open_enrollment": False,
                "self_enrollment": True,
                "restrict_enrollments_to_course_dates": False,
                "term_id": 123,
                "sis_course_id": "TEST101-1-1",
                "integration_id": "TEST101-1-1-123",
                "hide_final_grades": False,
                "time_zone": "America/New_York",
                "apply_assignment_group_weights": True,
                "storage_quota_mb": 100,
                "event": "offer",
                "default_view": "syllabus",
                "syllabus_body": "Welcome to Introduction to Testology 101! This is a test course.",
                "syllabus_course_summary": True,
                "grading_standard_id": 1,
                "grade_passback_setting": "nightly_sync",
                "course_format": "online",
                "image_id": 345,
                "image_url": "https://testology101.com/image.png",
                "remove_image": False,
                "remove_banner_image": True,
                "blueprint": False,
                "blueprint_restrictions": None,
                "use_blueprint_restrictions_by_object_type": True,
                "blueprint_restrictions_by_object_type_assignment": self.blueprint_restriction_object,
                "blueprint_restrictions_by_object_type_attachment": None,
                "blueprint_restrictions_by_object_type_discussion_topic": self.blueprint_restriction_object,
                "blueprint_restrictions_by_object_type_quiz": None,
                "blueprint_restrictions_by_object_type_wiki_page": self.blueprint_restriction_object,
                "enable_course_paces": True,
                "conditional_release": True,
                "offer": False,
                "override_sis_stickiness": True,
            },
            "course_settings": {
                "course_id": 1234,
                "allow_student_discussion_topics": True,
                "allow_student_forum_attachments": True,
                "allow_student_discussion_editing": True,
                "allow_student_organized_groups": True,
                "allow_student_discussion_reporting": True,
                "allow_student_anonymous_discussion_topics": True,
                "filter_speed_grader_by_student_group": True,
                "hide_final_grades": True,
                "hide_distribution_graphs": True,
                "hide_sections_on_course_users_page": True,
                "lock_all_announcements": True,
                "usage_rights_required": True,
                "restrict_student_past_view": True,
                "restrict_student_future_view": True,
                "show_announcements_on_home_page": True,
                "home_page_announcement_limit": 10,
                "syllabus_course_summary": True,
                "default_due_time": datetime.time(23, 59, 59),
                "conditional_release": True,
            },
            "section": {
                "section_id": 1234,
                "name": "Introduction to Testology 101 - Section 1 - Updated",
                "sis_section_id": "TEST101-1-1-123",
                "integration_id": "TEST101-1-1-123",
                "start_at": datetime.datetime(2023, 3, 13, 12, 0, 0),
                "end_at": datetime.datetime(2023, 6, 13, 23, 59, 59),
                "restrict_enrollments_to_section_dates": True,
                "override_sis_stickiness": True,
            },
        }
        self.test_urls = {
            "update_course": f"{self.url}/api/v1/courses/{self.test_data['course']['course_id']}",
            "update_course_settings": (
                f'{self.url}/api/v1/courses/{self.test_data["course_settings"]["course_id"]}/settings'
            ),
            "update_section": (f"{self.url}/api/v1/sections/{self.test_data['section']['section_id']}"),
        }

    def test_update_course(self):
        self.test_name = "update_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.update_course(
                    course_id=self.test_data["course"]["course_id"],
                    account_id=self.test_data["course"]["account_id"],
                    name=self.test_data["course"]["name"],
                    course_code=self.test_data["course"]["course_code"],
                    start_at=self.test_data["course"]["start_at"],
                    end_at=self.test_data["course"]["end_at"],
                    license=self.test_data["course"]["license"],
                    is_public=self.test_data["course"]["is_public"],
                    is_public_to_auth_users=self.test_data["course"]["is_public_to_auth_users"],
                    public_syllabus=self.test_data["course"]["public_syllabus"],
                    public_syllabus_to_auth=self.test_data["course"]["public_syllabus_to_auth"],
                    public_description=self.test_data["course"]["public_description"],
                    allow_student_wiki_edits=self.test_data["course"]["allow_student_wiki_edits"],
                    allow_wiki_comments=self.test_data["course"]["allow_wiki_comments"],
                    allow_student_forum_attachments=self.test_data["course"]["allow_student_forum_attachments"],
                    open_enrollment=self.test_data["course"]["open_enrollment"],
                    self_enrollment=self.test_data["course"]["self_enrollment"],
                    restrict_enrollments_to_course_dates=self.test_data["course"][
                        "restrict_enrollments_to_course_dates"
                    ],
                    term_id=self.test_data["course"]["term_id"],
                    sis_course_id=self.test_data["course"]["sis_course_id"],
                    integration_id=self.test_data["course"]["integration_id"],
                    hide_final_grades=self.test_data["course"]["hide_final_grades"],
                    time_zone=self.test_data["course"]["time_zone"],
                    apply_assignment_group_weights=self.test_data["course"]["apply_assignment_group_weights"],
                    storage_quota_mb=self.test_data["course"]["storage_quota_mb"],
                    event=self.test_data["course"]["event"],
                    default_view=self.test_data["course"]["default_view"],
                    syllabus_body=self.test_data["course"]["syllabus_body"],
                    syllabus_course_summary=self.test_data["course"]["syllabus_course_summary"],
                    grading_standard_id=self.test_data["course"]["grading_standard_id"],
                    grade_passback_setting=self.test_data["course"]["grade_passback_setting"],
                    course_format=self.test_data["course"]["course_format"],
                    image_id=self.test_data["course"]["image_id"],
                    image_url=self.test_data["course"]["image_url"],
                    remove_image=self.test_data["course"]["remove_image"],
                    remove_banner_image=self.test_data["course"]["remove_banner_image"],
                    blueprint=self.test_data["course"]["blueprint"],
                    blueprint_restrictions=self.test_data["course"]["blueprint_restrictions"],
                    use_blueprint_restrictions_by_object_type=self.test_data["course"][
                        "use_blueprint_restrictions_by_object_type"
                    ],
                    blueprint_restrictions_by_object_type_assignment=self.test_data["course"][
                        "blueprint_restrictions_by_object_type_assignment"
                    ],
                    blueprint_restrictions_by_object_type_attachment=self.test_data["course"][
                        "blueprint_restrictions_by_object_type_attachment"
                    ],
                    blueprint_restrictions_by_object_type_discussion_topic=self.test_data["course"][
                        "blueprint_restrictions_by_object_type_discussion_topic"
                    ],
                    blueprint_restrictions_by_object_type_quiz=self.test_data["course"][
                        "blueprint_restrictions_by_object_type_quiz"
                    ],
                    blueprint_restrictions_by_object_type_wiki_page=self.test_data["course"][
                        "blueprint_restrictions_by_object_type_wiki_page"
                    ],
                    enable_course_paces=self.test_data["course"]["enable_course_paces"],
                    conditional_release=self.test_data["course"]["conditional_release"],
                    offer=self.test_data["course"]["offer"],
                    override_sis_stickiness=self.test_data["course"]["override_sis_stickiness"],
                )
            ),
            self.success_response,
        )

    def test_update_course_settings(self):
        self.test_name = "update_course_settings"
        self.assertEqual(
            asyncio.run(
                self.canvas.update_course_settings(
                    course_id=self.test_data["course_settings"]["course_id"],
                    allow_student_discussion_topics=self.test_data["course_settings"][
                        "allow_student_discussion_topics"
                    ],
                    allow_student_forum_attachments=self.test_data["course_settings"][
                        "allow_student_forum_attachments"
                    ],
                    allow_student_discussion_editing=self.test_data["course_settings"][
                        "allow_student_discussion_editing"
                    ],
                    allow_student_organized_groups=self.test_data["course_settings"]["allow_student_organized_groups"],
                    allow_student_discussion_reporting=self.test_data["course_settings"][
                        "allow_student_discussion_reporting"
                    ],
                    allow_student_anonymous_discussion_topics=self.test_data["course_settings"][
                        "allow_student_anonymous_discussion_topics"
                    ],
                    filter_speed_grader_by_student_group=self.test_data["course_settings"][
                        "filter_speed_grader_by_student_group"
                    ],
                    hide_final_grades=self.test_data["course_settings"]["hide_final_grades"],
                    hide_distribution_graphs=self.test_data["course_settings"]["hide_distribution_graphs"],
                    hide_sections_on_course_users_page=self.test_data["course_settings"][
                        "hide_sections_on_course_users_page"
                    ],
                    lock_all_announcements=self.test_data["course_settings"]["lock_all_announcements"],
                    usage_rights_required=self.test_data["course_settings"]["usage_rights_required"],
                    restrict_student_past_view=self.test_data["course_settings"]["restrict_student_past_view"],
                    restrict_student_future_view=self.test_data["course_settings"]["restrict_student_future_view"],
                    show_announcements_on_home_page=self.test_data["course_settings"][
                        "show_announcements_on_home_page"
                    ],
                    home_page_announcement_limit=self.test_data["course_settings"]["home_page_announcement_limit"],
                    syllabus_course_summary=self.test_data["course_settings"]["syllabus_course_summary"],
                    default_due_time=self.test_data["course_settings"]["default_due_time"],
                    conditional_release=self.test_data["course_settings"]["conditional_release"],
                )
            ),
            self.success_response,
        )

    def test_update_section(self):
        self.test_name = "update_section"
        self.assertEqual(
            asyncio.run(
                self.canvas.update_section(
                    section_id=self.test_data["section"]["section_id"],
                    name=self.test_data["section"]["name"],
                    sis_section_id=self.test_data["section"]["sis_section_id"],
                    integration_id=self.test_data["section"]["integration_id"],
                    start_at=self.test_data["section"]["start_at"],
                    end_at=self.test_data["section"]["end_at"],
                    restrict_enrollments_to_section_dates=self.test_data["section"][
                        "restrict_enrollments_to_section_dates"
                    ],
                    override_sis_stickiness=self.test_data["section"]["override_sis_stickiness"],
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
