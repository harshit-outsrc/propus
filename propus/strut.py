from propus.api_client import RestAPIClient
from typing import AnyStr, List, Dict
import json


class Strut(RestAPIClient):
    _base_url = "https://api.strutlearning.com"
    _org = "calbright"

    def __init__(self, access_token, org=_org, base_url=_base_url):
        org = org if org else self._org
        super().__init__(
            authorization=f"Bearer {access_token}",
            base_url=base_url if base_url else self._base_url,
            additional_headers={
                "Accept": "application/vnd.strut.v2+json",
                "SL-Tenant": org,
            },
        )
        self.bulk_endpoints = {
            "fetch_competencies": "/competencies",
            "fetch_enrollments": "/enrollments",
            "fetch_users": "/users/users",
        }
        self.endpoints = {
            "fetch_user_by_id": ("/users/users/<user_id>", ["<user_id>"]),
            "fetch_enrollment_by_id": (
                "/enrollments/<enrollment_id>",
                ["<enrollment_id>"],
            ),
            "fetch_student_tags": (
                "/users/users/<user_id>?shallow=false&depth=0&include_state=true&structure_only=true&tags=true",
                ["<user_id>"],
            ),
            "remove_tags": ("/users/users/<strut_id>/tags/<tag_id>", ["<strut_id>", "<tag_id>"]),
            "assign_student_tags": ("/users/users/<strut_id>/tags", ["<strut_id>"]),
            "update_student": ("/users/users/<strut_id>", ["<strut_id>"]),
            "product_purchase": ("/products/<product_id>/purchase", ["<product_id>"]),
            "fetch_product_ids": ("/users/users/<user_id>/purchases", ["<user_id>"]),
        } | self.bulk_endpoints
        self.next_page_token = "start"
        self.pagination_fields = ["count", "start", "total"]
        self.program_tag_ids = {
            "Project Management": "57",
            "T2T Intro to Networks": "54",
            "Data Analysis": "7",
            "Career Readiness": "6",
            "HC DEI": "5",
            "Cybersecurity": "3",
            "IT Support": "2",
            "Medical Coding": "1",
        }
        self.valid_statuses = ["active", "disabled", "leave", "withdrawn"]
        self.valid_enrollment_statuses = ["active", "completed", "locked"]

    @staticmethod
    def build(**kwargs):
        access_token = kwargs.get("token")
        base_url = None if not kwargs.get("url") else kwargs.get("url")
        org = None if not kwargs.get("org") else kwargs.get("org")
        return Strut(access_token=access_token, org=org, base_url=base_url)

    def _get_data_and_next_page_token(self, results, params):
        """Processes a single set of results for data and the next page of results if applicable."""
        data = []
        next_page_token = results.pop(self.next_page_token, 0)
        query_count = results.pop("count", 0)
        total_records = results.pop("total", 0)
        next_page_token += query_count
        next_page_token = None if next_page_token >= total_records else next_page_token
        params[self.next_page_token] = next_page_token
        for k, v in results.items():
            if k not in self.pagination_fields:
                data = v
                break
        return data, next_page_token

    def _check_user_state(self, status):
        if status not in self.valid_statuses:
            raise Exception(f"status {status} is not recognized")

    def _check_enrollment_state(self, state):
        if state not in self.valid_enrollment_statuses:
            raise Exception(f"Invalid state value {state} for enrollment.")

    def _check_program_tag(self, program_name):
        if program_name not in self.program_tag_ids:
            raise Exception(f"program_name {program_name} is not recognized")

    def fetch_users(self, **kwargs):
        return self.get_bulk_data_by_endpoint("fetch_users", params=kwargs)

    def fetch_user_by_id(self, user_id, **kwargs):
        url = self._get_endpoint("fetch_user_by_id", {"<user_id>": user_id})
        return self._make_request(url, params=kwargs)

    def fetch_enrollments(self, **kwargs):
        return self.get_bulk_data_by_endpoint("fetch_enrollments", params=kwargs)

    def fetch_enrollment_by_id(self, enrollment_id, **kwargs):
        url = self._get_endpoint("fetch_enrollment_by_id", {"<enrollment_id>": enrollment_id})
        return self._make_request(url, params=kwargs)

    def create_enrollment(self, student_strut_id, competency_id, state="active", **kwargs):
        self._check_enrollment_state(state)
        url = self._get_endpoint("fetch_enrollments")
        enrollment_data = {"student_id": student_strut_id, "competency_id": competency_id, "state": state}
        return self._make_request(
            req_type="post", data=json.dumps({"enrollment": enrollment_data}), params=kwargs, url=url
        )

    def add_product_to_student(self, student_strut_id, product_id, **kwargs):
        url = self._get_endpoint("product_purchase", {"<product_id>": product_id})
        product_assignment_data = {"student_id": student_strut_id, "product_id": product_id}
        return self._make_request(
            req_type="post", data=json.dumps({"product_purchase": product_assignment_data}), params=kwargs, url=url
        )

    def update_enrollment(self, student_strut_id, enrollment_id, state="active", **kwargs):
        self._check_enrollment_state(state)
        url = self._get_endpoint("fetch_enrollment_by_id", {"<enrollment_id>": enrollment_id})
        enrollment_data = {"student_id": student_strut_id, "state": state}
        return self._make_request(
            req_type="put", data=json.dumps({"enrollment": enrollment_data}), params=kwargs, url=url
        )

    def fetch_competencies(self, **kwargs):
        return self.get_bulk_data_by_endpoint("fetch_competencies", params=kwargs)

    def fetch_student_enrollments(self, user_id, **kwargs):
        self.fetch_enrollments(student_id=user_id, **kwargs)

    def fetch_student_tags(self, user_id, **kwargs):
        url = self._get_endpoint("fetch_student_tags", {"<user_id>": user_id})
        return self._make_request(url, params=kwargs).get("tags")

    def fetch_product_ids(self, user_id, **kwargs):
        url = self._get_endpoint("fetch_product_ids", {"<user_id>": user_id})
        return self._make_request(url, params=kwargs)

    def remove_all_student_tags(self, strut_id: AnyStr, existing_tags: List) -> List[Dict]:
        """
        This function loops though tags 1-5 and issues a delete call for each one

        Args:
            strut_id (AnyStr): Student's Strut ID
            existing_tags (List): List of tag ids provided as str or int

        Returns:
            Dict: direct response from strut
        """

        existing_tags = {str(tag) for tag in existing_tags}
        req_responses = []
        tags_to_remove = filter(lambda tag: True if tag in existing_tags else False, self.program_tag_ids.values())
        for tag_id in tags_to_remove:
            url = self._get_endpoint("remove_tags", {"<strut_id>": strut_id, "<tag_id>": tag_id})
            resp = self._make_request(url, req_type="delete")
            req_responses.append(resp)
        return req_responses

    def assign_student_tags(self, strut_id: AnyStr, program_name: AnyStr) -> Dict:
        """
        This function updates the tag id attached to a student

        Args:
            strut_id (AnyStr): Student's Strut ID
            program_name (AnyStr): Strut Program Name

        Returns:
            Dict: direct response from strut
        """
        self._check_program_tag(program_name)

        url = self._get_endpoint("assign_student_tags", {"<strut_id>": strut_id})
        try:
            resp = self._make_request(
                url, req_type="post", data=json.dumps({"tag_id": self.program_tag_ids.get(program_name)})
            )
            return resp
        except Exception as exception:
            if resp.status == "409":  # Student tag already exists
                return
            raise exception

    def assign_student_state(self, strut_id: AnyStr, status: AnyStr) -> Dict:
        """
        This function updates the student's status in strut

        Args:
            strut_id (AnyStr): Student's Strut ID
            status (AnyStr): Status name to update the student to

        Returns:
            Dict: direct response from strut
        """
        self._check_user_state(status)

        url = self._get_endpoint("update_student", {"<strut_id>": strut_id})
        return self._make_request(url, req_type="put", data=json.dumps({"user": {"state": status}}))
