import asyncio
import datetime
import unittest
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasEnrollmentCreate(TestAPIClient):
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

        self.test_data = {
            "section_id": 1234,
            "user_id": 456,
            "enrollment_type": "StudentEnrollment",
            "start_at": datetime.datetime(2023, 1, 1),
            "end_at": datetime.datetime(2023, 12, 31),
            "role_id": 5,
            "enrollment_state": "active",
            "limit_privileges_to_course_section": True,
            "notify": True,
            "self_enrollment_code": "donuts",
            "self_enrolled": False,
            "associated_user_id": 600,
        }
        self.test_urls = {
            "create_enrollment": f"{self.url}/api/v1/sections/{self.test_data['section_id']}/enrollments",
        }

    def test_create_enrollment(self):
        self.test_name = "create_enrollment"
        self.assertEqual(
            asyncio.run(
                self.canvas.create_enrollment(
                    section_id=self.test_data["section_id"],
                    user_id=self.test_data["user_id"],
                    enrollment_type=self.test_data["enrollment_type"],
                    start_at=self.test_data["start_at"],
                    end_at=self.test_data["end_at"],
                    role_id=self.test_data["role_id"],
                    enrollment_state=self.test_data["enrollment_state"],
                    limit_privileges_to_course_section=self.test_data["limit_privileges_to_course_section"],
                    notify=self.test_data["notify"],
                    self_enrollment_code=self.test_data["self_enrollment_code"],
                    self_enrolled=self.test_data["self_enrolled"],
                    associated_user_id=self.test_data["associated_user_id"],
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
