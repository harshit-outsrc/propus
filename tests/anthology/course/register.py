import asyncio
from datetime import datetime
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyCourseRegister(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock

        self.test_urls = {
            "add_attendance": f"{self.url}/api/commands/Academics/Attendance/PostExternshipOnlineHours",
            "add_new_course": f"{self.url}/api/commands/Academics/StudentCourse/saveNew",
            "register_course": f"{self.url}/api/commands/Academics/StudentCourse/savestudentcourse",
        }

        self.test_data = {
            "student_id": 98753,
            "class_section_id": 8364,
            "start_date": datetime(2023, 3, 23),
            "end_date": datetime(2024, 6, 15),
            "student_course_id": 987,
            "student_enrollment_id": 3746,
            "minutes_to_add": 54,
            "enrollment_id": "BNMENROLL_!234",
            "course_id": 6,
            "course_name": "testing something on course",
            "term_id": 836,
            "hours": 10,
        }
        self.api_client.timeout = 30

    def test_register_course(self):
        self.test_name = "register_course"
        self._test_data = {
            "payload": {
                "StudentCourseId": self.test_data.get("student_course_id"),
                "StudentEnrollmentPeriodId": "BNMENROLL_!234",
                "CampusId": 5,
                "ClassSectionId": self.test_data.get("class_section_id"),
                "CourseId": self.test_data.get("course_id"),
                "TermId": self.test_data.get("term_id"),
                "Hours": self.test_data.get("hours"),
                "Comments": "Registered Via API",
                "Credits": 0,
                "Action": 2,
                "AllowOverrideRegistrationHold": True,
                "IsAllowedToOverrideLockedTermSequence": True,
                "IsAllowedPostCourseStartDateRegistration": True,
                "Description": "",
                "StartDate": self.test_data.get("start_date").strftime("%Y-%m-%dT00:00:00"),
                "EndDate": self.test_data.get("end_date").strftime("%Y-%m-%dT00:00:00"),
                "RetakeID": 0,
                "ReturnCode": 0,
                "IsPassFail": 1,
                "RetakeFee": "O",
                "IsAddDropPeriodClassSectionAllowed": True,
                "IsAllowedToOverrideClosedTerm": True,
                "IsAllowedToOverrideRegistrationGroup": True,
                "IsPreCoRequisiteValidationSkipped": True,
            }
        }
        self.assertEqual(
            asyncio.run(
                self.anthology.register_course(
                    **{
                        "student_course_id": self.test_data.get("student_course_id"),
                        "enrollment_id": self.test_data.get("enrollment_id"),
                        "class_section_id": self.test_data.get("class_section_id"),
                        "course_id": self.test_data.get("course_id"),
                        "hours": self.test_data.get("hours"),
                        "term_id": self.test_data.get("term_id"),
                        "start_date": self.test_data.get("start_date"),
                        "end_date": self.test_data.get("end_date"),
                    }
                )
            ),
            self.success_response,
        )

    def test_add_new_course(self):
        self.test_name = "add_new_course"
        self._test_data = {
            "payload": {
                "CampusId": 5,
                "ClassSectionId": self.test_data.get("class_section_id"),
                "CourseId": self.test_data.get("course_id"),
                "CourseName": self.test_data.get("course_name"),
                "CreatedDateTime": "2024-07-18T00:00:00",
                "EndDate": self.test_data.get("end_date").strftime("%Y-%m-%dT00:00:00"),
                "IsPassFail": 1,
                "LetterGrade": "",
                "ModFlag": "A",
                "Note": "Created via API",
                "RetakeFeeWaived": "0",
                "RetakeOverride": False,
                "RosterFlag": "",
                "StartDate": self.test_data.get("start_date").strftime("%Y-%m-%dT00:00:00"),
                "Status": "F",
                "StudentEnrollmentPeriodId": "BNMENROLL_!234",
                "StudentId": self.test_data.get("student_id"),
                "TermId": self.test_data.get("term_id"),
            }
        }
        self.assertEqual(
            asyncio.run(
                self.anthology.add_new_course(
                    **{
                        "student_id": self.test_data.get("student_id"),
                        "enrollment_id": self.test_data.get("enrollment_id"),
                        "class_section_id": self.test_data.get("class_section_id"),
                        "course_id": self.test_data.get("course_id"),
                        "course_name": self.test_data.get("course_name"),
                        "term_id": self.test_data.get("term_id"),
                        "start_date": self.test_data.get("start_date"),
                        "end_date": self.test_data.get("end_date"),
                    }
                )
            ),
            self.success_response,
        )

    def test_add_attendance(self):
        self.test_name = "add_attendance"
        self._test_data = {
            "payload": {
                "StudentId": self.test_data.get("student_id"),
                "ClassSectionId": self.test_data.get("class_section_id"),
                "StartDate": self.test_data.get("start_date").strftime("%Y-%m-%dT00:00:00"),
                "EndDate": self.test_data.get("end_date").strftime("%Y-%m-%dT00:00:00"),
                "AllowClosedTerm": True,
                "IsPostExternshipOnline": True,
                "Entity": {
                    "Id": -1,
                    "ClassSectionMeetingDateId": 0,
                    "AttendanceDate": datetime.now().strftime("%Y-%m-%dT00:00:00.000"),
                    "Attended": self.test_data.get("minutes_to_add"),
                    "Absent": 0,
                    "Status": "A",
                    "AttendedStatus": "A",
                    "Type": "O",
                    "UnitType": "M",
                    "Note": "",
                    "StudentCourseId": self.test_data.get("student_course_id"),
                    "StudentEnrollmentPeriodId": self.test_data.get("student_enrollment_id"),
                    "EntityState": 0,
                },
            }
        }
        self.assertEqual(
            asyncio.run(
                self.anthology.add_attendance(
                    **{
                        "student_id": self.test_data.get("student_id"),
                        "class_section_id": self.test_data.get("class_section_id"),
                        "start_date": self.test_data.get("start_date"),
                        "end_date": self.test_data.get("end_date"),
                        "student_course_id": self.test_data.get("student_course_id"),
                        "student_enrollment_id": self.test_data.get("student_enrollment_id"),
                        "minutes_to_add": self.test_data.get("minutes_to_add"),
                    }
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
