import json
import requests
from requests.exceptions import Timeout
from typing import AnyStr, Dict

from propus.api_client import FailedRequest, RestAPIClient
from propus.logging_utility import Logging


class Salesforce(RestAPIClient):
    """
    Class to be used for all Salesforce API integrations
    """

    _key_map = {"first_name": "FirstName", "last_name": "LastName"}
    _calbright_sf_account_id = "0013k00002lAtFyAAK"

    def __init__(self, access_token, base_url, version, env=None, ssm=None):
        super().__init__(authorization=access_token, base_url=base_url)
        self.logger = Logging.get_logger("propus/salesforce")
        self.version = version
        self.instance_url = base_url
        self.access_token = access_token
        self.env = env
        self.ssm = ssm
        self.endpoints = {
            # salesforce.py
            "custom_query": f"/services/data/{self.version}/query/",
            # _case.py
            "case_by_sfid": (
                f"/services/data/{self.version}/sobjects/Case/<sfid>",
                ["<sfid>"],
            ),
            "create_case": f"/services/data/{self.version}/sobjects/Case/",
            "update_case": (
                f"/services/data/{self.version}/sobjects/Case/<sfid>",
                ["<sfid>"],
            ),
            # _contact_record.py
            "contact_by_sfid": (
                f"/services/data/{self.version}/sobjects/Contact/<sfid>",
                ["<sfid>"],
            ),
            "update_contact": (
                f"/services/data/{self.version}/sobjects/Contact/<sfid>",
                ["<sfid>"],
            ),
            "create_contact": f"/services/data/{self.version}/sobjects/Contact/",
            # _veteran_record.py
            "create_vet_record": f"/services/data/{self.version}/sobjects/Veteran_Service_Record__c/",
            "update_vet_record": (
                f"/services/data/{self.version}/sobjects/Veteran_Service_Record__c/<vet_id>",
                ["<vet_id>"],
            ),
            "delete_vet_record": (
                f"/services/data/{self.version}/sobjects/Veteran_Service_Record__c/<vet_id>",
                ["<vet_id>"],
            ),
            # _event.py
            "create_event": f"/services/data/{self.version}/sobjects/Event/",
            # _end_of_term_grades.py
            "create_end_of_term_grade": f"/services/data/{self.version}/sobjects/C_End_of_Term_Grade__c/",
            "update_end_of_term_grade": (
                f"/services/data/{self.version}/sobjects/C_End_of_Term_Grade__c/<grade_id>",
                ["<grade_id>"],
            ),
            "delete_end_of_term_grade": (
                f"/services/data/{self.version}/sobjects/C_End_of_Term_Grade__c/<grade_id>",
                ["<grade_id>"],
            ),
            # _program_enrollments.py
            "create_program_enrollment_record": f"/services/data/{self.version}/sobjects/Program_Enrollments__c/",
            "delete_program_enrollment_record": (
                f"/services/data/{self.version}/sobjects/Program_Enrollments__c/<enrollment_id>",
                ["<enrollment_id>"],
            ),
            "update_program_enrollment_record": (
                f"/services/data/{self.version}/sobjects/Program_Enrollments__c/<enrollment_id>",
                ["<enrollment_id>"],
            ),
            # _task.py
            "create_task": f"/services/data/{self.version}/sobjects/Task/",
            # _bulk.py for API version 47.0 and later
            "create_bulk_query_job": f"/services/data/{self.version}/jobs/query",
            "query_bulk_job": (
                f"/services/data/{self.version}/jobs/query/<sf_jobid>",
                ["<sf_jobid>"],
            ),
            "query_bulk_job_results": (
                f"/services/data/{self.version}/jobs/query/<sf_jobid>/results",
                ["<sf_jobid>"],
            ),
            # _attachment
            "fetch_attachment": (
                f"/services/data/{self.version}/sobjects/Attachment/<attachment_id>/Body",
                ["<attachment_id>"],
            ),
            "create_attachment": f"/services/data/{self.version}/sobjects/Attachment",
            # _terms
            "create_term": f"/services/data/{self.version}/sobjects/hed__Term__c/",
        }
        self.timeout = 15

    @staticmethod
    def build_v2(env, ssm, version="v56.0"):
        current_key = ssm.get_param(f"salesforce.{env}.token", param_type="json")
        return Salesforce(
            access_token=current_key.get("bearer"),
            base_url=current_key.get("base_url"),
            version=version,
            env=env,
            ssm=ssm,
        )

    @staticmethod
    def build(
        username: AnyStr,
        password: AnyStr,
        consumer_key: AnyStr = None,
        consumer_secret: AnyStr = None,
        login_url: AnyStr = "test.salesforce.com",
        version="v56.0",
    ):
        def login(e, p, attempts=0):
            try:
                resp = requests.post(e, data=p, timeout=15)
            except Timeout:
                if attempts >= 2:
                    raise
                login(e, p, attempts + 1)
            return resp.json()

        payload = {
            "grant_type": "password",
            "client_id": consumer_key,
            "client_secret": consumer_secret,
            "username": username,
            "password": password,
        }
        endpoint = f"https://{login_url}/services/oauth2/token"
        j_resp = login(endpoint, payload)
        return Salesforce(f"Bearer {j_resp.get('access_token')}", j_resp.get("instance_url"), version)

    def login_invalid_session(self):
        def login_to_salesforce(e, p, attempts=0):
            try:
                resp = requests.post(e, data=p, timeout=15)
            except Timeout:
                if attempts >= 2:
                    raise
                login_to_salesforce(e, p, attempts + 1)
            return resp.json()

        creds = self.ssm.get_param(parameter_name=f"salesforce.{self.env}.login", param_type="json")
        payload = {
            "grant_type": "password",
            "client_id": creds.get("consumer_key"),
            "client_secret": creds.get("consumer_secret"),
            "username": creds.get("username"),
            "password": creds.get("password"),
        }
        endpoint = f"https://{creds.get('login_url')}/services/oauth2/token"
        j_resp = login_to_salesforce(endpoint, payload)
        bearer_token = f"Bearer {j_resp.get('access_token')}"
        self._update_auth(bearer_token)
        self.ssm.put_param(
            parameter_name=f"salesforce.{self.env}.token",
            description=f"Salesforce {self.env} Token for Login",
            value=json.dumps({"base_url": self.instance_url, "bearer": bearer_token}),
            overwrite=True,
        )

    def make_request(
        self, url, data=None, headers=None, params=None, req_type="get", timeout=None, should_retry=True
    ) -> Dict:
        """
        This is a wrapper above APIClient's _make_request function. It is used as a catch all make_request
        for Salesforce queries and attempt the request. If the request fails with a session expired
        error the session will be refreshed and then attempted again. If the request, fails again the error will
        be raised to the caller.

         Args:
            url (required): Full API endpoint path to call
            data (optional): JSON data; sub-classes may alternately override
                the DEFAULT_POST_TYPE to provide data in a different format
            headers (optional): dictionary of headers, provide if
                overriding the default API client headers
            params (optional): dictionary to be provided as a query string
            req_type: type of request to be made (defaults to GET)
            timeout (optional): max duration (seconds) integer for request
            should_retry (optional, Bool): If login has already been attempted once do not try again


        Returns:
            Response in JSON format
        """
        try:
            return self._make_request(url, data, headers, params, req_type, timeout)
        except FailedRequest as err:
            if "session expired" in str(err).lower() and should_retry is True:
                self.login_invalid_session()
                return self.make_request(url, data, headers, params, req_type, timeout, False)
            raise err

    def custom_query(self, soql_query: AnyStr):
        """
        custom_query takes in a SOQL query and issues that query against Salesforce. It materializes the whole result
        into a python list. This is suboptimal for large query results

        Args:
            soql_query (AnyStr): SOQL Query

        Returns:
            _type_: Results from Salesforce API
        """
        url = self._get_endpoint("custom_query")
        response = self.make_request(url, req_type="get", params={"q": soql_query})
        total_size = response.get("totalSize", 0)
        records = response.get("records", [])
        while response.get("done") is False:
            response = self.make_request(self.base_url + response.get("nextRecordsUrl"))
            records.extend(response.get("records", []))
        return {"totalSize": total_size, "records": records}

    from ._case import (
        fetch_case_details_record_by_case_number,
        fetch_case_record_by_sf_id,
        update_case_record,
        create_case_record,
    )
    from ._contact_record import (
        fetch_contact_accessibility_record_by_ccc_id,
        fetch_contact_details_record_by_ccc_id,
        fetch_contact_record_by_sf_id,
        fetch_salesforce_id_by_ccc_id,
        update_contact_record,
        create_contact_record,
    )
    from ._event import create_event
    from ._task import create_task
    from ._veteran_record import (
        _fetch_veteran_data,
        fetch_vet_record_by_sf_id,
        create_vet_record,
        update_vet_record,
        delete_vet_record,
        fetch_vet_record_by_contact_data,
        fetch_contact_vet_record_by_ccc_id,
    )
    from ._bulk import (
        _abort_query_job,
        _bulk_query_results,
        _create_query_job,
        _delete_query_job,
        _get_query_job,
        _get_query_job_results,
        get_dict_from_bulk_query_results,
        bulk_custom_query_operation,
    )
    from ._attachment import fetch_attachment, create_attachment
    from ._program_enrollments import (
        create_program_enrollment_record,
        _fetch_program_enrollment_data,
        delete_program_enrollment_record,
        update_program_enrollment_record,
    )
    from ._end_of_term_grades import (
        create_end_of_term_grade,
        update_end_of_term_grade,
        _format_course_name,
        _fetch_instructor,
        delete_end_of_term_grade,
    )
    from ._terms import create_term, fetch_terms
