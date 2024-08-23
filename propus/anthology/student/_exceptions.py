class StudentUpdateMissingFields(Exception):
    """Exception raised for update called without any fields to be updated"""

    def __init__(self):
        super().__init__("student update called with no fields to be updated")


class InvalidSearchParameters(Exception):
    """Exception raised for no or invalid search parameters supplied"""

    def __init__(self):
        super().__init__("no or invalid search parameters supplied")
