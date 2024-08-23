from typing import AnyStr
from gspread.exceptions import WorksheetNotFound

from propus.logging_utility import Logging


class MissingRequirements(Exception):
    """Exception raised with method called with missing requirements

    Attributes:
        func_name -- name of function called
        requirements -- variable names that are required
    """

    def __init__(self, func_name, requirements):
        super().__init__(f'{func_name} called missing one of the following requirement(s): "{requirements}"')


class Sheets:
    def __init__(self, client):
        self.client = client
        self.logger = Logging.get_logger("propus/gsuite/sheets.py")
        self.url_to_worksheet = {}

    @staticmethod
    def build(service_account_info):
        from google.oauth2 import service_account
        import gspread

        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds_with_scope = credentials.with_scopes(scope)
        return Sheets(gspread.authorize(creds_with_scope))

    def fetch_sheet(self, url: AnyStr, sheet_tab: int = 0):
        """
        Given a spreadsheet url we return the direct response from the fetch by document url:
        https://docs.gspread.org/en/latest/user-guide.html#opening-a-spreadsheet

        Args:
            url (str): url of the google spreadsheet
            sheet_tab (int): sheet tab number (O indexed).
                - Default is 0

        Returns:
            gspread.spreadsheet Object: instance of a gspread spreadsheet
        """
        self.logger.info("retrieving google sheet by url")
        if not self.url_to_worksheet.get(url):
            self.url_to_worksheet[url] = self.client.open_by_url(url)
        try:
            return self.url_to_worksheet.get(url).get_worksheet(sheet_tab)
        except WorksheetNotFound:
            self.logger.info("there is no sheet with that index in this worksheet")
            return None

    def update_cell(
        self,
        worksheet,
        content: AnyStr,
        row_num: int = None,
        cell_num: int = None,
        a1_notation: AnyStr = None,
    ) -> None:
        """
        Given a spreadsheet object, update a specific cell with content.

        Args:
            worksheet (gspread.spreadsheet): Object of spreadsheet to be updated
            content (AnyStr): Content to update a cell with
            row_num (int, optional): int of the row to be updated (in conjunction with cell_num).
                - Defaults to None.
            cell_num (int, optional): int of the cell to be updated (in conjunction with cell_num).
                - Defaults to None.
            a1_notation (AnyStr, optional): A1 notation of the cell to be updated (i.e. B2, C3)
                - Defaults to None.

        Raises:
            MissingRequirements: if coords is not passed and (cell_num and row_num is also num) an error is raised
        """
        if a1_notation is None and (row_num is None or cell_num is None):
            raise MissingRequirements("update_cell", ["coords", "a1_notation"])

        if a1_notation is not None:
            worksheet.update(a1_notation, content)
        else:
            worksheet.update_cell(row_num, cell_num, content)

    def append_row(self, sheet_key: str, row: list, sheet_tab: int = 0, starting_col: str = "A1"):
        """Append row data on sheet specified based on pass arguments. Defaults to Column A1 (should be first Column),
            range needs to be defined or unexpected results could occur

        Args:
            sheet_key (str): google spreadsheets key for fetching the sheet data
            row (list): data that will be inserted on the next row
            sheet_tab (int, optional): sheet to be used on google spreadsheets. Defaults to 0.
            starting_col (str, optional): Table Range that will determine where the appended row starts, required or
                unexpected results may occur. Defaults to "A1", expected starting column.
        """
        worksheet = self.fetch_sheet(f"https://docs.google.com/spreadsheets/d/{sheet_key}", sheet_tab)
        worksheet.append_row(row, table_range=starting_col)

    def open_by_key(self, key: AnyStr):
        """
        Given a spreadsheet key we return the direct response from the fetch by key:
        https://docs.gspread.org/en/latest/user-guide.html#opening-a-spreadsheet

        Args:
            key (str): key of the google spreadsheet

        Returns:
            gspread.spreadsheet Object: instance of a gspread spreadsheet
        """
        self.logger.info("retrieving google sheet by key")
        try:
            return self.client.open_by_key(key)
        except WorksheetNotFound:
            self.logger.info("there is no sheet with that key: {key}")
            return None
