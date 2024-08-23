from typing import Dict, AnyStr
from propus.api_client import RestAPIClient

from propus.anthology.endpoints import all_endpoints


class Anthology(RestAPIClient):
    """
    Class to be used for all Anthology API Integrations
    """

    _campus_id = 5

    def __init__(self, base_url, application_key):
        super().__init__(authorization=application_key, base_url=base_url)

        self.timeout = 30  # Anthology's APIs are incredibly slow and prone to timeouts.
        self.endpoints = all_endpoints

    @staticmethod
    def format_anthology_filters(supplied_filters: Dict) -> AnyStr:
        """
        There is a commonality on the way that anthology applies filters in many different API calls. This function
        will go through those similar filters and create a common query string

        Args:
            supplied_filters (Dict): dictionary of filter key and the corresponding True/False vale
        """
        filter_key_map = {
            "course_drop": "IsForDrop",
            "course_unregister": "IsForUnregister",
            "grade_drop": "IsDropGrade",
            "grade_pass_fail": "IsPassFail",
        }
        filter_string = ""
        for key, filter_val in supplied_filters.items():
            if not filter_key_map.get(key):
                continue
            if filter_string != "":
                filter_string += " and "
            filter_string += f"{filter_key_map.get(key)} eq {filter_val}"
        return filter_string

    def make_request(self, **kwargs):
        response = self._make_request(**kwargs)
        return response.get("payload").get("data") if response.get("payload", {}).get("data") else response

    from .certificate._create import create_certificate

    from .configuration._read import fetch_configurations
    from .configuration._create import create_term, create_start_date, validate_term, add_programs_to_start_date
    from .configuration._copy import copy_class_schedule

    from .course._change import fetch_course_change_reason
    from .course._drop import drop_course, fetch_drop_reason
    from .course._grade import post_final_grade, fetch_grade
    from .course._read import (
        fetch_all_courses,
        fetch_course,
        fetch_course_for_enrollment,
        fetch_term_for_courses,
        fetch_classes_for_courses,
        fetch_course_by_cccid,
        fetch_all_enrolled_courses,
    )
    from .course._register import register_course, add_new_course, add_attendance
    from .course._reinstate import reinstate_course
    from .course._unregister import unregister_course

    from .enrollment._create import create_enrollment
    from .enrollment._read import (
        fetch_enrollment_by_cccid,
        fetch_enrollment_by_enrollment_id,
        fetch_all_enrollments,
        fetch_student_enrollment_period_by_id,
    )

    from .student._create import create_student
    from .student._read import student_by_id, student_search  # refactored
    from .student._update import update_student, change_student_status
