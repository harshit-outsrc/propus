from datetime import datetime
import json
from typing import AnyStr, Dict


async def create_certificate(
    self, student_enrollment_id: int, notes: AnyStr, award_date: datetime = datetime.now(), degree_id: int = 5
) -> Dict:
    """
    This is a wrapper around anthology's create certificate API

    Args:
        student_enrollment_id (int): Anthology Student Enrollment ID
        notes (AnyStr): Any Notes to attribute to the certificate
        award_date (datetime, optional): date that the certificate was awarded.
            Defaults to datetime.now()).
        degree_id (int, optional): anthology degree id. Defaults to 5.


    Returns:
        Dict: if a 200 status code is returned the json response payload from anthology is returned
    """
    certificate_payload = {
        "id": -1,
        "awardedDate": f"{award_date.strftime('%Y/%m/%d')} 00:00:00",
        "degreeId": degree_id,
        "note": notes,
        "studentEnrollmentPeriodId": student_enrollment_id,
    }

    return self.make_request(
        req_type="post", url=self._get_endpoint("create_certificate"), data=json.dumps({"payload": certificate_payload})
    )
