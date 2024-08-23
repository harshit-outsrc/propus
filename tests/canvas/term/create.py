import asyncio
import datetime
import unittest
from tests.api_client import TestAPIClient
from propus.canvas import Canvas
from propus.canvas.term import TermOverride


class TestCanvasTermCreate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(application_key=self.application_key, base_url=self.url, auth_providers=auth_providers)
        self.canvas.request_service = self._req_mock

        self.test_data = {
            "account_id": 1,
            "name": "Spring 2024 2",
            "start_at": datetime.datetime(2024, 4, 1),
            "end_at": datetime.datetime(2024, 5, 1),
            "sis_term_id": "SPRING2024-2",
            "overrides": [
                TermOverride(
                    override_enrollment_type="TeacherEnrollment",
                    override_start_at=datetime.datetime(2024, 4, 1),
                    override_end_at=datetime.datetime(2024, 5, 1),
                ),
                TermOverride(
                    override_enrollment_type="StudentEnrollment",
                    override_start_at=datetime.datetime(2024, 4, 1),
                ),
            ],
        }

        self.test_urls = {
            "create_term": f"{self.url}/api/v1/accounts/{self.test_data['account_id']}/terms",
        }

    def test_create_term(self):
        self.test_name = "create_term"
        self.assertEqual(
            asyncio.run(
                self.canvas.create_term(
                    account_id=self.test_data["account_id"],
                    name=self.test_data["name"],
                    start_at=self.test_data["start_at"],
                    end_at=self.test_data["end_at"],
                    sis_term_id=self.test_data["sis_term_id"],
                )
            ),
            self.success_response,
        )

    def test_create_term_expanded(self):
        self.test_name = "create_term"
        self.assertEqual(
            asyncio.run(
                self.canvas.create_term(
                    account_id=self.test_data["account_id"],
                    name=self.test_data["name"],
                    start_at=self.test_data["start_at"],
                    end_at=self.test_data["end_at"],
                    sis_term_id=self.test_data["sis_term_id"],
                    overrides=self.test_data["overrides"],
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
