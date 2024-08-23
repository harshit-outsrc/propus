import asyncio
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyCourseReinstate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock
        self.test_urls = {
            "reinstate_course": f"{self.url}/api/commands/Academics/StudentCourse/ReinstateCourse",
        }
        self.student_course_id = "12349876_MNAS"
        self.api_client.timeout = 30

    def test_reinstate_course(self):
        self.test_name = "reinstate_course"
        self._test_data = {"payload": {"StudentCourseId": "12349876_MNAS"}}
        self.assertEqual(
            asyncio.run(self.anthology.reinstate_course(self.student_course_id)),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
