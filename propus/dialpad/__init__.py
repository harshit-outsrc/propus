import os
from typing import AnyStr

from dialpad import DialpadClient

from propus.api_client import RestAPIClient
from propus.logging_utility import Logging

from ._calls import get_call_info  # noqa: F401
from ._contacts import get_contact, get_contacts  # noqa: F401
from ._numbers import get_number, get_numbers  # noqa: F401
from ._stats import create_stats, get_stats  # noqa: F401
from ._users import get_user, get_users  # noqa: F401


class Dialpad(DialpadClient, RestAPIClient):
    """
    Class for Dialpad API integrations
    """

    # _base_url is used by both the DialpadClient and RestAPIClient
    _base_url = "https://dialpad.com"

    def __init__(self, authorization, base_url=_base_url):
        hosts = dict(live="https://dialpad.com", sandbox="https://sandbox.dialpad.com")

        env = os.environ.get("env")
        sandbox = False if env == "localhost" else True
        self._base_url = base_url or hosts.get("sandbox" if sandbox else "live")
        DialpadClient.__init__(self, sandbox=sandbox, token=authorization)
        RestAPIClient.__init__(self, authorization=f"Bearer {authorization}", base_url=self._base_url)
        self.logger = Logging.get_logger("propus/dialpad")
        self.endpoints = {
            # _calls.py
            "call": ("/api/v2/call/{callId}", ["{callId}"]),
            # _contacts.py
            "contact": ("/api/v2/contacts/{contactId}", ["{contactId}"]),
            "contacts": ("/api/v2/contacts/"),
            # _numbers.py
            "number": ("/api/v2/numbers/{numberId}", ["{numberId}"]),
            "numbers": ("/api/v2/numbers/"),
            # _stats.py
            "create_stats": ("/api/v2/stats/"),
            "stats": ("/api/v2/stats/{statsId}", ["{statsId}"]),
            # _users.py
            "user": ("/api/v2/users/{userId}", ["{userId}"]),
            "users": ("/api/v2/users/"),
        }
        self.next_page_token = "cursor"
        self.pagination_fields = ["cursor"]

    @staticmethod
    def build(authorization: AnyStr = None, base_url: AnyStr = None):
        """
        Singleton to build the Dialpad API Client.
        Args:
            authorization (AnyStr): Authorization for API client (i.e., API-Key)
            base_url (AnyStr): base url for API

        Returns:
            An instance of Dialpad Class
        """
        return Dialpad(authorization=authorization, base_url=base_url)
