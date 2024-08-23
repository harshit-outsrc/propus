import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestEndOfTermGrades(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock

        self.ccc_id = "CCCID"
        self.course = "BUS500"
        self.term_name = "Fall 2022"
        self.sf_id = "XXXXXXXXXXXXXXXXXX"
        self.term_id = "TERM-1234"
        self.grade_data = {
            "Course__c": f"{self.course} - Introduction to Structured Data",
            "Instructor__c": "0055G000008sii8QAA",
            "Name": f"{self.ccc_id}-{self.course}-{self.term_name}",
            "Status__c": "NOT GRADED",
            "Student__c": self.sf_id,
            "Term__c": self.term_id,
        }
        self._test_data = self._test_data | self.grade_data

        self.test_urls = {
            "create_end_of_term_grade": f"{self.url}/services/data/{self.version}/sobjects/C_End_of_Term_Grade__c/",
            "update_end_of_term_grade": f"{self.url}/services/data/{self.version}/sobjects/C_End_of_Term_Grade__c/{self.sf_id}",
            "delete_end_of_term_grade": f"{self.url}/services/data/{self.version}/sobjects/C_End_of_Term_Grade__c/{self.sf_id}",
        }
        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 15

    def test_create_end_of_term_grade(self):
        self.test_name = "create_end_of_term_grade"
        self.success_response = {"status": "success"}
        self.assertEqual(
            self.salesforce.create_end_of_term_grade(
                course=self.course, ccc_id=self.ccc_id, sf_id=self.sf_id, term_id=self.term_id, term_name=self.term_name
            ),
            self.success_response,
        )

    def test_update_end_of_term_grade(self):
        self.test_name = "update_end_of_term_grade"
        self.success_response = {"status": "success"}
        self.assertIsNone(
            self.salesforce.update_end_of_term_grade(
                grade_id=self.sf_id, course=self.course, Term__c=self.term_id, Status__c="NOT GRADED"
            )
        )

    def test_delete_end_of_term_grade(self):
        self.test_name = "delete_end_of_term_grade"
        self.success_response = {"status": "success"}
        self.assertIsNone(self.salesforce.delete_end_of_term_grade(grade_id=self.sf_id))


if __name__ == "__main__":
    unittest.main()
