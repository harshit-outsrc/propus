import unittest
from unittest.mock import MagicMock, Mock

from propus.gsuite import Sheets, MissingRequirements
from gspread.exceptions import WorksheetNotFound


class TestGoogleSheets(unittest.TestCase):
    def setUp(self) -> None:
        google_client = MagicMock()
        google_client.open_by_url = Mock(side_effect=self.open_by_url)
        self.sheets = Sheets(google_client)
        self.document_url = "https://blah.blah.calbright.google.com/gsheets/hello"
        self.expected_response = "this is the worksheet response"
        self.update_test_data = {
            "a1_notation": "ABCD:1234",
            "row_num": 1234,
            "cell_num": 4321,
            "content": "This is the new cell content",
        }
        self.sheet_number = 12
        self.sheet_tab = 0
        self.test_name = None
        self.func_called = None

    def test_fetch_sheet(self):
        self.test_name = "successful_flow"
        self.assertEqual(
            self.sheets.fetch_sheet(self.document_url, self.sheet_number),
            self.expected_response,
        )

    def test_append_row(self):
        self.test_name = "append_row"
        self.sheets.fetch_sheet = Mock()

        self.sheets.append_row(self.sheet_number, ["value", "value"])
        self.sheets.fetch_sheet.assert_called_with(
            f"https://docs.google.com/spreadsheets/d/{self.sheet_number}", self.sheet_tab
        )

    def test_fetch_sheet_error(self):
        self.test_name = "test_worksheet_not_found"
        self.assertIsNone(self.sheets.fetch_sheet(self.document_url, self.sheet_number))

    def open_by_url(self, url):
        self.assertEqual(url, self.document_url)
        worksheet_mock = MagicMock()
        worksheet_mock.get_worksheet = self.get_worksheet
        return worksheet_mock

    def get_worksheet(self, sheet_tab):
        if self.test_name == "test_worksheet_not_found":
            raise WorksheetNotFound("no worksheet found")
        self.assertEqual(sheet_tab, self.sheet_number)
        return self.expected_response

    def test_update_error(self):
        with self.assertRaises(MissingRequirements):
            self.sheets.update_cell("worksheet", "content")

        with self.assertRaises(MissingRequirements):
            self.sheets.update_cell("worksheet", "content", cell_num=123)

        with self.assertRaises(MissingRequirements):
            self.sheets.update_cell("worksheet", "content", row_num=123)

    def update(self, var1, var2, var3=None):
        if self.test_name == "update_by_a1_notation":
            self.assertEqual(var1, self.update_test_data.get("a1_notation"))
            self.assertEqual(var2, self.update_test_data.get("content"))
            self.assertIsNone(var3)
        else:
            self.assertEqual(var1, self.update_test_data.get("row_num"))
            self.assertEqual(var2, self.update_test_data.get("cell_num"))
            self.assertEqual(var3, self.update_test_data.get("content"))
        self.func_called = self.test_name

    def test_update_cell(self):
        worksheet = MagicMock()
        worksheet.update = Mock(side_effect=self.update)
        worksheet.update_cell = Mock(side_effect=self.update)

        self.test_name = "update_by_a1_notation"
        self.assertIsNone(
            self.sheets.update_cell(
                worksheet,
                self.update_test_data.get("content"),
                a1_notation=self.update_test_data.get("a1_notation"),
            )
        )
        self.assertEqual(self.func_called, self.test_name)

        self.test_name = "update_by_row_cell"
        self.assertIsNone(
            self.sheets.update_cell(
                worksheet,
                self.update_test_data.get("content"),
                row_num=self.update_test_data.get("row_num"),
                cell_num=self.update_test_data.get("cell_num"),
            )
        )
        self.assertEqual(self.func_called, self.test_name)


if __name__ == "__main__":
    unittest.main()
