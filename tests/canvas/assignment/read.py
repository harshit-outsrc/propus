import asyncio
import unittest
from unittest.mock import Mock
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasAssignmentRead(TestAPIClient):
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

        self.test_data = {"course_id": 1234, "assignment_id": 5678, "assignment_group_id": 9012}
        self.test_urls = {
            "get_course_assignments": f"{self.url}/api/v1/courses/{self.test_data['course_id']}/assignments",
            "get_assignment": f"{self.url}/api/v1/courses/{self.test_data['course_id']}"
            f"/assignments/{self.test_data['assignment_id']}",
            "get_course_assignment_groups": f"{self.url}/api/v1/courses/{self.test_data['course_id']}"
            f"/assignment_groups",
            "get_assignment_group": f"{self.url}/api/v1/courses/{self.test_data['course_id']}/assignment_groups/"
            f"{self.test_data['assignment_id']}",
        }

    def test_get_course_assignments(self):
        self.test_name = "get_course_assignments"
        self.assertEqual(
            asyncio.run(self.canvas.get_course_assignments(course_id=self.test_data.get("course_id"))),
            self.success_response,
        )

    def test_get_assignment(self):
        self.test_name = "get_assignment"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_assignment(
                    course_id=self.test_data.get("course_id"), assignment_id=self.test_data.get("assignment_id")
                ),
            ),
            self.success_response,
        )

    def test_get_course_assignment_groups(self):
        self.test_name = "get_course_assignment_groups"
        self.assertEqual(
            asyncio.run(self.canvas.get_course_assignment_groups(course_id=self.test_data.get("course_id"))),
            self.success_response,
        )

    def test_get_assignment_group(self):
        self.test_name = "get_assignment_group"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_assignment_group(
                    course_id=self.test_data.get("course_id"),
                    assignment_group_id=self.test_data.get("assignment_group_id"),
                )
            ),
            self.success_response,
        )

    def mock_make_request(self, **kwargs):
        self.assertEqual(kwargs.get("req_type"), "get")
        self.assertTrue(kwargs.get("url"), self.test_urls.get(self.test_name))
        return self.success_response


if __name__ == "__main__":
    unittest.main()
