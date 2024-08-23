import json
from typing import Dict, AnyStr


async def fetch_all_enrollments(self) -> Dict:
    """
    API Wrapper to fetch all enrollments in anthology

    Returns:
        Dict: direct response from anthology term query
    """
    return self.make_request(
        url=self._get_endpoint("enrollment_search"),
        params={"$expand": "Student,Program,ProgramVersion,StartTerm"},
    )


async def fetch_enrollment_by_cccid(self, ccc_id: AnyStr) -> Dict:
    """
    API Wrapper to fetch enrollments for a specific student

    Args:
        ccc_id (str): student ccc id

    Returns:
        Dict: direct response from anthology term query
    """
    return self.make_request(
        url=self._get_endpoint("enrollment_search"),
        params={
            "$filter": f"Student/StudentNumber eq '{ccc_id}'",
            "$expand": "Student,Program,ProgramVersion,StartTerm",
        },
    )


async def fetch_enrollment_by_enrollment_id(self, enrollment_id: AnyStr) -> Dict:
    """
    API Wrapper to fetch enrollments for a specific student

    Args:
        ccc_id (str): student ccc id

    Returns:
        Dict: direct response from anthology term query
    """
    return self.make_request(
        url=self._get_endpoint("enrollment_search"),
        params={
            "$filter": f"EnrollmentNumber eq '{enrollment_id}'",
            "$expand": "Student,Program,ProgramVersion,StartTerm",
        },
    )


async def fetch_student_enrollment_period_by_id(self, student_enrollment_id: int) -> Dict:
    """
    Anthology request to search for student enrollment period.

    Args:
        student_enrollment_id (int): Anthology enrollment ID

    Returns:
        Dict: direct response from anthology student enrollment period search
    """

    return self.make_request(
        req_type="post",
        url=self._get_endpoint("student_enrollment_period_search"),
        data=json.dumps({"payload": {"id": student_enrollment_id}}),
    )
