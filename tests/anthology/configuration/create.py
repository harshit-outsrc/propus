import asyncio
from datetime import datetime
from typing import List
import unittest

from propus.helpers.exceptions import (
    InvalidStringLength,
    InvalidDayOfWeek,
)
from propus.anthology.configuration._exception import InvalidTerm
from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyConfigurationCreate(TestAPIClient):
    def setUp(self):
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.start_data = {
            "id": -1,
            "campusGroupId": 0,
            "code": "2022-23-TERM-01",
            "isActive": True,
            "name": "2022-23-TERM-01",
            "shiftId": 0,
            "startDate": "2023/01/17 00:00:00",
            "campusGroup": {
                "id": 9173,
                "code": "K~990",
                "isActive": True,
                "name": "K~990",
                "type": "K",
                "campusList": [
                    {"id": 9745, "campusGroupId": 9173, "campusId": self.anthology._campus_id, "isCampusActive": True}
                ],
            },
        }
        self.term_data = {
            "id": -1,
            "addDropDate": "2023/02/16 00:00:00",
            "campusIdList": [5],
            "code": "2022-23-TERM-01",
            "startDate": "2023/01/17 00:00:00",
            "endDate": "2023/07/17 00:00:00",
            "isActive": True,
            "name": "2022-23-TERM-01",
            "shiftId": 0,
            "termUsage": 4,
            "sendCourseSectionDataToLms": True,
            "sendInstructorAssignmentsToLms": True,
            "sendStudentRegistrationDataToLms": True,
        }

        self.test_urls = {
            "start_date_create": f"{self.url}/api/commands/Academics/ShiftSchoolStartDate/SaveNew",
            "term_create": f"{self.url}/api/commands/Academics/Term/SaveNew",
        }

        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 30

    def test_start_date_errors(self):
        def testException(args: List, expected_exception: Exception):
            try:
                a, b = args
                asyncio.run(self.anthology.create_start_date(a, b))
            except expected_exception as err:
                return str(err)
            return False

        args = ["", None]
        self.assertTrue(
            testException(args, InvalidStringLength) is not False,
            msg="invalid term name length",
        )
        args[0] = "WAY_TO_LONG_STRING_HERE"
        self.assertTrue(
            testException(args, InvalidStringLength) is not False,
            msg="invalid term name length",
        )
        args[0] = "INVALID_TERM"
        self.assertTrue(testException(args, InvalidTerm) is not False, msg="invalid term name")
        args[0] = "2022-22-TERM-01"
        self.assertTrue(testException(args, InvalidTerm) is not False, msg="invalid term name")
        args[0] = "2022-23-TERM-01"

        args[1] = datetime(2022, 1, 2)
        self.assertTrue(
            testException(args, InvalidDayOfWeek) is not False,
            msg="invalid start_date day",
        )

    def test_start_date_create(self):
        self.test_name = "start_date_create"
        self._test_data = self._test_data | {"payload": self.start_data}
        self.assertEqual(
            asyncio.run(
                self.anthology.create_start_date(name=self.start_data.get("name"), start_date=datetime(2023, 1, 17))
            ),
            self.success_response,
        )

    def test_term_errors(self):
        def testException(args: List, expected_exception: Exception):
            try:
                a, b, c, d = args
                asyncio.run(self.anthology.create_term(a, b, c, d))
            except expected_exception as err:
                return str(err)
            return False

        args = ["", None, None, None]
        self.assertTrue(
            testException(args, InvalidStringLength) is not False,
            msg="invalid term name length",
        )
        args[0] = "WAY_TO_LONG_STRING_HERE"
        self.assertTrue(
            testException(args, InvalidStringLength) is not False,
            msg="invalid term name length",
        )
        args[0] = "INVALID_TERM"
        self.assertTrue(testException(args, InvalidTerm) is not False, msg="invalid term name")
        args[0] = "2022-22-TERM-01"
        self.assertTrue(testException(args, InvalidTerm) is not False, msg="invalid term name")
        args[0] = "2022-23-TERM-01"

        args[1] = datetime(2022, 1, 2)
        self.assertTrue(
            testException(args, InvalidDayOfWeek) is not False,
            msg="invalid start_date day",
        )

        args[1] = datetime(2022, 1, 4)
        args[2] = datetime(2022, 3, 2)
        self.assertTrue(
            testException(args, InvalidDayOfWeek) is not False,
            msg="invalid end_date day",
        )

        args[2] = datetime(2022, 3, 7)
        args[3] = datetime(2022, 3, 2)
        self.assertTrue(
            testException(args, InvalidDayOfWeek) is not False,
            msg="invalid add_drop day",
        )

        args[3] = datetime(2022, 3, 10)
        self.assertEqual(
            testException(args, Exception),
            "start_date to add_drop_date should be 30 days",
            msg="invalid add_drop day",
        )

    def test_term_create(self):
        self.test_name = "term_create"
        self._test_data = {"payload": self.term_data}
        self.assertEqual(
            asyncio.run(
                self.anthology.create_term(
                    term_name="2022-23-TERM-01",
                    start_date=datetime(2023, 1, 17),
                    end_date=datetime(2023, 7, 17),
                    add_drop_date=datetime(2023, 2, 16),
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
