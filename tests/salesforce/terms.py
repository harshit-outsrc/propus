from datetime import datetime
import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestSalesforceTerms(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.term_data = {
            "Name": "2023-24-TERM-07",
            "hed__Start_Date__c": "2023-08-15",
            "hed__End_Date__c": "2024-02-12",
            "hed__Account__c": self.salesforce._calbright_sf_account_id,
        }
        self._test_data = self._test_data | self.term_data

        self.test_urls = {
            "create_term": f"{self.url}/services/data/{self.version}/sobjects/hed__Term__c/",
            "fetch_all_terms": f"{self.url}/services/data/{self.version}/query/",
        }
        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 15

    def test_create_term(self):
        self.test_name = "create_term"
        self.success_response = {"status": "success"}
        self.assertEqual(
            self.salesforce.create_term(start_date=datetime.now().strptime("2023-08-15", "%Y-%m-%d")),
            self.success_response,
        )

    def test_fetch_terms(self):
        self.test_name = "fetch_all_terms"
        self.test_params[self.test_name] = {
            "q": "SELECT Id, Name, hed__Start_Date__c, hed__End_Date__c, Last_day_to_drop_without_a_W__c, Last_day_to_withdraw__c FROM hed__Term__c WHERE hed__Account__c ='0013k00002lAtFyAAK'"
        }
        self.success_response = {
            "totalSize": 3,
            "records": [
                {
                    "attributes": {
                        "type": "hed__Term__c",
                        "url": "/services/data/v56.0/sobjects/hed__Term__c/a0C3k00000UCaboEAD",
                    },
                    "Id": "a0C3k00000UCaboEAD",
                    "Name": "BAD_TERM",
                    "hed__Start_Date__c": "2020-07-21",
                    "hed__End_Date__c": "2021-01-18",
                    "Last_day_to_drop_without_a_W__c": "2020-08-20",
                    "Last_day_to_withdraw__c": "2020-10-27",
                },
                {
                    "attributes": {
                        "type": "hed__Term__c",
                        "url": "/services/data/v56.0/sobjects/hed__Term__c/a0C3k00000UCabuEAD",
                    },
                    "Id": "a0C3k00000UCabuEAD",
                    "Name": "2020-21-TERM-04",
                    "hed__Start_Date__c": "2020-07-28",
                    "hed__End_Date__c": "2021-01-25",
                    "Last_day_to_drop_without_a_W__c": "2020-08-27",
                    "Last_day_to_withdraw__c": "2020-11-03",
                },
                {
                    "attributes": {
                        "type": "hed__Term__c",
                        "url": "/services/data/v56.0/sobjects/hed__Term__c/a0C3k00000UCabvEAD",
                    },
                    "Id": "a0C3k00000UCabvEAD",
                    "Name": "2020-2021-TERM-05",
                    "hed__Start_Date__c": "2020-08-04",
                    "hed__End_Date__c": "2021-02-01",
                    "Last_day_to_drop_without_a_W__c": "2020-09-03",
                    "Last_day_to_withdraw__c": "2020-11-10",
                },
            ],
        }
        resp = self.salesforce.fetch_terms(False)
        self.assertEqual(len(resp), 2)
        self.assertIn("2020-21-TERM-04", [r.get("Name") for r in resp])
        self.assertIn("2020-2021-TERM-05", [r.get("Name") for r in resp])


if __name__ == "__main__":
    unittest.main()
