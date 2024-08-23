import asyncio
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyCourseChange(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.test_urls = {
            "course_change": f"{self.url}/ds/odata/StudentCourseStatusChangeReasons",
        }
        self.api_client.timeout = 30

    def test_fetch_course_change_reason(self):
        self.test_name = "course_change"
        self.assertEqual(asyncio.run(self.anthology.fetch_course_change_reason()), self.success_response)
        self.test_params[self.test_name] = {"$filter": "IsForDrop eq true"}
        self.assertEqual(asyncio.run(self.anthology.fetch_course_change_reason({"drop": True})), self.success_response)
        self.test_params[self.test_name] = {"$filter": "IsForUnregister eq true"}
        self.assertEqual(
            asyncio.run(self.anthology.fetch_course_change_reason({"unregister": True})), self.success_response
        )
        self.test_params[self.test_name] = {"$filter": "IsForDrop eq false and IsForUnregister eq false"}
        self.assertEqual(
            asyncio.run(self.anthology.fetch_course_change_reason({"drop": False, "unregister": False})),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
