import asyncio
from datetime import datetime
import unittest
from unittest.mock import Mock

from propus.anthology import Anthology
from tests.api_client import TestAPIClient
from propus.anthology.student._exceptions import StudentUpdateMissingFields
from propus.helpers.exceptions import InvalidDateStructure


class TestAnthologyStudentUpdate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock
        self.anthology.student_by_id = Mock(side_effect=self.student_by_id)

        self.existing_data = {"firstName": "Elvis", "lastName": "Presley"}

        self.student_data = {
            "student_id": "12345678",
            "student_number": "XF12345",
            "first_name": "Johnny",
            "last_name": "Appleseed",
            "email": "johnny.appleseed@newton.com",
            "dob": "2000/05/12",
            "enrollment_id": "4123415",
            "status_id": 88,
            "notes": "These are the notes",
            "effective_date": datetime(2020, 2, 2),
            "lad": datetime(2023, 1, 3),
        }

        self.test_urls = {
            "update_student": f"{self.url}/api/commands/Common/Student/Save",
            "change_student_status": f"{self.url}/api/commands/Academics/StudentEnrollmentPeriod/EnrollmentStatusChange",
        }
        self.api_client.timeout = 30

    async def student_by_id(self, _):
        return {"data": self.existing_data}

    def test_update_errors(self):
        self.test_name = "update_error_a"
        with self.assertRaises(InvalidDateStructure):
            asyncio.run(self.anthology.update_student(self.student_data.get("student_id"), dob="12345"))

        self.test_name = "update_error_b"
        with self.assertRaises(StudentUpdateMissingFields):
            asyncio.run(self.anthology.update_student(self.student_data.get("student_id")))

    def test_update_student(self):
        self.test_name = "update_student"
        self._test_data = {
            "payload": {
                "firstName": self.student_data.get("first_name"),
                "lastName": self.student_data.get("last_name"),
                "studentNumber": self.student_data.get("student_number"),
                "emailAddress": self.student_data.get("email"),
                "dateOfBirth": self.student_data.get("dob"),
                "studentAddressAssociation": 1,
            }
        }
        self.assertEqual(
            asyncio.run(self.anthology.update_student(self.student_data.get("student_id"), **self.student_data)),
            self.success_response,
        )

    def test_student_status(self):
        self.test_name = "change_student_status"
        self._test_data = {
            "payload": {
                "StudentEnrollmentPeriodId": self.student_data.get("enrollment_id"),
                "NewSchoolStatusId": self.student_data.get("status_id"),
                "EffectiveDate": self.student_data.get("effective_date").strftime("%Y/%m/%d 00:00:00"),
                "Note": self.student_data.get("notes"),
                "LastAttendedDate": self.student_data.get("lad").strftime("%Y/%m/%d 00:00:00"),
            }
        }
        self.assertEqual(
            asyncio.run(
                self.anthology.change_student_status(
                    student_enrollment_id=self.student_data.get("enrollment_id"),
                    new_status_id=self.student_data.get("status_id"),
                    note=self.student_data.get("notes"),
                    effective_date=self.student_data.get("effective_date"),
                    last_attendance_date=self.student_data.get("lad"),
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
