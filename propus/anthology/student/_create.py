from datetime import datetime
import json
from typing import AnyStr, Dict

from propus.helpers.input_validations import (
    validate_date,
    validate_email,
    validate_phone_number,
    validate_string_length,
)

from . import student_key_mapping


async def create_student(
    self,
    first_name: AnyStr,
    last_name: AnyStr,
    student_number: AnyStr,
    phone_number: AnyStr,
    dob: AnyStr,
    email: AnyStr,
    **kwargs,
) -> Dict:
    """
    API used to create new student records

    Args:
        first_name (str): [required] First name entry
        last_name (str): [required] Last name entry
        student_number (str): [required] Student Number (must be less than 11 characters)
        phone_number (str): [required] Phone Number in following format "(123) 123-1234"
        dob (str): [required] Date of Birth in the following format YYYY-MM-DD
        email (str): [required] Email Address

        [optional arguments as keyword arguments]
        street_address (str): [optional] full street address
        city (str): [optional]  address city
        postal_code (str): [optional]  address postal code
        middle_name (str): [optional]  student's middle name
    """
    validate_string_length(first_name, "first_name", max_len=100)
    validate_string_length(last_name, "last_name", max_len=100)
    validate_string_length(student_number, "student_number")
    validate_phone_number(phone_number)
    validate_date(dob, "YYYY/MM/DD")
    validate_email(email)

    student_payload = {
        "studentNumber": student_number,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "emailAddress": email,
        "id": -1,
        "schoolStatusId": 4,  # Application Received
        "campusId": self._campus_id,  # MAIN Campus,
        "countryId": "1",
        "countryName": "United States",
        "assignedAdmissionsRepId": 2,
        "leadSourceId": 680,
        "leadDate": f'{datetime.now().strftime("%Y/%m/%d")} 00:00:00',
        "state": "CA",
        "dateOfBirth": f"{dob} 00:00:00",
    }

    for key, json_key in student_key_mapping.items():
        if kwargs.get(key):
            student_payload[json_key] = kwargs.get(key)

    return self.make_request(
        req_type="post", url=self._get_endpoint("create_student"), data=json.dumps({"payload": student_payload})
    )
