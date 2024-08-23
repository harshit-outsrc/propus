import asyncio
from datetime import datetime
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyCourseDrop(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.test_urls = {
            "drop_course": f"{self.url}/api/commands/Academics/StudentCourse/DropCourse",
            "fetch_drop_reason": f"{self.url}/ds/odata/StudentCourseStatusChangeReasons",
        }

        self.drop_payload = {
            "student_course_id": 12345,
            "drop_date": datetime(2023, 11, 8, 9, 38, 52),
            "drop_reason_id": 3425,
            "letter_grade": "PASS!",
        }
        self._test_data = {
            "payload": {
                "StudentEnrollmentScheduleId": 12345,
                "DropDate": "2023/11/08 09:38:52",
                "DropReasonId": 3425,
                "AllowLdwOverride": True,
                "LetterGrade": "PASS!",
            }
        }
        self.api_client.timeout = 30

    def test_drop_course(self):
        self.test_name = "drop_course"
        self.assertEqual(asyncio.run(self.anthology.drop_course(**self.drop_payload)), self.success_response)

    def test_fetch_drop_reason(self):
        self.test_name = "fetch_drop_reason"
        self.assertEqual(asyncio.run(self.anthology.fetch_drop_reason()), self.success_response)


if __name__ == "__main__":
    unittest.main()
