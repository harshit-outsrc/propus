from propus.key_cdn import KeyCDN
from tests.api_client import TestAPIClient


class TestKeyCDN(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        # API client setup for test class
        self.api_client = KeyCDN(authorization=self.application_key, base_url=self.url)
        self.api_client.request_service = self._req_mock
        self.expected_headers["User-Agent"] = "keycdn-tools:https://calbright.org"
        # Test data
        self.ip_address = "1.1.1.1"
        self.host_name = "foo.bar"
        self.data_ip_address = {"host": self.ip_address}
        self.data_host_name = {"host": self.host_name}
        self.test_urls = {
            "get_geo_json_ip": f"{self.url}/geo.json",
            "get_geo_json_name": f"{self.url}/geo.json",
        }
        # Consolidate test data, urls, etc. from parent and child classes
        self._test_data = self._test_data | self.data_ip_address | self.data_host_name
        self.api_client.endpoints = self.api_client.endpoints | self._endpoints
        self.test_urls = self.test_urls | self._test_urls

    def test_get_geo_json_from_ip_address(self):
        self.test_name = "get_geo_json_ip"
        self.test_params[self.test_name] = self.data_ip_address
        response = self.api_client.get_geo_json(**self.data_ip_address)
        self.assertEqual(response, self.success_response)

    def test_get_geo_json_from_ip_host_name(self):
        self.test_name = "get_geo_json_name"
        self.test_params[self.test_name] = self.data_host_name
        response = self.api_client.get_geo_json(**self.data_host_name)
        self.assertEqual(response, self.success_response)


if __name__ == "__main__":
    import unittest

    unittest.main()
