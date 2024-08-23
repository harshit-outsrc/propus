import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestSalesforceBulkQuery(TestAPIClient, unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.test_data = {
            "id": "0000000000001",
            "operation": "query",
            "object": "Contact",
            "createdById": "1234TestingTester",
            "createdDate": "2026-1-11T17:50:19.000+0000",
            "systemModstamp": "2026-11-11T17:50:19.000+0000",
            "state": "UploadComplete",
            "concurrencyMode": "Parallel",
            "contentType": "CSV",
            "apiVersion": 59.0,
            "lineEnding": "LF",
            "columnDelimiter": "COMMA",
        }
        self._test_data = self._test_data | self.test_data

        self.test_urls = {
            "create_bulk_query_job": f"{self.url}/services/data/{self.version}/jobs/query",
            "query_bulk_job": f'{self.url}/services/data/{self.version}/jobs/query/{self.test_data.get("id")}',
            "query_bulk_job_results": f'{self.url}/services/data/{self.version}/jobs/query/{self.test_data.get("id")}/results',  # noqa: (E501)
        }
        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 15

    def test_create_query_job(self):
        self.test_name = "create_bulk_query_job"
        self.success_response = self.test_data
        query = "this is our salesforce SOQL bulk query"
        self.assertEqual(self.salesforce._create_query_job(query), self.success_response)

    def test_abort_query_job(self):
        self.test_name = "query_bulk_job"
        self.success_response = self._test_data
        self.success_response["state"] = "Aborted"
        self.assertEqual(
            self.salesforce._abort_query_job(self.test_data.get("id")),
            self.success_response,
        )

    def test_delete_query_job(self):
        self.api_client.default_headers = self.api_client.headers["delete"]
        self.test_name = "query_bulk_job"
        self.success_response = {"response": "204 No Content"}
        self.assertEqual(
            self.salesforce._delete_query_job(self.test_data.get("id")),
            self.success_response,
        )

    def test_get_query_job(self):
        self.test_name = "query_bulk_job"
        self.success_response = self.test_data
        self.success_response["state"] = "JobComplete"
        self.assertEqual(
            self.salesforce._get_query_job(self.test_data.get("id")),
            self.success_response,
        )

    def test_get_query_job_results(self):
        self.api_client.default_headers["accept"] = "text/csv"
        self.test_name = "query_bulk_job_results"
        self.response_text = "id, name, email, \n123test, Tester, test@test.com"
        self.success_headers = {
            "Content-Type": "text/csv",
            "Sforce-NumberOfRecords": 1,
            "Sforce-Locator": "null",
        }
        self.success_response = {
            "locator": "",
            "number_of_records": 1,
            "records": "id, name, email, \n123test, Tester, test@test.com",
        }

        self.json_response = False
        self.assertEqual(
            self.salesforce._get_query_job_results(self.test_data.get("id")),
            self.success_response,
        )

    def test_bulk_query_results(self):
        self.api_client.default_headers["accept"] = "text/csv"
        self.test_name = "query_bulk_job_results"
        self.response_text = "id, name, email \n123test, Tester, test@test.com \n456test, Tester2, test2@test.com"
        self.success_headers = {
            "Content-Type": "text/csv",
            "Sforce-NumberOfRecords": 2,
            "Sforce-Locator": "null",
        }
        self.success_response = "id, name, email \n123test, Tester, test@test.com \n456test, Tester2, test2@test.com"
        self.json_response = False
        self.assertEqual(
            tuple(self.salesforce._bulk_query_results(self.test_data.get("id"))),
            (self.success_response,),
        )

    def test_get_dict_of_bulk_query_results(self):
        csv_data = "id, name, email \n123test, Tester, test@test.com \n456test, Tester2, test2@test.com"
        self.assertIsInstance(Salesforce.get_dict_from_bulk_query_results(csv_data), list)


if __name__ == "__main__":
    unittest.main()
