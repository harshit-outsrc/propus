import asyncio
from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy import select, or_

from propus.logging_utility import Logging
from propus.helpers.etl import clean_phone, clean_ssn
from propus.helpers.sql_alchemy import upsert_changes
from propus.helpers.field_maps import (
    create_field_map,
    create_learner_status_map,
    extract_data_based_on_mapping,
)
from propus.helpers.exceptions import EntryNotFoundError

logger = Logging.get_logger("propus/helpers/anthology")


ANTHOLOGY_ADDRESS_FIELD_MAP = {
    "streetAddress": "address1",
    "streetAddress2": "address2",
    "city": "city",
    "state": "state",
    "postalCode": "zip",
}

ANTHOLOGY_LEARNER_STATUS_MAP = {
    -2: "Suspended by IT (pre-enrollment)",
    0: "Dropped",
    1: "Expressed Interest",
    2: "App Started",
    3: "App Submitted",
    4: "Started Orientation",
    5: "Completed Orientation",
    6: "Completed Ed Plan",
    6.5: "Completed CSEP",
    7: "Enrolled in Essentials",
    8: "Completed Essentials",
    9: "Met w/Program Director",
    10: "Enrolled in Program Pathway",
    11: "Started Program Pathway",
    12: "Completed Program Pathway",
    13: "Completed Industry Certification",
    14: "Paid Apprenticeship",
    15: "Full-Time Employment",
}

ANTHOLOGY_STUDENT_FIELD_MAP = {
    "ssn": "ssn",
    "dateOfBirth": "date_of_birth",  # Convert to date?
    "mobilePhoneNumber": "mobile_number",  # Clean / remove spaces and ()
    "otherPhoneNumber": "home_phone_number",  # Clean / remove spaces and ()
}

ANTHOLOGY_USER_FIELD_MAP = {
    "emailAddress": "calbright_email",
    "firstName": "first_name",
    "lastName": "last_name",
    "maidenName": "maiden_name",
    "middleName": "middle_name",
    "otherEmailAddress": "personal_email",
    "preferredName": "preferred_first_name",
    "rawPhoneNumber": "phone_number",
    "suffixId": "suffixId",  # Translated from the Anthology ID to the database ID within the user function
    "titleId": "titleId",  # Translated from the Anthology ID to the database ID within the user function
}

ANTHOLOGY_CLEAN_FIELD_FUNCTIONS = {
    "mobile_number": clean_phone,
    "home_phone_number": clean_phone,
    "ssn": clean_ssn,
}


def get_anthology_user(session, data: Dict = {}):
    """get_anthology_user uses the db session to get the User associated with the provided Anthology data.

    Args:
        session (SQLAlchemy.session): session of the SQLAlchemy session connection
        data (dict): request's decoded JSON data

    Returns:
        user (propus.sql.calbright.user.User): User object
    """
    from propus.calbright_sql.user import User

    try:
        ccc_id = data.get("studentNumber", "id_not_found")
        anthology_id = data.get("studentId", data.get("id", -123456789))
        user = session.execute(
            select(User).filter(or_(User.ccc_id == ccc_id, User.anthology_id == anthology_id))
        ).scalar_one()
        return user
    except Exception:
        raise EntryNotFoundError(f"ccc_id {ccc_id} or anthology_id {anthology_id}", User.__table__.name)


def update_address(payload={}):
    """
    API endpoint for processing changes to a Student.

    Example payload received from Anthology:
        {
            "isExcludedCrmIntegration": false,
            "addressTypeId": 0,
            "studentInquiryRequired": true,
            "extraCurricularsList": [],
            "programsList": [
                6
            ],
            "enrolledProgramIdList": [],
            "ethnicitiesList": [],
            "leadSourcesList": [
                680
            ],
            "deleteVeteranDetails": false,
            "vendors": [],
            "studentAddressAssociation": 0,
            "newAssignedAdmissionsRepId": 0,
            "assignedAdmissionsRepReassignedDate": "0001-01-01T00:00:00",
            "studentRelationshipAddress": null,
            "lastFourSsn": "",
            "customProperties": {},
            "multiValueCustomProperties": {},
            "originalCustomPropertiesValues": null,
            "originalMultiValueCustomPropertiesValues": null,
            "genderPronounList": [],
            "overridePrevEducAltPellValidation": false,
            "id": 5921,
            "acgEligReasonCode": null,
            "agencyId": 0,
            "alienNumber": "",
            "arAccountStatus": "X",
            "arBalance": 0.0000,
            "arNextTransactionNumber": 0,
            "assignedAdmissionsRepId": 2,
            "athleticIdentifier": null,
            "bestTimeToContact": "Anytime",
            "campusId": 5,
            "citizenId": 0,
            "city": "Clearwater",
            "collegeId": null,
            "countryId": 1,
            "countyId": 0,
            "createdDateTime": "2023-09-05T14:00:11",
            "cumulativeGpa": 0.000000,
            "cumulativeGpaPoints": 0.0000,
            "currencyCodeId": null,
            "currentLda": "2023-09-05T00:00:00",
            "dataBlockIndicator": false,
            "dateOfBirth": "2000-09-05T00:00:00",
            "dbiModifiedDate": null,
            "defaultAddressCode": null,
            "defaultMasterStudentAddressId": null,
            "defaultStudentAddressId": null,
            "disabled": "X",
            "driverLicenseNumber": "",
            "driverLicenseState": "",
            "emailAddress": "Anthtest@gmail.com",
            "employabilityAboutInfo": null,
            "employerId": 0,
            "employmentStatusId": 0,
            "externalStudentIdentifier": null,
            "extraCurricularActivityId": 0,
            "facebookUrl": null,
            "faGradPlusCounselingDate": null,
            "faRigorousHighSchoolProgramCodeId": null,
            "firstName": "Anthology",
            "genderId": 0,
            "gpaCredits": 0.0000,
            "hispanicLatino": null,
            "hsAcademicGpa": null,
            "instagramUrl": null,
            "isActive": true,
            "isAllowedBulkRegistrationByTrack": null,
            "isBadAddress": false,
            "isBadPhone": false,
            "isDdVeteran": false,
            "isEftDefaultForStipends": false,
            "isInDistrict": false,
            "isSscrError11Received": false,
            "lastActivityDate": null,
            "lastInterestDate": null,
            "lastModifiedDateTime": "2024-01-19T15:43:38.65",
            "lastModifiedUserId": 103,
            "lastName": "Test",
            "lastNameFirstFour": "Test",
            "lastStatementBeginDate": null,
            "lastStatementCloseDate": null,
            "lastStatementDate": null,
            "leadDate": "2023-09-05T00:00:00",
            "leadSourceId": 680,
            "leadTypeId": 0,
            "linkedInUrl": null,
            "maidenName": "",
            "maritalStatusId": 0,
            "mi": "",
            "middleName": "",
            "mobilePhoneNumber": "(777) 867-5309",
            "nationalityId": 0,
            "nickName": "",
            "niStudent": false,
            "note": "",
            "originalAssignedAdmissionsRepId": 2,
            "originalExpectedStartDate": "2023-07-11T00:00:00",
            "originalStartDate": null,
            "otherEmailAddress": "",
            "otherLanguageFirstName": null,
            "otherLanguageLastName": null,
            "otherLanguageMiddleName": null,
            "otherLanguageStudentFullName": null,
            "otherPhoneNumber": null,
            "personId": 6014,
            "phoneNumber": "(777) 867-5309",
            "pin": null,
            "postalCode": "33764",
            "postalCodeFirstThree": "337",
            "preferredContactType": "Ph",
            "preferredName": "Preferred Name",
            "previousEducationGpa": null,
            "previousEducationId": 1,
            "programGroupId": 6,
            "programId": 6,
            "rawFirstName": "Anthology",
            "rawLastName": "Test",
            "rawPhoneNumber": "7778675309",
            "rowVersion": "AAAAAADjJOI=",
            "schoolStatusId": 88,
            "shiftId": 8,
            "smsServiceProviderId": null,
            "sourceSystem": "C",
            "ssn": "",
            "startDate": "2023-07-11T00:00:00",
            "state": "FL",
            "statementComment": "",
            "streetAddress": "1313 Mockingbird Lane",
            "streetAddress2": null,
            "studentFullName": null,
            "studentIdentifier": null,
            "studentNumber": null,
            "subscribeToSms": false,
            "suffix": null,
            "suffixId": null,
            "titleId": 0,
            "twitterUrl": null,
            "veteran": "X",
            "workPhoneNumber": "(___) ___-____",
            "workPhoneNumberExtension": "",
            "originalState": "H4sIAAAAAAAEANVbUVMiORD+K5RPtw/IjCgqpdQBosseICXc3r5ZYaaBPjMJlWRE9tdfz4jW7up4pclollLQGkh/k07393UnnLSVYpvL+V+w+cp4CpdzbRSKBROb6WYFlbuEC326szRm1azVdLSEhOndBCMltZyb3Ugmtb0gqNfCoDYBhYzjd2ZQilo+sN65H6GJj2Os1+vddX1XqkX2wbD2bTiY5MNWUWjDRAQ7rZMCOPmFVj8+qWWvJ/lbKtg0dOl0hzVRmAd77P/t7bQOjvfCk1o+SisfstBmMZgB0+ZcpmqiRQGq+w+9BljtzWja0aLHcXEFTEvRlTH8gkkgP90xKgUbGwsQ0caZEwJbD7Q5ghilyQyUDx5Q7SiSqTATw0yqnSFqfbOeJ9VhPIuvAkwxRJgw/jrn7Qb0sEc2gjszVUxoFmXJ42VvLqV67yWmNS4ExO04QfpTCn0FK2cRsGcNzyw5GIz6MQiDc3wydS7CvgPaTDGBqexKYchP7pZ2W2wMjWw7DV2WrFLtjh2s8aDB7yD8yZQEaOPOa10OTK2ZyVabJS7JOSzgyUS5WLbdLBcrd3RlLRhyQB7RZ1cB+TA+o6dpHoTPk8P28usSW7BXrwbH1eBgGu43g6AZ2s9emqScBOYtXKyYcyKzp7Kf8I0lebNIAnwc3XZTpYgoBnHhBFo6mzyd/9gCpTXJOlxGN30RY8SMLJIEMykpGYlX4Z0zrq0pJ4uay3kHlVm6ncsgcD2XMxzKOBMHeaiXkGnPYM5SbtpxrEDrkoqPrZEhVV2gJibNFM/WYin0sbX3HpZQsxmHIl74iIrhTFEeUwOMQGjwpsL6CVVWZRVx1nuC6iUM+XZ5uBTGZmlId/+5yIbPmi22Lu0lKy43oPzRH/eIEniomD1Cdkc5RjC+Df5SqyuypVhGzBiRflBtKoNv0SeZeM4uFIvHPNWZgNXA6Q0lEck5u8KFVDLVn3GxpDsgdh8ruVAsyVillOx7jkqbESvUv28MXsnlYmM79RcgYp8ilpQtFQ0xeihtP6NeMYHRgCS4kCWsk8+6HbEYEoye1h8uxu/rPPSLluFbhG6GyHZe+7rD4pfp7cM0eI5tvJTC5aQ5QnYWfwUiEVa0N/CB0HpzsxW355KUNK4oy3jo274gYUwXCvuNH4htoiPVU0qqMLyCCChsi3L0h4HMtqcexERJdJ2Z6Ata5SRUSzTxY/VaQqNqvxqE1fB4Gh409+vN+tFuw7r/+yPqv7VDBg+DugtsbuXOlNzvClWuxrJdVf/g5QVnVq10YIGixPX+aKjLpYb3MFSWDWDPtZx8azZmMCe05KKnBcZb47Rx5ARV9p8/6n/IkAphp7nj7WtryBSarEL3q3MwRB/mBuOYgy+OkjPkkKt0x43E1h+Hh4efKkeNw+pBPTi2dd0oP73EuFfNlxFGN544coTbdphvSnckvWgEXyokXcC450dGHmD27lYQGYgpg6rnBIADlj6shqEzln7AXYTXhWC5NEtQpTT0LTEVp08Xtz0GpaW70yqNINy39fZvwBdj/LW348QXUpOseWYP1eK+6/XDhr1HHoHlNdp0qcAtRGuACuagFMTbU2rZFXcAx0tn+NxW34/DVu7HtQZ5izLVvTiNcj1UTrP7iRl/Tmlt95sulEzdsXbDESp/AF2xtc87ZwTPz0YXASuF24jaiNhc8NqVXH8lQUBBWST0mYbGfofEmNq8zrv54+zfL5f9U1uU95vDjsv/oyNrWEucG3d4rOEkegLqFiOgBHKLz20mu0jn992zyUYbSNwt6a713XvxzZzfpcBye6CqdT5wAijvg8skKe47vK8vSfUa56e9wnpYrwxldEMfnKGKKwMmrKXcT1j3yoj6dzgdtbVRWuk7SWc6UjiDqaRc6Vtna5LO53hXym1nA5fCBVM03KNNi5dPYbwhVq3P1v4j1U057Y3r6+tPFXqq0u+1Y5jZkUjxgih0nIVrL387ufUfrKtWpL48AAA=",
            "secureState": "H4sIAAAAAAAEAD3MQQrCMBAAwK9I7mZTeysqeFbpoSJel5C0C01Ssisxvl6s4ANm9qecsfb+7Ood56frPUumOGKst7q4zSvMkQ9qElk6ALaTC8g6kM2JkxdtU4CdMS00BgaXCWd6o1CKsMasfkNH/6OUokurUx6/sIHH9TKs7ZYiC0brFBw/juQnSpcAAAA=",
            "extendedProperties": [],
            "entityState": 3
            }
    """
    pass


def update_learner_status_history(payload={}):
    """
    API endpoint for processing changes to a Student.

    Example payload received from Anthology:
        {
            "isExcludedCrmIntegration": false,
            "addressTypeId": 0,
            "studentInquiryRequired": true,
            "extraCurricularsList": [],
            "programsList": [
                6
            ],
            "enrolledProgramIdList": [],
            "ethnicitiesList": [],
            "leadSourcesList": [
                680
            ],
            "deleteVeteranDetails": false,
            "vendors": [],
            "studentAddressAssociation": 0,
            "newAssignedAdmissionsRepId": 0,
            "assignedAdmissionsRepReassignedDate": "0001-01-01T00:00:00",
            "studentRelationshipAddress": null,
            "lastFourSsn": "",
            "customProperties": {},
            "multiValueCustomProperties": {},
            "originalCustomPropertiesValues": null,
            "originalMultiValueCustomPropertiesValues": null,
            "genderPronounList": [],
            "overridePrevEducAltPellValidation": false,
            "id": 5921,
            "acgEligReasonCode": null,
            "agencyId": 0,
            "alienNumber": "",
            "arAccountStatus": "X",
            "arBalance": 0.0000,
            "arNextTransactionNumber": 0,
            "assignedAdmissionsRepId": 2,
            "athleticIdentifier": null,
            "bestTimeToContact": "Anytime",
            "campusId": 5,
            "citizenId": 0,
            "city": "Clearwater",
            "collegeId": null,
            "countryId": 1,
            "countyId": 0,
            "createdDateTime": "2023-09-05T14:00:11",
            "cumulativeGpa": 0.000000,
            "cumulativeGpaPoints": 0.0000,
            "currencyCodeId": null,
            "currentLda": "2023-09-05T00:00:00",
            "dataBlockIndicator": false,
            "dateOfBirth": "2000-09-05T00:00:00",
            "dbiModifiedDate": null,
            "defaultAddressCode": null,
            "defaultMasterStudentAddressId": null,
            "defaultStudentAddressId": null,
            "disabled": "X",
            "driverLicenseNumber": "",
            "driverLicenseState": "",
            "emailAddress": "Anthtest@gmail.com",
            "employabilityAboutInfo": null,
            "employerId": 0,
            "employmentStatusId": 0,
            "externalStudentIdentifier": null,
            "extraCurricularActivityId": 0,
            "facebookUrl": null,
            "faGradPlusCounselingDate": null,
            "faRigorousHighSchoolProgramCodeId": null,
            "firstName": "Anthology",
            "genderId": 0,
            "gpaCredits": 0.0000,
            "hispanicLatino": null,
            "hsAcademicGpa": null,
            "instagramUrl": null,
            "isActive": true,
            "isAllowedBulkRegistrationByTrack": null,
            "isBadAddress": false,
            "isBadPhone": false,
            "isDdVeteran": false,
            "isEftDefaultForStipends": false,
            "isInDistrict": false,
            "isSscrError11Received": false,
            "lastActivityDate": null,
            "lastInterestDate": null,
            "lastModifiedDateTime": "2024-01-19T15:43:38.65",
            "lastModifiedUserId": 103,
            "lastName": "Test",
            "lastNameFirstFour": "Test",
            "lastStatementBeginDate": null,
            "lastStatementCloseDate": null,
            "lastStatementDate": null,
            "leadDate": "2023-09-05T00:00:00",
            "leadSourceId": 680,
            "leadTypeId": 0,
            "linkedInUrl": null,
            "maidenName": "",
            "maritalStatusId": 0,
            "mi": "",
            "middleName": "",
            "mobilePhoneNumber": "(777) 867-5309",
            "nationalityId": 0,
            "nickName": "",
            "niStudent": false,
            "note": "",
            "originalAssignedAdmissionsRepId": 2,
            "originalExpectedStartDate": "2023-07-11T00:00:00",
            "originalStartDate": null,
            "otherEmailAddress": "",
            "otherLanguageFirstName": null,
            "otherLanguageLastName": null,
            "otherLanguageMiddleName": null,
            "otherLanguageStudentFullName": null,
            "otherPhoneNumber": null,
            "personId": 6014,
            "phoneNumber": "(777) 867-5309",
            "pin": null,
            "postalCode": "33764",
            "postalCodeFirstThree": "337",
            "preferredContactType": "Ph",
            "preferredName": "Preferred Name",
            "previousEducationGpa": null,
            "previousEducationId": 1,
            "programGroupId": 6,
            "programId": 6,
            "rawFirstName": "Anthology",
            "rawLastName": "Test",
            "rawPhoneNumber": "7778675309",
            "rowVersion": "AAAAAADjJOI=",
            "schoolStatusId": 88,
            "shiftId": 8,
            "smsServiceProviderId": null,
            "sourceSystem": "C",
            "ssn": "",
            "startDate": "2023-07-11T00:00:00",
            "state": "FL",
            "statementComment": "",
            "streetAddress": "1313 Mockingbird Lane",
            "streetAddress2": null,
            "studentFullName": null,
            "studentIdentifier": null,
            "studentNumber": null,
            "subscribeToSms": false,
            "suffix": null,
            "suffixId": null,
            "titleId": 0,
            "twitterUrl": null,
            "veteran": "X",
            "workPhoneNumber": "(___) ___-____",
            "workPhoneNumberExtension": "",
            "originalState": "H4sIAAAAAAAEANVbUVMiORD+K5RPtw/IjCgqpdQBosseICXc3r5ZYaaBPjMJlWRE9tdfz4jW7up4pclollLQGkh/k07393UnnLSVYpvL+V+w+cp4CpdzbRSKBROb6WYFlbuEC326szRm1azVdLSEhOndBCMltZyb3Ugmtb0gqNfCoDYBhYzjd2ZQilo+sN65H6GJj2Os1+vddX1XqkX2wbD2bTiY5MNWUWjDRAQ7rZMCOPmFVj8+qWWvJ/lbKtg0dOl0hzVRmAd77P/t7bQOjvfCk1o+SisfstBmMZgB0+ZcpmqiRQGq+w+9BljtzWja0aLHcXEFTEvRlTH8gkkgP90xKgUbGwsQ0caZEwJbD7Q5ghilyQyUDx5Q7SiSqTATw0yqnSFqfbOeJ9VhPIuvAkwxRJgw/jrn7Qb0sEc2gjszVUxoFmXJ42VvLqV67yWmNS4ExO04QfpTCn0FK2cRsGcNzyw5GIz6MQiDc3wydS7CvgPaTDGBqexKYchP7pZ2W2wMjWw7DV2WrFLtjh2s8aDB7yD8yZQEaOPOa10OTK2ZyVabJS7JOSzgyUS5WLbdLBcrd3RlLRhyQB7RZ1cB+TA+o6dpHoTPk8P28usSW7BXrwbH1eBgGu43g6AZ2s9emqScBOYtXKyYcyKzp7Kf8I0lebNIAnwc3XZTpYgoBnHhBFo6mzyd/9gCpTXJOlxGN30RY8SMLJIEMykpGYlX4Z0zrq0pJ4uay3kHlVm6ncsgcD2XMxzKOBMHeaiXkGnPYM5SbtpxrEDrkoqPrZEhVV2gJibNFM/WYin0sbX3HpZQsxmHIl74iIrhTFEeUwOMQGjwpsL6CVVWZRVx1nuC6iUM+XZ5uBTGZmlId/+5yIbPmi22Lu0lKy43oPzRH/eIEniomD1Cdkc5RjC+Df5SqyuypVhGzBiRflBtKoNv0SeZeM4uFIvHPNWZgNXA6Q0lEck5u8KFVDLVn3GxpDsgdh8ruVAsyVillOx7jkqbESvUv28MXsnlYmM79RcgYp8ilpQtFQ0xeihtP6NeMYHRgCS4kCWsk8+6HbEYEoye1h8uxu/rPPSLluFbhG6GyHZe+7rD4pfp7cM0eI5tvJTC5aQ5QnYWfwUiEVa0N/CB0HpzsxW355KUNK4oy3jo274gYUwXCvuNH4htoiPVU0qqMLyCCChsi3L0h4HMtqcexERJdJ2Z6Ata5SRUSzTxY/VaQqNqvxqE1fB4Gh409+vN+tFuw7r/+yPqv7VDBg+DugtsbuXOlNzvClWuxrJdVf/g5QVnVq10YIGixPX+aKjLpYb3MFSWDWDPtZx8azZmMCe05KKnBcZb47Rx5ARV9p8/6n/IkAphp7nj7WtryBSarEL3q3MwRB/mBuOYgy+OkjPkkKt0x43E1h+Hh4efKkeNw+pBPTi2dd0oP73EuFfNlxFGN544coTbdphvSnckvWgEXyokXcC450dGHmD27lYQGYgpg6rnBIADlj6shqEzln7AXYTXhWC5NEtQpTT0LTEVp08Xtz0GpaW70yqNINy39fZvwBdj/LW348QXUpOseWYP1eK+6/XDhr1HHoHlNdp0qcAtRGuACuagFMTbU2rZFXcAx0tn+NxW34/DVu7HtQZ5izLVvTiNcj1UTrP7iRl/Tmlt95sulEzdsXbDESp/AF2xtc87ZwTPz0YXASuF24jaiNhc8NqVXH8lQUBBWST0mYbGfofEmNq8zrv54+zfL5f9U1uU95vDjsv/oyNrWEucG3d4rOEkegLqFiOgBHKLz20mu0jn992zyUYbSNwt6a713XvxzZzfpcBye6CqdT5wAijvg8skKe47vK8vSfUa56e9wnpYrwxldEMfnKGKKwMmrKXcT1j3yoj6dzgdtbVRWuk7SWc6UjiDqaRc6Vtna5LO53hXym1nA5fCBVM03KNNi5dPYbwhVq3P1v4j1U057Y3r6+tPFXqq0u+1Y5jZkUjxgih0nIVrL387ufUfrKtWpL48AAA=",
            "secureState": "H4sIAAAAAAAEAD3MQQrCMBAAwK9I7mZTeysqeFbpoSJel5C0C01Ssisxvl6s4ANm9qecsfb+7Ood56frPUumOGKst7q4zSvMkQ9qElk6ALaTC8g6kM2JkxdtU4CdMS00BgaXCWd6o1CKsMasfkNH/6OUokurUx6/sIHH9TKs7ZYiC0brFBw/juQnSpcAAAA=",
            "extendedProperties": [],
            "entityState": 3
            }
    """
    pass


def update_student(session, salesforce, data: Dict = {}):
    """update_student is triggered by Wasat when a Student entity is saved in Anthology.
    This then updates the databaes and Salesforce record as appropriate.

    Args:
        session (SQLAlchemy.session): session of the SQLAlchemy session connection
        salesforce (propus.RestAPIClient): Salesforce REST API Client
        data (dict): request's decoded JSON data
    """
    from propus.helpers.salesforce import SF_CURRENT_ADDRESS_FIELD_MAP, SF_STUDENT_MAP, SF_USER_MAP

    try:
        user = get_anthology_user(session, data)
        student = user.student
    except EntryNotFoundError as e:
        logger.error(e)
        return

    data_mappings = extract_data_based_on_mapping(
        data,
        dict(
            address=ANTHOLOGY_ADDRESS_FIELD_MAP,
            student=ANTHOLOGY_STUDENT_FIELD_MAP,
            user=ANTHOLOGY_USER_FIELD_MAP,
        ),
    )

    student_address = None
    for a in user.student.student_address:
        student_address = a
        if a.current:
            break
    address_updates = {}
    if student_address:
        address = student_address.address
        address_updates, address_updated = _update_address(session, address, data_mappings.get("address", {}))
        logger.info(f"Student address updated {address_updated}: {address_updates}")
    student_updates, student_updated = _update_student(session, student, data_mappings.get("student", {}))
    logger.info(f"Student updated {student_updated}: {student_updates}")
    user_updates, user_updated = _update_user(session, user, data_mappings.get("user", {}))
    logger.info(f"User updated {user_updated}: {user_updates}")

    updated_data = address_updates | student_updates | user_updates
    if updated_data:
        SF_MAP_FIELDS = SF_CURRENT_ADDRESS_FIELD_MAP | SF_STUDENT_MAP | SF_USER_MAP
        sf_updates = {k: updated_data.get(v) for k, v in SF_MAP_FIELDS.items() if updated_data.get(v)}
        sf_response = salesforce.update_contact_record(user.salesforce_id, **sf_updates)
        logger.info(f"Update sent to Salesforce: {sf_response}")


def update_student_course(session, salesforce, data: Dict = {}):
    """update_student_course is triggered by Wasat when a StudentCourse entity is saved in Anthology.
    This then updates the databaes and Salesforce record as appropriate.

    Args:
        session (SQLAlchemy.session): session of the SQLAlchemy session connection
        salesforce (propus.RestAPIClient): Salesforce REST API Client
        data (dict): request's decoded JSON data
    """
    learner_status_number = data.get("status")
    previous_learner_status_number = data.get("previousStatus")

    if learner_status_number == previous_learner_status_number:
        return

    try:
        user = get_anthology_user(session, data)

    except Exception as e:
        logger.error(f"Error getting user / student from Anthology data {data}: {e}")
        return

    try:
        learner_status_map = create_learner_status_map(session)
        learner_status = ANTHOLOGY_LEARNER_STATUS_MAP.get(learner_status_number)
        user.learner_status_id = learner_status_map.get(learner_status, "<learner_status_id not found>")
        user.save()
        logger.info(f"Learner status updated for {user} to {learner_status}")

    except Exception as e:
        logger.error(f"Error updating learner status for {user} to {learner_status}: {e}")

    try:
        sf_id = salesforce.get_sf_id_by_user(user)
        payload = {"cfg_Learner_Status__c": learner_status}
        salesforce.update_contact_record(sf_id, **payload)
        logger.info(f"Salesforce learner status updated for {user} to {learner_status}")

    except Exception as e:
        logger.error(f"Error updating Salesforce learner status for {user} to {learner_status}: {e}")

    return


def _update_address(session, address, data):
    """Helper method to upsert changes to an Address object.

    Args:
        session (SQLAlchemy.session): session of the SQLAlchemy session connection
        address (propus.sql.calbright.address.Address): SQLAlchemy Address object
        data (dict): data to be checked / upserted

    Returns:
        upserts (dict): Dictionary of upserted values
        upserted (boolean): Boolean if the object was upserted
    """
    from propus.calbright_sql.address import Address

    filters = dict(id=address.id)
    address_data = {v: data.get(k) for k, v in ANTHOLOGY_ADDRESS_FIELD_MAP.items() if data.get(k)}

    return upsert_changes(session, Address, address, address_data, **filters)


def _update_student(session, student, data):
    """Helper method to upsert changes to an Student object.

    Args:
        session (SQLAlchemy.session): session of the SQLAlchemy session connection
        address (propus.sql.calbright.student.Student): SQLAlchemy Student object
        data (dict): data to be checked / upserted

    Returns:
        upserts (dict): Dictionary of upserted values
        upserted (boolean): Boolean if the object was upserted
    """
    from propus.calbright_sql.student import Student

    filters = dict(ccc_id=student.ccc_id)
    student_data = {k: v(data.get(k)) for k, v in ANTHOLOGY_CLEAN_FIELD_FUNCTIONS.items() if data.get(k)}
    return upsert_changes(session, Student, student, student_data, **filters)


def _update_user(session, user, data):
    """Helper method to upsert changes to an User object.

    Args:
        session (SQLAlchemy.session): session of the SQLAlchemy session connection
        address (propus.sql.calbright.user.User): SQLAlchemy User object
        data (dict): data to be checked / upserted

    Returns:
        upserts (dict): Dictionary of upserted values
        upserted (boolean): Boolean if the object was upserted
    """
    from propus.calbright_sql.user import User

    filters = dict(ccc_id=user.ccc_id)
    user_data = {v: data.get(k) for k, v in ANTHOLOGY_USER_FIELD_MAP.items() if data.get(k)}

    if data.get("suffixId"):
        from propus.calbright_sql.suffix import Suffix

        suffix_map = create_field_map(session, Suffix, map_from="anthology_id", map_to="id")
        suffix_id = suffix_map.get(data.get("suffixId"))
        if suffix_id:
            user_data["suffix_id"] = suffix_id
        else:
            logger.error(f"Suffix not found for Anthology suffix {data.get('suffixId')}")

    if data.get("titleId"):
        from propus.calbright_sql.salutation import Salutation

        salutation_map = create_field_map(session, Salutation, map_from="anthology_id", map_to="id")
        salutation_id = salutation_map.get(data.get("titleId"))
        if salutation_id:
            user_data["salutation_id"] = salutation_id
        else:
            logger.error(f"Salutation not found for Anthology title {data.get('titleId')}")

    return upsert_changes(session, User, user, user_data, **filters)


def create_term(anthology, start_date: datetime, term_name: str):
    # Fetch All Terms
    terms = asyncio.run(anthology.fetch_configurations("term"))
    most_recent_term = max(terms.get("value"), key=lambda x: x.get("StartDate"))

    # Create the term
    term_creation_response = asyncio.run(
        anthology.create_term(
            term_name,
            start_date,
            end_date=start_date + timedelta(days=181),
            add_drop_date=start_date + timedelta(days=30),
        )
    )

    # Create the Start Term Date
    asyncio.run(anthology.create_start_date(term_name, start_date))

    # Add Programs to this term:
    asyncio.run(anthology.add_programs_to_start_date(term_name, start_date))

    # Copy the class schedule from the most recent term to this new term
    asyncio.run(anthology.copy_class_schedule(most_recent_term.get("Id"), term_creation_response.get("id")))
    return term_creation_response.get("id")
