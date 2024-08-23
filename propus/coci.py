from typing import Dict

from propus.api_client import RestAPIClient


class Coci(RestAPIClient):
    def __init__(self):
        super().__init__(authorization=None, base_url="https://coci2.ccctechcenter.org")
        self.endpoints = {
            "fetch_courses": "/courses/excel?college_filter[]=CALBRIGHT",
            "fetch_programs": "/programs/excel?college_filter[]=CALBRIGHT",
        }

    @staticmethod
    def format_resp(response):
        headers = []
        resp = []
        for idx, row in enumerate(response.text.split("\n")):
            if row == "":
                continue
            if idx == 0:
                for col in row.split(","):
                    # Remove surrounding quotes
                    title = col[1:-1].lower()
                    # remove the (CBO2) type of identifier
                    headers.append(title.split("(")[0].strip())
                continue
            row_split = row.split(",")
            resp.append({headers[i]: row_split[i].replace('"', "") for i in range(len(headers))})
        return resp

    def fetch_courses(self) -> Dict:
        """
        Wrapper to retrieve calbright courses from COCHI

        Returns:
            Dict: list of formatted dictionary of course data from COCHI
        """
        return self.format_resp(self._make_request(self._get_endpoint("fetch_courses")))

    def fetch_programs(self) -> Dict:
        """
        Wrapper to retrieve calbright programs from COCHI

        Returns:
            Dict: list of formatted dictionary of course data from COCHI
        """
        return self.format_resp(self._make_request(self._get_endpoint("fetch_programs")))
