from propus.panda_doc import PandaDoc
from tests.api_client import TestAPIClient


class TestPandaDoc(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        # API client setup for test class
        self.api_client = PandaDoc(authorization=self.application_key, base_url=self.url)
        self.api_client.request_service = self._req_mock
        # Test data
        self.count = self.status = 3
        self.doc_id = self.template_id = "123"
        self.cf_date = "2018-06-01"
        self.email = "you@me.com"
        self.recipient = "john@doe.com"
        self.test_urls = {
            "get_docs_list": f"{self.url}/public/v1/documents?count={self.count}&status=2&status={self.status}&template_id={self.template_id}&created_from={self.cf_date}&completed_from={self.cf_date}",  # noqa: E501
            "get_doc_details": f"{self.url}/public/v1/documents/{self.doc_id}/details",
            "create_doc": f"{self.url}/public/v1/documents",
            "send_doc": f"{self.url}/public/v1/documents/{self.doc_id}/send",
        }

    def test_create_document(self):
        self.test_name = "create_doc"
        self._test_data = {
            "template_uuid": self.template_id,
            "name": self.email,
            "recipients": [{"email": self.recipient, "first_name": "foo", "last_name": "bar", "role": "Student"}],
            "tokens": [{}],
        }
        self.test_params[self.test_name] = {}
        response = self.api_client.create_document_from_template(
            **{
                "template_id": self.template_id,
                "email_name": self.email,
                "recipient_first_name": "foo",
                "recipient_last_name": "bar",
                "recipient_email": self.recipient,
                "tokens": [{}],
                "fields": [{"Field1": {"value": True}}, {"Field2": {"value": "something"}}],
            }
        )
        self.assertEqual(response, self.success_response)

    def test_fetch_document_details(self):
        self.test_name = "get_doc_details"
        response = self.api_client.fetch_document_details(doc_id=self.doc_id)
        self.assertEqual(response, self.success_response)

    def test_list_documents(self):
        self.test_name = "get_docs_list"
        response = self.api_client.list_documents(
            **{
                "status": self.status,
                "created_from": self.cf_date,
                "completed_from": self.cf_date,
                "template_id": self.template_id,
                "count": self.count,
            }
        )
        self.assertEqual(response, self.success_response)

    def test_send_document(self):
        self.test_name = "send_doc"
        self._test_data = {
            "subject": "foo",
            "message": "bar",
            "silent": False,
            "forwarding_settings": {"forwarding_allowed": True, "forwarding_with_reassigning_allowed": True},
        }
        response = self.api_client.send_document(doc_id=self.doc_id, subject="foo", message="bar")
        self.assertEqual(response, self.success_response)


if __name__ == "__main__":
    import unittest

    unittest.main()
