from datetime import datetime
import re
from typing import AnyStr
from uuid import UUID

from propus.helpers.exceptions import (
    InvalidStringLength,
    InvalidEmail,
    InvalidPhoneNumber,
    InvalidDateStructure,
    InvalidDayOfWeek,
    InvalidUUID,
    InvalidListElement,
    InvalidField,
    InvalidSalesforceId,
    MissingRequiredKeyError,
    MissingOneRequiredKeyError,
)
from propus.logging_utility import Logging


logger = Logging.get_logger("input_validations.py")


def validate_learner_status_transition(from_status, to_status):
    learner_status_map = {
        None: ["Expressed Interest", "App Submitted"],
        "Expressed Interest": ["App Started"],
        "App Started": ["App Submitted"],
        "App Submitted": ["Ready for Onboarding", "Started Orientation"],
        "Ready for Onboarding": ["Started Orientation"],
        "Started Orientation": ["Completed Orientation"],
        "Completed Orientation": ["Completed CSEP"],
        "Completed CSEP": ["Enrolled in Program Pathway"],
        "Enrolled in Program Pathway": ["Dropped", "Started Program Pathway"],
        "Started Program Pathway": ["Dropped", "Completed Program Pathway"],
        "Dropped": ["Expressed Interest", "App Submitted"],
        "Completed Program Pathway": ["Expressed Interest", "App Submitted"],
    }
    if not learner_status_map.get(from_status):
        raise InvalidField("from_status", from_status)
    if to_status not in learner_status_map.get(from_status):
        raise InvalidField("to_status", to_status)
    return True


def validate_string_length(string, key_name, min_len=1, max_len=10, is_required: bool = True):
    """
    Validates the length of a string.

    Args:
        string (str): The string to be validated.
        key_name (str): The name of the key or field being validated.
        min_len (int, optional): Minimum allowed length (default is 1).
        max_len (int, optional): Maximum allowed length (default is 10).
        is_required (bool, optional): Flag indicating if the string is required (default is True).

    Raises:
        InvalidStringLength: If the length of the string is outside the specified range.
    """
    if is_required:
        validate_not_none(string, key_name)
    elif string is None:
        return

    if len(string) > max_len or len(string) < min_len:
        raise InvalidStringLength(key_name, min_len, max_len)


def validate_phone_number(
    phone_number, phone_format="(NNN) NNN-NNNN", key_name="phone number", is_required: bool = False
):
    """
    Validates a phone number based on a specified format.

    Args:
        phone_number (str): The phone number to be validated.
        phone_format (str, optional): The expected phone number format (default is "(NNN) NNN-NNNN").
        key_name (str, optional): The name of the key or field being validated (default is "phone number").
        is_required (bool, optional): Flag indicating if the phone number is required (default is False).

    Raises:
        InvalidPhoneNumber: If the phone number does not match the specified format.
    """
    if is_required:
        validate_not_none(phone_number, key_name)
    elif phone_number is None:
        return

    if phone_format == "(NNN) NNN-NNNN":
        if not re.fullmatch(r"^\([0-9]{3}\) [0-9]{3}-[0-9]{4}", phone_number):
            raise InvalidPhoneNumber(phone_number, phone_format, key_name)
    elif phone_format == "N" * 10:
        if not re.fullmatch(r"^[0-9]{10}", phone_number):
            raise InvalidPhoneNumber(phone_number, phone_format, key_name)
    elif phone_format == "e164":
        if not re.fullmatch(r"^\+[1-9]\d{1,14}$", phone_number):
            raise InvalidPhoneNumber(phone_number, phone_format, key_name)
    else:
        raise InvalidPhoneNumber(phone_number, "<Phone Format Not recognized>", key_name)


def validate_date(date, date_structure, key_name="date"):
    """
    Validates a date string based on a specified date structure.

    Args:
        date (str): The date string to be validated.
        date_structure (str): The expected date structure (e.g., "YYYY/MM/DD" or "YYYY-MM-DD").
        key_name (str, optional): The name of the key or field being validated (default is "date").

    Raises:
        InvalidDateStructure: If the date string does not match the specified structure.
    """
    date_structure_map = {
        "YYYY/MM/DD": re.fullmatch(r"^[0-9]{4}/[0-9]{2}/[0-9]{2}", date),
        "YYYY-MM-DD": re.fullmatch(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}", date),
    }
    for structure, regex_match in date_structure_map.items():
        if structure == date_structure:
            if not regex_match:
                raise InvalidDateStructure(date, date_structure, f"date ({date_structure})")
            return
    try:
        validate_not_none(date, "date")
        datetime.strptime(date, date_structure)
    except ValueError:
        raise InvalidDateStructure(date, date_structure, key_name)


def validate_email(email: AnyStr, key_name: AnyStr = "email", is_required: bool = False):
    """
    email validity checking. Returns error is an invalid email is sent

    Args:
        email (AnyStr): email variable to be checked
        key_name (AnyStr): name of the data type (i.e. email, calbright_email)

    Raises:
        InvalidAPIUsage: Raises an error to be returned to user if it does not pass this check
    """
    if is_required:
        validate_not_none(email, key_name)
    elif email is None:
        return
    if not re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
        raise InvalidEmail(email, key_name)


def validate_day_of_week(date, day_of_week, key_name):
    """
    Validates if a given date corresponds to a specific day of the week.

    Args:
        date (datetime.date): The date to be validated.
        day_of_week (int): The expected day of the week (Monday is 0 and Sunday is 6).
        key_name (str): The name of the key or field being validated.

    Raises:
        InvalidDayOfWeek: If the date does not correspond to the specified day of the week.
    """
    if date.weekday() != day_of_week:
        raise InvalidDayOfWeek(key_name)


def validate_uuid(uuid_to_test, version=4):
    """
    Check if `uuid_to_test` is a valid UUID.

    Args:
        uuid_to_test (str): The UUID string to be validated.
        version (int, optional): The UUID version (valid values: 1, 2, 3, 4).

    Returns:
        None: If `uuid_to_test` is a valid UUID.

    Raises:
        InvalidUUID: If `uuid_to_test` is not a valid UUID.

    Examples:
        >>> validate_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
        (Valid)

        >>> validate_uuid('c9bf9e57')
        InvalidUUID: UUID "c9bf9e57 (UUID version 4)" is an invalid UUID
    """
    try:
        _ = UUID(uuid_to_test, version=version)
    except ValueError:
        raise InvalidUUID(f"{uuid_to_test} (UUID version {version})")


def validate_element_in_list(element, list, key_name):
    """
    Validates the item against a list of valid items.

    Args:
        element: Item to validate
        list: List of valid items
        key_name (str): Name of the item being validated (for error message)

    Raises:
        InvalidListElement: If the item is not valid
    """
    if element not in list:
        raise InvalidListElement(element, list, key_name)


def validate_salesforce_id(sf_id, key_name="Salesforce Id", starts_with=""):
    """
    Validates a Salesforce ID.

    Args:
        sf_id (str): Salesforce ID to be validated.
        key_name (str, optional): Title of the Salesforce ID being validated (default is "Salesforce Id").
        starts_with (str, optional): The expected starting characters for the Salesforce ID (default is "003").


    Raises:
        InvalidAPIUsage: If the ID is invalid.
    """
    if not sf_id.startswith(starts_with):
        raise InvalidSalesforceId(key_name, starts_with)
    validate_string_length(sf_id, key_name, 15, 18)


def perform_validations(data, field_validations):
    """
    Validates the specified fields in the incoming data based on provided
    validation rules.

    Args:
        data (dict): Incoming data.
        field_validations (list of tuples): A list of tuples, where each tuple
            contains the field name, validation function, and validation
            arguments.
            In the field_validations list, each tuple has the structure (field_name, validation_func, *validation_args).
            The *validation_args syntax is used to capture any number of positional arguments that validation_func
            accepts.
                field_name: The name of the field to be validated.
                validation_func: The function used for validation.
                validation_args: list containing all the positional arguments passed for a particular validation.

    Returns:
        bool: True if all validations pass, False otherwise.

    Raises:
        InvalidAPIUsage: If any of the data fields are invalid or missing.

    Example:
        data = {
            "WhoId": "003ABC",
            "Id": "00UXYZ",
            "OwnerId": "005PQR",
            "Subject": "Meeting",
            "ActivityDate": "2023-12-31",
            "StartDateTime": "2023-12-31T10:00:00",
            "EndDateTime": "2023-12-31T12:00:00",
        }

        field_validations = [
            ("WhoId", validate_salesforce_id, ["WhoId"]),
            ("Id", validate_salesforce_id, ["Id", "00U"]),
            ("OwnerId", validate_salesforce_id, ["OwnerId", "005"]),
            # String length validations
            ("Subject", validate_string_length, ["Subject", 0, 200]) if data.get("Subject") else None,
            ("ActivityDateTime", validate_date, ["ActivityDateTime"]) if data.get("ActivityDate") else None,
            ("ActivityDate", validate_date, ["ActivityDate", "%Y-%m-%d"]) if data.get("ActivityDate") else None,
            ("StartDateTime", validate_date, ["StartDateTime"]) if data.get("StartDateTime") else None,
            ("EndDateTime", validate_date, ["EndDateTime"]) if data.get("EndDateTime") else None,
        ]

        # Remove None values from field_validations list
        field_validations = [validation for validation in field_validations if validation is not None]

        perform_validations(data, field_validations)

        In this example, the perform_validations function is used to validate various Salesforce fields
        such as WhoId, Id, OwnerId, Subject, ActivityDate, StartDateTime, and EndDateTime based on specified rules.
    """
    for field_name, validation_func, *validation_args in field_validations:
        field_value = data.get(field_name)
        try:
            if validation_args == []:
                validation_func(field_value)
            else:
                # validation_args is a list containing all the positional arguments passed for a particular validation.
                # Since validation_args is a list, we use *validation_args[0] to unpack its elements and pass them as
                # separate arguments to the validation function.
                validation_func(field_value, *validation_args[0])
        except Exception as e:
            logger.warning(e)
            raise InvalidField(field_name, field_value)


def validate_not_none(data, key_name: AnyStr):
    """
    Checks if the data supplied is valid

    Args:
        data (AnyType): data variable to be checked
        key_name (AnyStr): name of the data type (i.e. fistName, lastName)

    Raises:
        InvalidAPIUsage: Raises an error to be returned to user if it does not pass this check
    """
    if data is None:
        raise MissingRequiredKeyError(key_name)


def validate_value_exists_in_table(session, model, column_name, value):
    """
    Validates if a given value exists in the specified column of the specified
    model.

    Args:
        session: SQLAlchemy database session
        model: The SQLAlchemy model to perform the lookup on
        column_name (str): The name of the column to perform the lookup on
        value: The value to check for existence

    Raises:
        ValueError: If the value does not exist in the specified column
    """
    # Create a dynamic filter for the specified column and value
    filter_condition = {column_name: value}

    # Perform the lookup
    record = session.query(model).filter_by(**filter_condition).first()

    if not record:
        raise ValueError(
            f"The value '{value}' does not exist in the "
            f"{column_name} column of the {model.__tablename__} "
            f"table."
        )


def validate_at_least_one_required_key_present(data, keys):
    """
    Validates that at least one of the specified keys is present in the data dictionary.

    Args:
        data (dict): The data dictionary to check for field presence.
        keys (list): A list of keys names to check for presence.

    Raises:
        InvalidAPIUsage: If none of the required fields are present in the data dictionary.
    """
    if not any(data.get(key) for key in keys):
        raise MissingOneRequiredKeyError(keys)
