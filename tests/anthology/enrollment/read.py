import asyncio
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyEnrollmenteRead(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock
        self.test_urls = {
            "fetch_enrollment_by_cccid": f"{self.url}/ds/odata/StudentEnrollmentPeriods",
            "fetch_enrollment_by_enrollment_id": f"{self.url}/ds/odata/StudentEnrollmentPeriods",
        }
        self.test_data = {
            "student_id": "anth_1234_ABC",
            "enrollment_id": 84658,
        }
        self.api_client.timeout = 30

    def test_fetch_enrollment_by_cccid(self):
        self.test_name = "fetch_enrollment_by_cccid"
        self.assertEqual(
            asyncio.run(self.anthology.fetch_enrollment_by_cccid(ccc_id=self.test_data.get("student_id"))),
            self.success_response,
        )

    def test_fetch_enrollment_by_enrollment_id(self):
        self.test_name = "fetch_enrollment_by_enrollment_id"
        self.assertEqual(
            asyncio.run(
                self.anthology.fetch_enrollment_by_enrollment_id(enrollment_id=self.test_data.get("enrollment_id"))
            ),
            self.success_response,
        )

    def test_fetch_student_enrollment_period_by_id(self):
        self.test_name = "fetch_student_enrollment_period_by_id"
        self._test_data = {"payload": {"id": "84658"}}
        self.assertEqual(
            asyncio.run(
                self.anthology.fetch_student_enrollment_period_by_id(
                    student_enrollment_id=self.test_data.get("enrollment_id")
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
