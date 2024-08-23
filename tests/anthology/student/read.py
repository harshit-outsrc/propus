import asyncio
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient
from propus.anthology.student._exceptions import InvalidSearchParameters


class TestAnthologyStudentRead(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.search_data = {
            "student_number": "STUDENT_123_ZXY",
            "first_name": "Johnny",
            "last_name": "Appleseed",
        }

        self.test_urls = {
            "student_by_id": f"{self.url}/api/commands/Common/Student/get",
            "student_search": f"{self.url}/ds/odata/Students",
        }
        self.api_client.timeout = 30

    def test_read_errors(self):
        with self.assertRaises(InvalidSearchParameters):
            asyncio.run(self.anthology.student_search(bad_filter=True))

    def test_student_by_id(self):
        self.test_name = "student_by_id"
        self._test_data = {"payload": {"id": self.search_data.get("student_number")}}
        self.assertEqual(
            asyncio.run(self.anthology.student_by_id(self.search_data.get("student_number"))),
            self.success_response,
        )

    def test_student_search(self):
        self.test_name = "student_search"
        self.test_params[self.test_name] = {
            "$filter": f"FirstName eq '{self.search_data.get('first_name')}' and LastName eq '{self.search_data.get('last_name')}' and StudentNumber eq '{self.search_data.get('student_number')}'"
        }
        self.assertEqual(
            asyncio.run(self.anthology.student_search(**self.search_data)),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
