import asyncio
import unittest
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasEnrollmentDelete(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(application_key=self.application_key, base_url=self.url, auth_providers=auth_providers)
        self.canvas.request_service = self._req_mock

        self.test_data = {"enrollment_id": 910, "course_id": 345}
        self.test_urls = {
            "conclude_delete_deactivate_enrollment": (
                f"{self.url}/api/v1/courses/{self.test_data['course_id']}"
                f"/enrollments/{self.test_data['enrollment_id']}"
            )
        }

    def test_conclude_enrollment(self):
        self.test_name = "conclude_delete_deactivate_enrollment"
        self.assertEqual(
            asyncio.run(
                self.canvas.conclude_delete_deactivate_enrollment(
                    course_id=self.test_data.get("course_id"),
                    enrollment_id=self.test_data.get("enrollment_id"),
                    task="conclude",
                )
            ),
            self.success_response,
        )

    def test_delete_enrollment(self):
        self.test_name = "conclude_delete_deactivate_enrollment"
        self.assertEqual(
            asyncio.run(
                self.canvas.conclude_delete_deactivate_enrollment(
                    course_id=self.test_data.get("course_id"),
                    enrollment_id=self.test_data.get("enrollment_id"),
                    task="delete",
                )
            ),
            self.success_response,
        )

    def test_deactivate_enrollment(self):
        self.test_name = "conclude_delete_deactivate_enrollment"
        self.assertEqual(
            asyncio.run(
                self.canvas.conclude_delete_deactivate_enrollment(
                    course_id=self.test_data.get("course_id"),
                    enrollment_id=self.test_data.get("enrollment_id"),
                    task="deactivate",
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
