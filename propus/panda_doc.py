import json
from typing import AnyStr, Dict, List

from propus.api_client import RestAPIClient


class PandaDoc(RestAPIClient):
    def __init__(self, authorization, base_url):
        super().__init__(authorization=authorization, base_url=base_url)
        self.endpoints = {
            "get_doc_details": ("/public/v1/documents/<doc_id>/details", ["<doc_id>"]),
            "get_docs_list": ("/public/v1/documents?<query>", ["<query>"]),
            "create_doc": "/public/v1/documents",
            "send_doc": ("/public/v1/documents/<doc_id>/send", ["<doc_id>"]),
            "download_doc": ("/public/v1/documents/<doc_id>/download?separate_files=false", ["<doc_id>"]),
        }

    @staticmethod
    def build(authorization: AnyStr, base_url: AnyStr = "https://api.pandadoc.com"):
        """
        Singleton to build the PandaDoc Client.
        Args:
            authorization (AnyStr): API key used to query PandaDocs
            base_url (AnyStr): : base url for PandaDoc API
               - Defaults to https://api.pandadoc.com

        Returns:
            An instance of PandaDoc Class
        """
        return PandaDoc(authorization=f"API-Key {authorization}", base_url=base_url)

    def list_documents(
        self,
        status: int = None,
        created_from: AnyStr = None,
        completed_from: AnyStr = None,
        template_id=None,
        count: int = 100,
    ) -> Dict:
        """
        Wrapper for PandaDocs list document API.
        Documentation can be found here: https://developers.pandadoc.com/reference/list-documents

        Args:
            status (int, optional): Document Status. Defaults to None.
            created_from (AnyStr, optional): Return results where the date_created field is greater than or equal
                to this value. Format (YYYY-mm-ddTHH:MM:SS)
                    - Defaults to None.
            completed_from (AnyStr, optional): Return results where the date_completed field is greater than or equal
                to this value. Format (YYYY-mm-ddTHH:MM:SS)
                    - Defaults to None.
            template_id (AnyStr, optional): Return results where the template_id matches document templates
                    - Defaults to None.
            count (int, optional): Specify how many document results to return.
                    - Defaults to 100.

        Returns:
            Dict: Dictionary response from the PandaDoc API
        """
        query = f"count={count}&status=2"
        if status:
            query += f"&status={status}"
        if template_id:
            query += f"&template_id={template_id}"
        if created_from:
            query += f"&created_from={created_from}"
        if completed_from:
            query += f"&completed_from={completed_from}"

        url = self._get_endpoint("get_docs_list", {"<query>": query})
        return self._make_request(url)

    def fetch_document_details(self, doc_id: AnyStr) -> Dict:
        """
        Wrapper for PandaDocs document details API.
        Documentation can be found here: https://developers.pandadoc.com/reference/document-details

        Args:
            doc_id (AnyStr): ID of the document to be retrieved

        Returns:
            Dict: Dictionary response from the PandaDoc API
        """
        url = self._get_endpoint("get_doc_details", {"<doc_id>": doc_id})
        return self._make_request(url)

    def create_document_from_template(
        self,
        template_id: AnyStr,
        email_name: AnyStr,
        recipient_first_name: AnyStr,
        recipient_last_name: AnyStr,
        recipient_email: AnyStr,
        tokens: List[Dict],
        fields: List[Dict] = None,
    ):
        payload = {
            "template_uuid": template_id,
            "name": email_name,
            "recipients": [
                {
                    "email": recipient_email,
                    "first_name": recipient_first_name,
                    "last_name": recipient_last_name,
                    "role": "Student",
                }
            ],
            "tokens": tokens,
        }

        if fields:
            payload["fields"] = {k: v for field in fields for k, v in field.items()}

        url = self._get_endpoint("create_doc")
        return self._make_request(url, data=json.dumps(payload), req_type="post", params={})

    def send_document(self, doc_id: AnyStr, subject: AnyStr, message: AnyStr):
        payload = {
            "subject": subject,
            "message": message,
            "silent": False,
            "forwarding_settings": {
                "forwarding_allowed": True,
                "forwarding_with_reassigning_allowed": True,
            },
        }
        url = self._get_endpoint("send_doc", {"<doc_id>": doc_id})
        return self._make_request(url, data=json.dumps(payload), req_type="post")

    def download_document(self, doc_id: AnyStr):
        return self._make_request(self._get_endpoint("download_doc", {"<doc_id>": doc_id}))
