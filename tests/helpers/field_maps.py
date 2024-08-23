import unittest

from propus.helpers.field_maps import extract_data_based_on_mapping


class TestFieldMaps(unittest.TestCase):
    def setUp(self):
        self.data = {
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "john.doe@example.com",
            "Phone": "1234567890",
        }
        self.dict_to_column_mapping = {
            "student": {
                "Email": "personal_email",
                "FirstName": "first_name",
                "LastName": "last_name",
                "Phone": "phone_number",
            }
        }

        self.expected_mapping_result = {
            "student": {
                "personal_email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "1234567890",
            }
        }
        self.empty_map = {}

    def test_extract_data_with_valid_mapping(self):
        result = extract_data_based_on_mapping(self.data, self.dict_to_column_mapping)
        self.assertDictEqual(result, self.expected_mapping_result)

    def test_extract_data_with_empty_mapping(self):
        result = extract_data_based_on_mapping(self.data, self.empty_map)
        self.assertDictEqual(result, self.empty_map)

    def test_extract_data_with_missing_key(self):
        key, value = next(iter(self.dict_to_column_mapping["student"].items()))
        self.data.pop(key)
        result = extract_data_based_on_mapping(self.data, self.dict_to_column_mapping)
        self.expected_mapping_result["student"].pop(value)
        self.assertDictEqual(result, self.expected_mapping_result)


if __name__ == "__main__":
    unittest.main()
