import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.sql import func
from propus.calbright_sql.course import Course
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.course_version_section import CourseVersionSection
from propus.calbright_sql.program_version_course import ProgramVersionCourse
from propus.calbright_sql.enrollment import LMS
from propus.helpers.sql_calbright.course_version_sections import create_course_version_section_records


class TestCourseVersionSectionsHelper(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()

    @patch("propus.calbright_sql.course.Course", autospec=True)
    @patch("propus.calbright_sql.course_version.CourseVersion", autospec=True)
    @patch("propus.calbright_sql.course_version_section.CourseVersionSection", autospec=True)
    @patch("propus.calbright_sql.program_version_course.ProgramVersionCourse", autospec=True)
    def test_create_course_version_section_records(
        self, MockProgramVersionCourse, MockCourseVersionSection, MockCourseVersion, MockCourse
    ):
        mock_max_section_result = MagicMock()
        mock_max_section_result.course_code = "BUS500"
        mock_max_section_result.max_section_id = 3
        self.session_mock.query.return_value.join.return_value.join.return_value.join.return_value.group_by.return_value.all.return_value = [
            mock_max_section_result
        ]

        mock_course_version = MagicMock()
        mock_course_version.lms = "canvas"
        mock_program_version_course = MagicMock()
        mock_course_version.course_program_version = [mock_program_version_course]
        mock_program_version_course.course_version.course.course_code = "BUS500"
        mock_course_instructor = MagicMock()
        mock_course_instructor.instructor.id = 1
        mock_course_version.course.course_instructor = [mock_course_instructor]
        self.session_mock.query.return_value.filter.return_value.all.return_value = [mock_course_version]

        self.session_mock.query.return_value.join.return_value.filter.return_value.first.return_value = None

        result = create_course_version_section_records(self.session_mock)

        self.assertTrue(result)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()
        added_section = self.session_mock.add.call_args[0][0]
        self.assertEqual(added_section.section_id, 4)
        self.assertEqual(added_section.section_name, "BUS500-4")
        self.assertEqual(added_section.lms, LMS("Canvas"))


if __name__ == "__main__":
    unittest.main()
