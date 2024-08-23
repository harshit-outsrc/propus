from datetime import datetime, timedelta
import json
from math import floor
import re
from typing import AnyStr, Dict

from propus.helpers.input_validations import validate_day_of_week, validate_string_length
from propus.anthology.configuration._exception import InvalidTerm, InvalidStartEndDates


@staticmethod
def validate_term(term: AnyStr):
    """
    Validates the term matches our Calbright naming convention
        Matching Naming Convention 2023-24-Term-19

    Args:
        term (AnyStr): term to be checked against valid checks. It first checks format, then ensures the 2 years
            are simply a year apart

    Raises:
        InvalidTerm
    """
    if not re.fullmatch(r"^[0-9]{4}-[0-9]{2}-TERM-[0-9]{2}", term):
        raise InvalidTerm()
    if int(term[5:7]) - int(term[2:4]) != 1:
        raise InvalidTerm()


async def create_term(
    self, term_name: AnyStr, start_date: datetime, end_date: datetime, add_drop_date: datetime
) -> Dict:
    """
    API wrapper to create a term within Anthology

    Args:
        term_name (AnyStr): Name/Code of the term to be created. Format: YYYY-YY-TERM-## (i.e. 2022-23-TERM-29)
        start_date (datetime): Start Date of Term
        end_date (datetime): End Date of Term
        add_drop_date (datetime): Add/Drop Date of Term

    Returns:
        Dict: Response from Anthology
    """
    validate_string_length(term_name, key_name="term_name", max_len=16)
    self.validate_term(term_name)
    validate_day_of_week(start_date, 1, "start_date")
    validate_day_of_week(end_date, 0, "end_date")
    validate_day_of_week(add_drop_date, 3, "add_drop_date")
    if (add_drop_date - start_date).days != 30:
        raise InvalidStartEndDates()

    term_payload = {
        "id": -1,
        "addDropDate": add_drop_date.strftime("%Y/%m/%d 00:00:00"),
        "campusIdList": [self._campus_id],
        "code": term_name,
        "startDate": start_date.strftime("%Y/%m/%d 00:00:00"),
        "endDate": end_date.strftime("%Y/%m/%d 00:00:00"),
        "isActive": True,
        "name": term_name,
        "shiftId": 8,
        "termUsage": 7,
        "sendCourseSectionDataToLms": True,
        "sendInstructorAssignmentsToLms": True,
        "sendStudentRegistrationDataToLms": True,
        "instructionalWeeks": 26,
        "isSapTerm": True,
        "isStandardTerm": 2,
        "registration": True,
        "financialAid": True,
        "studentAccounts": True,
        "isActive": True,
    }

    return self.make_request(
        req_type="post", url=self._get_endpoint("create_term"), data=json.dumps({"payload": term_payload})
    )


async def create_start_date(self, name: AnyStr, start_date: datetime) -> Dict:
    """
    API wrapper to create a start date within Anthology

    Args:
        name (AnyStr): Name/Code of the term to be created. Format: YYYY-YY-TERM-## (i.e. 2022-23-TERM-29)
        start_date (datetime): Start Date of Term

    Returns:
        Dict: Response from Anthology
    """
    validate_string_length(name, key_name="name", max_len=16)
    self.validate_term(name)

    validate_day_of_week(start_date, 1, "start_date")

    start_date_payload = {
        "id": -1,
        "campusGroupId": 0,
        "code": name,
        "isActive": True,
        "name": name,
        "shiftId": 0,
        "startDate": start_date.strftime("%Y/%m/%d 00:00:00"),
        "campusGroup": {
            "id": 9173,
            "code": "K~990",
            "isActive": True,
            "name": "K~990",
            "type": "K",
            "campusList": [
                {
                    "id": 9745,
                    "campusGroupId": 9173,
                    "campusId": self._campus_id,
                    "isCampusActive": True,
                }
            ],
        },
    }

    return self.make_request(
        req_type="post", url=self._get_endpoint("create_start_date"), data=json.dumps({"payload": start_date_payload})
    )


async def add_programs_to_start_date(self, term_name: str, start_date: datetime) -> Dict:
    program_resp = await self.fetch_configurations(configuration_type="program")
    start_request_body = []
    for prog in program_resp.get("value"):
        if prog.get("Code") == "CONED":
            continue
        prog_ver_resp = await self.fetch_configurations(configuration_type="program_version", program_id=prog.get("Id"))
        for prog_ver in prog_ver_resp.get("value"):
            total_weeks = prog_ver.get("TotalWeeks")
            mid_point_date = start_date + timedelta(days=(floor(total_weeks / 2)) * 7)
            grad_date = start_date + timedelta(total_weeks * 7)
            max_grad_date = grad_date + timedelta(days=(floor(total_weeks / 2)) * 7)
            start_request_body.append(
                {
                    "ProgramVersionId": prog_ver.get("Id"),
                    "IsSelected": True,
                    "ProgramCode": prog.get("Code"),
                    "Code": term_name,
                    "ProgramVersionCode": prog_ver.get("Code"),
                    "ProgramVersionName": prog_ver.get("Name"),
                    "StartDate": f"{start_date.strftime('%Y/%m/%d')} 00:00:00",
                    "MidPointDate": f"{mid_point_date.strftime('%Y/%m/%d')} 00:00:00",
                    "ExpectedGradDate": f"{grad_date.strftime('%Y/%m/%d')} 00:00:00",
                    "MaxGradDate": f"{max_grad_date.strftime('%Y/%m/%d')} 00:00:00",
                    "ExternshipStartDate": None,
                    "MinBudgetStarts": None,
                    "MaxBudgetStarts": None,
                    "BudgetStarts": None,
                    "Name": term_name,
                    "StartDateId": 0,
                    "IsActive": False,
                    "IsProgramActive": True,
                    "IsExternStartDateRequired": False,
                    "BudgetTuition": None,
                    "CampusList": "MAIN",
                    "CampusGroupId": None,
                    "Id": 0,
                    "ShiftId": 0,
                    "ShiftName": None,
                    "CancelDate": None,
                    "BudgetedShow": None,
                }
            )

    return self.make_request(
        req_type="post",
        url=self._get_endpoint("save_school_start_date"),
        data=json.dumps({"payload": {"SchoolStartDateList": start_request_body}}),
    )
