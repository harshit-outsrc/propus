from typing import AnyStr, Dict, List

from propus.api_client import RestAPIClient

VALID_EMAIL_STATUSES = ["valid"]
INVALID_EMAIL_STATUSES = [
    "invalid",
    "catch-all",
    "unknown",
    "spamtrap",
    "abuse",
    "do_not_mail",
]


class ZeroBounce(RestAPIClient):
    def __init__(self, authorization, base_url):
        super().__init__(authorization=None, base_url=base_url)
        self.params = {"api_key": authorization}
        self.timeout = 30
        self.endpoints = {
            "get_api_usage": "/v2/getapiusage",
            "get_credits": "/v2/getcredits",
            "validate_email": "/v2/validate",
            "validate_email_batch": "/v2/validatebatch",
        }

    @staticmethod
    def build(authorization: AnyStr, base_url: AnyStr = "https://api.zerobounce.net"):
        """
        Singleton to build the ZeroBounce Client.
        Args:
            authorization (AnyStr): API key used to query ZeroBounce (used in params)
            base_url (AnyStr): : base url for ZeroBounce API
               - Defaults to https://api.zerobounce.net

        Returns:
            An instance of ZeroBounce Class
        """
        return ZeroBounce(authorization=authorization, base_url=base_url)

    def get_api_usage(self, start_date: AnyStr, end_date: AnyStr) -> Dict:
        """
        Wrapper for ZeroBounce API Usage API.
        Documentation: https://www.zerobounce.net/docs/email-validation-api-quickstart/#get_aPI_usage__v2__
        Args:
            start_date (AnyStr): Start date (inclusive) of API usage request (format: yyyy-mm-dd)
            end_date (AnyStr): End date (inclusive) or API usage request (format: yyyy-mm-dd)

        Returns:
            Dict, e.g.,
            {
                'total': 570,
                'status_valid': 553,
                'status_invalid': 0,
                [...],
                'sub_status_toxic': 0,
                'sub_status_global_suppression': 2,
                [...],
                'start_date': '5/1/2023',
                'end_date': '5/18/2023'
            }
        """
        params = self.params | {"start_date": start_date, "end_date": end_date}
        url = self._get_endpoint("get_api_usage")
        return self._make_request(url, params=params)

    def get_credits(self) -> Dict:
        """
        Wrapper for ZeroBounce Get Credits API.
        Documentation: https://www.zerobounce.net/docs/email-validation-api-quickstart#get_balance__v2__
        Args:
            None

        Returns:
            Dict, e.g.,
            {'Credits': '2073'}
        """
        url = self._get_endpoint("get_credits")
        return self._make_request(url, params=self.params)

    def validate_email_address(self, email: AnyStr, ip_address: AnyStr = None) -> Dict:
        """
        Wrapper for ZeroBounce Single Email Validator - Real Time API.
        Documentation: https://www.zerobounce.net/docs/email-validation-api-quickstart/#validate_emails__v2__
        Args:
            email (AnyStr): Email address to verify (required)
            ip_address (AnyStr): Accompanying IP address to verify (optional)

        Returns:
            Dict, e.g.,
                {
                    "address":"flowerjill@aol.com",
                    "status":"valid",
                    "sub_status":"",
                    [...],
                    "processed_at":"2017-04-01 02:48:02.592"
                }
        """
        params = self.params | {"email": email}
        if ip_address:
            params = params | {"ip_address": ip_address}
        url = self._get_endpoint("validate_email")
        return self._make_request(url, params=params)

    def validate_email_address_batch(self, email_batch: List) -> Dict:
        """
        Wrapper for ZeroBounce Batch Email Validator - Real Time API.
        Documentation: https://www.zerobounce.net/docs/email-validation-api-quickstart/#batch_validate_emails__v2__
        Args:
            email_batch (List): List of lists of email addresses and IP addresses (optional) to validate
                Format:[
                    ["valid@example.com", "1.1.1.1"],
                    ["another@example.com"],
                ]

        Returns:
            Dict, e.g.,
                {
                    "email_batch": [
                        {
                            "address": "valid@example.com",
                            [...],
                            "processed_at": "2020-09-17 17:43:11.829"
                        },
                        {
                            "address": "invalid@example.com",
                            [...],
                            "processed_at": "2020-09-17 17:43:11.830"
                        },
                        {
                            "address": "disposable@example.com",
                            [...],]
                            "processed_at": "2020-09-17 17:43:11.830"
                        }
                    ],
                    "errors": []
                }
        """
        email_list = []
        for email in email_batch:
            if len(email) == 1:
                email_list.append({"email_address": email[0]})
            elif len(email) == 2:
                email_list.append({"email_address": email[0], "ip_address": email[1]})
        params = self.params | {"email_batch": email_list}
        url = self._get_endpoint("validate_email_batch")
        return self._make_request(url, params=params)
