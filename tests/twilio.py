import unittest

from propus.twilio import Twilio
from tests.api_client import TestAPIClient


class TestTwilio(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.sid = "foo"
        self.auth_token = "some_testing_jwt"
        # API client setup for test class
        self.api_client = Twilio(account_sid=self.sid, auth_token=self.auth_token)
        self.api_client.request_service = self._req_mock
        self.endpoints = {
            "accounts": "/2010-04-01/Accounts.json",
            "addresses": f"/2010-04-01/Accounts/{self.sid}/Addresses.json",
        }
        self.test_urls = {
            "accounts": f"{self.url}/2010-04-01/Accounts.json",
            "addresses": f"{self.url}/2010-04-01/Accounts/{self.sid}/Addresses.json",
        }

        # Consolidate test data, endpoints, urls from parent and child classes
        self.api_client.endpoints = self.api_client.endpoints | self.endpoints | self._endpoints
        self.test_urls = self.test_urls | self._test_urls


if __name__ == "__main__":
    unittest.main()
