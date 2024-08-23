from typing import Literal, Union, Optional
import urllib.parse


async def get_term(self, account_id: Union[str, int], term_id: Union[str, int]) -> dict:
    """
    Get a term by ID
    :param self:
    :param account_id: The ID of the account to get the term from
    :param term_id: The ID of the term to get
    :return: A term object
    """
    return self.make_request(
        req_type="get",
        url=self._get_endpoint("get_term", {"<account_id>": account_id, "<term_id>": term_id}),
    )


async def list_terms(
    self,
    account_id: Union[str, int],
    workflow_state: Literal["active", "deleted", "all"] = "active",
    include: Optional[list[Literal["overrides", "course_count"]]] = None,
    term_name: Optional[str] = None,
) -> list[dict]:
    """
    List terms for an account
    :param self:
    :param account_id: The ID of the account to list terms for
    :param workflow_state: The state of the terms to list. Options are "active", "deleted", "all"
    :param include: The additional information to include in the response. Options are "overrides", "course_count"
    :param term_name: The name of the term to filter by
    :return: A list of terms
    """
    payload = {"workflow_state[]": workflow_state}
    if include is not None:
        payload["include[]"] = include
    if term_name is not None:
        payload["term_name"] = term_name

    url = self._get_endpoint("list_terms", {"<account_id>": account_id})
    query_params = urllib.parse.urlencode(payload, doseq=True)
    url = f"{url}?{query_params}"

    return self.make_request(req_type="get", url=url)
