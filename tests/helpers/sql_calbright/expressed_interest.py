import unittest
from unittest.mock import patch, MagicMock, Mock

from propus.helpers.sql_calbright.expressed_interest import create_expressed_interest_record
from propus.calbright_sql.user import User
from propus.calbright_sql.expressed_interest import ExpressInterest, LeadSource, BrowserType
from propus.calbright_sql.program import Program


class TestExpressedInterestHelper(unittest.TestCase):
    def setUp(self):
        self.new_program_id = "ZXY_PROGRAM_9876"
        self.program_id = "ABC_PROGRAM_1234"
        session_mock = MagicMock()
        session_mock.add = Mock(side_effect=self.session_add)
        self.mock_data = {
            "session": session_mock,
            "user": User(
                id="USER_ID_1234", expressed_interest_user=[ExpressInterest(program_interest_id=self.program_id)]
            ),
            "program_interest_id": "Cyber;It;Networks",
        }
        self.session_add_called = False

    @patch("propus.helpers.sql_calbright.expressed_interest.find_enum_value")
    @patch("propus.helpers.sql_calbright.expressed_interest.fetch_programs_by_name")
    def test_create_expressed_interest_record_no_programs(self, mock_fetch_programs_by_name, mock_find_enum_value):
        self.assertIsNone(create_expressed_interest_record(None, None, {}))

        mock_fetch_programs_by_name.return_value = []
        create_expressed_interest_record(
            session=self.mock_data.get("session"),
            user=self.mock_data.get("user"),
            expressed_interest_data={"program_interest_id": self.mock_data.get("program_interest_id")},
        )
        mock_fetch_programs_by_name.assert_called_once_with(
            self.mock_data.get("session"), self.mock_data.get("program_interest_id").split(";")
        )
        mock_find_enum_value.assert_not_called()

    @patch("propus.helpers.sql_calbright.expressed_interest.find_enum_value")
    @patch("propus.helpers.sql_calbright.expressed_interest.fetch_programs_by_name")
    def test_create_expressed_interest_record_no_new_programs(self, mock_fetch_programs_by_name, mock_find_enum_value):
        mock_fetch_programs_by_name.return_value = [Program(id=self.program_id)]
        create_expressed_interest_record(
            session=self.mock_data.get("session"),
            user=self.mock_data.get("user"),
            expressed_interest_data={"program_interest_id": self.mock_data.get("program_interest_id")},
        )
        mock_fetch_programs_by_name.assert_called_once_with(
            self.mock_data.get("session"), self.mock_data.get("program_interest_id").split(";")
        )
        mock_find_enum_value.assert_not_called()

    @patch("propus.helpers.sql_calbright.expressed_interest.fetch_programs_by_name")
    def test_create_expressed_interest_record(self, mock_fetch_programs_by_name):
        mock_fetch_programs_by_name.return_value = [Program(id=self.new_program_id)]
        create_expressed_interest_record(
            session=self.mock_data.get("session"),
            user=self.mock_data.get("user"),
            expressed_interest_data={
                "program_interest_id": self.mock_data.get("program_interest_id"),
                "lead_source": "Social Media",
                "browser_type": "Mobile",
            },
        )
        mock_fetch_programs_by_name.assert_called_once_with(
            self.mock_data.get("session"), self.mock_data.get("program_interest_id").split(";")
        )
        self.assertTrue(self.session_add_called)

    def session_add(self, obj):
        self.assertTrue(isinstance(obj, ExpressInterest))
        self.assertEqual(obj.program_interest_id, self.new_program_id)
        self.assertEqual(obj.lead_source, LeadSource.social_media)
        self.assertEqual(obj.browser_type, BrowserType.mobile)
        self.session_add_called = True


if __name__ == "__main__":
    unittest.main()
