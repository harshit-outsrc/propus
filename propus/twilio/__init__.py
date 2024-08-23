from typing import AnyStr
import base64

from twilio.rest import Client

from propus.api_client import RestAPIClient
from propus.logging_utility import Logging


class Twilio(Client, RestAPIClient):
    """
    Class for Twilio API integrations
    """

    # https://www.twilio.com/docs/messaging/api#base-urls
    # Base URL for Message Resource, MessageFeedbackResource, and Media Resource
    _base_url = "https://api.twilio.com/2010-04-01"
    # The Deactivations Resource also uses the https://messaging.twilio.com/v1 base URL.
    # API Resources related to Messaging Services use:
    _messaging_url = "https://messaging.twilio.com/v1"
    # Pricing information for Messaging uses the https://pricing.twilio.com/v1 base URL.
    _pricing_url = "https://pricing.twilio.com/v1"

    def __init__(self, account_sid, auth_token, base_url=_base_url):
        Client.__init__(self, username=account_sid, account_sid=account_sid, password=auth_token)
        user_pass = f"{account_sid}:{auth_token}"
        base_64_string = base64.b64encode(user_pass.encode()).decode()
        RestAPIClient.__init__(self, authorization=f"Basic {base_64_string}", base_url=base_url)
        self.sid = account_sid
        self.logger = Logging.get_logger("propus/twilio")
        self.instance_url = base_url
        self.next_page_token = "next_page_uri"
        self.pagination_fields = [
            "first_page_uri",
            "next_page_uri",
            "previous_page_uri",
            "end",
            "start",
            "page_size",
            "uri",
        ]
        self.endpoints = {
            # account
            "accounts": ("/2010-04-01/Accounts.json"),
            "addresses": (f"/2010-04-01/Accounts/{self.sid}/Addresses.json"),
            "conferences": (f"/2010-04-01/Accounts/{self.sid}/Conferences.json"),
            "signing_keys": (f"/2010-04-01/Accounts/{self.sid}/SigningKeys.json"),
            "transcriptions": (f"/2010-04-01/Accounts/{self.sid}/Transcriptions.json"),
            "connect_apps": (f"/2010-04-01/Accounts/{self.sid}/ConnectApps.json"),
            "sip": (f"/2010-04-01/Accounts/{self.sid}/SIP.json"),
            "authorized_connect_apps": (f"/2010-04-01/Accounts/{self.sid}/AuthorizedConnectApps.json"),
            "usage": (f"/2010-04-01/Accounts/{self.sid}/Usage.json"),
            "keys": (f"/2010-04-01/Accounts/{self.sid}/Keys.json"),
            "applications": (f"/2010-04-01/Accounts/{self.sid}/Applications.json"),
            "recordings": (f"/2010-04-01/Accounts/{self.sid}/Recordings.json"),
            "short_codes": (f"/2010-04-01/Accounts/{self.sid}/SMS/ShortCodes.json"),
            "calls": (f"/2010-04-01/Accounts/{self.sid}/Calls.json"),
            "notifications": (f"/2010-04-01/Accounts/{self.sid}/Notifications.json"),
            "incoming_phone_numbers": (f"/2010-04-01/Accounts/{self.sid}/IncomingPhoneNumbers.json"),
            "queues": (f"/2010-04-01/Accounts/{self.sid}/Queues.json"),
            "messages": (f"/2010-04-01/Accounts/{self.sid}/Messages.json"),
            "outgoing_caller_ids": (f"/2010-04-01/Accounts/{self.sid}/OutgoingCallerIds.json"),
            "available_phone_numbers": (f"/2010-04-01/Accounts/{self.sid}/AvailablePhoneNumbers.json"),
            "balance": (f"/2010-04-01/Accounts/{self.sid}/Balance.json"),
        }

    @staticmethod
    def build(
        account_sid: AnyStr = None,
        auth_token: AnyStr = None,
        base_url=_base_url,
        **kwargs,
    ):
        return Twilio(account_sid=account_sid, auth_token=auth_token, base_url=base_url, **kwargs)

    from ._message import (
        fetch_message,
        fetch_messages,
    )

    def _return_result(result, as_object=False):
        """Helper method to return Twilio result as a Twilio class object / Python dict

        Arguments:
            result (object): Twilio object (e.g., Twilio message)
            as_object (boolean): (optional) Return the result as Twilio Client object.
                Defaults to False (returns as Python dictionary object)

        Returns:
            data (object / dict): Data retreieved (as Twilio object / Python dict)
        """
        if as_object:
            return result

        return result.__dict__

    def _return_results(results, as_object=False):
        """Helper method to return Twilio results as an iterable of Twilio class objects / Python dicts

        Arguments:
            results (objects): Twilio objects (e.g., Twilio messages)
            as_object (boolean): (optional) Return the results as Twilio Client objects.
                Defaults to False (returns as Python dictionary objects)

        Returns:
            data (iterable): Data objects retreieved as Twilio objects / Python dictionaries
        """
        if as_object:
            return results

        return [i.__dict__ for i in results]
