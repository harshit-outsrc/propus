import asyncio
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyConfigurationRead(TestAPIClient):
    """
    Since all of the configuration retriever functions are similar this test class will test all files
    """

    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.test_urls = {
            "configuration_billing_method": f"{self.url}/ds/campusnexus/BillingMethods?$filter=Id eq 1",
            "configuration_catalog_year": f"{self.url}/ds/campusnexus/ProgramVersions/CampusNexus.GetAreaOfStudyCatalogList(programVersionId=567842)?&$format=json&$count=true&$filter=IsMapped eq true and IsActive eq true or(Id eq 567842 and IsActive eq false)&$orderby=Name",
            "configuration_ethnicity": f"{self.url}/ds/odata/Ethnicities?$filter=IsActive%20eq%20true&$select=Id,Name",
            "configuration_gender": f"{self.url}/ds/odata/Genders?$filter=IsActive%20eq%20true&$select=Id,Name",
            "configuration_grade_level": f"{self.url}/ds/campusnexus/GradeLevels?&$format=json&$count=true&$filter=IsActive eq true&$orderby=Name",
            "configuration_program": f"{self.url}/ds/campusnexus/Programs/CampusNexus.GetEnrollmentProgramList(campusId=5,degreeProgram=0)?&$format=json&$filter=IsActive eq true or (Id eq 0)&$orderby=Name",
            "configuration_program_version": f"{self.url}/ds/campusnexus/ProgramVersions/CampusNexus.GetEnrollmentProgramVersions(campusId=5)?&$format=json&$count=true&$filter=ProgramId eq 98563 and IsActive eq true and IsDegreeProgram eq false or (Id eq 0)&$orderby=Name",
            "configuration_pronoun": f"{self.url}/ds/odata/GenderPronouns?$filter=IsActive eq true&$select=Id,Name",
            "configuration_school_status": f"{self.url}/ds/odata/SchoolStatuses?$filter=IsActive eq true&$select=Id,Name",
            "configuration_shift": f"{self.url}/ds/campusnexus/Shifts?$select=Id,Code,Name,IsActive&$format=json&$count=true&$filter=CampusGroup/CampusList/any(cl:cl/CampusId eq 5) and IsActive eq true&$orderby=Name",
            "configuration_start_date": f"{self.url}/ds/campusnexus/SchoolStartDates/CampusNexus.GetEnrollmentSchoolStartDates(campusId=5,programVersionId=jdskdasnjk)?&$format=json&$count=true&$filter=IsActive eq true&$orderby=StartDate desc",
            "configuration_term": f"{self.url}/ds/odata/Terms?$orderby=StartDate&$select=Code,StartDate,EndDate,AddDropDate,Id",
            "configuration_title": f"{self.url}/ds/odata/Titles?$filter=IsActive eq true&$select=Id,Name",
        }
        self.api_client.timeout = 30

    def test_configuration_read(self):
        configuration_tests = {
            "billing_method": {},
            "catalog_year": {"program_version_id": 567842},
            "ethnicity": {},
            "gender": {},
            "grade_level": {},
            "program": {},
            "program_version": {"program_id": 98563},
            "pronoun": {},
            "school_status": {},
            "shift": {},
            "start_date": {"program_version_id": "jdskdasnjk"},
            "term": {},
            "title": {},
        }
        for config, args in configuration_tests.items():
            self.test_name = f"configuration_{config}"
            self.assertEqual(asyncio.run(self.anthology.fetch_configurations(config, **args)), self.success_response)


if __name__ == "__main__":
    unittest.main()
