import asyncio
import unittest
import urllib.parse
from unittest.mock import Mock
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasEnrollmentRead(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(
            application_key=self.application_key,
            base_url=self.url,
            additional_headers=None,
            auth_providers=auth_providers,
        )
        self.canvas.request_service = self._req_mock
        self.canvas.make_request = Mock(side_effect=self.mock_make_request)

        self.test_data = {
            "user_id": 12,
            "course_id": 2348,
            "course": {
                "type[]": "StudentEnrollment",
                "role[]": "Student",
                "state[]": "active",
                "include[]": ["total_scores", "current_points"],
                "user_id": 1,
                "grading_period_id": 2,
                "enrollment_term_id": 4,
                "sis_account_id[]": "TEST-101",
                "sis_course_id[]": ["TEST-101", "TEST-102"],
                "sis_section_id[]": ["TEST-101", "TEST-102"],
                "sis_user_id[]": [1, 2, 3],
                "created_for_sis_id[]": False,
            },
            "section_id": 678,
            "enrollment_id": 910,
        }
        course_query_params = urllib.parse.urlencode(self.test_data["course"], doseq=True)

        self.test_urls = {
            "list_enrollments_for_user": f"{self.url}/api/v1/users/{self.test_data['user_id']}/enrollments",
            "list_enrollments_for_course": (
                f"{self.url}/api/v1/courses/{self.test_data['course_id']}/enrollments?{course_query_params}"
            ),
            "list_enrollments_for_section": f'{self.url}/api/v1/sections/{self.test_data["section_id"]}/enrollments',
            "list_students_in_course": f"{self.url}/api/v1/courses/{self.test_data['course_id']}/students",
            "get_single_enrollment": f"{self.url}/api/v1/accounts/1/enrollments/{self.test_data['enrollment_id']}",
        }

    def test_list_enrollments_for_user(self):
        self.test_name = "list_enrollments_for_user"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_enrollments(
                    object_type="user",
                    object_id=self.test_data.get("user_id"),
                )
            ),
            self.success_response,
        )

    def test_list_enrollments_for_course(self):
        self.test_name = "list_enrollments_for_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_enrollments(
                    object_type="course",
                    object_id=self.test_data["course_id"],
                    enrollment_type=self.test_data["course"]["type[]"],
                    role=self.test_data["course"]["role[]"],
                    state=self.test_data["course"]["state[]"],
                    include=self.test_data["course"]["include[]"],
                    user_id=self.test_data["course"]["user_id"],
                    grading_period_id=self.test_data["course"]["grading_period_id"],
                    enrollment_term_id=self.test_data["course"]["enrollment_term_id"],
                    sis_account_id=self.test_data["course"]["sis_account_id[]"],
                    sis_course_id=self.test_data["course"]["sis_course_id[]"],
                    sis_section_id=self.test_data["course"]["sis_section_id[]"],
                    sis_user_id=self.test_data["course"]["sis_user_id[]"],
                    created_for_sis_id=self.test_data["course"]["created_for_sis_id[]"],
                )
            ),
            self.success_response,
        )

    def test_list_enrollments_for_section(self):
        self.test_name = "list_enrollments_for_section"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_enrollments(
                    object_type="section",
                    object_id=self.test_data.get("section_id"),
                )
            ),
            self.success_response,
        )

    def test_list_students_in_course(self):
        self.test_name = "list_students_in_course"
        self.assertEqual(
            asyncio.run(self.canvas.list_students_in_course(course_id=self.test_data["course_id"])),
            self.success_response,
        )

    def test_get_single_enrollment(self):
        self.test_name = "get_single_enrollment"
        self.assertEqual(
            asyncio.run(self.canvas.get_single_enrollment(enrollment_id=self.test_data["enrollment_id"])),
            self.success_response,
        )

    def mock_make_request(self, **kwargs):
        self.assertEqual(kwargs.get("req_type"), "get")
        self.assertTrue(kwargs.get("url"), self.test_urls.get(self.test_name))
        return self.success_response


if __name__ == "__main__":
    unittest.main()
