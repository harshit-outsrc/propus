from typing import AnyStr, Dict

from propus.helpers.input_validations import validate_phone_number

# _numbers.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def get_number(self, number: AnyStr) -> Dict:
    """Retrieve the given number's details.
    Documentation: https://developers.dialpad.com/reference/numbersget

    Arguments:
        number (AnyStr): Phone number in e164 format (e.g., +15105551212)

    Returns:
        data (dict): Data dictionary returned
    """
    validate_phone_number(number, phone_format="e164", is_required=True)

    return self.get_data_by_endpoint(endpoint="number", params={"{number}": number})


def get_numbers(self, status: AnyStr = None, limit: int = None):
    """Retrieve the numbers.
    Documentation: https://developers.dialpad.com/reference/numberslist

    Arguments:
        status (AnyStr): (optional) Status to filter by.
        limit (int): (optional) The maximum number of results to return.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if status:
        params["status"] = status
    if limit:
        params["limit"] = limit

    return self.get_bulk_data_by_endpoint(endpoint="numbers", params=params)
