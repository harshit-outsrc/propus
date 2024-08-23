from propus.symplicity.csm import CSM
from tests.api_client import TestAPIClient


class TestCSM(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        # API client setup for test class
        self.api_client = CSM(access_token=self.application_key)
        self.api_client.request_service = self._req_mock

        self.student_id = "789123897sadbj1278bduyy"

        self.field_name = "student_picklist_items"
        self.test_urls = {
            "list_students": f"{CSM._base_url}/students",
            "list_staff": f"{CSM._base_url}/staff",
            "student_picklist": f"{CSM._base_url}/picklists/students/{self.field_name}",
            "disable_student": f"{CSM._base_url}/students/{self.student_id}",
        }

    def test_list_students(self):
        self.test_name = "list_students"
        self.test_params[self.test_name] = {
            "page": 3,
            "perPage": 14,
            "keywords": "KEY WORDS!!",
            "sort": "this direction",
            "customFields": "SURE",
        }
        self.assertEqual(
            self.api_client.list_students(
                **{
                    "page": 3,
                    "per_page": 14,
                    "keywords": "KEY WORDS!!",
                    "sort": "this direction",
                    "custom_fields": "SURE",
                }
            ),
            self.success_response,
        )

    def test_list_staff(self):
        self.test_name = "list_staff"
        self.test_params[self.test_name] = {
            "page": 3,
            "perPage": 14,
            "keywords": "KEY WORDS!!",
            "sort": "this direction",
            "customFields": "SURE",
        }
        self.assertEqual(
            self.api_client.list_staff(
                **{
                    "page": 3,
                    "per_page": 14,
                    "keywords": "KEY WORDS!!",
                    "sort": "this direction",
                    "custom_fields": "SURE",
                }
            ),
            self.success_response,
        )

    def test_fetch_form_picklist(self):
        self.test_name = "student_picklist"
        self.assertEqual(self.api_client.fetch_form_picklist(self.field_name), self.success_response)

    def test_disable_student(self):
        self.test_name = "disable_student"
        self._test_data = {"accountDisabled": True, "accountBlocked": "1"}
        self.assertEqual(self.api_client.disable_student(self.student_id), self.success_response)


if __name__ == "__main__":
    import unittest

    unittest.main()
