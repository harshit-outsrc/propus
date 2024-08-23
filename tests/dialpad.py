import unittest

from propus.dialpad import Dialpad
from tests.api_client import TestAPIClient


class TestDialpad(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.auth_token = "some_testing_jwt"
        call_id = "foo123"
        contact_id = "bar456"
        number_id = "baz789"
        stats_id = "tata"
        user_id = "titi"
        # API client setup for test class
        self.api_client = Dialpad(authorization=self.auth_token)
        self.api_client.request_service = self._req_mock
        self.endpoints = {
            "call": f"/api/v2/call/{call_id}",
            "contact": f"/api/v2/contacts/{contact_id}",
            "contacts": "/api/v2/contacts/",
            "number": f"/api/v2/numbers/{number_id}",
            "numbers": "/api/v2/numbers/",
            "create_stats": "/api/v2/stats/",
            "stats": f"/api/v2/stats/{stats_id}",
            "user": f"/api/v2/users/{user_id}",
            "users": "/api/v2/users/",
        }
        self.test_urls = {
            "call": f"{self.url}/api/v2/call/{call_id}",
            "contact": f"{self.url}/api/v2/contacts/{contact_id}",
            "contacts": f"{self.url}/api/v2/contacts/",
            "number": f"{self.url}/api/v2/numbers/{number_id}",
            "numbers": f"{self.url}/api/v2/numbers/",
            "create_stats": f"{self.url}/api/v2/stats/",
            "stats": f"{self.url}/api/v2/stats/{stats_id}",
            "user": f"{self.url}/api/v2/users/{user_id}",
            "users": f"{self.url}/api/v2/users/",
        }

        # Consolidate test data, endpoints, urls from parent and child classes
        self.api_client.endpoints = self.api_client.endpoints | self.endpoints | self._endpoints
        self.test_urls = self.test_urls | self._test_urls


if __name__ == "__main__":
    unittest.main()
