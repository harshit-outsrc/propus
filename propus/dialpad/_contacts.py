from typing import AnyStr, Dict

# _contacts.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def get_contact(self, contact_id: AnyStr) -> Dict:
    """Retrieve the given contact's details.
    Documentation: https://developers.dialpad.com/reference/contactsget

    Arguments:
        contact_id (AnyStr): Contact ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="contact", params={"{contactId}": contact_id})


def get_contacts(self, owner_id: AnyStr = None, limit: int = None, include_local: bool = False):
    """Retrieve the contacts.
    Documentation: https://developers.dialpad.com/reference/contactslist

    Arguments:
        owner_id (AnyStr): (optional) The id of the user who owns the contact.
        limit (int): (optional) The maximum number of results to return.
        include_local (bool): (optional) If set to True company local contacts will be included. default False.

    Returns:
        data (dict): Data dictionary returned
    """
    params = {}
    if owner_id:
        params["owner_id"] = owner_id
    if limit:
        params["limit"] = limit
    if include_local:
        params["include_local"] = include_local

    return self.get_bulk_data_by_endpoint(endpoint="contacts", params=params)
