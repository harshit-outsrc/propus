import unittest
from unittest.mock import MagicMock, Mock

from propus.hubspot.exceptions import EmailFailedToSend, ApiNotSuccessful
from tests.api_client import TestAPIClient
from tests.hubspot.base import BaseHubspotTest


class TestHubspotTransactionalEmails(BaseHubspotTest, TestAPIClient):
    def setUp(self) -> None:
        self.salesforce_task_data = {"test": "data", "this": "should_create_a_task"}
        self.task_created = False
        return super().setUp()

    def test_send_transactional_email(self):
        self.test_name = "send_transactional_email"
        salesforce = MagicMock()
        salesforce.create_task = Mock(side_effect=self.create_task)
        self.assertEqual(
            self.hubspot.send_transactional_email(
                email_id=self.test_data.get("emailId"),
                to_email=self.test_data.get("to"),
                from_email=self.test_data.get("from"),
                cc=self.test_data.get("cc"),
                bcc=self.test_data.get("bcc"),
                reply_to=self.test_data.get("reply_to"),
                reply_to_list=self.test_data.get("reply_to_list"),
                email_name=self.test_data.get("email_name"),
                contact_properties=self.test_data.get("contact_properties"),
                custom_properties=self.test_data.get("custom_properties"),
                salesforce_task={
                    "client": salesforce,
                    "task_data": self.salesforce_task_data,
                },
            ),
            self.test_data.get("status_id"),
        )
        self.assertTrue(self.task_created)

    def create_task(self, **kwargs):
        self.assertEqual(kwargs, self.salesforce_task_data)
        self.task_created = True

    def test_check_email_status(self):
        self.test_name = "status_id_check"
        self.assertEqual(
            self.hubspot.check_email_sent_status(self.test_data.get("status_id")),
            self.expected_response,
        )

    def test_transactional_errors(self):
        self.test_name = "send_email_error"
        with self.assertRaises(EmailFailedToSend):
            self.hubspot.send_transactional_email(None, None)

        self.test_name = "check_email_status_error"
        with self.assertRaises(ApiNotSuccessful):
            self.hubspot.check_email_sent_status(None)


if __name__ == "__main__":
    unittest.main()
