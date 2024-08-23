import json
from typing import AnyStr, Dict, List

from .exceptions import EmailFailedToSend, ApiNotSuccessful


def send_transactional_email(
    self,
    email_id: int,
    to_email: AnyStr,
    from_email: AnyStr = None,
    cc: List[AnyStr] = None,
    bcc: List[AnyStr] = None,
    reply_to: AnyStr = None,
    reply_to_list: List[AnyStr] = None,
    email_name: AnyStr = None,
    contact_properties: Dict = None,
    custom_properties: Dict = None,
    salesforce_task: Dict = None,
) -> Dict:
    """
    This method is used to send an email designed in the marketing email tool.

    After you design and publish a transactional email in your HubSpot account, you can use this API to include
    customization options to the email, then send it to the intended recipient. The Email ID provided in the marketing
    email tool specifies which template to include in your API request.

    Find more details here: https://legacydocs.hubspot.com/docs/methods/email/transactional_email/single-send-overview

    Args:
        email_id (AnyStr): The emailId field is the content ID for the transactional email, which can be found i
            email tool UI.
        to_email (AnyStr): The recipient of the email
        from_email (AnyStr, optional): The From header for the email. You can define a from name with the following
            format: "from":"Sender Name <sender@hubspot.com>". Defaults to None.
        cc (List[AnyStr], optional): A list of email addresses to send as Cc. Defaults to None.
        bcc (List[AnyStr], optional): A list of email addresses to send as Bcc. Defaults to None.
        reply_to (AnyStr, optional): The Reply-To header for the email. Defaults to None.
        reply_to_list (List[AnyStr], optional): A list of Reply-To header values for the email. Defaults to None.
        email_name (AnyStr, optional): Hubspot email template name used for recording email activity on Hubspot contact
            records. Add to contact_properties array for property "last_system_email_sent". Defaults to None.
        contact_properties (Dict, optional): The contact_properties field is a dictionary of contact property
            values. Each contact property value contains a name and value property. Defaults to None.
        custom_properties (Dict, optional): The custom_properties field is a dictionary of custom property values not
            recorded in Hubspot. Each property value contains a name and value property. Defaults to None.
        salesforce_task (Dict, optional): If supplied this will be used to generate a task on a salesforce contact
            record. Required keys are "client" (Salesforce Instance from Propus) and "task_data" (a dictionary
            of the payload to send to propus.salesforce.create_task)

    Returns:
        AnyStr: email status ID to check if message sent successfully
    """
    message = {"to": to_email}
    var_map = {"from": from_email, "cc": cc, "bcc": bcc, "replyTo": reply_to, "replyToList": reply_to_list}
    for var, key in var_map.items():
        if key is not None:
            message[var] = key

    payload = {"emailId": email_id, "message": message}

    if email_name is not None:
        if not contact_properties:
            contact_properties = {}
        contact_properties["last_system_email_sent"] = email_name

    if contact_properties is not None:
        payload["contactProperties"] = contact_properties

    if custom_properties is not None:
        payload["customProperties"] = custom_properties

    url = self._get_endpoint("send_email")
    post_headers = self.headers.get("post")

    resp = self.request_service.post(url, headers=post_headers, data=json.dumps(payload), timeout=20)
    if resp.status_code < 200 or resp.status_code >= 300:
        raise EmailFailedToSend(resp.status_code, resp.text)
    if salesforce_task is not None:
        salesforce_task.get("client").create_task(**salesforce_task.get("task_data"))
    return resp.json().get("statusId")


def check_email_sent_status(self, status_id: AnyStr) -> Dict:
    """
    The SendResult is an enumeration of possible results when attempting to send the email. In practice, if the status
    code of the response is in the 400 range you should not attempt to resend. If the response is in the 500
    range then the request failed.

    Args:
        status_id (AnyStr): status_id of the email sent

    Raises:
        ApiNotSuccessful: Response code sent if not 200 range

    Returns:
        Dict: Dictionary response from hubspot. See hubspot docs for more info
    """
    try:
        url = self._get_endpoint("check_status", {"{statusId}": status_id})
        get_headers = self.headers.get("get")

        resp = self.request_service.get(url, headers=get_headers, timeout=20)
        if resp.status_code < 200 or resp.status_code >= 300:
            raise ApiNotSuccessful(resp.status_code, resp.text)
        return resp.json()
    except Exception:
        raise ApiNotSuccessful(500, "Internal Server Error")
