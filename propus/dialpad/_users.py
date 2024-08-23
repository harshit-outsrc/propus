from typing import AnyStr, Dict

# _users.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def get_user(self, user_id: AnyStr) -> Dict:
    """Retrieve the given user's details.
    Documentation: https://developers.dialpad.com/reference/usersget

    Arguments:
        user_id (AnyStr): User ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="user", params={"{userId}": user_id})


def get_users(
    self,
    state: AnyStr = None,
    company_admin: bool = None,
    limit: int = None,
    email: AnyStr = None,
    number: AnyStr = None,
):
    """Retrieve the users.
    Documentation: https://developers.dialpad.com/reference/userslist

    Arguments:
        state (AnyStr): (optional) Filter results by the specified user state (e.g. active, suspended, deleted)
        company_admin (bool): (optional) If provided, filter results by the specified
            value to return only company admins or only non-company admins.
        limit (int): (optional) The maximum number of results to return.
        email (AnyStr): (optional) The user's email.
        number (AnyStr): Phone number in e164 format (e.g., +15105551212)

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if state:
        params["state"] = state
    if company_admin:
        params["company_admin"] = company_admin
    if limit:
        params["limit"] = limit
    if email:
        params["email"] = email
    if number:
        _number = f"+1{number}" if number[0:1] != "+1" else number
        params["number"] = _number

    return self.get_bulk_data_by_endpoint(endpoint="users", params=params)
