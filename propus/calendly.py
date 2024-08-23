from typing import AnyStr, Dict

from propus.api_client import RestAPIClient


class Calendly(RestAPIClient):
    def __init__(self, authorization, base_url):
        super().__init__(authorization=authorization, base_url=base_url)
        self.endpoints = {
            "fetch_user": ("/users/<user_id>", ["<user_id>"]),
            "fetch_event_type": ("/event_types/<event_id>", ["<event_id>"]),
            "fetch_scheduled_events": "/scheduled_events",
        }

    @staticmethod
    def build(authorization: AnyStr, base_url: AnyStr = "https://api.calendly.com"):
        """
        Singleton to build the Calendly Client.
        Args:
            authorization (AnyStr): API key used to query Calendly
            base_url (AnyStr): : base url for Calendly API
               - Defaults to https://api.calendly.com

        Returns:
            An instance of Calendly Class
        """
        return Calendly(authorization=f"Bearer {authorization}", base_url=base_url)

    def fetch_event_type(self, event_id: AnyStr) -> Dict:
        """
        Wrapper for Calendly Event Types API.
        Documentation can be found here: https://developer.calendly.com/api-docs/c1f9db4a585da-get-event-type

        Args:
            event_id (AnyStr): UUID of event id

        Returns:
            Dict: Dictionary response from the Calendly API
        """
        url = self._get_endpoint("fetch_event_type", {"<event_id>": event_id})
        return self._make_request(url)

    def fetch_user(self, user_id: AnyStr) -> Dict:
        """
        Wrapper for Calendly User API.
        Documentation can be found here: https://developer.calendly.com/api-docs/ff9832c5a6640-get-user

        Args:
            user_id (AnyStr): user's id

        Returns:
            Dict: Dictionary response from the Calendly API
        """
        url = self._get_endpoint("fetch_user", {"<user_id>": user_id})
        return self._make_request(url)

    def fetch_scheduled_events(self, organization: AnyStr, **kwargs):
        """
        Wrapper for Calendly Scheduled Events API
        Documentation can be found here: https://developer.calendly.com/api-docs/2d5ed9bbd2952-list-events
        Organization is required and additional args can be sent in as kwargs

        Args:
            organization (AnyStr): Pass organization parameter to return events for that organization
                (requires admin/owner privilege)
        """
        url = self._get_endpoint("fetch_scheduled_events")
        kwargs["organization"] = organization
        return self._make_request(url, params=kwargs)
