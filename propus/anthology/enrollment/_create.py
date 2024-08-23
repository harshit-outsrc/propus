from datetime import datetime
import json
from typing import Dict


async def create_enrollment(
    self,
    student_id: int,
    program_id: int,
    program_version_id: int,
    grade_level_id: int,
    start_date: datetime,
    grad_date: datetime,
    catalog_year_id: int,
    version_start_date: int,
    billing_method: int = 1,
    shift_id: int = 8,
    application_received_date: datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    enrollment_date: datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
) -> Dict:
    """
    This is a wrapper around anthology's create enrollment API

    Args:
        student_id (int): anthology's student id
        program_id (int): Calbright's top level program id
             - options can be retrieved with anthology.get_program
        program_version_id (int): Calbright's inner program version id
            - options can be retrieved with anthology.get_program_version(<program_id>)
        grade_level_id (int): Student's highest grade level
            - options can be retrieved with anthology.get_grade_level
        start_date (datetime): enrollment start date
        grad_date (datetime): enrollment proposed grad date
        catalog_year_id (int): id of the catalog year
            - options can be retrieved with anthology.get_catalog_year(<program_version_id>)
        version_start_date (int): id of the version start date
            - options can be retrieved with anthology.get_start_date
        billing_method (int, optional): billing method (default is set to Bill by program). Defaults to 2.
            - options can be retrieved with anthology.get_billing_method
        shift_id (int, optional): shift ID (default is ansyncronous). Defaults to 8.
            - options can be retrieved with anthology.get_shift


    Returns:
        Dict: if a 200 status code is returned the json response payload from anthology is returned
    """

    enrollment_payload = {
        "IsDegreeProgramType": False,
        "entity": {
            "id": -1,
            "campusId": 5,
            "assignedAdmissionsRepId": 2,  # SystemAdministrator
            "schoolStatusId": 95,  # Enrolled in Program Pathway
            "studentId": student_id,
            "programId": program_id,
            "programVersionId": program_version_id,
            "billingMethodId": billing_method,
            "catalogYearId": catalog_year_id,
            "expectedStartDate": f"{start_date.strftime('%Y-%m-%d')}T00:00:00",
            "graduationDate": f"{grad_date.strftime('%Y-%m-%d')}T00:00:00",
            "gradeLevelId": grade_level_id,
            "shiftId": shift_id,
            "startDateId": version_start_date,
            "applicationReceivedDate": application_received_date,
            "enrollmentDate": enrollment_date,
        },
    }
    return self.make_request(
        req_type="post", url=self._get_endpoint("create_enrollment"), data=json.dumps({"payload": enrollment_payload})
    )
