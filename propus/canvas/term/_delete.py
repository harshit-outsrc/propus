from typing import Union


async def delete_term(self, account_id: Union[str, int], term_id: Union[str, int]) -> dict:
    """
    Delete a term.
    :param self:
    :param account_id: The ID of the account.
    :param term_id: The ID of the term.
    :return: The deleted term object.
    """
    return self.make_request(
        req_type="delete",
        url=self._get_endpoint(
            "delete_term",
            {"<account_id>": account_id, "<term_id>": term_id},
        ),
    )
