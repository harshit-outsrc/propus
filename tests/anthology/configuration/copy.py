import asyncio
from datetime import datetime
from typing import List
import unittest

from propus.helpers.exceptions import (
    InvalidStringLength,
    InvalidDayOfWeek,
)
from propus.anthology.configuration._exception import InvalidTerm
from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyConfigurationCopy(TestAPIClient):
    def setUp(self):
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.copy_data = {
            "CampusId": 5,
            "CopyClassScheduleOption": "ALL",
            "CourseId": 2,
            "ExtendedPropertyList": [
                {"IsExtendedProperty": True, "Name": "XB01 Accounting Method"},
                {"IsExtendedProperty": True, "Name": "XB02 Date First Census"},
                {"IsExtendedProperty": True, "Name": "XB04 Contract Education Code"},
                {"IsExtendedProperty": True, "Name": "XB08 DSPS Special Status"},
                {"IsExtendedProperty": True, "Name": "XB09 Work Based Learning Activities"},
                {"IsExtendedProperty": True, "Name": "XB10 CVU/CVC Status"},
                {"IsExtendedProperty": True, "Name": "XB12 Instructional Material Cost"},
                {"IsExtendedProperty": True, "Name": "Census Date"},
            ],
            "Id": 0,
            "IsCopyAttendanceRules": True,
            "IsCopyBookList": True,
            "IsCopyCourseFeeSchedule": True,
            "IsCopyCourseSharingCampuses": True,
            "IsCopyDays": True,
            "IsCopyDocuments": True,
            "IsCopyGradeBook": True,
            "IsCopyHideFaculty": True,
            "IsCopyHideLocation": True,
            "IsCopyInstructor": True,
            "IsCopyLmsVendor": False,
            "IsCopyMaxCourseSections": True,
            "IsCopyRegistrationRelationships": True,
            "IsCopyRooms": True,
            "IsCopySecondaryInstructor": True,
            "IsCopySelectedOnlyAndCrossList": True,
            "IsCopyTimes": True,
            "IsCopyWaitList": True,
            "IsCrossList": True,
            "IsInstructorAttributes": True,
            "IsOnlyValidation": False,
            "IsSecondSecondaryCode": True,
            "isValidationMessageDisplayed": False,
            "IsVariableCredits": True,
            "NewSectionCode": "",
            "SourceTermId": "SOURCE_TERM_123",
            "TargetTermID": "TARGET_TERM_123",
        }

        self.test_urls = {
            "copy_class_schedule": f"{self.url}/api/commands/Academics/ClassSection/CopyClassSchedule",
        }

        self.test_urls = self.test_urls | self._test_urls
        self.api_client.timeout = 30

    def test_copy_class_schedule(self):
        self.test_name = "copy_class_schedule"
        self._test_data = {"payload": self.copy_data}
        self.assertEqual(
            asyncio.run(
                self.anthology.copy_class_schedule(source_term_id="SOURCE_TERM_123", target_term_id="TARGET_TERM_123")
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
