from propus.zero_bounce import ZeroBounce
from tests.api_client import TestAPIClient


class TestZeroBounce(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        # API client setup for test class
        self.api_client = ZeroBounce(authorization=self.application_key, base_url=self.url)
        self.api_client.request_service = self._req_mock
        self.timeout = 30
        # Test data
        self.email = "you@me.com"
        self.ip_address = "1.1.1.1"
        self.date = "2022-06-01"
        self.data_api = {"start_date": self.date, "end_date": self.date}
        self.data_batch = {"email_batch": [[self.email], [self.email, self.ip_address]]}
        self.data_email = {"email": self.email, "ip_address": self.ip_address}
        self.test_urls = {
            "get_api_usage": f"{self.url}/v2/getapiusage",
            "get_credits": f"{self.url}/v2/getcredits",
            "validate_email": f"{self.url}/v2/validate",
            "validate_email_batch": f"{self.url}/v2/validatebatch",
        }
        # Consolidate test data, urls, etc. from parent and child classes
        self._test_data = self._test_data | self.data_api | self.data_batch | self.data_email
        self.api_client.endpoints = self.api_client.endpoints | self._endpoints
        self.test_urls = self.test_urls | self._test_urls

    def test_get_api_usage(self):
        self.test_name = "get_api_usage"
        self.test_params[self.test_name] = {
            "api_key": self.application_key,
            "start_date": self.date,
            "end_date": self.date,
        }
        response = self.api_client.get_api_usage(**self.data_api)
        self.assertEqual(response, self.success_response)

    def test_get_credits(self):
        self.test_name = "get_credits"
        self.test_params[self.test_name] = {"api_key": self.application_key}
        response = self.api_client.get_credits()
        self.assertEqual(response, self.success_response)

    def test_validate(self):
        self.test_name = "validate_email"
        self.test_params[self.test_name] = {
            "api_key": self.application_key,
            "email": self.email,
            "ip_address": self.ip_address,
        }
        response = self.api_client.validate_email_address(**self.data_email)
        self.assertEqual(response, self.success_response)

    def test_validate_batch(self):
        self.test_name = "validate_email_batch"
        self.test_params[self.test_name] = {
            "api_key": self.application_key,
            "email_batch": [
                {"email_address": self.email},
                {"email_address": self.email, "ip_address": self.ip_address},
            ],
        }
        response = self.api_client.validate_email_address_batch(**self.data_batch)
        self.assertEqual(response, self.success_response)


if __name__ == "__main__":
    import unittest

    unittest.main()
