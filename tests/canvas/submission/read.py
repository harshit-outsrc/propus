import asyncio
import datetime
import unittest
import urllib.parse
from unittest.mock import Mock
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasSubmissionRead(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(
            application_key=self.application_key,
            base_url=self.url,
            additional_headers=None,
            auth_providers=auth_providers,
        )
        self.canvas.request_service = self._req_mock
        self.canvas.make_request = Mock(side_effect=self.mock_make_request)

        self.test_data = {
            "course_id": 123,
            "section_id": 456,
            "assignment_id": 789,
            "user_id": 12,
            "single_assignment_query_params": {
                "include[]": ["submission_comments", "rubric_assessment", "assignment", "user", "group"],
                "grouped": True,
            },
            "multiple_assignment_query_params": {
                "student_ids[]": [123, 456],
                "assignment_ids[]": [789, 101],
                "grouped": False,
                "post_to_sis": True,
                "submitted_since": datetime.datetime(2023, 3, 1),
                "graded_since": datetime.datetime(2023, 3, 20),
                "grading_period_id": 22,
                "workflow_state": "submitted",
                "enrollment_state": "active",
                "state_based_on_date": False,
                "order": "graded_at",
                "order_direction": "descending",
                "include[]": ["visibility", "course", "user", "total_scores"],
            },
            "single_submission_query_params": {
                "include[]": ["submission_comments", "rubric_assessment", "submission_history", "user", "read_status"],
            },
            "submission_summary_query_params": {"grouped": True},
            "list_missing_submissions_for_user_query_params": {
                "observed_user_id": 123,
                "include[]": ["planner_overrides", "course"],
                "filter[]": ["submittable", "current_grading_period"],
                "course_ids[]": [123, 456],
            },
        }
        single_assignment_query_params = urllib.parse.urlencode(
            self.test_data["single_assignment_query_params"], doseq=True
        )
        # This converts the datetime objects to an iso string format to match the expected query params
        formatted_multiple_assignment_course_query_params = {
            k: (v.isoformat() if isinstance(v, datetime.datetime) else v)
            for k, v in self.test_data["multiple_assignment_query_params"].items()
        }

        multiple_assignment_course_query_params = urllib.parse.urlencode(
            formatted_multiple_assignment_course_query_params, doseq=True
        )

        multiple_assignment_section_query_params = urllib.parse.urlencode({"student_ids[]": "all"})

        single_submission_query_params = urllib.parse.urlencode(
            self.test_data["single_submission_query_params"], doseq=True
        )

        submission_summary_query_params = urllib.parse.urlencode(
            self.test_data["submission_summary_query_params"], doseq=True
        )

        missing_submissions_query_params = urllib.parse.urlencode(
            self.test_data["list_missing_submissions_for_user_query_params"], doseq=True
        )

        self.test_urls = {
            "list_assignment_submissions_for_single_assignment_course": (
                f"{self.url}/api/v1/courses/{self.test_data['course_id']}/assignments/"
                f"{self.test_data['assignment_id']}/submissions?{single_assignment_query_params}"
            ),
            "list_assignment_submissions_for_single_assignment_section": (
                f"{self.url}/api/v1/sections/{self.test_data['section_id']}/assignments/"
                f"{self.test_data['assignment_id']}/submissions?"
            ),
            "list_assignment_submissions_for_multiple_assignments_course": (
                f"{self.url}/api/v1/courses/{self.test_data['course_id']}/students"
                f"/submissions?{multiple_assignment_course_query_params}"
            ),
            "list_assignment_submissions_for_multiple_assignments_section": (
                f"{self.url}/api/v1/sections/{self.test_data['section_id']}"
                f"/students/submissions?{multiple_assignment_section_query_params}"
            ),
            "get_single_submission_course": (
                f"{self.url}/api/v1/courses/{self.test_data['course_id']}/assignments/"
                f"{self.test_data['assignment_id']}/submissions/{self.test_data['user_id']}"
                f"?{single_submission_query_params}"
            ),
            "get_single_submission_section": (
                f"{self.url}/api/v1/sections/{self.test_data['section_id']}/assignments/"
                f"{self.test_data['assignment_id']}/submissions/{self.test_data['user_id']}?"
            ),
            "get_submission_summary_course": (
                f"{self.url}/api/v1/courses/{self.test_data['course_id']}/assignments/"
                f"{self.test_data['assignment_id']}/submission_summary?{submission_summary_query_params}"
            ),
            "get_submission_summary_section": (
                f"{self.url}/api/v1/sections/{self.test_data['section_id']}/assignments/"
                f"{self.test_data['assignment_id']}/submission_summary?{submission_summary_query_params}"
            ),
            "list_missing_submissions_for_user_simple": (
                f"{self.url}/api/v1/users/{self.test_data['user_id']}/missing_submissions?"
            ),
            "list_missing_submissions_for_user_expanded": (
                f"{self.url}/api/v1/users/{self.test_data['user_id']}"
                f"/missing_submissions?{missing_submissions_query_params}"
            ),
        }

    def test_list_assignment_submissions_for_single_assignment_course(self):
        self.test_name = "list_assignment_submissions_for_single_assignment_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_assignment_submissions_for_single_assignment(
                    object_type="course",
                    object_id=self.test_data["course_id"],
                    assignment_id=self.test_data["assignment_id"],
                    include=self.test_data["single_assignment_query_params"]["include[]"],
                    grouped=self.test_data["single_assignment_query_params"]["grouped"],
                )
            ),
            self.success_response,
        )

    def test_list_assignment_submissions_for_single_assignment_section(self):
        self.test_name = "list_assignment_submissions_for_single_assignment_section"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_assignment_submissions_for_single_assignment(
                    object_type="section",
                    object_id=self.test_data["section_id"],
                    assignment_id=self.test_data["assignment_id"],
                )
            ),
            self.success_response,
        )

    def test_list_assignment_submissions_for_multiple_assignments_course(self):
        self.test_name = "list_assignment_submissions_for_multiple_assignments_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_assignment_submissions_for_multiple_assignments(
                    object_type="course",
                    object_id=self.test_data["course_id"],
                    student_ids=self.test_data["multiple_assignment_query_params"]["student_ids[]"],
                    assignment_ids=self.test_data["multiple_assignment_query_params"]["assignment_ids[]"],
                    grouped=self.test_data["multiple_assignment_query_params"]["grouped"],
                    post_to_sis=self.test_data["multiple_assignment_query_params"]["post_to_sis"],
                    submitted_since=self.test_data["multiple_assignment_query_params"]["submitted_since"],
                    graded_since=self.test_data["multiple_assignment_query_params"]["graded_since"],
                    grading_period_id=self.test_data["multiple_assignment_query_params"]["grading_period_id"],
                    workflow_state=self.test_data["multiple_assignment_query_params"]["workflow_state"],
                    enrollment_state=self.test_data["multiple_assignment_query_params"]["enrollment_state"],
                    state_based_on_date=self.test_data["multiple_assignment_query_params"]["state_based_on_date"],
                    order=self.test_data["multiple_assignment_query_params"]["order"],
                    order_direction=self.test_data["multiple_assignment_query_params"]["order_direction"],
                    include=self.test_data["multiple_assignment_query_params"]["include[]"],
                )
            ),
            self.success_response,
        )

    def test_list_assignment_submissions_for_multiple_assignments_section(self):
        self.test_name = "list_assignment_submissions_for_multiple_assignments_section"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_assignment_submissions_for_multiple_assignments(
                    object_type="section",
                    object_id=self.test_data["section_id"],
                )
            ),
            self.success_response,
        )

    def test_get_single_submission_course(self):
        self.test_name = "get_single_submission_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_single_submission(
                    object_type="course",
                    object_id=self.test_data["course_id"],
                    assignment_id=self.test_data["assignment_id"],
                    user_id=self.test_data["user_id"],
                    include=self.test_data["single_submission_query_params"]["include[]"],
                )
            ),
            self.success_response,
        )

    def test_get_single_submission_section(self):
        self.test_name = "get_single_submission_section"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_single_submission(
                    object_type="section",
                    object_id=self.test_data["section_id"],
                    assignment_id=self.test_data["assignment_id"],
                    user_id=self.test_data["user_id"],
                )
            ),
            self.success_response,
        )

    def test_get_submission_summary_course(self):
        self.test_name = "get_submission_summary_course"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_submission_summary(
                    object_type="course",
                    object_id=self.test_data["course_id"],
                    assignment_id=self.test_data["assignment_id"],
                    grouped=self.test_data["submission_summary_query_params"]["grouped"],
                )
            ),
            self.success_response,
        )

    def test_get_submission_summary_section(self):
        self.test_name = "get_submission_summary_section"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_submission_summary(
                    object_type="section",
                    object_id=self.test_data["section_id"],
                    assignment_id=self.test_data["assignment_id"],
                    grouped=self.test_data["submission_summary_query_params"]["grouped"],
                )
            ),
            self.success_response,
        )

    def test_list_missing_submissions_for_user_simple(self):
        self.test_name = "list_missing_submissions_for_user_simple"
        self.assertEqual(
            asyncio.run(self.canvas.list_missing_submissions_for_user(user_id=self.test_data["user_id"])),
            self.success_response,
        )

    def test_list_missing_submissions_for_user_expanded(self):
        self.test_name = "list_missing_submissions_for_user_expanded"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_missing_submissions_for_user(
                    user_id=self.test_data["user_id"],
                    observed_user_id=self.test_data["list_missing_submissions_for_user_query_params"][
                        "observed_user_id"
                    ],
                    include=self.test_data["list_missing_submissions_for_user_query_params"]["include[]"],
                    filter=self.test_data["list_missing_submissions_for_user_query_params"]["filter[]"],
                    course_ids=self.test_data["list_missing_submissions_for_user_query_params"]["course_ids[]"],
                )
            ),
            self.success_response,
        )

    def mock_make_request(self, **kwargs):
        self.assertEqual(kwargs.get("req_type"), "get")
        self.assertTrue(kwargs.get("url"), self.test_urls.get(self.test_name))
        return self.success_response


if __name__ == "__main__":
    unittest.main()
