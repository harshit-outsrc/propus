from typing import AnyStr, Dict, List

# _marketing.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def get_email(self, email_id: AnyStr) -> Dict:
    """Retrieve the given email's data.
    Documentation: https://developers.hubspot.com/docs/api/marketing/marketing-email#retrieve-a-marketing-email

    Arguments:
        email_id (AnyStr): Email ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="email", params={"{emailId}": email_id})


def get_emails(self, limit: int = None):
    """Retrieve the emails.
    Documentation: https://legacydocs.hubspot.com/docs/methods/email/get_emails_by_id

    Arguments:
        limit (int): (optional) The maximum number of results to return.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if limit:
        params["limit"] = limit

    return self.get_bulk_data_by_endpoint(endpoint="emails", params=params)


def get_stats(
    self, inverval: AnyStr = None, start_time: AnyStr = None, end_time: AnyStr = None, email_ids: List = None
):
    """Retrieve statistics of marketing emails.
    Documentation: https://developers.hubspot.com/docs/api/marketing/marketing-email

    Arguments:
        inverval (AnyStr): (optional) Interval to report statistics in
            (e.g., YEAR, QUARTER, ... QUARTER-HOUR, MINUTE...).
        start_time (AnyStr): (optional) Start timestamp in ISO 8601 format (e.g., 2023-01-02T12:34:56Z).
        end_time (AnyStr): (optional) End timestamp in ISO 8601 format (e.g., 2023-01-03T12:34:56Z).
        email_ids (List): (optional) Filter by email IDs. Only include statistics of emails with these IDs.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if inverval:
        params["inverval"] = inverval.upper()
    if start_time:
        params["startTimestamp"] = start_time
    if end_time:
        params["endTimestamp"] = end_time
    if email_ids:
        params["emailIds"] = email_ids

    return self.get_bulk_data_by_endpoint(endpoint="stats", params=params)


def get_stats_list(
    self,
    inverval: AnyStr = None,
    start_time: AnyStr = None,
    end_time: AnyStr = None,
    email_ids: List = None,
    email_property: AnyStr = None,
):
    """Retrieve statistics of marketing emails. It also returns the list of emails that were sent during the time span.
    Documentation: https://developers.hubspot.com/docs/api/marketing/marketing-email

    Arguments:
        inverval (AnyStr): (optional) Interval to report statistics in
            (e.g., YEAR, QUARTER, ... QUARTER-HOUR, MINUTE...).
        start_time (AnyStr): (optional) Start timestamp in ISO 8601 format
            (e.g., 2023-01-02T12:34:56Z).
        end_time (AnyStr): (optional) End timestamp in ISO 8601 format (e.g., 2023-01-03T12:34:56Z).
        email_ids (List): (optional) Filter by email IDs. Only include statistics of emails with these IDs.
        email_property (AnyStr): (optional) Specifies which email properties should be returned.
            All properties will be returned by default.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if inverval:
        params["inverval"] = inverval.upper()
    if start_time:
        params["startTimestamp"] = start_time
    if end_time:
        params["endTimestamp"] = end_time
    if email_ids:
        params["emailIds"] = email_ids
    if email_property:
        params["property"] = email_property

    return self.get_bulk_data_by_endpoint(endpoint="stats_list", params=params)
