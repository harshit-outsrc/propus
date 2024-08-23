import unittest
from unittest.mock import MagicMock, Mock, patch

from propus.helpers.sql_calbright.contact import update_address, update_contact_preferences
from propus.calbright_sql.address import Address
from propus.calbright_sql.student import Student
from propus.calbright_sql.student_address import StudentAddress
from propus.calbright_sql.student_contact_time import StudentContactTime
from propus.calbright_sql.preferred_contact_time import PreferredContactTime
from propus.calbright_sql.preferred_contact_method import PreferredContactMethod
from propus.calbright_sql.student_contact_method import StudentContactMethod


class TestContactHelper(unittest.TestCase):
    def setUp(self):
        self.test_name = ""
        self.session_called_times = 0

        self.session_mock = MagicMock()
        self.session_mock.add = Mock(side_effect=self.session_add)
        self.session_mock.delete = Mock(side_effect=self.session_delete)
        self.ccc_id = "TEST_1234_CCC_ID"
        self.address_data = {
            "address1": "123 Main Street",
            "city": "Sacramento",
            "state": "CA",
            "zip": "94203",
            "country": "US",
        }

    def test_update_address(self):
        self.test_name = "update_address"
        self.session_called_times = 0
        update_address(self.session_mock, None, None)
        self.assertEqual(self.session_called_times, 0)
        update_address(self.session_mock, None, {"1": "1", "2": "2"})
        self.assertEqual(self.session_called_times, 0)

        update_address(
            session=self.session_mock,
            student=Student(
                student_address=[
                    StudentAddress(
                        address=Address(**self.address_data),
                        current=True,
                    )
                ],
            ),
            address_data=self.address_data,
        )
        self.assertEqual(self.session_called_times, 0)

        update_address(
            session=self.session_mock,
            student=Student(
                ccc_id=self.ccc_id,
                student_address=[
                    StudentAddress(
                        address=Address(**(self.address_data | {"address1": "125 Main Street", "city": "Nowhere"})),
                        current=True,
                    )
                ],
            ),
            address_data=self.address_data,
        )
        self.assertEqual(self.session_called_times, 2)

    @patch("propus.helpers.sql_calbright.contact.create_field_map_from_composite_key")
    def test_update_contact_preferences(self, mock_create_field_map_from_composite_key):
        self.test_name = "update_contact_prefs"
        self.session_called_times = 0
        mock_create_field_map_from_composite_key.return_value = {"now": "NOW_123", "later": "LATER_123"}
        update_contact_preferences(
            self.session_mock,
            student=Student(
                ccc_id=self.ccc_id,
                student_preferred_contact_time=[
                    StudentContactTime(
                        preferred_contact_time=PreferredContactTime(id="NOW_123", preferred_contact_time="now")
                    )
                ],
            ),
            new_data="later",
            req_type="time",
        )
        self.assertEqual(self.session_called_times, 1)

        mock_create_field_map_from_composite_key.return_value = {"phone": "PHONE_123", "email": "EMAIL_123"}
        update_contact_preferences(
            self.session_mock,
            student=Student(
                ccc_id=self.ccc_id,
                student_preferred_contact_method=[
                    StudentContactMethod(
                        preferred_contact_method=PreferredContactMethod(
                            id="EMAIL_123", preferred_contact_method="email"
                        )
                    )
                ],
            ),
            new_data="email;phone",
            req_type="method",
        )
        self.assertEqual(self.session_called_times, 2)

    def session_delete(self, obj):
        self.assertIsInstance(obj, StudentContactTime)
        self.assertEqual(obj.preferred_contact_time.id, "NOW_123")

    def session_add(self, obj):
        self.session_called_times += 1
        if self.test_name == "update_address" and self.session_called_times == 1:
            self.assertIsInstance(obj, Address)
            self.assertEqual(obj.address1, self.address_data.get("address1"))
            self.assertEqual(obj.city, self.address_data.get("city"))
            self.assertEqual(obj.state, self.address_data.get("state"))
            self.assertEqual(obj.zip, self.address_data.get("zip"))
            self.assertEqual(obj.country, self.address_data.get("country"))
            self.assertEqual(obj.county, "Sacramento")
        elif self.test_name == "update_address" and self.session_called_times == 2:
            self.assertIsInstance(obj, StudentAddress)
            self.assertEqual(obj.student_id, self.ccc_id)
            self.assertIsInstance(obj.address, Address)
        elif self.test_name == "update_contact_prefs" and self.session_called_times == 1:
            self.assertIsInstance(obj, StudentContactTime)
            self.assertEqual(obj.contact_time_id, "LATER_123")
            self.assertEqual(obj.ccc_id, self.ccc_id)
        elif self.test_name == "update_contact_prefs" and self.session_called_times == 2:
            self.assertIsInstance(obj, StudentContactMethod)
            self.assertEqual(obj.contact_method_id, "PHONE_123")
            self.assertEqual(obj.ccc_id, self.ccc_id)


if __name__ == "__main__":
    unittest.main()
