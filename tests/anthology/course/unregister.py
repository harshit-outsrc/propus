import asyncio
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyCourseUnregister(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock
        self.unregister_payload = {
            "student_course_id": 12345,
            "reason": "SOME REASON TO UNREGISTER",
            "description": "This is the full description!",
        }
        self.test_urls = {
            "unregister_course": f"{self.url}/api/commands/Academics/StudentCourse/UnregisterStudentCourse",
        }
        self.api_client.timeout = 30

    def test_unregister_course(self):
        self.test_name = "unregister_course"
        self._test_data = {
            "payload": {
                "IsUnregisterCall": True,
                "IsMultipleUnregisterEnabled": True,
                "StudentCourseId": self.unregister_payload.get("student_course_id"),
                "Comments": self.unregister_payload.get("reason"),
                "Description": self.unregister_payload.get("description"),
            }
        }
        self.assertEqual(
            asyncio.run(self.anthology.unregister_course(**self.unregister_payload)),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
