import asyncio
from datetime import datetime
from typing import List
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient

from propus.helpers.exceptions import InvalidStringLength, InvalidEmail, InvalidPhoneNumber, InvalidDateStructure


class TestAnthologyStudentCreate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.payload_data = {
            "studentNumber": "12345679",
            "firstName": "calbright",
            "lastName": "college",
            "phoneNumber": "(916) 986-1234",
            "emailAddress": "you@me.com",
            "dateOfBirth": "1967/05/21",
            "city": "San Francisco",
            "streetAddress": "123 Main Street",
            "postalCode": "123456",
            "middleName": "community",
        }

        self.test_urls = {
            "create_student": f"{self.url}/api/commands/Common/Student/SaveNew",
        }
        self.api_client.timeout = 30

    def test_create_errors(self):
        def testException(args: List, expected_exception: Exception):
            try:
                a, b, c, d, e, f = args
                asyncio.run(self.anthology.create_student(a, b, c, d, e, f))
            except expected_exception:
                return True
            return False

        self.assertTrue(
            testException(["", "only_last"] + [None] * 4, InvalidStringLength),
            msg="empty first_name should fail",
        )
        self.assertTrue(
            testException(["first_only", ""] + [None] * 4, InvalidStringLength),
            msg="empty last_name should fail",
        )
        self.assertTrue(
            testException(["first", "name", ""] + [None] * 3, InvalidStringLength),
            msg="empty student_id fail",
        )
        self.assertTrue(
            testException(["first", "name", "123456789010"] + [None] * 3, InvalidStringLength),
            msg="long student_id fail",
        )
        self.assertTrue(
            testException(["first", "name", "123456789010"] + [None] * 3, InvalidStringLength),
            msg="long student_id fail",
        )
        self.assertTrue(
            testException(
                ["first", "name", "1234", "123 123-1234"] + [None] * 2,
                InvalidPhoneNumber,
            ),
            msg="invalid phone number test 1",
        )
        self.assertTrue(
            testException(
                ["first", "name", "1234", "(123)123-1234"] + [None] * 2,
                InvalidPhoneNumber,
            ),
            msg="invalid phone number test 2",
        )
        self.assertTrue(
            testException(
                ["first", "name", "1234", "(123) 123-1234", "1901-01-01", None],
                InvalidDateStructure,
            ),
            msg="invalid birthdate",
        )
        self.assertTrue(
            testException(
                [
                    "first",
                    "name",
                    "1234",
                    "(123) 123-1234",
                    "1901/01/01",
                    "bad.email@com",
                ],
                InvalidEmail,
            ),
            msg="invalid email test 1",
        )

    def test_minimum_create(self):
        self.test_name = "create_student"
        self._test_data = {
            "payload": {
                "studentNumber": self.payload_data.get("studentNumber"),
                "firstName": self.payload_data.get("firstName"),
                "lastName": self.payload_data.get("lastName"),
                "phoneNumber": self.payload_data.get("phoneNumber"),
                "emailAddress": self.payload_data.get("emailAddress"),
                "id": -1,
                "schoolStatusId": 4,
                "campusId": 5,
                "countryId": "1",
                "countryName": "United States",
                "assignedAdmissionsRepId": 2,
                "leadSourceId": 680,
                "leadDate": f"{datetime.now().strftime('%Y/%m/%d')} 00:00:00",
                "state": "CA",
                "dateOfBirth": f"{self.payload_data.get('dateOfBirth')} 00:00:00",
            }
        }

        self.assertEqual(
            asyncio.run(
                self.anthology.create_student(
                    first_name=self.payload_data.get("firstName"),
                    last_name=self.payload_data.get("lastName"),
                    student_number=self.payload_data.get("studentNumber"),
                    phone_number=self.payload_data.get("phoneNumber"),
                    dob=self.payload_data.get("dateOfBirth"),
                    email=self.payload_data.get("emailAddress"),
                )
            ),
            self.success_response,
        )

    def test_expanded_create(self):
        self.test_name = "create_student"
        self._test_data = {
            "payload": {
                "studentNumber": self.payload_data.get("studentNumber"),
                "firstName": self.payload_data.get("firstName"),
                "lastName": self.payload_data.get("lastName"),
                "phoneNumber": self.payload_data.get("phoneNumber"),
                "emailAddress": self.payload_data.get("emailAddress"),
                "id": -1,
                "schoolStatusId": 4,
                "campusId": 5,
                "countryId": "1",
                "countryName": "United States",
                "assignedAdmissionsRepId": 2,
                "leadSourceId": 680,
                "leadDate": f"{datetime.now().strftime('%Y/%m/%d')} 00:00:00",
                "state": "CA",
                "dateOfBirth": f"{self.payload_data.get('dateOfBirth')} 00:00:00",
                "city": self.payload_data.get("city"),
                "streetAddress": self.payload_data.get("streetAddress"),
                "postalCode": self.payload_data.get("postalCode"),
                "middleName": self.payload_data.get("middleName"),
            }
        }

        self.assertEqual(
            asyncio.run(
                self.anthology.create_student(
                    first_name=self.payload_data.get("firstName"),
                    last_name=self.payload_data.get("lastName"),
                    student_number=self.payload_data.get("studentNumber"),
                    phone_number=self.payload_data.get("phoneNumber"),
                    dob=self.payload_data.get("dateOfBirth"),
                    email=self.payload_data.get("emailAddress"),
                    city=self.payload_data.get("city"),
                    street_address=self.payload_data.get("streetAddress"),
                    postal_code=self.payload_data.get("postalCode"),
                    middle_name=self.payload_data.get("middleName"),
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
