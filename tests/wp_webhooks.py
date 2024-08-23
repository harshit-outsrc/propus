import unittest

from propus.wp_webhooks import WPWebhook
from tests.api_client import TestAPIClient


class TestWPWebhook(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.wp = WPWebhook(base_url=None, api_key="Authorization some_testing_jwt!", wh_env="beta")
        self.wp._make_request = self._req_mock
        self._req_mock.return_value = self.success_response
        self.api_client.default_headers = self.expected_headers

        self.api_client.timeout = 10

    def test_update_user(self):
        self.test_name = "update_user"
        self.assertEqual(
            self.wp.update_user(user_id="id", user_meta={}, user_email="email"),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
