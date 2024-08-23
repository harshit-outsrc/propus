import json
from time import sleep

from propus.api_client import RestAPIClient
from propus.logging_utility import Logging


class CSM(RestAPIClient):
    _base_url = "https://calbright-csm.symplicity.com/api/public/v1"

    def __init__(self, access_token):
        super().__init__(authorization=access_token, base_url=self._base_url)
        self.logger = Logging.get_logger("propus/csm")
        self.endpoints = {
            "list_students": "/students",
            "list_staff": "/staff",
            "batch_student_job": "/students",
            "batch_job_results": ("/batch/<batch_id>", ["<batch_id>"]),
            "update_student": ("/students/<student_id>", ["<student_id>"]),
            "student_picklist": ("/picklists/students/<field_name>", ["<field_name>"]),
        }
        self.timeout = 25

    @staticmethod
    def build(api_key: str):
        return CSM(api_key)

    def list_students(
        self,
        page: int = 1,
        per_page: int = 500,
        keywords: str = None,
        sort: str = "schoolStudentId",
        custom_fields: int = 1,
    ):
        """
        List students from the API.

        Args:
            page (int): The page number to return (default 1).
            per_page (int): The number of results per page (default/max 500).
            keywords (str): An optional keyword to search students by.
            sort (str): The field to sort the results by (default "schoolStudentId").
            custom_fields (int): Technically a boolean (0 - no custom fields) (default 1).

        Returns:
            The results of calling CSM's API to fetch the students.
        """
        return self._list_people("students", page, per_page, keywords, sort, custom_fields)

    def list_staff(
        self,
        page: int = 1,
        per_page: int = 500,
        keywords: str = None,
        sort: str = "email",
        custom_fields: int = 1,
    ):
        """
        List staff from the API.

        Args:
            page (int): The page number to return (default 1).
            per_page (int): The number of results per page (default/max 500).
            keywords (str): An optional keyword to search staff by.
            sort (str): The field to sort the results by (default "email").
            custom_fields (int): Technically a boolean (0 - no custom fields) (default 1).

        Returns:
            The results of calling CSM's API to fetch the staff.
        """
        return self._list_people("staff", page, per_page, keywords, sort, custom_fields)

    def _list_people(self, people_type, page, per_page, keywords, sort, custom_fields):
        params = {
            "page": page,
            "perPage": per_page,
            "sort": sort,
            "customFields": custom_fields,
        }
        if keywords:
            params["keywords"] = keywords

        url = self._get_endpoint("list_students") if people_type == "students" else self._get_endpoint("list_staff")
        return self._make_request(url, params=params)

    def disable_student(self, student_id: str):
        """Disable a student by ID.

        Args:
            student_id (str): The CSM ID of the student to disable.

        Returns:
            The response from CSM API to disable the student.
        """
        return self.update_student(student_id, {"accountDisabled": True, "accountBlocked": "1"})

    def update_student(self, student_id: str, data: dict):
        """Update a student by ID.

        Args:
            student_id (str): The CSM ID of the student to update.
            data (dict): The data to update the student with.

        Returns:
            The response from CSM API to update the student.
        """
        return self._make_request(
            self._get_endpoint("update_student", {"<student_id>": student_id}), req_type="put", data=json.dumps(data)
        )

    def batch_create_students(self, create_data: dict):
        """Process a batch job by polling for completion.
        This function makes a request to create a batch job, then polls the
        status endpoint on an exponential backoff, retrieving the results once complete.

        Args:
            create_data (dict): The data for the batch job request.

        Returns:
            The final response from the batch job once completed.
        """
        return self._process_batch_job(create_data, "create")

    def batch_update_students(self, update_data: dict):
        """Process a batch job by polling for completion.
        This function makes a request to create an update batch job, then polls the
        status endpoint on an exponential backoff, retrieving the results once complete.

        Args:
            update_data (dict): The data for the batch job request.

        Returns:
            The final response from the batch job once completed.
        """
        return self._process_batch_job(update_data, "update")

    def _process_batch_job(self, data: dict, job_type: str):
        url = self._get_endpoint("batch_student_job")
        batch_response = self._make_request(
            url, req_type="post" if job_type == "create" else "put", data=json.dumps(data), params={"batch": 1}
        )
        batch_id = batch_response.get("id")
        sleep_in_seconds = 0
        while batch_response.get("status") != "completed":
            sleep_in_seconds += 1
            sleep(sleep_in_seconds**2)

            url = self._get_endpoint("batch_job_results", {"<batch_id>": batch_id})
            batch_response = self._make_request(url)
        return batch_response

    def fetch_form_picklist(self, field_name: str):
        """
        Retrieves the possible picklist options for a supplied field name

        Args:
            field_name (str): String name of the field to retrieve the picklist for.

        Returns:
            dict: the response from CSM API
        """
        return self._make_request(self._get_endpoint("student_picklist", {"<field_name>": field_name}))
