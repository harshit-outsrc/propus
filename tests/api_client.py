import json
import unittest
from unittest.mock import MagicMock, Mock

from propus.api_client import RestAPIClient
from propus.api_client import (
    DEFAULT_CLIENT_TIMEOUT,
    FailedRequest,
    MissingElement,
    TooManyRequests,
    UndefinedEndpoint,
)


class TestAPIClient(unittest.TestCase):
    """
    Parent class for REST API Client Tests.

    Basic use:
        Create a sub-class of the TestAPIClient, and instantiate with
        the corresponding RestAPIClient sub-class to be tested.

        Several functional and error tests are present based on the
        parent RestAPIClient class. Additional tests should be added for
        API client specific methods.

        There are also built-in methods for make_request() to provide
        mock responses to API call requests, and check_data() for
        performing checks on data passed to / from the API client.

    Instantiation:
        from .api_client import TestAPIClient
        from propus.api_client import NewAPIClient

        class NewTestClient(TestAPIClient):
            def setUp(self) -> None:
                super().setUp()
                # API client setup for test class
                self.api_client = NewAPIClient(
                    authorization=self.application_key, base_url=self.url
                )
                self.api_client.request_service = self._req_mock
                self.timeout = <api_client_specific_setting>
                # Test data
                self.foo_bar = {"bar": "baz"}
                self.p1 = "1"
                self.endpoints = {"an": "/endpoint", "another": ("/end/<p1>/point", ["<p1>"])}
                self.test_urls = {"test_1": f"{self.url}/endpoint", "test_2": f"{self.url}/end/1/point/"}
                # Consolidate test data, endpoints, urls from parent and child classes
                self._test_data = self.foo_bar | self._test_data
                self.api_client.endpoints = self.api_client.endpoints | self.endpoints | self._endpoints
                self.test_urls = self.test_urls | self._test_urls

            def a_new_test(self):
                url = self.api_client._get_endpoint("foo")
                response = self.api_client._make_request(url)
                self.assertTrue(response, self.success_response)
    """

    def setUp(self) -> None:
        # Setup for TestAPIClient as parent class
        self.timeout = DEFAULT_CLIENT_TIMEOUT
        req_mock = MagicMock()
        req_mock.delete = Mock(side_effect=self.make_request)
        req_mock.get = Mock(side_effect=self.make_request)
        req_mock.head = Mock(side_effect=self.make_request)
        req_mock.options = Mock(side_effect=self.make_request)
        req_mock.patch = Mock(side_effect=self.make_request)
        req_mock.post = Mock(side_effect=self.make_request)
        req_mock.put = Mock(side_effect=self.make_request)
        self._req_mock = req_mock
        self.url = "https://some_test_url.api.com"
        self.application_key = "Authorization some_testing_jwt!"
        # API client specifics for test class
        self.api_client = RestAPIClient(authorization=self.application_key, base_url=self.url)
        self.api_client.request_service = self._req_mock
        # Test data
        self.expected_headers = {
            "accept": "application/json",
            "Authorization": "Authorization some_testing_jwt!",
        }
        self.test_name = None
        self.success_response = {"test": "success"}
        self.bulk_response = {"data": [self.success_response], "next_page_token": None}
        self.bulk_success_response = [self.success_response]
        self.success_headers = {"headers": "exist"}
        self.response_text = ""
        self._test_data = {"foo": "bar", "bar": "baz"}
        self._required_parameters = {"<bar>": "baz"}
        self._bulk_endpoints = {
            "tata": "/v1/tata",
            "titi": ("/v1/tata/titi/<toto>", ["<toto>"]),
        }
        self._endpoints = {
            "_foo": "/v1/foo",
            "_bar": ("/v1/foo/<bar>", ["<bar>"]),
            "_baz": ("/v1/foo/<baz>", ["<baz>"]),
        } | self._bulk_endpoints
        self._test_urls = {
            "test_delete": f"{self.url}/v1/foo",
            "test_get": f"{self.url}/v1/foo",
            "test_get_required_parameters": f"{self.url}/v1/foo/baz",
            "test_get_data_by_endpoint": f"{self.url}/v1/foo",
            "test_get_bulk_data_by_endpoint": f"{self.url}/v1/tata",
            "test_head": f"{self.url}/v1/foo",
            "test_options": f"{self.url}",
            "test_patch": f"{self.url}/v1/foo",
            "test_post": f"{self.url}/v1/foo",
            "test_put": f"{self.url}/v1/foo",
        }

        self.test_params = {}
        self.json_response = True

        # Consolidate test data, endpoints, urls from parent and child classes
        self.test_data = {} | self._test_data
        self.api_client.bulk_endpoints = self.api_client.bulk_endpoints | self._bulk_endpoints
        self.api_client.endpoints = self.api_client.endpoints | self._endpoints | self.api_client.bulk_endpoints
        self.test_urls = {} | self._test_urls

    def check_data(self, data, expected_dict=None):
        expected_dict = expected_dict if expected_dict else self._test_data
        for key, value in data.items():
            if isinstance(data.get(key), list):
                for item in data.get(key):
                    self.assertIn(item, expected_dict.get(key))
            elif isinstance(data.get(key), dict):
                if expected_dict.get(key):
                    self.check_data(value, expected_dict.get(key))
            elif expected_dict.get(key):
                self.assertEqual(value, expected_dict.get(key))

    def make_request(self, url, data=None, headers=None, params=None, timeout=None, req_type="get"):
        req_time = timeout if timeout else self.timeout
        req_headers = headers if headers else self.api_client.headers.get(req_type)
        self.assertEqual(req_time, self.api_client.timeout)

        status_code = 200
        text = self.response_text
        if self.test_name == "too_many_requests":
            status_code = 429
            text = "too many requests"
        elif self.test_name == "failed_request":
            status_code = 400
            text = "bad api request!"
        elif self.test_name == "missing_element":
            status_code = 404
            text = "<bar>"
        elif self.test_name == "method_not_implemented":
            status_code = 418
            text = "API client request method (foo) not implemented"
        elif self.test_name == "undefined_endpoint":
            status_code = 405
            text = "_baz"
        else:
            self.assertEqual(url, self.test_urls.get(self.test_name))

        expected_headers = self.api_client.default_headers | {}

        if data is not None:
            expected_headers["Content-Type"] = "application/json"
            try:
                self.check_data(json.loads(data))
            except:
                pass

        if params and self.test_params.get(self.test_name):
            self.assertEqual(params, self.test_params.get(self.test_name))
        self.assertEqual(req_headers, expected_headers)

        response = MagicMock()
        response.headers = self.success_headers
        response.status_code = status_code
        response.text = text
        response.json = Mock(side_effect=lambda: self.success_response)
        if self.test_name == "test_get_bulk_data_by_endpoint":
            response.json = Mock(side_effect=lambda: self.bulk_response)
        if not self.json_response:
            response.json = Mock(side_effect=ValueError())
        response.content = str(self.success_response)

        if response.status_code == 400:
            raise FailedRequest(response.status_code, response.text)
        elif response.status_code == 429:
            raise TooManyRequests()
        elif response.status_code == 404:
            raise MissingElement(response.text)
        elif response.status_code == 405:
            raise FailedRequest(response.status_code, response.text)
        elif response.status_code == 418:
            raise FailedRequest(response.status_code, response.text)
        else:
            return response


class APIClientTests(TestAPIClient):
    def test_error_too_many_requests(self):
        self.test_name = "too_many_requests"
        error_occurred = False
        try:
            self.make_request(self.url)
        except TooManyRequests as err:
            error_occurred = True
            self.assertEqual(str(err), "API limit reached")
        self.assertTrue(error_occurred)

    def test_error_failed_request(self):
        self.test_name = "failed_request"
        error_occurred = False
        try:
            self.make_request(self.url)
        except FailedRequest as err:
            error_occurred = True
            self.assertEqual(str(err), "RequestFailed (status 400): bad api request!")
        self.assertTrue(error_occurred)

    def test_error_method_not_implemented(self):
        self.test_name = "method_not_implemented"
        error_occurred = False
        try:
            self.make_request(self.url, headers=self.api_client.default_headers, req_type="foo")
        except FailedRequest as err:
            error_occurred = True
            self.assertEqual(
                str(err),
                "RequestFailed (status 418): API client request method (foo) not implemented",
            )
        self.assertTrue(error_occurred)

    def test_error_undefined_endpoint(self):
        self.test_name = "undefined_endpoint"
        error_occurred = False
        try:
            self.api_client._get_endpoint("lorem")
        except UndefinedEndpoint as err:
            error_occurred = True
            self.assertEqual(str(err), "API client endpoint (lorem) is undefined or malformed")
        self.assertTrue(error_occurred)

    def test_error_missing_element(self):
        self.test_name = "missing_element"
        error_occurred = False
        try:
            url = self.api_client._get_endpoint("_baz", parameters=self._required_parameters)
            self.make_request(url)
        except MissingElement as err:
            error_occurred = True
            self.assertEqual(str(err), "API endpoint requires missing path element (<baz>)")
        self.assertTrue(error_occurred)

    def test_delete(self):
        self.test_name = "test_delete"
        url = self.api_client._get_endpoint("_foo")
        response = self.api_client._make_request(url, req_type="delete")
        self.assertEqual(response, self.success_response)

    def test_get(self):
        self.test_name = "test_get"
        url = self.api_client._get_endpoint("_foo")
        response = self.api_client._make_request(url)
        self.assertEqual(response, self.success_response)

    def test_get_data_by_endpoint(self):
        self.test_name = "test_get_data_by_endpoint"
        response = self.api_client.get_data_by_endpoint("_foo")
        self.assertEqual(response, self.success_response)

    def test_get_bulk_data_by_endpoint(self):
        self.test_name = "test_get_bulk_data_by_endpoint"
        response = self.api_client.get_bulk_data_by_endpoint("tata")
        self.assertEqual(response, self.bulk_success_response)

    def test_get_required_parameters(self):
        self.test_name = "test_get_required_parameters"
        url = self.api_client._get_endpoint("_bar", parameters=self._required_parameters)
        response = self.api_client._make_request(url)
        self.assertEqual(response, self.success_response)

    def test_head(self):
        self.test_name = "test_head"
        url = self.api_client._get_endpoint("_foo")
        response = self.api_client._make_request(url, req_type="head")
        self.assertEqual(response, self.success_response)

    def test_options(self):
        self.test_name = "test_options"
        response = self.api_client._make_request(self.url, req_type="options")
        self.assertEqual(response, self.success_response)

    def test_patch(self):
        self.test_name = "test_patch"
        url = self.api_client._get_endpoint("_foo")
        response = self.api_client._make_request(url, req_type="patch", data=json.dumps(self.test_data))
        self.assertEqual(response, self.success_response)

    def test_post(self):
        self.test_name = "test_post"
        url = self.api_client._get_endpoint("_foo")
        response = self.api_client._make_request(url, req_type="post", data=json.dumps(self.test_data))
        self.assertEqual(response, self.success_response)

    def test_put(self):
        self.test_name = "test_put"
        url = self.api_client._get_endpoint("_foo")
        response = self.api_client._make_request(url, req_type="put", data=json.dumps(self.test_data))
        self.assertEqual(response, self.success_response)


if __name__ == "__main__":
    unittest.main()
