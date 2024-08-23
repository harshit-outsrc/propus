import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestProgramEnrollment(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock
        self.sf_id = "XXXXXXXXXXXXXXXXXX"

        self.program_enrollment_data = {
            "Enrollment_Status__c": "status",
            "Program_Name__c": "name",
            "Date_of_Enrollment__c": "date",
            "Contact__c": "contact",
        }
        self._test_data = self._test_data | self.program_enrollment_data

        self.test_urls = {
            "create_program_enrollment_record": (
                f"{self.url}/services/data/{self.version}/sobjects/Program_Enrollments__c/"
            ),
            "delete_program_enrollment": f"{self.url}/services/data/{self.version}/sobjects/Program_Enrollments__c/{self.sf_id}",
        }
        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 15

    def test_create_program_enrollment_record(self):
        self.test_name = "create_program_enrollment_record"
        self.success_response = {"status": "success"}
        self.assertEqual(
            self.salesforce.create_program_enrollment_record(
                enrollment_status=self.program_enrollment_data.get("Enrollment_Status__c"),
                program_name=self.program_enrollment_data.get("Program_Name__c"),
                date_of_enrollment=self.program_enrollment_data.get("Date_of_Enrollment__c"),
                contact=self.program_enrollment_data.get("Contact__c"),
            ),
            self.success_response,
        )

    def test_delete_program_enrollment(self):
        self.test_name = "delete_program_enrollment"
        self.success_response = {"status": "success"}
        self.assertIsNone(self.salesforce.delete_program_enrollment_record(enrollment_id=self.sf_id))


if __name__ == "__main__":
    unittest.main()
