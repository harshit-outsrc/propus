import unittest
from unittest.mock import MagicMock

from propus.gsuite import Licensing


class TestGSuiteLicensing(unittest.TestCase):
    def setUp(self) -> None:
        self.response = {
            "productId": "101031",
            "userId": "test@calbrightcollege.org",
            "selfLink": "https://licensing.googleapis.com/apps/licensing/v1/product/101031/sku/1010310003/user/test@calbrightcollege.org",
            "skuId": "1010310003",
        }
        self.no_data = {}
        self.test_data = {
            "calbright_email": "test@calbrightcollege.org",
            "product_id": "1234",
            "sku_id": "4321",
        }
        self.bad_data = {
            "calbright_email": "broken@calbright",
        }
        licensing = MagicMock()
        licensing.licenseAssignments().get().execute = MagicMock(return_value=self.response)
        licensing.licenseAssignments().delete().execute = MagicMock(return_value=self.response)
        self.client = Licensing(client=licensing)

    def test_get_license(self):
        self.test_name = "get_license"
        self.assertEqual(self.client.get_license(**self.test_data), self.response)

    def test_delete_license(self):
        self.test_name = "delete_license"
        self.client.test_name = "delete_license"
        self.assertEqual(
            self.client.get_license(**self.test_data),
            self.response,
        )

    def test_delete_license_error(self):
        self.test_name = "delete_license_error"
        with self.assertRaises(Exception):
            self.client.delete_license(**self.no_data)

    def test_get_license_error(self):
        self.test_name = "get_license_error"
        with self.assertRaises(Exception):
            self.client.get_license(**self.no_data)

    def test_delete_license_email_error(self):
        self.test_name = "delete_license_email_error"
        with self.assertRaises(Exception):
            self.client.delete_license(**self.bad_data)

    def test_get_license_email_error(self):
        self.test_name = "get_license_email_error"
        with self.assertRaises(Exception):
            self.client.get_license(**self.bad_data)


if __name__ == "__main__":
    unittest.main()
