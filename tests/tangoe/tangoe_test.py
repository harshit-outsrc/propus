import unittest
from unittest.mock import MagicMock
from propus.tangoe.tangoe import TangoeMobile
from tests.api_client import TestAPIClient
from unittest.mock import MagicMock, Mock

class TangoeTest(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.application_key = "some_testing_jwt!"
        headers = {
            "API-Token": self.application_key
        }
        self.api_client = TangoeMobile(_base_url="", headers=headers)
        req_mock = MagicMock()
        req_mock.get = Mock(side_effect=self.get_request)
        req_mock.post = Mock(side_effect=self.post_request)
        self.api_client.request_service = req_mock
        self.test_urls = {
            "activity": f"{self.api_client.base_url}/activities",
            "people": f"{self.api_client.base_url}/people/find_one",
            "lines": f"{self.api_client.base_url}/lines",
            "devices": f"{self.api_client.base_url}/devices"
        }
    
    def get_request(self, url, headers=None, timeout=20, **kwargs):
        self.assertIsNotNone(headers)
        self.assertEqual(headers.get("API-Token"), f"{self.application_key}")
        response = self.fetch_response(url, headers)
        return response

    def fetch_response(self, url, headers):
        if "error" in self.test_name:
            response = MagicMock()
            response.status_code = 400
            response.text = self.error_message
            return response

        self.assertIsNotNone(headers)
        self.assertEqual(headers.get("API-Token"), f"{self.application_key}")
        expected_url = self.test_urls.get(self.test_name)
        response = MagicMock()
        response.status_code = 200
        response.json = Mock(return_value=self.success_response)
        response.content = str(self.success_response)
        return response

    def post_request(self, url, data=None, headers=None, timeout=20, **kwargs):
        self.assertIsNotNone(headers)
        self.assertEqual(headers.get("API-Token"), f"{self.application_key}")
        response = self.fetch_response(url, headers)
        return response

    def test_request_hotspot(self):

        self.test_name = "request_hotspot"
        self.test_params[self.test_name] = {
            "activity" : {
            "activity_type_id" : 45,
            "employee_id" : "0012349",
            "shipping_address_attributes" : {
                "address1" : "123 N Fake St.",
                "address2" : "Apt. 0",
                "city" : "Indianapolis",
                "zip" : "46220",
                "state" : "IN",
                "country_id" : 52123291,
                "ship_attention" : "Joe Smith"
            },
            "business_ref_device_id" : 243910,
            "comment" : "this is a comment",
            "remote_activity_id" : "the_remote_system_unique_id"
            }
            }
        self.assertEqual(self.api_client.request_hotspot(self.test_params[self.test_name]),self.success_response,)
    
    def test_request_chromebook(self):

        self.test_name = "request_chromebook"
        self.test_params[self.test_name] = {
            "activity" : {
            "activity_type_id" : 22,
            "employee_id" : "0012349",
            "shipping_address_attributes" : {
                "address1" : "123 N Fake St.",
                "address2" : "Apt. 0",
                "city" : "Indianapolis",
                "zip" : "46220",
                "state" : "IN",
                "country_id" : 52123291,
                "ship_attention" : "Joe Smith"
            },
            "business_ref_device_id" : 243910,
            "comment" : "this is a comment",
            "remote_activity_id" : "the_remote_system_unique_id"
            }
            }
        self.assertEqual(self.api_client.request_chromebook(self.test_params[self.test_name]),self.success_response,)

    
    def test_suspend_hotspot(self):

        self.test_name = "suspend_hotspot"
        self.test_params[self.test_name] = { 
        "activity" : {
        "activity_type_id" : 1,
        "line_id" : 7170057, 
        "employee_id" : "0012349",
        "comment" : "",
        "remote_activity_id" : "the_remote_system_unique_id"
        }
        }
        self.assertEqual(self.api_client.suspend_hotspot(self.test_params[self.test_name]),self.success_response,)
    
    def test_return_hotspot(self):

        self.test_name = "return_hotspot"
        self.test_params[self.test_name] = { "activity":
            { "activity_type_id": 46,
            "employee_id": "0012349",
            "shipping_address_attributes": {
                "address1": "123 N Fake St.",
                "address2": "Apt. 0",
                "city": "Indianapolis",
                "zip": "46220",
                "country_id": 52123291,
                "state": "IN",
                "ship_attention": "Joe Smith"
            },
            "comment": "",
            "return_imei": 1234567891234567,
            "return_generic_serial": "12345656",
            "return_tracking_number": "fkj234r24tv4v",
            "return_courier_id": 1,
            "remote_activity_id" : "the_remote_system_unique_id"
            }
        }
        self.assertEqual(self.api_client.return_hotspot(self.test_params[self.test_name]),self.success_response,)
    
    def test_return_chromebook(self):

        self.test_name = "return_chromebook"
        self.test_params[self.test_name] =  { "activity": { 
        "activity_type_id": 46,
        "employee_id": "0012349",
        "shipping_address_attributes": {
        "address1": "123 N Fake St.",
        "address2": "Apt. 0",
        "city": "Indianapolis",
        "zip": "46220",
        "country_id": 52123291,
        "state": "IN",
        "ship_attention": "Frank Smith"
    },
        "comment": "",
        "return_imei": 1231234325678901,
        "return_generic_serial": "",
        "return_tracking_number": "fkj234r24tv4v",
        "return_courier_id": 3,
        "remote_activity_id" : "the_remote_system_unique_id"
        }
        }
        self.assertEqual(self.api_client.return_chromebook(self.test_params[self.test_name]),self.success_response,)
    
    
    def test_hotspot_stolen(self):

        self.test_name = "hotspot_stolen"
        self.test_params[self.test_name] = {
        "activity" : {
        "activity_type_id" : 1,
        "employee_id": "0012349",
        "line_id" : 7170057,
        "comment" : "",
        "sleep_until" : "2025-11-16",
        "remote_activity_id" : "the_remote_system_unique_id"
        }
        }
        self.assertEqual(self.api_client.hotspot_stolen(self.test_params[self.test_name]),self.success_response,)

    def test_get_user(self):

        self.test_name = "get_user"
        user_id = "0012345"
        self.assertEqual(self.api_client.get_user(user_id),self.success_response,)
        
    def test_get_lines(self):

        self.test_name = "get_lines"
        user_id = "0012349"
        self.assertEqual(self.api_client.get_lines(user_id),self.success_response,)
        
    def test_get_devices(self):

        self.test_name = "get_devices"
        user_id = "0012345"
        self.assertEqual(self.api_client.get_devices(user_id),self.success_response,)
    
if __name__ == "__main__":
    import unittest
    unittest.main()
