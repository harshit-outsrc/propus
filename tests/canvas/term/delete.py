import asyncio
import unittest

from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasTermDelete(TestAPIClient):
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

        self.test_data = {
            "account_id": 1,
            "term_id": 1234,
        }

        self.test_urls = {
            "delete_term": (
                f"{self.url}/api/v1/accounts/{self.test_data['account_id']}/terms/{self.test_data['term_id']}"
            ),
        }

    def test_delete_term(self):
        self.test_name = "delete_term"
        self.assertEqual(
            asyncio.run(
                self.canvas.delete_term(
                    account_id=self.test_data["account_id"],
                    term_id=self.test_data["term_id"],
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
