import asyncio
import unittest
import datetime
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasCourseCreate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(application_key=self.application_key, base_url=self.url, auth_providers=auth_providers)
        self.canvas.request_service = self._req_mock

        self.test_data = {
            "course": {
                "account_id": 1,
                "course_name": "Introduction to Testology",
                "course_code": "TEST101",
                "term_id": 1,
                "sis_course_id": "TEST101-1",
                "start_at": datetime.datetime(2023, 3, 13),
                "end_at": datetime.datetime(2023, 6, 13),
                "allow_wiki_comments": True,
                "open_enrollment": False,
                "hide_final_grades": True,
                "syllabus_body": "Welcome to Introduction to Testology! This is a test course.",
                "course_format": "blended",
            },
            "section": {
                "course_id": 1,
                "name": "Testology 101 - Section 1",
                "sis_section_id": "TEST101-1-1",
                "start_at": datetime.datetime(2023, 3, 13),
                "end_at": datetime.datetime(2023, 6, 13),
                "restrict_enrollments_to_section_dates": True,
                "enable_sis_reactivation": False,
            },
        }
        self.test_urls = {
            "create_course": (f"{self.url}/api/v1/accounts/1/courses"),
            "create_section": (f"{self.url}/api/v1/courses/1/sections"),
        }

    def test_create_course(self):
        self.test_name = "create_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.create_course(
                    account_id=self.test_data["course"]["account_id"],
                    course_name=self.test_data["course"]["course_name"],
                    course_code=self.test_data["course"]["course_code"],
                    term_id=self.test_data["course"]["term_id"],
                    sis_course_id=self.test_data["course"]["sis_course_id"],
                    start_at=self.test_data["course"]["start_at"],
                    end_at=self.test_data["course"]["end_at"],
                    allow_wiki_comments=self.test_data["course"]["allow_wiki_comments"],
                    open_enrollment=self.test_data["course"]["open_enrollment"],
                    hide_final_grades=self.test_data["course"]["hide_final_grades"],
                    syllabus_body=self.test_data["course"]["syllabus_body"],
                    course_format=self.test_data["course"]["course_format"],
                )
            ),
            self.success_response,
        )

    def test_create_section(self):
        self.test_name = "create_section"
        self.assertEqual(
            asyncio.run(
                self.canvas.create_section(
                    course_id=self.test_data["section"]["course_id"],
                    name=self.test_data["section"]["name"],
                    sis_section_id=self.test_data["section"]["sis_section_id"],
                    start_at=self.test_data["section"]["start_at"],
                    end_at=self.test_data["section"]["end_at"],
                    restrict_enrollments_to_section_dates=self.test_data["section"][
                        "restrict_enrollments_to_section_dates"
                    ],
                    enable_sis_reactivation=self.test_data["section"]["enable_sis_reactivation"],
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
