import json
from datetime import datetime, timedelta
import re

from propus.helpers.calbright import format_term_name


class InvalidTermStartDate(Exception):
    pass


def create_term(self, start_date: datetime):
    """Create a term record in Salesforce.

    This function takes a start date and creates a term dictionary
    with name, dates and account fields to insert as a new record.

    It validates the start date is a Tuesday and calculates the
    term number. Dates like end date are calculated from
    the start date.

    Args:
        start_date (datetime): The start date of the term.

    Returns:
        dict: The term data to insert via API.

    Raises:
        InvalidTermStartDate: If start date is not a Tuesday.
    """

    if start_date.weekday() != 1:
        raise InvalidTermStartDate("Term start date must be on a Tuesday")
    data = {
        "Name": format_term_name(start_date),
        "hed__Start_Date__c": start_date.strftime("%Y-%m-%d"),
        "hed__End_Date__c": (start_date + timedelta(days=181)).strftime("%Y-%m-%d"),
        "hed__Account__c": self._calbright_sf_account_id,
    }
    return self.make_request(self._get_endpoint("create_term"), data=json.dumps(data), req_type="post")


def fetch_terms(self, future_terms=True):
    """Fetch terms from Salesforce.

    This function queries Salesforce for term records associated with a given account.

    It retrieves the specified fields for each term and filters by start date if future_terms
    is True. Terms are filtered and appended to the response list if they match the
    expected name format or are the BETA term.

    Args:
        future_terms (bool): Whether to include only future terms.

    Returns:
        List[dict]: The term records fetched from Salesforce.
    """

    fields_to_retrieve = [
        "Id",
        "Name",
        "hed__Start_Date__c",
        "hed__End_Date__c",
        "Last_day_to_drop_without_a_W__c",
        "Last_day_to_withdraw__c",
    ]
    resp = self.custom_query(
        "SELECT {} FROM hed__Term__c WHERE hed__Account__c ='0013k00002lAtFyAAK'{}".format(
            ", ".join(fields_to_retrieve),
            f" AND hed__Start_Date__c >= {datetime.now().strftime('%Y-%m-%d')}" if future_terms else "",
        )
    )
    if resp.get("totalSize") == 0:
        return []
    response = []
    for term_resp in resp.get("records"):
        if not (
            re.search(r"\d{4}-(\d{2}|\d{4})-TERM-\d{2}", term_resp.get("Name"))
            or term_resp.get("Name") == "2019-2020-BETA"
        ):
            continue
        response.append(term_resp)
    return response
