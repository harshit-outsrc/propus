import unittest

from mock_alchemy.mocking import AlchemyMagicMock
from unittest.mock import patch, MagicMock

from propus.helpers.anthology import (
    get_anthology_user,
    update_student,
    update_student_course,
)
from propus.calbright_sql.user import User
from propus.helpers.exceptions import EntryNotFoundError


class TestAnthologyHelpers(unittest.TestCase):
    def setUp(self) -> None:
        # Test data
        self.user = User(first_name="foo", last_name="bar", ccc_id="FOOBAR1", anthology_id=-1)
        session = AlchemyMagicMock()
        session.add(self.user)
        session.commit()
        self.session = session
        self.salesforce = MagicMock()
        self.bad_data = {"firstName": "User", "middleName": "Does Not", "lastName": "Exist", "ccc_id": "BARBAZ2"}
        self.course_data = {"previousStatus": 0, "status": 10}
        self.student_data = {"middleName": "baz", "studentNumber": "FOOBAR1"}

    @patch("propus.salesforce._contact_record.update_contact_record")
    @patch("propus.helpers.sql_alchemy.upsert_changes")
    def test_update_student(self, upsert_changes_mock, salesforce_mock):
        upsert_changes_mock.return_value = {"middle_name": "baz"}, True
        salesforce_mock.return_value = {"response": {"data": {"foo": "bar"}}}
        update_student(self.session, self.salesforce, self.student_data)

    @patch("propus.salesforce._contact_record.update_contact_record")
    @patch("propus.helpers.anthology.create_learner_status_map")
    @patch("propus.helpers.anthology.get_anthology_user")
    def test_update_student_course(self, get_user_mock, status_map_mock, salesforce_mock):
        get_user_mock.return_value = self.user
        status_map_mock.return_value = {0: "Foo", 6: "bar", 10: "baz"}
        salesforce_mock.return_value = {"response": {"data": {"foo": "bar"}}}
        update_student_course(self.session, self.salesforce, self.course_data)

    @patch("propus.helpers.anthology.select")
    def test_get_student_error(self, mock_select):
        mock_select.return_value = self.user
        with self.assertRaises(EntryNotFoundError):
            get_anthology_user(self.session, self.bad_data)


if __name__ == "__main__":
    unittest.main()
