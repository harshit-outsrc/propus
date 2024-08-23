from typing import AnyStr
import requests
from requests.exceptions import Timeout

from propus.api_client import RestAPIClient
from propus.logging_utility import Logging


class Zoom(RestAPIClient):
    """
    Class for Zoom API integrations
    """

    _base_url = "https://api.zoom.us/v2"

    def __init__(self, access_token, account_id, base_url=_base_url):
        super().__init__(authorization=access_token, base_url=base_url, additional_headers=dict(Host="api.zoom.us"))
        self.logger = Logging.get_logger("propus/zoom")
        self.instance_url = base_url
        self.access_token = access_token
        self.account_id = account_id
        self.pagination_fields = ["next_page_token", "page_count", "page_number", "page_size", "total_records"]
        self.bulk_endpoints = {
            # _meeting.py
            "past_meeting_participants": ("/past_meetings/{meetingId}/participants", ["{meetingId}"]),
            "polls": ("/meetings/{meetingId}/polls", ["{meetingId}"]),
            "registrants": ("/meetings/{meetingId}/registrants", ["{meetingId}"]),
            # _user.py
            "user_meetings": ("/users/{userId}/meetings", ["{userId}"]),
            "users": ("/users"),
        }
        self.endpoints = {
            # _account.py
            "virtual_background": ("/accounts/{accountId}/settings/virtual_backgrounds", ["{accountId}"]),
            # _meeting.py
            "meeting": ("/meetings/{meetingId}", ["{meetingId}"]),
            "past_meeting_details": ("/past_meetings/{meetingId}", ["{meetingId}"]),
            "past_meeting_instances": ("/past_meetings/{meetingId}/instances", ["{meetingId}"]),
            "meeting_invitation": ("/meetings/{meetingId}/invitation", ["{meetingId}"]),
            "meeting_polls": ("/meetings/{meetingId}/polls", ["{meetingId}"]),
            "past_meeting_polls": ("/past_meetings/{meetingId}/polls", ["{meetingId}"]),
            "past_meeting_qa": ("/past_meetings/{meetingId}/qa", ["{meetingId}"]),
            "poll": ("/meetings/{meetingId}/polls/{pollId}", ["{meetingId}", "{pollId}"]),
            "registrant": ("/meetings/{meetingId}/registrants/{registrantId}", ["{meetingId}", "{registrantId}"]),
            "registration_questions": ("/meetings/{meetingId}/registrants/questions", ["{meetingId}"]),
            "survey": ("/meetings/{meetingId}/survey", ["{meetingId}"]),
            # _user.py
            "user": ("/users/{userId}", ["{userId}"]),
            "user_assistants": ("/users/{userId}/assistants", ["{userId}"]),
            "user_schedulers": ("/users/{userId}/schedulers", ["{userId}"]),
            "user_summary": ("/users/summary"),
        } | self.bulk_endpoints

    @staticmethod
    def build(
        account_id: AnyStr = None,
        client_id: AnyStr = None,
        client_secret: AnyStr = None,
        grant_type: AnyStr = "account_credentials",
        login_url: AnyStr = "zoom.us/oauth/token",
        **kwargs,
    ):
        def login(endpoint, auth, data, attempts=0):
            try:
                response = requests.post(endpoint, auth=auth, data=data, timeout=15)
            except Timeout:
                if attempts >= 2:
                    raise
                login(endpoint, auth, data, attempts + 1)
            return response.json()

        endpoint = f"https://{login_url}/"
        auth = (client_id, client_secret)
        data = {
            "grant_type": grant_type,
            "account_id": account_id,
        }
        json_response = login(endpoint, auth, data)
        return Zoom(f"Bearer {json_response.get('access_token')}", account_id=account_id)

    def _get_data_and_next_page_token(self, results, params):
        data = []
        next_page_token = results.pop("next_page_token", None)
        params["next_page_token"] = next_page_token
        for k, v in results.items():
            if k not in self.pagination_fields:
                data = v
                break
        return data, next_page_token

    from ._account import (
        create_virtual_background,
        delete_virtual_background,
    )

    from ._meeting import (
        fetch_meeting,
        fetch_meeting_invitation,
        fetch_meeting_polls,
        fetch_past_meeting_details,
        fetch_past_meeting_instances,
        fetch_past_meeting_participants,
        fetch_past_meeting_polls,
        fetch_past_meeting_qa,
        fetch_poll,
        fetch_polls,
        fetch_registrant,
        fetch_registrants,
        fetch_registration_questions,
        fetch_survey,
    )

    from ._user import (
        create_user,
        fetch_user,
        fetch_user_meetings,
        fetch_user_assistants,
        fetch_user_schedulers,
        fetch_user_summary,
        fetch_users,
    )
