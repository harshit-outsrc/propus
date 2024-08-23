import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestSalesforceQuery(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.test_urls = {"custom_query": f"{self.url}/services/data/salesforce_version/query/"}
        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 15

    def test_custom_query(self):
        self.test_name = "custom_query"
        query = "this is our salesforce SOQL custom query"
        self.test_params[self.test_name] = {"q": query}
        self.success_response = {"totalSize": 5, "records": [1, 2, 3, 4]}
        self.assertEqual(self.salesforce.custom_query(query), self.success_response)


if __name__ == "__main__":
    unittest.main()
