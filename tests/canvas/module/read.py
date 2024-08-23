import asyncio
import unittest
from unittest.mock import Mock
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasModuleRead(TestAPIClient):
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
            "course_id": 1234,
        }
        self.test_urls = {
            "get_course_modules": f"{self.url}/api/v1/courses/{self.test_data['course_id']}/modules",
        }

    def test_get_course_modules(self):
        self.test_name = "get_course_modules"
        self.assertEqual(
            asyncio.run(self.canvas.get_course_modules(course_id=self.test_data.get("course_id"))),
            self.success_response,
        )

    def mock_make_request(self, **kwargs):
        self.assertEqual(kwargs.get("req_type"), "get")
        self.assertTrue(kwargs.get("url"), self.test_urls.get(self.test_name))
        return self.success_response


if __name__ == "__main__":
    unittest.main()
