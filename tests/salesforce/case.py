import unittest
from unittest.mock import patch

from propus.salesforce import Salesforce
from propus.salesforce.exceptions import CreateCaseUnknownRecordType, CreateCaseMissingFields
from tests.api_client import TestAPIClient


class TestSalesforceCaseRecord(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.test_data = {
            "case_number": "123456789",
            "s_id": "ABC_123_XYZ",
            "Subject": "Test Case",
            "Description": "This is a test case.",
            "Status": "New",
            "Priority": "High",
            "ContactId": "1234567890",
            "Reason": "Technical Issue",
            "issue__c": "a",
            "Issue_Description__c": "s",
            "Preventing_Student_Access__c": "No",
        }

        self._test_data = self._test_data | self.test_data

        case_urls = {
            "case_by_sfid": f'{self.url}/services/data/{self.version}/sobjects/Case/{self.test_data.get("s_id")}',
            "update_case": f'{self.url}/services/data/{self.version}/sobjects/Case/{self.test_data.get("s_id")}',
            "create_case": f"{self.url}/services/data/{self.version}/sobjects/Case/",
        }

        self.test_urls = case_urls | self._test_urls
        self.api_client.timeout = 15

    @patch("propus.salesforce.Salesforce.custom_query")
    def test_fetch_case_details_record_by_case_number(self, mock_custom_query):
        mock_custom_query.return_value = {"response": {"data": [self.test_data]}}
        result = self.salesforce.fetch_case_details_record_by_case_number(self.test_data["case_number"])
        self.assertEqual(result, {"response": {"data": [self.test_data]}})

    def test_fetch_case_record_by_sf_id(self):
        self.test_name = "case_by_sfid"
        self.success_response = {"response": {"data": self.test_data}}
        self.assertEqual(
            self.salesforce.fetch_case_record_by_sf_id(self.test_data.get("s_id")),
            self.success_response,
        )

    def test_update_case_record(self):
        self.test_name = "update_case"
        self.success_response = {"response": {"data": self.test_data}}
        self.assertIsNone(self.salesforce.update_case_record(self.test_data.get("s_id"), **self.test_data))

    def test_create_case_record(self):
        self.test_name = "create_case"
        self.success_response = {"response": {"data": self.test_data}}
        self.assertIsNotNone(self.salesforce.create_case_record("Welcome Services Case", **self.test_data))

    def test_create_case_errors(self):
        self.test_name = "create_case"
        with self.assertRaises(CreateCaseUnknownRecordType):
            self.salesforce.create_case_record("bad_record_type", **self.test_data)
        with self.assertRaises(CreateCaseMissingFields):
            self.salesforce.create_case_record(
                "Welcome Services Case", **{"issue__c": "a", "Issue_Description__c": "s"}
            )


if __name__ == "__main__":
    unittest.main()
