# _account.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RESTApiClient class.
# These functions are loaded in the __init__.py file


def create_virtual_background(self, file, **kwargs):
    """Upload virtual background files for all users on the account to use.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/uploadVB

    Arguments:
        file (file): Image file

    Returns:
        data (dict): Data dictionary returned
    """
    data = dict(file=file)
    params = {"{accountId}": self.account_id}
    endpoint = self._get_endpoint("virtual_background", parameters=params)
    response = self._make_request(endpoint, data=data, parameters=kwargs, req_type="post")

    return response


def delete_virtual_background(self, file_ids, **kwargs):
    """Delete an account's existing virtual background files.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/delVB

    Arguments:
        file_ids (str or list): String file ID or List of file IDs
            file_ids is passed to Zoom as a query-string parameter of
            comma-separated list of file IDs to delete.

    Returns:
        None: HTTP Status Code 204 (deleted) / no content

    """
    if isinstance(file_ids, str):
        file_ids = file_ids
    elif isinstance(file_ids, list):
        file_ids = ",".join(file_ids)
    parameters = {"{accountId}": self.account_id}
    endpoint = self._get_endpoint("virtual_background", parameters=parameters)
    response = self._make_request(endpoint, params={"file_ids": file_ids} | kwargs, req_type="delete")

    return response
