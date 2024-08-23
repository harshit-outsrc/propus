import unittest

from propus.salesforce import Salesforce
from propus.salesforce.exceptions import CreateContactUnknownRecordType, CreateContactMissingFields
from tests.api_client import TestAPIClient


class TestSalesforceContactRecord(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.test_data = {
            "ccc_id": "123687683712",
            "s_id": "ABC_123_XYZ",
            "FirstName": "XYZ_56723_ABG",
            "LastName": "BLAH_UNDER_BLAH",
            "Email": "you@me.com",
            "cfg_Learner_Status__c": "Expressed Interest",
            "Phone": "ABV123903",
        }

        self._test_data = self._test_data | self.test_data

        contact_urls = {
            "contact_by_sfid": f'{self.url}/services/data/{self.version}/sobjects/Contact/{self.test_data.get("s_id")}',
            "update_contact": f'{self.url}/services/data/{self.version}/sobjects/Contact/{self.test_data.get("s_id")}',
            "create_contact": f"{self.url}/services/data/{self.version}/sobjects/Contact/",
        }

        self.test_urls = contact_urls | self._test_urls
        self.api_client.timeout = 15

    def test_fetch_vet_record_by_sf_id(self):
        self.test_name = "contact_by_sfid"
        self.success_response = {"response": {"data": self.test_data}}
        self.assertEqual(
            self.salesforce.fetch_contact_record_by_sf_id(self.test_data.get("s_id")),
            self.success_response,
        )

    def test_update_contact_record(self):
        self.test_name = "update_contact"
        self.success_response = {"response": {"data": self.test_data}}
        self.assertIsNone(self.salesforce.update_contact_record(self.test_data.get("s_id"), **self.test_data))

    def test_create_contact_record(self):
        self.test_name = "create_contact"
        self.success_response = {"response": {"data": self.test_data}}
        self.assertIsNotNone(self.salesforce.create_contact_record("learner", **self.test_data))

    def test_create_contact_errors(self):
        self.test_name = "create_contact"
        with self.assertRaises(CreateContactUnknownRecordType):
            self.salesforce.create_contact_record("bad_record_type", **self.test_data)
        with self.assertRaises(CreateContactMissingFields):
            self.salesforce.create_contact_record("learner", Email="Hello", LastName="Test", FirstName="Test")


if __name__ == "__main__":
    unittest.main()
