class SalesforceError(Exception):
    """Base Salesforce API exception

    Attributes:
        status_code -- status_code
        message -- message response from API
    """

    def __init__(self, status_code, message):
        super().__init__(f"Unknown error: {status_code} response with message: {message}")


class SalesforceOperationError(Exception):
    """Base error for Bulk API 2.0 operations

    Attributes:
        status_code -- status_code
        message -- message response from API
    """

    def __init__(self, message):
        super().__init__(f"Error on Bulk Query: {message}")


class SalesforceJobFailed(Exception):
    """Base error for Bulk API 2.0 operations

    Attributes:
        state -- job state
        job_id -- job id
        message -- message response from API
    """

    def __init__(self, job_state, job_id, number_records_processed):
        super().__init__(f"Error on Bulk Query: {job_state} - {job_id}, records processed {number_records_processed}")


class CreateContactUnknownRecordType(Exception):
    """Error raised when user selects unknown record type

    Attributes:
        record_type -- supplied record type
    """

    def __init__(self, record_type):
        super().__init__(f"record_type of {record_type} not accepted. Options are learner, visitor, vendors, employer")


class CreateContactMissingFields(Exception):
    """Error raised when required fields are not supplied

    Attributes:
        required_fields -- field missing for creating a contact
    """

    def __init__(self, required_fields):
        super().__init__(f"Missing required field for contact creation: {required_fields}")


class CreateCaseUnknownRecordType(Exception):
    """Error raised when user selects unknown record type

    Attributes:
        record_type -- supplied record type
    """

    def __init__(self, record_type):
        super().__init__(f"Record type of {record_type} not accepted.")


class CreateCaseMissingFields(Exception):
    """Error raised when required fields are not supplied

    Attributes:
        required_fields -- field missing for creating a case
    """

    def __init__(self, required_fields, case_type):
        super().__init__(f"Missing required field for {case_type} case creation: {required_fields}")
