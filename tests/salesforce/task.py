import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestSalesforceTask(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.event_data = {
            "Subject": "THIS IS THE SUBJECT",
            "Description": "THIS IS THE TEST DESCRIPTION!",
            "OwnerId": "THIS IS ME!!!",
            "Status": "Event-status",
            "WhoId": "ABC_67543_XYZ",
            "ActivityDate": "TODAY!!",
        }
        self._test_data = self._test_data | self.event_data
        self.test_urls = {"create_task": f"{self.url}/services/data/{self.version}/sobjects/Task/"} | self._test_urls
        self.api_client.timeout = 15

    def test_create_task(self):
        self.test_name = "create_task"
        self.success_response = {"status": "success"}

        self.assertEqual(
            self.salesforce.create_task(
                self.event_data.get("WhoId"),
                activity_date=self.event_data.get("ActivityDate"),
                subject=self.event_data.get("Subject"),
                description=self.event_data.get("Description"),
                owner_id=self.event_data.get("OwnerId"),
                type=self.event_data.get("Type"),
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
