import json
import unittest
from unittest.mock import MagicMock, Mock

from propus.hubspot import Hubspot


class BaseHubspotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.application_key = "some_testing_jwt!"
        self.hubspot = Hubspot(api_key=self.application_key)
        req_mock = MagicMock()
        req_mock.get = Mock(side_effect=self.get_request)
        req_mock.post = Mock(side_effect=self.post_request)
        self.hubspot.request_service = req_mock
        self.test_name = None
        self.error_message = "this is the error message"

        self.test_data = {
            "emailId": 123456789,
            "to": "you@me.com",
            "from": "from@calbright.org",
            "cc": "cc_me@calbright.com",
            "bcc": "do_not_see@cal.com",
            "reply_to": "reply to me",
            "reply_to_list": "reply to all of these",
            "email_name": "emails name recorded in hubspot",
            "contact_properties": {
                "testProp1": "something1",
                "testProp2": "something2",
            },
            "custom_properties": {"testProp2": "all our custom properties"},
            "status_id": "calbrightStatusID12345",
        }

        self.expected_response = {
            "statusId": self.test_data.get("status_id"),
            "payload": {"data": "successful call"},
        }

        self._url_mapping = {
            "send_transactional_email": "https://api.hubapi.com/marketing/v3/transactional/single-email/send",
            "status_id_check": "https://api.hubapi.com/marketing/v3/email/send-statuses/calbrightStatusID12345",
        }

        self.expected_data = {
            "send_transactional_email": {
                "emailId": 123456789,
                "message": {
                    "to": "you@me.com",
                    "from": "from@calbright.org",
                    "cc": "cc_me@calbright.com",
                    "bcc": "do_not_see@cal.com",
                    "replyTo": "reply to me",
                    "replyToList": "reply to all of these",
                },
                "contactProperties": {
                    "testProp1": "something1",
                    "testProp2": "something2",
                    "last_system_email_sent": "emails name recorded in hubspot",
                },
                "customProperties": {"testProp2": "all our custom properties"},
            }  # noqa: E501
        }

    def get_request(self, url, headers, timeout):
        self.assertEqual(timeout, 20)
        return self.fetch_response(url, headers)

    def fetch_response(self, url, headers):
        if "error" in self.test_name:
            response = MagicMock()
            response.status_code = 400
            response.text = self.error_message
            return response

        self.assertEqual(headers.get("Authorization"), f"Bearer {self.application_key}")
        expected_url = self._url_mapping.get(self.test_name)
        expected_resp = self.expected_response
        self.assertEqual(url, expected_url)
        response = MagicMock()
        response.status_code = 200
        response.json = Mock(side_effect=lambda: expected_resp)
        return response

    def post_request(self, url, data, headers, timeout):
        self.assertEqual(timeout, 20)
        response = self.fetch_response(url, headers)
        if self.expected_data.get(self.test_name):
            json_data = json.loads(data)
            self.assertEqual(json_data, self.expected_data.get(self.test_name))
        return response
