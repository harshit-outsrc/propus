import asyncio
import unittest

from propus.anthology import Anthology
from tests.api_client import TestAPIClient


class TestAnthologyCourseRead(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        self.anthology = Anthology(application_key=self.application_key, base_url=self.url)
        self.anthology.request_service = self._req_mock
        self.test_urls = {
            "fetch_course_for_enrollment": f"{self.url}/api/course-registration/students/anth_1234_ABC/student-enrollment-periods/84658/student-courses",
            "course_by_id": f"{self.url}/api/commands/Academics/StudentCourse/get",
            "fetch_class_terms": f"{self.url}/ds/campusnexus/Terms/CampusNexus.GetStudentCourseRegistrationTermListCustom(campusId=5,courseIds='1234,8NBHJ')?$select=TermName,TermCode,Id,TermStartDate,TermEndDate,CodeAndName&%24format=json&%24count=true&%24orderby=TermCode",
            "fetch_classes_for_courses": f"{self.url}/ds/campusnexus/ClassSections/CampusNexus.GetStudentCourseRegistrationClassScheduleList(campusId=5,termId=2023-24-TERM-12,courseIds='1234,8NBHJ',isCrossReferenceCourse=false,studentId=anth_1234_ABC,crossRefCourseId=0, isTransferSection = false)?$select=Id,CourseCode,CourseName,SectionCode,SectionName,CourseId,CampusId,StartDate,EndDate,IsActive,DeliveryMethodName,InstructorName&$orderby=CourseName,SectionCode",
            "fetch_all_courses": f"{self.url}/ds/odata/Courses",
            "fetch_course_by_cccid": f"{self.url}/ds/odata/StudentCourses",
        }
        self.test_data = {
            "student_id": "anth_1234_ABC",
            "enrollment_id": 84658,
            "course_id": "MN_123_Z",
            "course_ids": ["1234", "8NBHJ"],
            "term_id": "2023-24-TERM-12",
        }
        self.api_client.timeout = 30

    def test_fetch_all_courses(self):
        self.test_name = "fetch_all_courses"
        self.assertEqual(asyncio.run(self.anthology.fetch_all_courses()), self.success_response)

    def test_fetch_classes_for_courses(self):
        self.test_name = "fetch_classes_for_courses"
        self.assertEqual(
            asyncio.run(
                self.anthology.fetch_classes_for_courses(
                    self.test_data.get("student_id"),
                    self.test_data.get("term_id"),
                    self.test_data.get("course_ids"),
                )
            ),
            self.success_response,
        )

    def test_fetch_course_for_enrollments(self):
        self.test_name = "fetch_course_for_enrollment"
        self.assertEqual(
            asyncio.run(
                self.anthology.fetch_course_for_enrollment(
                    self.test_data.get("student_id"),
                    self.test_data.get("enrollment_id"),
                )
            ),
            self.success_response,
        )

    def test_course_by_id(self):
        self.test_name = "course_by_id"
        self._test_data = {"payload": {"id": "MN_123_Z"}}
        self.assertEqual(
            asyncio.run(self.anthology.fetch_course(self.test_data.get("course_id"))), self.success_response
        )

    def test_fetch_terms_for_courses(self):
        self.test_name = "fetch_class_terms"
        self.assertEqual(
            asyncio.run(self.anthology.fetch_term_for_courses(course_ids=self.test_data.get("course_ids"))),
            self.success_response,
        )

    def test_fetch_course_by_cccid(self):
        self.test_name = "fetch_course_by_cccid"
        self.assertEqual(
            asyncio.run(
                self.anthology.fetch_course_by_cccid(
                    ccc_id=self.test_data.get("student_id"), enrollment_id=self.test_data.get("enrollment_id")
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
