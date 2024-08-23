from typing import AnyStr, Dict

from propus.api_client import RestAPIClient


class KeyCDN(RestAPIClient):
    def __init__(self, authorization, base_url, additional_headers=None):
        super().__init__(authorization=None, base_url=base_url, additional_headers=additional_headers)
        self.endpoints = {"get_geo_json": "/geo.json"}

    @staticmethod
    def build(authorization: AnyStr = None, base_url: AnyStr = "https://tools.keycdn.com"):
        """
        Singleton to build the KeyCDN Client.
        Args:
            authorization (AnyStr): Authorization is set in the User-Agent header
            base_url (AnyStr): : base url for KeyCDN API
               - Defaults to https://tools.keycdn.com

        Returns:
            An instance of KeyCDN Class
        """
        additional_headers = {"User-Agent": "keycdn-tools:https://calbright.org"}
        return KeyCDN(
            authorization=authorization,
            base_url=base_url,
            additional_headers=additional_headers,
        )

    def get_geo_json(self, host: AnyStr) -> Dict:
        """
        Wrapper for KeyCDN IP Location Finder API.
        Documentation: https://tools.keycdn.com/geo
        Args:
            host (AnyStr): IP address (v4) or host name to lookup

        Returns:
            Dict, e.g.,
            {
                "status":"success",
                "description":"Data successfully received.",
                "data":{
                    "geo":{
                        "host":"www.example.com",
                        "ip":"93.184.216.34",
                        "rdns":"93.184.216.34",
                        "asn":15133,
                        "isp":"MCI Communications Services, Inc. dba Verizon Business",
                        "country_name":"United States",
                        "country_code":"US",
                        "region_name":"Massachusetts",
                        "region_code":"MA",
                        "city":"Norwell",
                        "postal_code":"02061",
                        "continent_name":"North America",
                        "continent_code":"NA",
                        "latitude":42.1596,
                        "longitude":-70.8217,
                        "metro_code":506,
                        "timezone":"America/New_York",
                        "datetime":"2019-06-01 00:00:00"
                    }
                }
            }
        """
        params = {"host": host}
        url = self._get_endpoint("get_geo_json")
        return self._make_request(url, params=params)
