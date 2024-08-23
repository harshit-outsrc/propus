from typing import AnyStr, Dict

# _events.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def get_campaign(self, campaign_id: AnyStr) -> Dict:
    """Retrieve the given campaign's data.
    Documentation: https://legacydocs.hubspot.com/docs/methods/email/get_campaign_data

    Arguments:
        campaign_id (AnyStr): Campaign ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="campaign", params={"{campaignId}": campaign_id})


def get_campaigns(self, limit: int = None):
    """Retrieve the campaigns.
    Documentation: https://legacydocs.hubspot.com/docs/methods/email/get_campaigns_by_id

    Arguments:
        limit (int): (optional) The maximum number of results to return.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if limit:
        params["limit"] = limit

    return self.get_bulk_data_by_endpoint(endpoint="campaigns", params=params)


def get_recent_campaigns(self, limit: int = 10):
    """Retrieve the campaigns with recent activity. The campaign IDs
    are returned in descending order of most-recent activity.
    Documentation: https://legacydocs.hubspot.com/docs/methods/email/get_campaigns

    Arguments:
        limit (int): (optional) The maximum number of results to return.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if limit:
        params["limit"] = limit

    return self.get_bulk_data_by_endpoint(endpoint="recent_campaigns", params=params)


def get_event(self, event_id: AnyStr, created: int) -> Dict:
    """Retrieve the given email event's data.
    Documentation: https://legacydocs.hubspot.com/docs/methods/email/get_event_by_id

    Arguments:
        eventId (AnyStr): Event ID
        created: (int): The creation timestamp (in milliseconds since epoch) of the event to return.

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="campaign", params={"{eventId}": event_id, "{created}": created})


def get_events(self, limit: int = None):
    """Retrieve the email events.
    Documentation: https://legacydocs.hubspot.com/docs/methods/email/get_events

    Arguments:
        limit (int): (optional) The maximum number of results to return.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if limit:
        params["limit"] = limit

    return self.get_bulk_data_by_endpoint(endpoint="campaigns", params=params)
