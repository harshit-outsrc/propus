import unittest
from unittest.mock import patch

from propus.helpers.sql_calbright.term_grades import upsert_eotg_records
from propus.calbright_sql.user import User
from propus.calbright_sql.course import Course
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.enrollment_course_term import EnrollmentCourseTerm


class TestUpsertEotgRecords(unittest.TestCase):

    def setUp(self):
        self.mock_data = {
            "session": "MOCK_SESSION",
            "user": User(id="USER_ID"),
            "grade_status": "GRADE_STATUS",
            "term_id": "TERM_ID",
            "term_start_date": "2024-02-02",
            "sf_grade_id": "GRADE_ID",
            "course": Course(id="COURSE_ID"),
            "instructor_id": "INSTRUCTOR_1234",
            "grade_id": "GRADE_ID_6780",
            "grade_date": "SOME_DATE",
            "drop_date": "ANOTHER_DROP_DATE",
            "withdrawn_date": "WITH_DRAWN_DATE",
            "modified_at": "MODIFIED AT",
            "created_at": "CREATED_AT_Date",
            "certified_by_id": "CERTIFIER",
            "certified_date": "CERTIFIED_DATE",
        }

    @patch("propus.helpers.sql_calbright.term_grades.update_or_create")
    @patch("propus.helpers.sql_calbright.term_grades.fetch_matching_enrollment")
    @patch("propus.helpers.sql_calbright.term_grades.fetch_course_version")
    def test_inserts_new_record(
        self, mock_fetch_course_version, mock_fetch_matching_enrollments, mock_update_or_create
    ):
        scv = "SALESFORCE_COURSE_VERSION"
        enrollment_id = "ENROLLMENT_ID"
        course_version_id = "COURSE_VERSION_1234"

        mock_fetch_matching_enrollments.return_value = Enrollment(id=enrollment_id, salesforce_course_version=scv)
        mock_update_or_create.return_value = ["obj", "created"]

        mock_fetch_course_version.return_value = course_version_id

        course_version = CourseVersion(id="COURSE_12345")
        this_course = Course(course_version_course=[course_version])

        self.mock_data["course"] = this_course
        upsert_eotg_records(**self.mock_data)

        expected_data = {
            "grade_salesforce_id": self.mock_data.get("sf_grade_id"),
            "term_id": self.mock_data.get("term_id"),
            "grade_status": self.mock_data.get("grade_status"),
            "enrollment_id": enrollment_id,
            "course_version_id": course_version_id,
            "instructor_id": self.mock_data.get("instructor_id"),
            "grade_id": self.mock_data.get("grade_id"),
            "grade_date": self.mock_data.get("grade_date"),
            "drop_date": self.mock_data.get("drop_date"),
            "withdraw_date": self.mock_data.get("withdrawn_date"),
            "modified_at": self.mock_data.get("modified_at"),
            "created_at": self.mock_data.get("created_at"),
            "certified_by_id": self.mock_data.get("certified_by_id"),
            "certified_date": self.mock_data.get("certified_date"),
        }

        mock_fetch_matching_enrollments.assert_called_once_with(
            user=self.mock_data.get("user"),
            term_start_date=self.mock_data.get("term_start_date"),
            grade_id=self.mock_data.get("sf_grade_id"),
            course_versions=[course_version],
        )
        mock_fetch_course_version.assert_called_once_with(self.mock_data.get("session"), this_course, scv)
        mock_update_or_create.assert_called_once_with(
            self.mock_data.get("session"),
            EnrollmentCourseTerm,
            expected_data,
            enrollment_id=enrollment_id,
            course_version_id=course_version_id,
            term_id=self.mock_data.get("term_id"),
        )


if __name__ == "__main__":
    unittest.main()
