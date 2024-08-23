import asyncio
import unittest
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasEnrollmentUpdate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(application_key=self.application_key, base_url=self.url, auth_providers=auth_providers)
        self.canvas.request_service = self._req_mock
        self.expected_headers = self.expected_headers | {"Content-Type": "application/json"}
        self.test_data = {"enrollment_id": 910, "course_id": 345}
        self.test_urls = {
            "reactivate_enrollment": (
                f"{self.url}/api/v1/courses/{self.test_data['course_id']}"
                f"/enrollments/{self.test_data['enrollment_id']}/reactivate"
            )
        }

    def test_reactivate_enrollment(self):
        self.test_name = "reactivate_enrollment"
        self.api_client.default_headers["Content-Type"] = "application/json"
        self.assertEqual(
            asyncio.run(
                self.canvas.reactivate_enrollment(
                    course_id=self.test_data.get("course_id"),
                    enrollment_id=self.test_data.get("enrollment_id"),
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
