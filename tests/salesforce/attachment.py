import unittest
import base64

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestAttachment(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock
        self.test_urls = {
            "create_attachment": f"{self.url}/services/data/{self.version}/sobjects/Attachment",
            "fetch_attachment": f"{self.url}/services/data/{self.version}/sobjects/Attachment/1/Body",
        }

        self.api_client.timeout = 15

    def test_create_attachment(self):
        self.test_name = "create_attachment"
        self.success_response = {"status": "success"}
        self.assertEqual(
            self.salesforce.create_attachment(
                extension="pdf",
                parent_id="id",
                file_name="file_name",
                base64_encoded_file=str(base64.b64encode(bytes("content", "utf-8"))),
            ),
            self.success_response,
        )

    def test_fetch_attachment(self):
        self.test_name = "fetch_attachment"
        self.success_response = {"status": "success"}
        self.assertEqual(self.salesforce.fetch_attachment(1), self.success_response)


if __name__ == "__main__":
    unittest.main()
