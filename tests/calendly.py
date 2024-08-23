from propus.calendly import Calendly
from tests.api_client import TestAPIClient


class TestCalendly(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        # API client setup for test class
        self.api_client = Calendly(authorization=self.application_key, base_url=self.url)
        self.api_client.request_service = self._req_mock
        # Test data
        self.event_id = "efa5e954-fdae-4ad8-89c3-ccf9aef5cd46"
        self.user_id = "537227f9-bbd3-4b43-a885-ba1f42ea8eb2"
        self.organization_id = "0a8f5eba-7785-47c5-be77-ea70da1c1048"
        self.test_queries = {"test": "response"}
        self.test_urls = {
            "fetch_user": f"{self.url}/users/{self.user_id}",
            "fetch_event_type": f"{self.url}/event_types/{self.event_id}",
            "fetch_scheduled_events": f"{self.url}/scheduled_events",
        }
        # Consolidate test data, endpoints, urls from parent and child classes
        self.api_client.endpoints = self.api_client.endpoints | self._endpoints
        self.test_urls = self.test_urls | self._test_urls

    def test_fetch_event_type(self):
        self.test_name = "fetch_event_type"
        response = self.api_client.fetch_event_type(self.event_id)
        self.assertEqual(response, self.success_response)

    def test_fetch_user(self):
        self.test_name = "fetch_user"
        response = self.api_client.fetch_user(self.user_id)
        self.assertEqual(response, self.success_response)

    def test_fetch_scheduled_events(self):
        self.test_name = "fetch_scheduled_events"
        self.test_params[self.test_name] = {"organization": self.organization_id} | self.test_queries
        response = self.api_client.fetch_scheduled_events(self.organization_id, **self.test_queries)
        self.assertEqual(response, self.success_response)


if __name__ == "__main__":
    import unittest

    unittest.main()
