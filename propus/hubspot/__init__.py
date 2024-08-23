from hubspot import HubSpot

from propus.api_client import RestAPIClient
from propus.logging_utility import Logging


class Hubspot(HubSpot, RestAPIClient):
    def __init__(self, api_key):
        HubSpot.__init__(self, access_token=api_key)
        self.api_key = f"Bearer {api_key}"
        self.base_url = "https://api.hubapi.com"
        RestAPIClient.__init__(self, authorization=self.api_key, base_url=self.base_url)
        self.logger = Logging.get_logger("propus/hubspot")
        self.next_page_token = "offset"
        self.pagination_fields = ["offset", "paging"]
        self.endpoints = {
            # ._events
            "campaign": ("/email/public/v1/campaigns/{campaignId}", ["{campaignId}"]),
            "campaigns": ("/email/public/v1/campaigns/by-id"),
            "event": ("/email/public/v1/events/{created}/{eventId}", ["{created}", "{eventId}"]),
            "events": ("/email/public/v1/events"),
            "recent_campaigns": ("/email/public/v1/campaigns"),
            # ._marketing
            "email": ("/marketing/v3/emails/{emailId}", ["{emailId}"]),
            "emails": ("/marketing/v3/emails"),
            "stats": ("/marketing/v3/emails/statistics/histogram"),
            "stats_list": ("/marketing/v3/emails/statistics/list"),
            # ._transactional_email
            "check_status": ("/marketing/v3/email/send-statuses/{statusId}", ["{statusId}"]),
            "send_email": ("/marketing/v3/transactional/single-email/send"),
        }

    @staticmethod
    def build(key):
        return Hubspot(api_key=key)

    from ._transactional_email import send_transactional_email, check_email_sent_status
