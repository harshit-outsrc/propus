import json
from propus.logging_utility import Logging
from propus.api_client import RestAPIClient


class TangoeMobile(RestAPIClient):

    def __init__(self, _base_url, headers):
        super().__init__(base_url=_base_url, additional_headers=headers)
        self.logger = Logging.get_logger("propus/tangoe/tangoe")
        self.endpoints = {
            "activity": "/activities",
            "lines": "/lines",
            "people": "/people/find_one",
            "devices": "/devices"
        }

    @staticmethod
    def build(config: dict):
        access_token = config.get("api_token")
        _base_url = config.get("base_url")
        headers = {
            "API-Token": access_token
        }
        return TangoeMobile(_base_url, headers)

    def request_hotspot(self, data):
        """
        Request a hotspot device through the API.

        Activity Name: Pick Device
        Activity Type ID: 45

        Args:
            data (dict): The data dictionary containing the activity details.
                Expected structure:
                {
                    "activity": {
                        "employee_id": str,
                        "shipping_address_attributes": {
                            "address1": str,
                            "address2": str,
                            "city": str,
                            "zip": str,
                            "state": str,
                            "country_id": int,
                            "ship_attention": str
                        },
                        "business_ref_device_id": int,
                        "comment": str,
                        "remote_activity_id": str
                    }
                }

            Returns:
            The response from the API after making the request.

            Raises:
            ValueError: If the expected values are not being passed.
        """

        required_fields = ["activity_type_id", "employee_id", "shipping_address_attributes", "business_ref_device_id"]
        shipping_address_fields = ["address1", "address2", "city", "zip", "state", "country_id", "ship_attention"]

        activity = data.get("activity", {})
        for field in required_fields:
            if field not in activity:
                raise ValueError(f"Missing field: {field}")

        shipping_address = activity.get("shipping_address_attributes", {})
        for field in shipping_address_fields:
            if field not in shipping_address:
                raise ValueError(f"Missing shipping address field: {field}")

        url = self._get_endpoint("activity")

        return self._make_request(url, req_type="post", data=json.dumps(data))

    def request_chromebook(self, data):
        """
        Request a Chromebook device through the API.

        Activity Name: Device Purchase
        Activity Type ID: 22

        Args:
            data (dict): The data dictionary containing the activity details.
                Expected structure:
                {
                    "activity": {
                        "employee_id": str,
                        "shipping_address_attributes": {
                            "address1": str,
                            "address2": str,
                            "city": str,
                            "zip": str,
                            "state": str,
                            "country_id": int,
                            "ship_attention": str
                        },
                        "business_ref_device_id": int,
                        "comment": str,
                        "remote_activity_id": str
                    }
                }

        Returns:
            The response from the API after making the request.

        Raises:
            ValueError: If the expected values are not being passed.
        """
        url = self._get_endpoint("activity")
        activity = data.get("activity", {})

        required_fields = [
            "employee_id",
            "shipping_address_attributes",
            "business_ref_device_id"
        ]

        for field in required_fields:
            if field not in activity or (isinstance(activity.get(field), str) and not activity.get(field).strip()):
                raise ValueError(f"Missing required field in activity data: {field}")

        shipping_address_attributes = activity.get("shipping_address_attributes", {})
        shipping_required_fields = [
            "address1",
            "city",
            "zip",
            "state",
            "country_id"
        ]

        for field in shipping_required_fields:
            if (field not in shipping_address_attributes or
                (isinstance(shipping_address_attributes.get(field), str) and
                    not shipping_address_attributes.get(field).strip())):
                raise ValueError(f"Missing required field in shipping address: {field}")

        return self._make_request(url, req_type="post", data=json.dumps(data))

    def suspend_hotspot(self, data):
        """
        Suspend a hotspot device through the API.

        Activity Name: Suspend
        Activity Type ID: 1

        Args:
            data (dict): The data dictionary containing the activity details.
                Expected structure:
                {
                    "activity": {
                        "line_id": int,
                        "employee_id": str,
                        "comment": str,
                        "remote_activity_id": str
                    }
                }

        Returns:
            The response from the API after making the request.

        Raises:
        ValueError: If the activity data is empty or if any expected values are missing.
        """
        url = self._get_endpoint("activity")
        activity = data.get("activity", {})

        required_fields = ["line_id", "employee_id"]
        for field in required_fields:
            if field not in activity:
                raise ValueError(f"Missing required field in activity data: {field}")
        return self._make_request(url, req_type="post", data=json.dumps(data))

    def return_hotspot(self, data):
        """
        Return a hotspot device through the API.

        Activity Name: Device Return
        Activity Type ID: 46

        Args:
            data (dict): The data dictionary containing the activity details.
                Expected structure:
                {
                    "activity": {
                        "employee_id": str,
                        "shipping_address_attributes": {
                            "address1": str,
                            "address2": str,
                            "city": str,
                            "zip": str,
                            "state": str,
                            "country_id": int,
                            "ship_attention": str
                        },
                        "comment": str,
                        "return_imei": int,
                        "return_generic_serial": str,
                        "return_tracking_number": str,
                        "return_courier_id": int,
                        "remote_activity_id": str
                    }
                }

        Returns:
            The response from the API after making the request.
        Raises:
        ValueError: If the activity data is empty or if any expected values are missing.
        """
        url = self._get_endpoint("activity")
        activity = data.get("activity", {})

        required_fields = [
            "employee_id",
            "shipping_address_attributes",
            "return_imei",
            "return_tracking_number",
            "return_courier_id",
            "activity_type_id",
        ]

        for field in required_fields:
            if field not in activity or (isinstance(activity[field], str) and not activity[field].strip()):
                raise ValueError(f"Missing required field in activity data: {field}")
        return self._make_request(url, req_type="post", data=json.dumps(data))

    def return_chromebook(self, data):
        """
        Return a Chromebook device through the API.

        Activity Name: Device Return
        Activity Type ID: 46

        Args:
            data (dict): The data dictionary containing the activity details.
                Expected structure:
                {
                    "activity": {
                        "employee_id": str,
                        "shipping_address_attributes": {
                            "address1": str,
                            "address2": str,
                            "city": str,
                            "zip": str,
                            "state": str,
                            "country_id": int,
                            "ship_attention": str
                        },
                        "comment": str,
                        "return_imei": int,
                        "return_generic_serial": str,
                        "return_tracking_number": str,
                        "return_courier_id": int,
                        "remote_activity_id": str
                    }
                }

        Returns:
            The response from the API after making the request.

        Raises:
        ValueError: If the activity data is empty or if any expected values are missing.
        """
        url = self._get_endpoint("activity")
        activity = data.get("activity", {})

        required_fields = [
            "employee_id",
            "shipping_address_attributes",
            "return_imei",
            "return_tracking_number",
            "return_courier_id",
            "activity_type_id",
        ]

        for field in required_fields:
            if field not in activity or (isinstance(activity[field], str) and not activity[field].strip()):
                raise ValueError(f"Missing required field in activity data: {field}")
        return self._make_request(url, req_type="post", data=json.dumps(data))

    def hotspot_stolen(self, data):
        """
        Report a stolen hotspot device by cancelling the line.

        Activity Name: Line Cancel
        Activity Type ID: 1
        Next step will be to request a new hotspot.

        Args:
            data (dict): The data dictionary containing the activity details.
                Expected structure:
                {
                    "activity": {
                        "employee_id": str,
                        "line_id": int,
                        "comment": str,
                        "sleep_until": str,
                        "remote_activity_id": str
                    }
                }

        Returns:
            The response from the API after making the request.

        Note:
            For reporting a stolen Chromebook, call the request_chromebook method.
        Raises:
            ValueError: If the activity data is empty or if any expected values are missing.
        """

        url = self._get_endpoint("activity")
        activity = data.get("activity", {})

        required_fields = [
            "employee_id",
            "line_id",
            "sleep_until",
            "remote_activity_id"
        ]

        for field in required_fields:
            if field not in activity or (isinstance(activity[field], str) and not activity[field].strip()):
                raise ValueError(f"Missing required field in activity data: {field}")

        payload = {
            "activity_type_id": 1,
            "employee_id": activity.get("employee_id"),
            "line_id": activity.get("line_id"),
            "comment": activity.get("comment"),
            "sleep_until": activity.get("sleep_until"),
            "remote_activity_id": activity.get("remote_activity_id")
        }
        return self._make_request(url, req_type="post", data=json.dumps(payload))

    def get_user(self, user_id):
        """
        Fetch a User

        Args:
            user_id (str): The user's employee ID.

        Returns:
            The response from the API after making the request.

        Raises:
            ValueError: If user_id is not provided or is empty.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("Invalid user_id provided. It should be a non-empty string.")

        url = f"{self._get_endpoint('people')}?employee_id={user_id}"
        return self._make_request(url, req_type="get")

    def get_lines(self, user_id):
        """
        Fetch a Line

        Args:
            user_id (str): The user's employee ID.

        Returns:
            The response from the API after making the request.

        Raises:
            ValueError: If user_id is not provided or is empty.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("Invalid user_id provided. It should be a non-empty string.")

        url = f"{self._get_endpoint('lines')}?employee_id={user_id}"
        return self._make_request(url, req_type="get")

    def get_devices(self, user_id):
        """
        Fetch Devices

        Args:
            user_id (str): The user's employee ID.

        Returns:
            The response from the API after making the request.

        Raises:
            ValueError: If user_id is not provided or is empty.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("Invalid user_id provided. It should be a non-empty string.")

        url = f"{self._get_endpoint('devices')}?employee_id={user_id}"
        return self._make_request(url, req_type="get")
