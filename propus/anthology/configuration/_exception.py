class InvalidTerm(Exception):
    def __init__(self):
        super().__init__("term name does not match the format YYYY-YY-TERM-## (i.e. 2022-23-TERM-29)")


class InvalidStartEndDates(Exception):
    def __init__(self):
        super().__init__("start_date to add_drop_date should be 30 days")
