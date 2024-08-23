class InvalidEventType(Exception):
    """Exception raised for invalid event type

    Attributes:
        event_type -- event type submitted
    """

    def __init__(self, event_type):
        super().__init__(f'Unkown Event Type: "{event_type}"')


class MissingRequiredData(Exception):
    """Exception raised for missing required data for event

    Attributes:
        event_type -- event type submitted
        req_fields -- fields that are required for event type
    """

    def __init__(self, event_type, req_fields):
        super().__init__(f'Missing Event Required Data: "{event_type}" requires the following fields: {req_fields}')
