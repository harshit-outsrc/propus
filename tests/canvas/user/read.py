import asyncio
import datetime
import unittest
import urllib.parse
from unittest.mock import Mock

from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasUserRead(TestAPIClient):
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
            "user_id": 1234,
            "account_id": 1,
            "start_time": datetime.datetime(2023, 3, 13),
            "end_time": datetime.datetime.now(),
        }
        start_end_string = urllib.parse.urlencode(
            {"start_time": self.test_data["start_time"].isoformat(), "end_time": self.test_data["end_time"].isoformat()}
        )
        self.test_urls = {
            "get_user": f"{self.url}/api/v1/users/{self.test_data['user_id']}",
            "get_user_profile": f"{self.url}/api/v1/users/{self.test_data['user_id']}/profile",
            "list_users_in_account": f"{self.url}/api/v1/accounts/{self.test_data['account_id']}/users",
            "get_user_page_views": f"{self.url}/api/v1/users/{self.test_data['user_id']}/page_views?{start_end_string}",
        }

    def test_get_user(self):
        self.test_name = "get_user"
        self.assertEqual(
            asyncio.run(self.canvas.get_user(user_id=self.test_data.get("user_id"))),
            self.success_response,
        )

    def test_get_user_profile(self):
        self.test_name = "get_user_profile"
        self.assertEqual(
            asyncio.run(self.canvas.get_user_profile(user_id=self.test_data.get("user_id"))),
            self.success_response,
        )

    def test_list_users_in_account(self):
        self.test_name = "list_users_in_account"
        self.assertEqual(
            asyncio.run(self.canvas.list_users_in_account(account_id=self.test_data.get("account_id"))),
            self.success_response,
        )

    def test_get_user_page_views(self):
        self.test_name = "get_user_page_views"
        self.assertEqual(
            asyncio.run(
                self.canvas.get_user_page_views(
                    user_id=self.test_data.get("user_id"),
                    start_time=self.test_data.get("start_time"),
                    end_time=self.test_data.get("end_time"),
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
