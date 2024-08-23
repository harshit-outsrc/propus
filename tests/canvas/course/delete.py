import asyncio
import unittest
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasCourseDelete(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(application_key=self.application_key, base_url=self.url, auth_providers=auth_providers)
        self.canvas.request_service = self._req_mock

        self.test_data = {
            "course_id": 1234,
            "section_id": 5678,
        }
        self.test_urls = {
            "delete_course": f"{self.url}/api/v1/courses/{self.test_data['course_id']}",
            "conclude_course": f"{self.url}/api/v1/courses/{self.test_data['course_id']}",
            "delete_section": f"{self.url}/api/v1/sections/{self.test_data['section_id']}",
        }

    def test_delete_course(self):
        self.test_name = "delete_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.delete_or_conclude_course(course_id=self.test_data.get("course_id"), event="delete")
            ),
            self.success_response,
        )

    def test_conclude_course(self):
        self.test_name = "conclude_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.delete_or_conclude_course(course_id=self.test_data.get("course_id"), event="conclude")
            ),
            self.success_response,
        )

    def test_delete_section(self):
        # Note: I'm not sure how else to handle this - it requires different headers than the
        #     course delete methods, so this goes back to possibly adjusting the request_service to include
        #     post headers in the delete method.
        #     This is re-instantiating the canvas object without the additional headers

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
            "section_id": 5678,
        }
        self.test_urls = {
            "delete_section": f"{self.url}/api/v1/sections/{self.test_data['section_id']}",
        }

        self.test_name = "delete_section"
        self.assertEqual(
            asyncio.run(self.canvas.delete_section(section_id=self.test_data.get("section_id"))),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
