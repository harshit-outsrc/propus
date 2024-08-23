import unittest

from propus.helpers.salesforce import validate_data_attribute_type


class TestSalesforceInputValidations(unittest.TestCase):
    def setUp(self):
        self.data = {
            "attributes": {"type": "Contact", "url": "/services/data/v56.0/sobjects/Contact/0033k00003LwIHhAAN"}
        }

    def test_valid_contact_data_type(self):
        # This should not raise any exception
        self.assertIsNone(validate_data_attribute_type(self.data["attributes"], "Contact"))


if __name__ == "__main__":
    unittest.main()
