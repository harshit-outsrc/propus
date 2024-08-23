class EmailFailedToSend(Exception):
    """Exception raised when an email fails to send

    Attributes:
        status_code -- status code from API request
        reason -- explanation of failure
    """

    def __init__(self, status_code, reason):
        super().__init__(f"email failed to send (status: {status_code}): {reason}")


class ApiNotSuccessful(Exception):
    """Exception raised when an api call is not successful

    Attributes:
        status_code -- status code from API request
        reason -- explanation of failure
    """

    def __init__(self, status_code, reason):
        super().__init__(f"API returned non 200 status (status: {status_code}): {reason}")
