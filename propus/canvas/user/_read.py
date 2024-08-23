import datetime
import urllib.parse
from typing import Union


async def get_user(self, user_id: Union[str, int]) -> dict:
    """
    Get a single user by their ID.
    :param self:
    :param user_id: Canvas ID for the user
    :return: The user object
    """
    return self.make_request(
        req_type="get",
        url=self._get_endpoint("get_user", {"<user_id>": user_id}),
    )


async def get_user_profile(self, user_id: Union[str, int]) -> dict:
    """
    Get a single user's profile by their ID.
    :param self:
    :param user_id: Canvas ID for the user
    :return: The user profile object
    """
    return self.make_request(
        req_type="get",
        url=self._get_endpoint("get_user_profile", {"<user_id>": user_id}),
    )


async def list_users_in_account(self, account_id: Union[str, int]) -> list[dict]:
    """
    List the users in an account.
    :param self:
    :param account_id: Canvas ID for the account
    :return: A list of user objects
    """
    return self.make_request(
        req_type="get",
        url=self._get_endpoint("list_users_in_account", {"<account_id>": account_id}),
    )


async def get_user_page_views(
    self, user_id: Union[str, int], start_time: datetime.datetime, end_time: datetime.datetime
) -> list[dict]:
    """
    Get the page views for a user.
    :param self:
    :param user_id: Canvas ID for the user
    :param start_time: Start of the date range
    :param end_time: End of the date range
    :return: A list of page view objects
    """
    payload = {}
    if start_time is not None:
        payload["start_time"] = start_time.isoformat()
    if end_time is not None:
        payload["end_time"] = end_time.isoformat()

    url = self._get_endpoint("get_user_page_views", {"<user_id>": user_id})
    query_params = urllib.parse.urlencode(payload, doseq=True)
    url = f"{url}?{query_params}"
    return self.make_request(req_type="get", url=url)
