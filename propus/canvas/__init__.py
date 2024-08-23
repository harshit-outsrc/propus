from propus.api_client import RestAPIClient
from propus.canvas.endpoints import all_endpoints
from propus.logging_utility import Logging


class Canvas(RestAPIClient):

    _account_id = 1

    def __init__(
        self,
        base_url: str,
        application_key: str,
        auth_providers: dict,
        # Note - this is to work around the RestAPIClient not including post headers for the delete method
        additional_headers={"Content-Type": "application/json"},
    ):
        super().__init__(
            authorization=application_key,
            base_url=base_url,
            additional_headers=additional_headers,
        )
        self.logger = Logging.get_logger("propus/canvas")

        self.endpoints = all_endpoints
        self.auth_providers = auth_providers

    def make_request(self, **kwargs):
        req_type = kwargs.get("req_type", "get")
        url = kwargs.get("url", "")
        data = kwargs.get("data", None)
        headers = kwargs.get("headers", None)
        params = kwargs.get("params", None)
        timeout = kwargs.get("timeout", None)

        all_results = []
        next_url = url
        while next_url:
            response = self._make_request(
                next_url,
                data=data,
                headers=headers,
                params=params,
                req_type=req_type,
                timeout=timeout,
                include_full_response=True,
            )

            json_response = response.json()
            if isinstance(json_response, list):
                all_results.extend(json_response)
            elif json_response.get("payload", {}):
                all_results.extend(json_response.get("payload"))
            # if the method is a post, etc. then just return the json object...
            elif req_type != "get":
                return json_response
            else:
                all_results.append(json_response)

            next_url = response.links.get("next", {}).get("url")

        return all_results if all_results else json_response

    from .user._create import create_user
    from .user._update import update_user
    from .user._read import (
        get_user,
        get_user_profile,
        list_users_in_account,
        get_user_page_views,
    )

    from .course._create import create_course, create_section
    from .course._read import get_course, get_section
    from .course._update import update_course, update_course_settings, update_section
    from .course._delete import delete_or_conclude_course, delete_section

    from .enrollment._create import create_enrollment
    from .enrollment._read import list_students_in_course, list_enrollments, get_single_enrollment
    from .enrollment._update import reactivate_enrollment
    from .enrollment._delete import conclude_delete_deactivate_enrollment

    from .module._read import get_course_modules

    from .term._create import create_term
    from .term._read import get_term, list_terms
    from .term._update import update_term
    from .term._delete import delete_term

    from .submission._read import (
        list_assignment_submissions_for_single_assignment,
        list_assignment_submissions_for_multiple_assignments,
        get_single_submission,
        get_submission_summary,
        list_missing_submissions_for_user,
    )

    from .assignment._read import (
        get_course_assignments,
        get_assignment,
        get_course_assignment_groups,
        get_assignment_group,
    )
