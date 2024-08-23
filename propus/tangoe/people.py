import base64
import json

from propus.api_client import RestAPIClient
from propus.logging_utility import Logging


class TangoePeople(RestAPIClient):

    def __init__(self, access_token, _base_url, grant_type, username, password, token_username, token_password):
        self._base_url = _base_url
        self.GRANT_TYPE = grant_type
        self.USERNAME = username
        self.PASSWORD = password
        self.token_username = token_username
        self.token_password = token_password
        self.access_token = access_token
        super().__init__(authorization=access_token, base_url=self._base_url)
        self.logger = Logging.get_logger("propus/tangoe/people")
        self.endpoints = {
            "people": "/people",
            "token": "/authentication/token"
        }

    @staticmethod
    def build(config: dict):
        access_token = config.get("access_token")
        _base_url = config.get("people_base_url")
        grant_type = config.get("GRANT_TYPE")
        username = config.get("USERNAME")
        password = config.get("PASSWORD")
        token_username = config.get("token_username")
        token_password = config.get("token_password")
        return TangoePeople(access_token, _base_url, grant_type, username, password, token_username, token_password)

    def generate_token(self):
        """
        Genrate new token:
        To create or remove user, we have to generate the token. To generate a token we would need create
        a bearer token using the credentials that tangoe has provided.

        """
        url = (
            self._get_endpoint("token") +
            f"?grant_type={self.GRANT_TYPE}&username={self.USERNAME}&password={self.PASSWORD}"
        )
        username = self.token_username
        password = self.token_password
        credentials = f'{username}:{password}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': "application/json"
        }

        response = self._make_request(url, req_type="post", headers=headers)
        self.access_token = response.get("access_token")
        return response

    def create_user(self, data):
        """
        Create a new user through the API.

        Args:
            data (dict): The data dictionary containing the user details.
                Expected structure:
                {
                    "person": {
                        "email": str,
                        "employee_id": str,
                        "group_id": int,
                        "name_first": str,
                        "name_last": str,
                        "country_ids": list of int,
                        "shipping_address_attributes": {
                            "address1": str,
                            "address2": str,
                            "city": str,
                            "state": str,
                            "zip": str,
                            "country_id": int,
                            "ship_attention": str
                        }
                    }
                }

        Returns:
            The response from the API after making the request.
        """
        person = data.get("person", {})

        # Validate required fields
        required_person_fields = [
            "email",
            "employee_id",
            "group_id",
            "name_first",
            "name_last",
            "new_base_country_membership_country_id"
        ]
        for field in required_person_fields:
            if field not in person or (isinstance(person[field], str) and not person[field].strip()):
                raise ValueError(f"Missing required field in person data: {field}")

        shipping_address_attributes = person.get("shipping_address_attributes", {})
        required_address_fields = ["address1", "city", "state", "zip", "country_id"]
        for field in required_address_fields:
            value = shipping_address_attributes.get(field)
            if field not in shipping_address_attributes or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"Missing required field in shipping address: {field}")
        headers = {
            'Authorization': self.access_token,
            'Content-Type': "application/json"
        }
        url = self._get_endpoint("people")
        return self._make_request(url, req_type="post", data=json.dumps(data), headers=headers)

    def remove_user(self, user_id):
        """
        Deactivate a user through the API.

        Args:
            user_id (str): The ID of the user to deactivate.

        Returns:
            The response from the API after making the request.

        Raises:
            ValueError: If the user_id is missing or invalid.
        """
        if not user_id or not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("Invalid user_id")
        headers = {
            'Authorization': self.access_token,
            'Content-Type': "application/json"
        }
        payload = {
            "person":
                {
                    "active": "false"
                }
        }
        url = self._get_endpoint("people") + f"/{user_id}"
        return self._make_request(url, req_type="put", data=json.dumps(payload), headers=headers)
