import asyncio
from datetime import datetime
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyEnrollmentCreate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.test_urls = {
            "create_enrollment": f"{self.url}/api/commands/Academics/StudentEnrollmentPeriod/EnrollStudent",
        }

        self.payload = {
            "studentId": "STUDENT_1234",
            "programId": "IT_12345",
            "programVersionId": "CMS_1234",
            "billingMethodId": "METHOD_1234",
            "catalogYearId": "YEAR_1234",
            "expectedStartDate": datetime(2023, 3, 1),
            "graduationDate": datetime(2023, 9, 1),
            "gradeLevelId": "GRADE_1234",
            "shiftId": "SHIFT_1234",
            "startDateId": "START_DATE_1234",
        }
        self.api_client.timeout = 30

    def test_create_enrollment(self):
        self.test_name = "create_enrollment"
        self._test_data = {
            "payload": {
                "IsDegreeProgramType": False,
                "entity": {
                    "id": -1,
                    "campusId": 5,
                    "assignedAdmissionsRepId": 2,
                    "schoolStatusId": 95,
                    "studentId": self.payload.get("studentId"),
                    "programId": self.payload.get("programId"),
                    "programVersionId": self.payload.get("programVersionId"),
                    "billingMethodId": self.payload.get("billingMethodId"),
                    "catalogYearId": self.payload.get("catalogYearId"),
                    "expectedStartDate": "2023-03-01T00:00:00",
                    "graduationDate": "2023-09-01T00:00:00",
                    "gradeLevelId": self.payload.get("gradeLevelId"),
                    "shiftId": self.payload.get("shiftId"),
                    "startDateId": self.payload.get("startDateId"),
                },
            }
        }
        self.assertEqual(
            asyncio.run(
                self.anthology.create_enrollment(
                    student_id=self.payload.get("studentId"),
                    program_id=self.payload.get("programId"),
                    program_version_id=self.payload.get("programVersionId"),
                    grade_level_id=self.payload.get("gradeLevelId"),
                    start_date=self.payload.get("expectedStartDate"),
                    grad_date=self.payload.get("graduationDate"),
                    catalog_year_id=self.payload.get("catalogYearId"),
                    version_start_date=self.payload.get("startDateId"),
                    billing_method=self.payload.get("billingMethodId"),
                    shift_id=self.payload.get("shiftId"),
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
