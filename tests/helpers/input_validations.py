import unittest

from unittest.mock import MagicMock

from propus.helpers.input_validations import (
    validate_element_in_list,
    validate_not_none,
    validate_string_length,
    validate_email,
    validate_phone_number,
    validate_value_exists_in_table,
    validate_at_least_one_required_key_present,
    validate_date,
    validate_salesforce_id,
)
from propus.helpers.exceptions import (
    InvalidListElement,
    MissingRequiredKeyError,
    InvalidStringLength,
    InvalidEmail,
    InvalidPhoneNumber,
    MissingOneRequiredKeyError,
    InvalidDateStructure,
    InvalidSalesforceId,
)


class TestInputValidations(unittest.TestCase):
    def setUp(self):
        self.valid_statuses = [
            "App Submitted",
            "Ready for Onboarding",
            "Started Orientation",
            "Completed Orientation",
        ]
        self.learner_status_orientation = "Started Orientation"
        self.learner_status_leave = "On Leave"

        self.session = MagicMock()
        self.model = MagicMock()
        self.column_name = "some_column"
        self.value = "some_value"
        self.model.__tablename__ = "mock_table_name"
        self.valid_date_YYYY_MM_DD = "2023-12-06"
        self.valid_date_structure_YYYY_MM_DD = "YYYY-MM-DD"
        self.valid_custom_key_name = "custom_date_key"

        self.valid_date_YYYY_MM_DD_alternative_format = "2023/12/06"
        self.invalid_date_structure = "DD-MM-YYYY"
        self.invalid_date_string = "invalid_date"
        self.data = {
            "attributes": {"type": "Contact", "url": "/services/data/v56.0/sobjects/Contact/0033k00003LwIHhAAN"}
        }
        self.valid_id = "003ABCDE123456789"
        self.invalid_id_startswith = "005ABCDE123456789"  # Does not start with "003"
        self.invalid_id_length = "003ABCDE123456789000000"  # More than 18 characters
        self.valid_data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        self.missing_keys_data = {"key4": "value4", "key5": "value5"}
        self.empty_data = {}
        self.required_keys = ["key1", "key2", "key3"]

    def test_validate_element_in_list(self):
        # Test with a valid learner status
        self.assertIsNone(
            validate_element_in_list(self.learner_status_orientation, self.valid_statuses, "Learner Status")
        )

    def test_validate_element_not_in_list(self):
        # Test with an invalid learner status
        with self.assertRaises(InvalidListElement) as context:
            validate_element_in_list(self.learner_status_leave, self.valid_statuses, "learner status")
        self.assertEqual(
            str(context.exception),
            f"Invalid learner status: {self.learner_status_leave} not found in {self.valid_statuses}",
        )

    def test_check_required(self):
        error_caught = False
        try:
            validate_not_none(None, "keyName")
        except MissingRequiredKeyError as err:
            self.assertEqual(str(err), "Missing Key: keyName is required")
            error_caught = True
        self.assertTrue(error_caught)

        self.assertIsNone(validate_not_none("valid string", "keyName"))

    def test_check_valid_string(self):
        key_title = "keyName"

        error_caught = False
        try:
            validate_string_length("abcd", key_title, min_len=5)
        except InvalidStringLength as err:
            self.assertEqual(str(err), 'Passed key "keyName" is an invalid length(max: 10, min: 5)')
            error_caught = True
        self.assertTrue(error_caught)

        error_caught = False
        try:
            validate_string_length("abcdefghijk", key_title, max_len=5)
        except InvalidStringLength as err:
            self.assertEqual(str(err), 'Passed key "keyName" is an invalid length(max: 5, min: 1)')
            error_caught = True
        self.assertTrue(error_caught)

        self.assertIsNone(validate_string_length(None, key_title, is_required=False))
        self.assertIsNone(validate_string_length("1234", key_title))

    def test_check_valid_email(self):
        key_title = "emailTitle"

        error_caught = False
        try:
            validate_email("bad@bad_email", key_title)
        except InvalidEmail as err:
            self.assertEqual(str(err), 'emailTitle "bad@bad_email" is an invalid email')
            error_caught = True
        self.assertTrue(error_caught)

        self.assertIsNone(validate_email(None, key_title, is_required=False))
        self.assertIsNone(validate_email("you@me.com", key_title, is_required=False))

    def test_check_phone_number(self):
        key_title = "phoneNumber"

        error_caught = False
        try:
            validate_phone_number("bad(phone)-number", key_name=key_title)
        except InvalidPhoneNumber as err:
            self.assertEqual(
                str(err),
                'phoneNumber "bad(phone)-number" is an invalid phone number. Must match (NNN) NNN-NNNN',
            )
            error_caught = True
        self.assertTrue(error_caught)

        self.assertIsNone(validate_phone_number(None, key_name=key_title))
        self.assertIsNone(validate_phone_number("(123) 456-7890", key_name=key_title))

    def test_value_exists(self):
        # Mock a record existing with the specified value
        self.session.query().filter_by().first.return_value = MagicMock()

        # should not raise an error since the value exists
        validate_value_exists_in_table(self.session, self.model, self.column_name, self.value)

        # Mock no record existing with the specified value
        self.session.query().filter_by().first.return_value = None

        # should raise a ValueError since the value does not exist
        with self.assertRaises(ValueError):
            validate_value_exists_in_table(self.session, self.model, self.column_name, self.value)

    def test_valid_date_structure_YYYY_MM_DD(self):
        try:
            validate_date(self.valid_date_YYYY_MM_DD, self.valid_date_structure_YYYY_MM_DD)
        except InvalidDateStructure as e:
            self.assertEqual(str(e), 'date "2023-12-06" is an invalid. Must match YYYY-MM-DD format')

    def test_valid_date_structure_YYYY_MM_DD_with_custom_key_name(self):
        try:
            validate_date(self.valid_date_YYYY_MM_DD, self.valid_date_structure_YYYY_MM_DD, self.valid_custom_key_name)
        except InvalidDateStructure as e:
            self.assertEqual(str(e), 'custom_date_key "2023-12-06" is an invalid. Must match YYYY-MM-DD format')

    def test_valid_date_structure_YYYY_MM_DD_alternative_format(self):
        with self.assertRaises(InvalidDateStructure) as context:
            validate_date(self.valid_date_YYYY_MM_DD_alternative_format, self.valid_date_structure_YYYY_MM_DD)
        self.assertEqual(
            str(context.exception), 'date (YYYY-MM-DD) "2023/12/06" is an invalid. Must match YYYY-MM-DD format'
        )

    def test_invalid_date_structure(self):
        with self.assertRaises(InvalidDateStructure) as context:
            validate_date(self.valid_date_YYYY_MM_DD, self.invalid_date_structure)
        self.assertEqual(str(context.exception), 'date "2023-12-06" is an invalid. Must match DD-MM-YYYY format')

    def test_invalid_date_string(self):
        with self.assertRaises(InvalidDateStructure) as context:
            validate_date(self.invalid_date_string, self.valid_date_structure_YYYY_MM_DD)
        self.assertEqual(
            str(context.exception), 'date (YYYY-MM-DD) "invalid_date" is an invalid. Must match YYYY-MM-DD format'
        )

    def test_valid_salesforce_id(self):
        try:
            validate_salesforce_id(self.valid_id)
        except InvalidSalesforceId as e:
            self.fail(f"Unexpected InvalidSalesforceId exception: {str(e)}")

    def test_invalid_salesforce_id_startswith(self):
        with self.assertRaises(InvalidSalesforceId) as context:
            validate_salesforce_id(self.invalid_id_startswith, starts_with="003")
        self.assertEqual(str(context.exception), "Salesforce Id should start with 003")

    def test_invalid_salesforce_id_length(self):
        with self.assertRaises(InvalidStringLength) as context:
            validate_salesforce_id(self.invalid_id_length)
        self.assertEqual(str(context.exception), 'Passed key "Salesforce Id" is an invalid length(max: 18, min: 15)')

    def test_valid_data(self):
        # The function should not raise an exception for valid data
        try:
            validate_at_least_one_required_key_present(self.valid_data, self.required_keys)
        except MissingOneRequiredKeyError as e:
            self.fail(f"Unexpected exception: {e}")

    def test_missing_keys(self):
        # The function should raise MissingOneRequiredKeyError for missing keys
        with self.assertRaises(MissingOneRequiredKeyError) as context:
            validate_at_least_one_required_key_present(self.missing_keys_data, self.required_keys)

        # Check if the correct error message is raised
        expected_error_message = f"At least one of the required keys {self.required_keys} must be present"
        self.assertEqual(str(context.exception), expected_error_message)

    def test_empty_data(self):
        # The function should raise MissingOneRequiredKeyError for empty data
        with self.assertRaises(MissingOneRequiredKeyError) as context:
            validate_at_least_one_required_key_present(self.empty_data, self.required_keys)

        # Check if the correct error message is raised
        expected_error_message = f"At least one of the required keys {self.required_keys} must be present"
        self.assertEqual(str(context.exception), expected_error_message)


if __name__ == "__main__":
    unittest.main()
