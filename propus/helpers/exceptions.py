class InvalidStringLength(Exception):
    """Exception raised for invalid string lengths

    Attributes:
        key_name: name of key supplied
        min_len: min length of variable
        max_len: max length of variable
    """

    def __init__(self, key_name, min_len, max_len):
        super().__init__(f'Passed key "{key_name}" is an invalid length(max: {max_len}, min: {min_len})')


class InvalidEmail(Exception):
    """Exception raised for invalid email input

    Attributes:
        email_input -- email input supplied
        key_name -- name of the key
    """

    def __init__(self, email_input, key_name):
        super().__init__(f'{key_name} "{email_input}" is an invalid email')


class InvalidPhoneNumber(Exception):
    """Exception raised for invalid phone number input

    Attributes:
        phone_input -- phone number input supplied
        key_name -- name of the key
    """

    def __init__(self, phone_input, phone_format, key_name):
        super().__init__(f'{key_name} "{phone_input}" is an invalid phone number. Must match {phone_format}')


class InvalidDateStructure(Exception):
    """Exception raised for invalid date of date structure

    Attributes:
        dob_input -- email input supplied
    """

    def __init__(self, value, structure, key_name):
        super().__init__(f'{key_name} "{value}" is an invalid. Must match {structure} format')


class InvalidDayOfWeek(Exception):
    """Exception raised for invalid day of week passed in

    Attributes:
        key_name -- name of key being tested
    """

    def __init__(self, key_name):
        super().__init__(f"{key_name} is an invalid day of week")


class InvalidUUID(Exception):
    """Exception raised for invalid uuid input

    Attributes:
        uuid_input -- uuid input supplied
    """

    def __init__(self, uuid_input):
        super().__init__(f'UUID "{uuid_input}" is an invalid UUID')


class InvalidListElement(Exception):
    """Exception raised for invalid list element

    Attributes:
        element -- element that is invalid
        list -- list of valid elements
        key_name -- name of the key
    """

    def __init__(self, element, list, key_name):
        super().__init__(f"Invalid {key_name}: {element} not found in {list}")


class InvalidDataAttribute(Exception):
    """Exception raised for missing or invalid data attribute

    Attributes:
        attribute -- attribute that is missing or invalid
        valid_types -- list of valid data types
        key_name -- name of the key
    """

    def __init__(self, attribute_type, missing=False):
        if missing:
            super().__init__("Missing Attributes: Received data does not have the expected 'attributes' key'")
        else:
            super().__init__(f"Invalid Attributes: Received data type is not '{attribute_type}'")


class InvalidField(Exception):
    """Exception raised for an invalid field value.

    Attributes:
        field_name -- name of the invalid field
        field_value -- value received for the field
    """

    def __init__(self, field_name, field_value):
        super().__init__(f"Invalid {field_name}: Received value '{field_value}'")


class InvalidSalesforceId(Exception):
    """Exception raised for an invalid Salesforce ID.

    Attributes:
        key_title -- title of the Salesforce ID being validated
        starts_with -- expected starting characters for the Salesforce ID
    """

    def __init__(self, key_title, starts_with):
        super().__init__(f"{key_title} should start with {starts_with}")


class EntryNotFoundError(Exception):
    """Exception raised when a certain entry is not found in a table

    Attributes:
        entry_id -- the identifier of the missing entry
        table_name -- the name of the table where the entry is expected
    """

    def __init__(self, entry_id, table_name):
        super().__init__(f"Entry with ID {entry_id} not found in the {table_name} table")


class MappingError(Exception):
    """Exception raised for a mapping error when a value is not found in a table's column.

    Attributes:
        column -- the column that is not found in the table
        value -- the corresponding value for the key
        table_name -- the name of the table where the key-value pair is expected
    """

    def __init__(self, column, value, table_name):
        super().__init__(f"{column} '{value}' not found in table {table_name}")


class JSONDecodeError(Exception):
    """Exception raised for an invalid JSON object.

    Attributes:
        data -- invalid JSON data
    """

    def __init__(self, data):
        super().__init__(f"Invalid JSON: {data}")


class MissingRequiredKeyError(Exception):
    """Exception raised for a missing required key.

    Attributes:
        key_name -- name of the missing key
    """

    def __init__(self, key_name):
        super().__init__(f"Missing Key: {key_name} is required")


class MissingOneRequiredKeyError(Exception):
    """Exception raised when at least one of the required keys is missing.

    Attributes:
        keys -- list of required keys that are missing
    """

    def __init__(self, keys):
        super().__init__(f"At least one of the required keys {keys} must be present")


class InvalidKeyList(Exception):
    """Exception raised for invalid key list

    Attributes:
        invalid_keys: Composite key containing the invalid key
    """

    def __init__(self, invalid_key):
        super().__init__(f"Invalid key in the key list: {invalid_key}")


class MissingCourseLmsId(Exception):
    """Exception raised for missing course lms id

    Attributes:
        course_id: course id
    """

    def __init__(self, course_version_id):
        super().__init__(f"Missing course lms id for course version id: {course_version_id}")


class MissingCanvasUserId(Exception):
    """Exception raised for missing canvas user id

    Attributes:
        user_id: user id
    """

    def __init__(self, ccc_id):
        super().__init__(f"Missing canvas user id for ccc_id: {ccc_id}")


class NoEnrollmentFound(Exception):
    """Exception raised for missing enrollment

    Attributes:
        ccc_id: ccc_id
    """

    def __init__(self, ccc_id):
        super().__init__(f"No enrollment found for ccc_id: {ccc_id}")


class NoCourseEnrollmentsFound(Exception):
    """Exception raised for missing course enrollments

    Attributes:
        course_id: course_id
    """

    def __init__(self, ccc_id):
        super().__init__(f"No enrollments found for ccc_id: {ccc_id}")
