import unittest

from propus.salesforce import Salesforce
from tests.api_client import TestAPIClient


class TestSalesforceVeteranRecord(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.version = "salesforce_version"
        self.salesforce = Salesforce(self.application_key, self.url, self.version)
        self.salesforce.request_service = self._req_mock
        self.test_id = "ABC_67543_XYZ"
        self.email = "test@clabright.org"
        self.vet_record_id = "VR_123456"

        self.vet_data = {
            "Related_Student__c": "XYZ_56723_ABG",
            "Status__c": "VR STATUS",
            "Intake_Form_Sent_Date__c": "TODAY",
            "Intake_Form_Submitted_Date__c": "YESTERDAY",
            "Do_You_Have_Any_Disabilities__c": "Calbright1234",
            "Branch_of_Service__c": "1;2;3",
            "Calbright_Student_Supports_Interested_In__c": "a;b;c;d",
            "Community_Support_Services_Interested_In__c": "z;x;y",
            "Intake_stated_Program_of_Study__c": "12379128939128",
            "Other_Status__c": "This is the other status",
            "Other_Branch_of_Service__c": "This is the other branch of service",
            "Intake_stated_program_Other__c": "This is the other intake program",
        }
        self._test_data = self._test_data | self.vet_data

        self.test_urls = {
            "vet_record_by_sf_id": f"{self.url}/services/data/salesforce_version/query/",
            "vet_by_ccid": f"{self.url}/services/data/salesforce_version/query/",
            "create_vet_record": f"{self.url}/services/data/{self.version}/sobjects/Veteran_Service_Record__c/",
            "update_vet_record": f"{self.url}/services/data/{self.version}/sobjects/Veteran_Service_Record__c/{self.vet_record_id}",
            "delete_vet_record": f"{self.url}/services/data/{self.version}/sobjects/Veteran_Service_Record__c/{self.vet_record_id}",
        }
        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 15

    def test_fetch_vet_record_by_sf_id(self):
        self.test_name = "vet_record_by_sf_id"
        self.test_params[self.test_name] = {
            "q": f"SELECT Id, Intake_Form_Sent_Date__c, Intake_Form_Submitted_Date__c,\n    Branch_of_Service__c, Do_You_Have_Any_Disabilities__c, Community_Support_Services_Interested_In__c, Status__c FROM\n    Veteran_Service_Record__c WHERE Related_Student__c = '{self.test_id}'"
        }  # noqa:E501
        self.success_response = {"totalSize": 5, "records": [1, 2, 3, 4]}
        self.assertEqual(
            self.salesforce.fetch_vet_record_by_sf_id(self.test_id),
            self.success_response,
        )

    def test_fetch_vet_record_by_ccc_id(self):
        self.test_name = "vet_by_ccid"
        self.test_params[self.test_name] = {
            "q": f"SELECT Id, Related_Student__r.Id, Intake_Form_Sent_Date__c,\n    Intake_Form_Submitted_Date__c, Branch_of_Service__c, Do_You_Have_Any_Disabilities__c,\n    Community_Support_Services_Interested_In__c, Status__c FROM Veteran_Service_Record__c\n    WHERE Related_Student__r.cfg_CCC_ID__c = '{self.test_id}' AND Related_Student__r.cfg_Calbright_Email__c = '{self.email}'"
        }  # noqa:E501
        self.success_response = {"totalSize": 1, "records": [1, 2, 3, 4]}
        self.assertEqual(
            self.salesforce.fetch_vet_record_by_contact_data(self.test_id, self.email),
            self.success_response,
        )

    def test_create_vet_record(self):
        self.test_name = "create_vet_record"
        self.success_response = {"status": "success"}
        self.assertEqual(
            self.salesforce.create_vet_record(
                self.vet_data.get("Related_Student__c"),
                intake_form_sent=self.vet_data.get("Intake_Form_Sent_Date__c"),
                intake_form_submitted=self.vet_data.get("Intake_Form_Submitted_Date__c"),
                status=self.vet_data.get("Status__c"),
                disabilities=self.vet_data.get("Do_You_Have_Any_Disabilities__c"),
                branch_of_service=self.vet_data.get("Branch_of_Service__c").split(";"),
                student_supports=self.vet_data.get("Calbright_Student_Supports_Interested_In__c").split(";"),
                community_support=self.vet_data.get("Community_Support_Services_Interested_In__c").split(";"),
                program_of_study=self.vet_data.get("Intake_stated_Program_of_Study__c"),
                other_status=self.vet_data.get("Other_Status__c"),
                other_branch_of_service=self.vet_data.get("Other_Branch_of_Service__c"),
                other_program_of_study=self.vet_data.get("Intake_stated_program_Other__c"),
            ),
            self.success_response,
        )

    def test_update_vet_record(self):
        self.test_name = "update_vet_record"
        self.success_response = {"status": "updated"}
        self.assertIsNone(self.salesforce.update_vet_record(self.vet_record_id, status=self.test_data.get("Status__c")))

    def test_delete_vet_record(self):
        self.test_name = "delete_vet_record"
        self.success_response = {"status": "updated"}
        self.assertIsNone(self.salesforce.delete_vet_record(self.vet_record_id))


if __name__ == "__main__":
    unittest.main()
