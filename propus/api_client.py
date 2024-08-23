import requests
from typing import AnyStr, Dict, Union

DEFAULT_CLIENT_TIMEOUT = 10
DEFAULT_REQUEST_SERVICE = requests


class FailedRequest(Exception):
    """Exception raised for failed API request

    Attributes:
       status_code: status code from API request
       reason: API request failure message
    """

    def __init__(self, status_code, reason):
        super().__init__(f"RequestFailed (status {status_code}): {reason}")


class MissingElement(Exception):
    """Exception raised when a required path element is missing

    Attributes:
       key: name of the missing path element
    """

    def __init__(self, key):
        super().__init__(f"API endpoint requires missing path element ({key})")


class TooManyRequests(Exception):
    """Exception raised when API limit has been reached"""

    def __init__(self):
        super().__init__("API limit reached")


class UndefinedEndpoint(Exception):
    """Exception raised when calling for an undefined endpoint

    Attributes:
       endpoint: name of the endpoint requested
    """

    def __init__(self, endpoint):
        super().__init__(f"API client endpoint ({endpoint}) is undefined or malformed")


class UnsupportedBulkEndpoint(Exception):
    """Exception raised when calling for a bulk request on an endpoint where that is not supported.

    Attributes:
       endpoint: name of the endpoint requested
    """

    def __init__(self, endpoint):
        super().__init__(f"API client endpoint ({endpoint}) is not configured for a bulk get request")


class RestAPIClient:
    """
    Parent class for REST API Clients.

    Basic use:
        from propus.api_client import RestAPIClient

        api_client = RestAPIClient.build(authorization="foo", base_url="https://api.bar.com")
        url = api_client._get_endpoint(
            endpoint="endpoint_name",
            parameters={"anything": "required"},
        )
        response = api_client._make_request(url)

    Instantiation:
        RestAPIClient.build(
            authorization=<API_KEY_TOKEN_OR_SIMILAR>,
            base_url=<https://api.provider.com>
        )

        Note that sub-classes by default will use an authorization header,
        although they can also be easily modified for alternate approaches,
        such as providing a Bearer Token, or an API key as part of a query string.

    Sub-class __init__:
        When defining a sub-class call super().__init__() then define API endpoints:

        class NewAPIClient(RESTAPIClient):
            super().__init__(authorization=authorization, base_url=base_url)
            self.next_page_token = "next_page_token"
            self.pagination_fields = ["next_page_token", "page_count", "page_number", "page_size", "total_records"]
            self.bulk_endpoints = {
                "ex_1": "/v1/an/example",
            }
            self.endpoints = {
                "ex_2": (
                    "/v1/a/<required_parameter>/<rp_2>",
                    ["<required_parameter>", "<rp_2>"],
                ),
            } | self.bulk_endpoints

        where "ex_1" is the key (endpoint name) that will be called, and the value
        may be provided either as the path segment, such as "/v1/an/example",
        or as a tuple providing the path segment and a list of required parameters
        that build the path segment, such as, ("/v1/<rp_2>", ["<rp_2>"]).

        Other attributes of the API client may be optionally added or overwritten:
            self.foo = "bar"
            self.timeout = 30
    """

    def __init__(
        self,
        authorization: AnyStr = None,
        base_url: AnyStr = None,
        additional_headers: Dict = None,
    ):
        self.base_url = base_url
        self.request_service = DEFAULT_REQUEST_SERVICE
        self.default_headers = {"accept": "application/json"}
        if authorization:
            self.default_headers["Authorization"] = authorization
        if additional_headers:
            self.default_headers = self.default_headers | additional_headers

        post_headers = {"Content-Type": "application/json"}
        self.headers = {
            "delete": self.default_headers,
            "get": self.default_headers,
            "head": self.default_headers,
            "options": self.default_headers,
            "patch": self.default_headers | post_headers,
            "post": self.default_headers | post_headers,
            "put": self.default_headers | post_headers,
        }
        self.bulk_endpoints = {}
        self.endpoints = {} | self.bulk_endpoints
        self.next_page_token = "next_page_token"
        self.pagination_fields = ["next_page_token", "page_count", "page_number", "page_size", "total_records"]
        self.timeout = DEFAULT_CLIENT_TIMEOUT

        self.non_json_content_types = ["text/csv", "application/pdf"]

    @staticmethod
    def build(authorization: AnyStr = None, base_url: AnyStr = None):
        """
        Singleton to build the RestAPI Client.
        Args:
            authorization (AnyStr): Authorization for API client (e.g., API-Key, Bearer, etc.)
            base_url (AnyStr): base url for API

        Returns:
            An instance of RestAPI Class
        """
        return RestAPIClient(authorization=authorization, base_url=base_url)

    def _update_auth(self, auth):
        for headers in self.headers.values():
            headers["Authorization"] = auth

    def _make_request(
        self,
        url,
        data=None,
        headers=None,
        params=None,
        req_type="get",
        timeout=None,
        include_full_response=False,
    ) -> Union[Dict, requests.Response]:
        """
        Wrapper for making API requests using the API clients request_service.

        Args:
            url (required): Full API endpoint path to call
            data (optional): JSON data; sub-classes may alternately override
                the DEFAULT_POST_TYPE to provide data in a different format
            headers (optional): dictionary of headers, provide if
                overriding the default API client headers
            params (optional): dictionary to be provided as a query string
            req_type: type of request to be made (defaults to GET)
            timeout (optional): max duration (seconds) integer for request
            include_full_response: boolean to include the full response object instead of just .json()


        Returns:
            Response in JSON format, or alternatively the full response object if include_full_response is True
        """
        req_time = timeout if timeout else self.timeout
        req_headers = headers if headers else self.headers.get(req_type)

        if req_type == "delete":
            response = self.request_service.delete(url, headers=req_headers, data=data, params=params, timeout=req_time)
        elif req_type == "get":
            response = self.request_service.get(url, headers=req_headers, params=params, timeout=req_time)
        elif req_type == "head":
            response = self.request_service.head(url, headers=req_headers, data=data, params=params, timeout=req_time)
        elif req_type == "options":
            response = self.request_service.options(
                url, headers=req_headers, data=data, params=params, timeout=req_time
            )
        elif req_type == "patch":
            response = self.request_service.patch(url, headers=req_headers, data=data, params=params, timeout=req_time)
        elif req_type == "post":
            response = self.request_service.post(url, headers=req_headers, data=data, params=params, timeout=req_time)
        elif req_type == "put":
            response = self.request_service.put(url, headers=req_headers, data=data, params=params, timeout=req_time)
        else:
            response = requests.models.Response(
                status_code=418, text="API client request method ({req_type}) not implemented"
            )
        if response.ok:
            if len(response.content) > 0:
                try:
                    return response.json() if not include_full_response else response
                except ValueError:
                    return response
            return

        if response.status_code == 429:
            raise TooManyRequests()

        raise FailedRequest(response.status_code, response.text)

    def _get_endpoint(self, endpoint: AnyStr = None, parameters: Dict = {}) -> AnyStr:
        """
        Method to build the full API endpoint path and validate for any required path elements

        Args:
            endpoint (required): Name of the endpoint to be built.
            parameters (optional): dictionary of path elements to be substituted in the endpoint path


        Returns:
            URL in string format
        """
        _endpoint = self.endpoints.get(endpoint)
        if not _endpoint:
            raise UndefinedEndpoint(endpoint)
        elif isinstance(_endpoint, str):
            return f"{self.base_url}{_endpoint}"
        elif isinstance(_endpoint, tuple) and len(_endpoint) <= 2:
            target = _endpoint[0]
            required_keys = [] if len(_endpoint) == 1 else _endpoint[1]
            for key in required_keys:
                replacement = parameters.get(key)
                if not replacement:
                    raise MissingElement(key)
                target = target.replace(key, str(replacement))
            return f"{self.base_url}{target}"
        else:
            raise UndefinedEndpoint(endpoint)

    def get_data_by_endpoint(
        self,
        endpoint=None,
        data=None,
        headers=None,
        params={},
        req_type="get",
        timeout=None,
        page_size=None,
        retries=1,
        **kwargs,
    ):
        """
        Method to build the full API endpoint path and validate for any
        required path elements and then perform a get (default) request.

        Args:
            endpoint (required): Name of the endpoint to be built.
            params (optional): dictionary of path elements to be substituted
                in the endpoint path and/or query parameters passed to the endpoint.


        Returns:
            data: Data retrieved.
        """
        _endpoint = self._get_endpoint(endpoint=endpoint, parameters=params | kwargs)
        if page_size:
            params["page_size"] = page_size
        while retries:
            try:
                return self._make_request(
                    _endpoint, data=data, headers=headers, params=params | kwargs, req_type=req_type, timeout=timeout
                )
            except requests.exceptions.ReadTimeout as e:
                if retries:
                    retries -= 1
                else:
                    raise e

    def _get_data_and_next_page_token(self, results, params):
        """Processes a single set of results for data and the next page of results if applicable."""
        data = []
        next_page_token = results.pop(self.next_page_token, None)
        params[self.next_page_token] = next_page_token
        for k, v in results.items():
            if k not in self.pagination_fields:
                data = v
                break
        return data, next_page_token

    def _yield_bulk_data(self, endpoint, data, headers, params, req_type, timeout, page_size, retries, **kwargs):
        """Yields a generator from query results to process large amounts of data"""
        if page_size:
            params["page_size"] = page_size
        next_page_token = "START"
        while next_page_token:
            results = self.get_data_by_endpoint(
                endpoint=endpoint,
                data=data,
                headers=headers,
                params=params,
                req_type=req_type,
                timeout=timeout,
                retries=retries,
                **kwargs,
            )
            data, next_page_token = self._get_data_and_next_page_token(results, params)
            yield data

    def get_bulk_data_by_endpoint(
        self,
        endpoint=None,
        data=None,
        headers=None,
        params={},
        req_type="get",
        timeout=None,
        page_size=None,
        retries=1,
        **kwargs,
    ):
        """
        Method to build the full API endpoint path and validate for any required path elements
        and then perform a bulk request.

        Args:
            endpoint (required): Name of the endpoint to be built.
            data (optional): Data payload provided with the request.
            headers (optional): Additional headers provided with the request.
            parameters (optional): dictionary of path elements to be substituted in the endpoint path
                and/or query parameters passed to the endpoint.
            req_type (optional): Request type.
            timeout (optional): Request timeout override
            page_size (optional): Page size of query results.


        Returns:
            bulk_data (list): List of retrieved records.
        """
        _endpoint = self.bulk_endpoints.get(endpoint)
        if not _endpoint:
            raise UnsupportedBulkEndpoint(endpoint)

        results = self._yield_bulk_data(
            endpoint=endpoint,
            data=data,
            headers=headers,
            params=params,
            req_type=req_type,
            timeout=timeout,
            page_size=page_size,
            retries=retries,
            **kwargs,
        )
        bulk_data = []
        for _, record in enumerate(results):
            bulk_data += record

        return bulk_data
