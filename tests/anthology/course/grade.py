import asyncio
from datetime import datetime
import unittest
from unittest.mock import Mock


from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologCourseGrade(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock
        self.test_urls = {
            "fetch_grade": f"{self.url}/ds/odata/GradeScaleLetterGrades",
            "post_grades": f"{self.url}/api/commands/Academics/StudentCourse/PostFinalGrade",
        }
        self.course_id = "calbright_1234"
        self.grade_data = {
            "letterGrade": "EXCELLENT",
            "endDate": "2023/11/03T00:00:00",
            "payStatus": "yes",
            "gradePoints": "5",
        }
        self.api_client.timeout = 30

    async def get_course_data(self, course_id):
        self.assertEqual(course_id, self.course_id)
        return {"data": self.grade_data}

    def test_post_grade(self):
        self.test_name = "post_grades"
        self.anthology.fetch_course = Mock(side_effect=self.get_course_data)
        self.assertEqual(
            asyncio.run(
                self.anthology.post_final_grade(
                    self.course_id, self.test_data.get("letterGrade"), datetime(2023, 11, 3)
                )
            ),
            self.success_response,
        )

    def test_fetch_grades(self):
        self.test_name = "fetch_grade"
        self.assertEqual(asyncio.run(self.anthology.fetch_grade()), self.success_response)
        self.test_params[self.test_name] = {"$filter": "IsDropGrade eq true"}
        self.assertEqual(asyncio.run(self.anthology.fetch_grade({"drop": True})), self.success_response)
        self.test_params[self.test_name] = {"$filter": "IsPassFail eq true"}
        self.assertEqual(asyncio.run(self.anthology.fetch_grade({"pass_fail": True})), self.success_response)
        self.test_params[self.test_name] = {"$filter": "IsDropGrade eq false and IsPassFail eq false"}
        self.assertEqual(
            asyncio.run(self.anthology.fetch_grade({"drop": False, "pass_fail": False})),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
