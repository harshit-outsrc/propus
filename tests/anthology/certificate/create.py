import asyncio
from datetime import datetime
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyCertificateCreate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock
        self.cert_data = {
            "id": -1,
            "studentEnrollmentPeriodId": 12345,
            "note": "These are the notes",
            "awardedDate": "2023/11/13 00:00:00",
            "degreeId": 4321,
        }
        self._test_data = self._test_data | {"payload": self.cert_data}

        self.test_urls = {
            "create_certificate": f"{self.url}/api/commands/Academics/StudentEnrollmentPeriodDegree/SaveNew"
        }

        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 30

    def test_create_certificate(self):
        self.test_name = "create_certificate"
        self.assertEqual(
            asyncio.run(
                self.anthology.create_certificate(
                    student_enrollment_id=self.cert_data.get("studentEnrollmentPeriodId"),
                    notes=self.cert_data.get("note"),
                    award_date=datetime(2023, 11, 13),
                    degree_id=self.cert_data.get("degreeId"),
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
