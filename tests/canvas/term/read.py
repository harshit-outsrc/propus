import asyncio
import unittest
import urllib.parse
from unittest.mock import Mock
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasTermRead(TestAPIClient):
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
            "account_id": 1,
            "term_id": 1234,
            "list_terms_query_params": {
                "workflow_state[]": "deleted",
                "include[]": ["overrides", "course_count"],
                "term_name": "Spring 2024",
            },
        }

        list_terms_query_params = urllib.parse.urlencode(self.test_data["list_terms_query_params"], doseq=True)

        self.test_urls = {
            "get_term": f"{self.url}/api/v1/accounts/{self.test_data['account_id']}/terms/{self.test_data['term_id']}",
            "list_terms": f"{self.url}/api/v1/accounts/{self.test_data['account_id']}/terms?{list_terms_query_params}",
        }

    def test_get_term(self):
        self.test_name = "get_term"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_term(
                    account_id=self.test_data["account_id"],
                    term_id=self.test_data["term_id"],
                )
            ),
            self.success_response,
        )

    def test_list_terms(self):
        self.test_name = "list_terms"
        self.assertEqual(
            asyncio.run(
                self.canvas.list_terms(
                    account_id=self.test_data["account_id"],
                    workflow_state=self.test_data["list_terms_query_params"]["workflow_state[]"],
                    include=self.test_data["list_terms_query_params"]["include[]"],
                    term_name=self.test_data["list_terms_query_params"]["term_name"],
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
