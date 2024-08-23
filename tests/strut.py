import unittest
from unittest.mock import Mock

from propus.strut import Strut
from tests.api_client import TestAPIClient


class TestStrut(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        # API client setup for test class
        self.api_client = Strut.build(access_token=self.application_key)
        self.api_client.request_service = self._req_mock
        self.api_client._yield_bulk_data = Mock(return_value=[self.success_response])
        self.bulk_success_response = ["test"]
        # Test data
        self.user_id = "1234509876"
        self.enrollment_id = "783267823"
        self.product_id = "12345"
        self.test_urls = {
            "fetch_user_by_id": f"{self.api_client._base_url}/users/users/{self.user_id}",
            "fetch_enrollments": f"{self.api_client._base_url}/enrollments",
            "fetch_enrollment_by_id": f"{self.api_client._base_url}/enrollments/{self.enrollment_id}",
            "fetch_competencies": f"{self.api_client._base_url}/competencies",
            "remove_student_tags": f"{self.api_client._base_url}/users/users/{self.user_id}/tags/123",
            "assign_student_tags": f"{self.api_client._base_url}/users/users/{self.user_id}/tags",
            "assign_student_state": f"{self.api_client._base_url}/users/users/{self.user_id}",
            "create_enrollment": f"{self.api_client._base_url}/enrollments",
            "update_enrollment": f"{self.api_client._base_url}/enrollments/{self.enrollment_id}",
            "product_purchase": f"{self.api_client._base_url}/products/{self.product_id}/purchase",
        }
        # Consolidate test data, endpoints, urls from parent and child classes
        self.api_client.endpoints = self.api_client.endpoints | self._endpoints
        self.test_urls = self.test_urls | self._test_urls
        self.api_client.program_tag_ids = {"program_name_abc": "123"}

    def test_fetch_users(self):
        self.test_name = "fetch_users"
        response = self.api_client.fetch_users()
        self.assertEqual(response, self.bulk_success_response)

    def test_fetch_user_by_id(self):
        self.test_name = "fetch_user_by_id"
        self.test_params[self.test_name] = {"compressed": True, "depth": 2}
        response = self.api_client.fetch_user_by_id(self.user_id, **self.test_params.get(self.test_name))
        self.assertEqual(response, self.success_response)

    def test_update_enrollment(self):
        self.test_name = "update_enrollment"
        self.test_params[self.test_name] = {"student_id": self.user_id}
        response = self.api_client.update_enrollment(
            student_strut_id=self.user_id, enrollment_id=self.enrollment_id, **self.test_params.get(self.test_name)
        )
        self.assertEqual(response, self.success_response)

    def test_create_enrollment(self):
        self.test_name = "create_enrollment"
        self.test_params[self.test_name] = {"student_id": self.user_id}
        response = self.api_client.create_enrollment(
            student_strut_id=self.user_id, competency_id="competency_id", **self.test_params.get(self.test_name)
        )
        self.assertEqual(response, self.success_response)

    def test_fetch_enrollments(self):
        self.test_name = "fetch_enrollments"
        self.test_params[self.test_name] = {"student_id": self.user_id}
        response = self.api_client.fetch_enrollments(**self.test_params.get(self.test_name))
        self.assertEqual(response, self.bulk_success_response)

    def test_fetch_enrollment_by_id(self):
        self.test_name = "fetch_enrollment_by_id"
        self.test_params[self.test_name] = {"include_state": True, "depth": 5}
        response = self.api_client.fetch_enrollment_by_id(self.enrollment_id, **self.test_params.get(self.test_name))
        self.assertEqual(response, self.success_response)

    def test_fetch_competencies(self):
        self.test_name = "fetch_competencies"
        self.test_params[self.test_name] = {"include_state": True, "depth": 5}
        response = self.api_client.fetch_competencies(**self.test_params.get(self.test_name))
        self.assertEqual(response, self.bulk_success_response)

    def test_remove_all_student_tags(self):
        self.test_name = "remove_student_tags"
        response = self.api_client.remove_all_student_tags(self.user_id, [1, 2, 3])
        self.assertEqual(response, [])

    def test_assign_student_tags(self):
        with self.assertRaises(Exception):
            self.api_client.assign_student_tags(self.user_id, "unknown_program_name")

        self.test_name = "assign_student_tags"
        self._test_data = self._test_data | {"tag_id": "123"}
        response = self.api_client.assign_student_tags(self.user_id, "program_name_abc")
        self.assertEqual(response, self.success_response)

    def test_add_product_to_student(self):
        self.test_name = "product_purchase"
        self.test_params[self.test_name] = {"student_id": self.user_id, "product_id": self.product_id}
        response = self.api_client.add_product_to_student(self.user_id, self.product_id)
        self.assertEqual(response, self.success_response)

    def test_assign_student_state(self):
        with self.assertRaises(Exception):
            self.api_client.assign_student_state(self.user_id, "unknown_status")

        self.test_name = "assign_student_state"
        self._test_data = self._test_data | {"user": {"state": "active"}}
        response = self.api_client.assign_student_state(self.user_id, "active")
        self.assertEqual(response, self.success_response)


if __name__ == "__main__":
    unittest.main()
