from unittest.mock import MagicMock

from propus.zoom import Zoom
from tests.api_client import TestAPIClient


class TestZoom(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        foo = "bar"
        # API client setup for test class
        self.api_client = Zoom(access_token="Bearer foo", account_id=foo)
        # Test data
        # Keeping camelCase to reduce on edits/errors and stick with copy/paste from Zoom docs
        self.params = {
            "{accountId}": foo,
            "file": foo,
            "{meetingId}": foo,
            "{pollId}": foo,
            "{registrantId}": foo,
            "{userId}": foo,
        }
        self.empty_response = {}
        self.single_response = self.params | self.empty_response
        self.paginated_response = {"page_size": 1, "total_records": 1, "users": [self.single_response]}
        self.bulk_response = [self.single_response]
        # Endpoints to POST data
        self.create_urls = {
            # _account.py
            "virtual_background": f"{self.url}/accounts/{foo}/settings/virtual_backgrounds",
            # _user.py
            "user": f"{self.url}/users",
        }
        # Endpoints to DELETE data
        self.delete_urls = {
            # _account.py
            "virtual_background": f"{self.url}/accounts/{foo}/settings/virtual_backgrounds",
        }
        # Endpoints to GET data
        # One object with no parameters
        self.no_param_urls = {
            "user_summary": f"{self.url}/users/summary",
        }
        # One object with one parameter
        self.one_param_urls = {
            # _meeting.py
            "meeting": f"{self.url}/meetings/{foo}",
            "meeting_polls": f"{self.url}/meetings/{foo}/polls",
            "meeting_invitation": f"{self.url}/meetings/{foo}/invitation",
            "past_meeting_details": f"{self.url}/past_meetings/{foo}",
            "past_meeting_instances": f"{self.url}/past_meetings/{foo}/instances",
            "past_meeting_polls": f"{self.url}/past_meetings/{foo}/polls",
            "past_meeting_qa": f"{self.url}/past_meetings/{foo}/qa",
            "registration_questions": f"{self.url}/meetings/{foo}/registrants/questions",
            "survey": f"{self.url}/meetings/{foo}/survey",
            # _user.py
            "user": f"{self.url}/users/{foo}",
            "user_assistants": f"{self.url}/users/{foo}/assistants",
            "user_schedulers": f"{self.url}/users/{foo}/schedulers",
        }
        # One object with two parameters
        self.two_param_urls = {
            # _meeting.py
            "poll": f"{self.url}/meetings/{foo}/polls/{foo}",
            "registrant": f"{self.url}/meetings/{foo}/registrants/{foo}",
        }
        # Multiple objects with no parameter
        self.no_param_page_urls = {
            "users": f"{self.url}/users",
        }
        # Multiple objects with one parameter
        self.one_param_page_urls = {
            # _meeting.py
            "past_meeting_participants": f"{self.url}/past_meetings/{foo}/participants",
            "polls": f"{self.url}/meetings/{foo}/polls",
            "registrants": f"{self.url}/meetings/{foo}/registrants",
            # _user.py
            "user_meetings": f"{self.url}/users/{foo}/meetings",
        }
        self.fetch_urls = self.no_param_urls | self.one_param_urls | self.two_param_urls
        self.fetch_bulk_urls = self.no_param_page_urls | self.one_param_page_urls
        # Consolidate test data, urls, etc. from parent and child classes
        self._test_data = self._test_data
        self.api_client.endpoints = self.api_client.endpoints | self._endpoints
        self.test_urls = self.fetch_urls | self.fetch_bulk_urls | self._test_urls

    def test_get_data_by_endpoint(self):
        """Tests all endpoints that do not retrieve paginated results"""
        self.test_name = "test_get_data_by_endpoint"
        self.api_client._make_request = MagicMock(return_value=self._make_request())
        for endpoint, url in self.fetch_urls.items():
            response = self.api_client.get_data_by_endpoint(endpoint, params=self.params)
            self.assertEqual(response, self.single_response)

    def test_get_bulk_data_by_endpoint(self):
        """Tests all endpoints that retrieve paginated results"""
        self.test_name = "test_get_bulk_data_by_endpoint"
        self.api_client._make_request = MagicMock(return_value=self._make_request())
        for endpoint, url in self.fetch_bulk_urls.items():
            response = self.api_client.get_bulk_data_by_endpoint(endpoint, params=self.params)
            self.assertEqual(response, self.bulk_response)

    def test_create_functions(self):
        """Tests all `create` helper functions"""
        self.test_name = "test_create_functions"
        self.api_client._make_request = MagicMock(return_value=self._make_request())
        for k, v in self.create_urls.items():
            test_function = getattr(self.api_client, f"create_{k}")
            self.assertEqual(test_function(v), self.single_response)

    def test_delete_functions(self):
        """Tests all `delete` helper functions"""
        self.test_name = "test_delete_functions"
        self.api_client._make_request = MagicMock(return_value=self._make_request())
        for k, v in self.delete_urls.items():
            test_function = getattr(self.api_client, f"delete_{k}")
            self.assertEqual(test_function(v), self.empty_response)

    def test_fetch_functions(self):
        """Tests all `fetch` helper functions that do not receive paginated data"""
        self.test_name = "test_fetch_functions"
        self.api_client._make_request = MagicMock(return_value=self._make_request())
        for k, v in self.no_param_urls.items():
            test_function = getattr(self.api_client, f"fetch_{k}")
            self.assertEqual(test_function(), self.single_response)
        for k, v in self.one_param_urls.items():
            test_function = getattr(self.api_client, f"fetch_{k}")
            self.assertEqual(test_function(k), self.single_response)
        for k, v in self.two_param_urls.items():
            test_function = getattr(self.api_client, f"fetch_{k}")
            self.assertEqual(test_function(k, v), self.single_response)

    def test_bulk_fetch_functions(self):
        """Tests all `fetch` helper functions that receive paginated data"""
        self.test_name = "test_bulk_fetch_functions"
        self.api_client._make_request = MagicMock(return_value=self._make_request())
        for k, v in self.no_param_page_urls.items():
            test_function = getattr(self.api_client, f"fetch_{k}")
            self.assertEqual(test_function(), self.bulk_response)
        for k, v in self.one_param_page_urls.items():
            test_function = getattr(self.api_client, f"fetch_{k}")
            self.assertEqual(test_function(k), self.bulk_response)

    def _make_request(self):
        """Test helper function to provide mock responses for different types of API calls to Zoom."""
        if self.test_name and "bulk" in self.test_name:
            return self.paginated_response
        elif self.test_name and "delete" in self.test_name:
            return self.empty_response
        else:
            return self.single_response


if __name__ == "__main__":
    import unittest

    unittest.main()
