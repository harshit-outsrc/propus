# _service.py
# Convenience functions that call the Twilio client.
# These functions are loaded in the __init__.py file


def fetch_service(self, sid=None, as_object=False):
    """Fetch a Twilio service from the Client.messaging.v1.services class.
    Documentation: https://www.twilio.com/docs/messaging/api/service-resource#fetch-a-service-resource

    Arguments:
        sid (str): The SID of the Service resource to fetch.
        as_object (boolean): (optional) Return the results as Twilio Client object.
            Defaults to False (returns as Python dictionary objects)

    Returns:
        data (list): Data retreieved

    Example Service:
        {
            "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "sid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "date_created": "2015-07-30T20:12:31Z",
            "date_updated": "2015-07-30T20:12:33Z",
            "friendly_name": "My Service!",
            "inbound_request_url": "https://www.example.com/",
            "inbound_method": "POST",
            "fallback_url": null,
            "fallback_method": "POST",
            "status_callback": "https://www.example.com",
            "sticky_sender": true,
            "mms_converter": true,
            "smart_encoding": false,
            "fallback_to_long_code": true,
            "area_code_geomatch": true,
            "validity_period": 600,
            "scan_message_content": "inherit",
            "synchronous_validation": true,
            "usecase": "marketing",
            "us_app_to_person_registered": false,
            "use_inbound_webhook_on_number": true,
            "links": {
                "phone_numbers": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/PhoneNumbers",
                "short_codes": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/ShortCodes",
                "alpha_senders": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/AlphaSenders",
                "messages": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages",
                "us_app_to_person": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Compliance/Usa2p",
                "us_app_to_person_usecases": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Compliance/Usa2p/Usecases",
                "channel_senders": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/ChannelSenders"
            },
            "url": "https://messaging.twilio.com/v1/Services/MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            }
    """
    return self._return_result(self.messaging.v1.services(sid).fetch(), as_object)


def fetch_services(self, as_object=False, **kwargs):
    """Fetch Twilio Services from the Client.messaging.v1.services class.
    Documentation: https://www.twilio.com/docs/messaging/api/service-resource#read-multiple-service-resources

    Arguments:
        as_object (boolean): (optional) Return the results as Twilio Client object
            Defaults to False (returns as Python dictionary object)
        Kwargs (dict): (optional) Dictionary of kwargs to pass to the function
            E.g., kwargs = dict(date_sent=datetime(2016, 8, 31, 0, 0, 0), from_='+15017122661', to='+15558675310', limit=20)

    Returns:
        data (list): Data retreieved
    """
    return self._return_results(self.messaging.v1.services.list(**kwargs), as_object)
