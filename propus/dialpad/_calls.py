from typing import AnyStr, Dict

# _calls.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def get_call_info(self, call_id: AnyStr) -> Dict:
    """Retrieve the given call's details.
    Documentation: https://developers.dialpad.com/reference/callget_call_info

    Arguments:
        call_id (AnyStr): Call ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="call", params={"{callId}": call_id})
