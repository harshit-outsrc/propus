from datetime import datetime
import json
from typing import Dict, AnyStr

from propus.anthology.student._exceptions import StudentUpdateMissingFields

from propus.helpers.input_validations import (
    validate_date,
    validate_email,
    validate_phone_number,
    validate_string_length,
)

from . import student_key_mapping


async def update_student(self, anthology_id: int, **kwargs) -> Dict:
    payload = await self.student_by_id(anthology_id)

    fields_updated = False
    for key, value in kwargs.items():
        if not student_key_mapping.get(key):
            if key in payload:
                payload[key] = value if value else ""
            else:
                continue
        if key == "first_name":
            validate_string_length(value, "first_name", max_len=100)
        elif key == "last_name":
            validate_string_length(value, "last_name", max_len=100)
        elif key == "student_number":
            validate_string_length(value, "student_number")
        elif key == "phone_number":
            validate_phone_number(value)
        elif key == "dob":
            validate_date(value, "YYYY/MM/DD")
        elif key == "email":
            validate_email(value)
        payload[student_key_mapping.get(key)] = value
        fields_updated = True

    if not fields_updated:
        raise StudentUpdateMissingFields

    # Not sure why this is needed see support case:
    # https://support.campusmgmt.com/production/nav_to.do?uri=incident.do%3Fsys_id=12d3ff371b5921141aab0e93cc4bcb60%26sysparm_stack=incident_list.do%3Fsysparm_query=active=true  # noqa
    payload["studentAddressAssociation"] = 1

    return self.make_request(
        req_type="post", url=self._get_endpoint("update_student"), data=json.dumps({"payload": payload})
    )


async def change_student_status(
    self,
    student_enrollment_id: int,
    new_status_id: int,
    note: AnyStr = "",
    effective_date: datetime = datetime.now(),
    last_attendance_date: datetime = datetime.now(),
) -> Dict:
    """
    Anthology request to update student statuses.
        - NDS-Completed: 88,
        - NDS-Withdrawn: 86,
        - NDS-Administrative Drop: 89,
        - NDS-Administrative Withdrawal: 96,

    Args:
        student_enrollment_id (int): Anthology enrollment ID
        new_status_id (int): new Anthology status ID
        note (AnyStr, optional): Note to attribute with the status change
            Defaults to ''.
        effective_date (datetime, optional): When the status change should be affective
            Defaults to datetime.now().
        last_attendance_date (datetime, optional): Last date of attendance (required for completing course)
            Defaults to datetime.now().

    Returns:
        Dict: direct response from anthology course register
    """
    payload = {
        "StudentEnrollmentPeriodId": student_enrollment_id,
        "NewSchoolStatusId": new_status_id,
        "EffectiveDate": effective_date.strftime("%Y/%m/%d 00:00:00"),
        "Note": note,
    }

    enrollment_status_date_required = [88, 86, 89, 96]

    if new_status_id in enrollment_status_date_required:
        payload["LastAttendedDate"] = last_attendance_date.strftime("%Y/%m/%d 00:00:00")
        if new_status_id != 88:
            payload["WithdrawalDate"] = effective_date.strftime("%Y/%m/%d 00:00:00")
            payload["DeterminationDate"] = effective_date.strftime("%Y/%m/%d 00:00:00")

    return self.make_request(
        req_type="post", url=self._get_endpoint("change_student_status"), data=json.dumps({"payload": payload})
    )
