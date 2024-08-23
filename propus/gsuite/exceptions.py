class UserUpdateMissingFields(Exception):
    """Exception raised for update called without any fields to be updated"""

    def __init__(self):
        super().__init__("user update called with no fields to be updated")


class UserCreateRequestsReached(Exception):
    """Exception raised for reaching max request amount on generating new user"""

    def __init__(self):
        super().__init__("user create reached max requests without creating new user")


class UserAttemptingToCreateExists(Exception):
    """Exception raised for attempting to create existing user"""

    def __init__(self):
        super().__init__("user attempting to create already exists")


class LicensingException(Exception):
    """Exception raised by the licensing client"""

    def __init__(self, msg, method=None, **kwargs):
        super().__init__(f"Licensing exception for method {method} with kwargs {kwargs}: {msg}")
