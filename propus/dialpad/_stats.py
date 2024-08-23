from typing import AnyStr, Dict

# _stats.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def get_stats(self, stat_id: AnyStr) -> Dict:
    """Retrieve the given stat's details.
    Documentation: https://developers.dialpad.com/reference/statsget

    Arguments:
        stat_id (AnyStr): Statistics ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="stat", params={"{statId}": stat_id})


def create_stats(self, params: Dict = {}) -> Dict:
    """Initiate processing statistics.
    Documentation: https://developers.dialpad.com/reference/statscreate

    Arguments:
        params (Dict): (optional) Dictionary of apx. a dozen available query parameters.

    Returns:
        data (dict): Data dictionary returned
    """
    # Set defaults for required fields export_type == records and stat_type == calls
    params["export_type"] = params.get("export_type", "records")
    params["stat_type"] = params.get("stat_type", "calls")
    # target_id and target_type are required for stat_type choices csat and dispositions
    if (
        params.get("stat_type") in ["csat", "dispositions"]
        and not params.get("target_id")
        and not params.get("target_type")
    ):
        raise

    return self._make_request(self._get_endpoint("stats"), params=params)
