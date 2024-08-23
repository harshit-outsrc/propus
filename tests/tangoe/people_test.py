from propus.tangoe.people import TangoePeople
from tests.api_client import TestAPIClient
from unittest.mock import MagicMock, Mock


class TangoePeopleTest(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.application_key = "some_testing_jwt!"
        self.api_client = TangoePeople(access_token=f"Bearer {self.application_key}", _base_url="", grant_type="", username="", password="", token_username="", token_password="")
        req_mock = MagicMock()
        req_mock.put = Mock(side_effect=self.put_request)
        req_mock.post = Mock(side_effect=self.post_request)
        self.api_client.request_service = req_mock
        self.test_urls = {
            "activity": f"{self.api_client._base_url}/people"
        }
 
    def get_request(self, url, headers=None, timeout=20, **kwargs):
        self.assertEqual(timeout, 20)
        return self.fetch_response(url, headers)

    def fetch_response(self, url, headers):
        if "error" in self.test_name:
            response = MagicMock()
            response.status_code = 400
            response.text = self.error_message
            return response

        self.assertIsNotNone(headers)
        self.assertEqual(headers.get("Authorization"), f"Bearer {self.application_key}")
        expected_url = self.test_urls.get(self.test_name)
        response = MagicMock()
        response.status_code = 200
        response.json = Mock(return_value=self.success_response)
        response.content = str(self.success_response)
        return response

    def post_request(self, url, data=None, headers=None, timeout=20, **kwargs):
        self.assertIsNotNone(headers)
        self.assertEqual(headers.get("Authorization"), f"Bearer {self.application_key}")
        response = self.fetch_response(url, headers)
        return response
    
    def put_request(self, url, data=None, headers=None, timeout=20, **kwargs):
        self.assertIsNotNone(headers)
        self.assertEqual(headers.get("Authorization"), f"Bearer {self.application_key}")
        response = self.fetch_response(url, headers)
        return response
        
    def test_create_user(self):
        self.test_name = "create_user"
        self.test_params[self.test_name] ={ 
        "person":{
            "email":"frank.smith@calbrightcollege.com",
            "employee_id":"0012349",
            "group_id":6847,
            "name_first":"Frank",
            "name_last":"Smith",
            "country_ids":[52123291],
            "new_base_country_membership_country_id":52123291,
            "shipping_address_attributes": {
            "address1":"123 Main St.",
            "address2":"",
            "city":"Yourtown",
            "country_id":52123291,
            "ship_attention":"Frank Smith",
            "state":"IN",
            "zip":"46278" 
        }
        }
        }
        self.assertEqual(self.api_client.create_user(self.test_params[self.test_name]),self.success_response,)

    def test_remove_user(self):
        self.test_name = "remove_user"
        self.test_params[self.test_name] ={ 
        "person":
            {
                "active":"false"
                }
            }
        self.user_id = '33163340'
        self.assertEqual(self.api_client.remove_user(self.user_id),self.success_response,)

if __name__ == "__main__":
    import unittest
    unittest.main()

