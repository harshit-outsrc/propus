# _message.py
# Convenience functions that call the Twilio client.
# These functions are loaded in the __init__.py file


def fetch_message(self, sid=None, as_object=False):
    """Fetch a Twilio message from the Client.messages() function.
    Documentation: https://www.twilio.com/docs/messaging/api/message-resource?code-sample=code-fetch-message&code-language=Python&code-sdk-version=8.x#fetch-a-message-resource

    Arguments:
        sid (str): The SID of the Message resource to be fetched
        as_object (boolean): (optional) Return the results as Twilio Client object.
            Defaults to False (returns as Python dictionary objects)

    Returns:
        data (list): Data retreieved

    Example Message:
        {
            "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "api_version": "2010-04-01",
            "body": "Hi there",
            "date_created": "Thu, 24 Aug 2023 05:01:45 +0000",
            "date_sent": "Thu, 24 Aug 2023 05:01:45 +0000",
            "date_updated": "Thu, 24 Aug 2023 05:01:45 +0000",
            "direction": "outbound-api",
            "error_code": null,
            "error_message": null,
            "from": "+15557122661",
            "num_media": "0",
            "num_segments": "1",
            "price": null,
            "price_unit": null,
            "messaging_service_sid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "status": "queued",
            "subresource_uris": {
                "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Media.json"
            },
            "to": "+15558675310",
            "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
        }

        Message status values
        Source: https://www.twilio.com/docs/messaging/api/message-resource?code-sample=code-fetch-message&code-language=Python&code-sdk-version=8.x#message-status-values
            queued: The API request to send an outbound message was successful and the message is queued to be sent out by a specific From sender. For messages sent without a Messaging Service this is the initial Status value of the Message resource.
            sending: Twilio is in the process of dispatching the outbound message to the nearest upstream carrier in the network.
            sent: The nearest upstream carrier accepted the outbound message.
            failed: The outbound message failed to send. This can happen for various reasons including queue overflows, Account suspensions and media errors. Twilio does not charge you for failed messages.
            delivered: Twilio has received confirmation of outbound message delivery from the upstream carrier, and, where available, the destination handset.
            undelivered: Twilio received a delivery receipt indicating that the outbound message was not delivered. This can happen for many reasons including carrier content filtering and the availability of the destination handset.
            receiving: The inbound message was received by Twilio and is currently being processed.
            received: The inbound message was received and processing is complete.
            accepted: [Messaging Service only] Twilio has received your API request to immediatedly send an outbound message with a Messaging Service. If you did not provide a specific From sender in the service's Sender Pool to use, the service is dynamically selecting a From sender. For unscheduled messages to be sent with a Messaging Service, this is the initial Status value of the Message resource.
            scheduled: [Messaging Service only] The Message resource is scheduled to be sent with a Messaging Service. If you schedule a message with a Messaging Service, this is the initial Status value of the Message resource.
            read: WhatsApp only: The recipient opened the outbound message. Recipient must have read receipts enabled.
            canceled: [Messaging Service only] The message scheduled with a Messaging Service has been canceled.
    """
    return self._return_result(self.messages(sid).fetch(), as_object)


def fetch_messages(self, as_object=False, **kwargs):
    """Fetch Twilio messages from the Client.messages.list() function.
    Documentation: https://www.twilio.com/docs/messaging/api/message-resource?code-sample=code-list-all-message-resources&code-language=Python&code-sdk-version=8.x

    Arguments:
        as_object (boolean): (optional) Return the results as Twilio Client object
            Defaults to False (returns as Python dictionary object)
        Kwargs (dict): (optional) Dictionary of kwargs to pass to the function
            E.g., kwargs = dict(date_sent=datetime(2016, 8, 31, 0, 0, 0), from_='+15017122661', to='+15558675310', limit=20)

    Returns:
        data (list): Data retreieved
    """
    return self._return_results(self.messages.list(**kwargs), as_object)
