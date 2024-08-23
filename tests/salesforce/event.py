import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestSalesforceEvent(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.event_data = {
            "Subject": "THIS IS THE SUBJECT",
            "Description": "THIS IS THE TEST DESCRIPTION!",
            "OwnerId": "THIS IS ME!!!",
            "Type": "Event-Type",
            "WhoId": "ABC_67543_XYZ",
            "DurationInMinutes": 12346,
            "StartDateTime": "SOME_DATE IN THE FUTURE",
        }
        self._test_data = self._test_data | self.event_data
        self.test_urls = {"create_event": f"{self.url}/services/data/{self.version}/sobjects/Event/"} | self._test_urls
        self.api_client.timeout = 15

    def test_create_event(self):
        self.test_name = "create_event"
        self.success_response = {"status": "success"}

        self.assertEqual(
            self.salesforce.create_event(
                self.event_data.get("WhoId"),
                self.event_data.get("StartDateTime"),
                self.event_data.get("DurationInMinutes"),
                subject=self.event_data.get("Subject"),
                description=self.event_data.get("Description"),
                assignee_id=self.event_data.get("OwnerId"),
                type=self.event_data.get("Type"),
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
