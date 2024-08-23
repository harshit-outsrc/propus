from datetime import datetime, timedelta
import unittest
from unittest.mock import MagicMock, Mock, patch


from propus.helpers.sql_calbright.enrollment import (
    fetch_program_version_by_course_versions,
    fetch_matching_enrollment,
    MissingEnrollment,
    fetch_course_version,
    MissingCourseVersion,
    NoMatchingProgramVersion,
    upsert_enrollment,
    MultipleInProgressEnrollments,
    NoMatchingFirstTerm,
    get_instructor_loads,
    get_instructors_to_assign,
    assign_enrollment_course_term_sections,
)
from propus.calbright_sql.course import Course
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.course_version_section import CourseVersionSection
from propus.calbright_sql.enrollment_course_term import EnrollmentCourseTerm
from propus.calbright_sql.program_version_course import ProgramVersionCourse
from propus.calbright_sql.student import Student
from propus.calbright_sql.user import User
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.enrollment_status import EnrollmentStatus
from propus.calbright_sql.program_version import ProgramVersion
from propus.calbright_sql.term import Term


class TestEnrollmentHelper(unittest.TestCase):
    def setUp(self):
        self.program_id = "MATCHING_PROGRAM_ID"
        self.term_start_date = datetime.now() + timedelta(days=5)
        self.matching_enrollment = Enrollment(
            program_version=ProgramVersion(program_id=self.program_id),
            enrollment_date=datetime.now(),
            withdrawn_date=datetime.now() + timedelta(days=30),
        )
        self.user = User(
            student=Student(
                enrollment_student=[
                    Enrollment(program_version=ProgramVersion(program_id="wrong_id")),
                    Enrollment(
                        salesforce_course_version="1",
                        program_version=ProgramVersion(program_id=self.program_id),
                        enrollment_date=self.term_start_date + timedelta(days=2),
                    ),
                    Enrollment(
                        salesforce_course_version="2",
                        program_version=ProgramVersion(program_id=self.program_id),
                        enrollment_date=datetime.now(),
                        drop_date=self.term_start_date - timedelta(days=8),
                    ),
                    Enrollment(
                        salesforce_course_version="3",
                        program_version=ProgramVersion(program_id=self.program_id),
                        enrollment_date=datetime.now(),
                        withdrawn_date=self.term_start_date - timedelta(days=8),
                    ),
                    Enrollment(
                        salesforce_course_version="4",
                        program_version=ProgramVersion(program_id=self.program_id),
                        enrollment_date=datetime.now(),
                        completion_date=self.term_start_date - timedelta(days=8),
                    ),
                ]
            )
        )
        self.fpv_query_count = 1
        self.fpv_query_resp = "EXPECTED_PROGRAM_VERSION_ID"
        self.update_performed = False
        self.first_term_query_response = None
        self.enrollment_data = {
            "enrollment_date": "2024-04-22",
            "enrollment_status": EnrollmentStatus(id="Enrollment_status_123"),
            "enrollment_salesforce_id": "SF_ENROLLMENT_ID_XYZ",
        }
        self.session_mock = MagicMock()
        self.session_mock.add = Mock(side_effect=self.add_new_enrollment)
        self.session_mock.execute = Mock(side_effect=self.first_term_query)

    def fpv_query(self, _):
        all_mock = MagicMock()
        return_mock = MagicMock()
        return_mock.unique.return_value = all_mock
        if self.fpv_query_count == 1:
            self.fpv_query_count += 1
            all_mock.all.return_value = []
            return return_mock

        all_mock.all.return_value = [ProgramVersionCourse(program_version_id=self.fpv_query_resp)]
        return return_mock

    def test_fetch_program_version_by_course_versions(self):
        session_mock = MagicMock()
        session_mock.scalars = Mock(side_effect=self.fpv_query)

        with self.assertRaises(NoMatchingProgramVersion):
            fetch_program_version_by_course_versions(session_mock, "Data Analysis", "BUS500 - v2.0, BUS501 - v2.0")

        resp = fetch_program_version_by_course_versions(session_mock, "Data Analysis", "BUS500 - v2.0, BUS501 - v2.0")
        self.assertEqual(resp.program_version_id, self.fpv_query_resp)

    def test_fetch_course_version(self):
        cv_id = "COURSE_VERSION_1234"
        c_id = "COURSE_768439"
        cv = "IT520 - v2.0, IT525 - v3.0"
        first_mock = MagicMock()
        first_mock.first.return_value = None
        self.session_mock.scalars.return_value = first_mock

        with self.assertRaises(MissingCourseVersion):
            fetch_course_version(session=self.session_mock, sf_course_versions=cv, course=Course(course_code="IT525"))

        first_mock = MagicMock()
        first_mock.first.return_value = CourseVersion(id=cv_id, course_id=c_id, version_id=3.0)
        self.session_mock.scalars.return_value = first_mock

        course_version_id = fetch_course_version(
            session=self.session_mock, sf_course_versions=cv, course=Course(course_code="IT525")
        )
        self.assertEqual(course_version_id, cv_id)

    def test_fetch_matching_enrollment(self):
        with self.assertRaises(MissingEnrollment):
            fetch_matching_enrollment(User(student=Student(enrollment_student=[])), None, None, None)

        with self.assertRaises(MissingEnrollment):
            fetch_matching_enrollment(
                user=self.user,
                term_start_date=self.term_start_date,
                grade_id="N/A",
                course_versions=[
                    CourseVersion(
                        course_program_version=[
                            ProgramVersionCourse(program_version=ProgramVersion(program_id=self.program_id))
                        ]
                    )
                ],
            )

        self.user.student.enrollment_student.append(self.matching_enrollment)
        enrollment = fetch_matching_enrollment(
            user=self.user,
            term_start_date=self.term_start_date,
            grade_id="N/A",
            course_versions=[
                CourseVersion(
                    course_program_version=[
                        ProgramVersionCourse(program_version=ProgramVersion(program_id=self.program_id))
                    ]
                )
            ],
        )
        self.assertEqual(enrollment, self.matching_enrollment)

    @patch("propus.helpers.sql_calbright.enrollment.update_or_create")
    def test_upsert_enrollment_update(self, update_or_create):
        enrollment_id = "ENROLLMENT_ID_1234"
        upsert_enrollment(
            self.session_mock,
            user=User(
                ccc_id="TEST_CCC_ID",
                student=Student(
                    enrollment_student=[
                        Enrollment(
                            enrollment_salesforce_id=self.enrollment_data.get("enrollment_salesforce_id"),
                            program_version_id="PROG_VERSION",
                            enrollment_status=EnrollmentStatus(status="Started"),
                            id=enrollment_id,
                        )
                    ],
                ),
            ),
            enrollment_data=self.enrollment_data,
        )
        update_or_create.assert_called_once_with(self.session_mock, Enrollment, self.enrollment_data, id=enrollment_id)

    def test_upsert_enrollment_create_new(self):
        with self.assertRaises(MultipleInProgressEnrollments):
            upsert_enrollment(
                self.session_mock,
                user=User(
                    ccc_id="TEST_CCC_ID",
                    student=Student(
                        enrollment_student=[
                            Enrollment(
                                program_version_id="PROG_VERSION", enrollment_status=EnrollmentStatus(status="Started")
                            )
                        ],
                    ),
                ),
                enrollment_data={},
            )

        first_mock = MagicMock()
        first_mock.first.return_value = None
        self.session_mock.scalars.return_value = first_mock

        self.first_term_query_response = None
        with self.assertRaises(NoMatchingFirstTerm):
            upsert_enrollment(
                self.session_mock,
                user=User(ccc_id="TEST_CCC_ID", student=Student(enrollment_student=[])),
                enrollment_data=self.enrollment_data,
            )

        first_mock = MagicMock()
        self.first_term_query_response = Term(id="Term_ID_123")
        first_mock.first.return_value = self.first_term_query_response
        self.session_mock.scalars.return_value = first_mock
        first_mock.first.return_value = self.first_term_query_response

        upsert_enrollment(
            self.session_mock,
            user=User(ccc_id="TEST_CCC_ID", student=Student(enrollment_student=[])),
            enrollment_data=self.enrollment_data,
        )
        self.assertTrue(self.update_performed)

    def add_new_enrollment(self, enrollment):
        self.assertTrue(isinstance(enrollment, Enrollment))
        self.assertEqual(enrollment.enrollment_date, self.enrollment_data.get("enrollment_date"))
        self.assertEqual(enrollment.enrollment_status_id, self.enrollment_data.get("enrollment_status").id)
        self.assertEqual(enrollment.first_term.id, self.first_term_query_response.id)
        self.update_performed = True

    def first_term_query(self, _):
        response_mock = MagicMock()
        response_mock.first.return_value = self.first_term_query_response
        return response_mock

    @patch("propus.calbright_sql.course_version_section.CourseVersionSection", autospec=True)
    @patch("propus.calbright_sql.enrollment_course_term.EnrollmentCourseTerm", autospec=True)
    @patch("propus.calbright_sql.enrollment.Enrollment", autospec=True)
    @patch("propus.calbright_sql.enrollment_status.EnrollmentStatus", autospec=True)
    def test_get_instructor_loads(
        self, MockEnrollmentStatus, MockEnrollment, MockEnrollmentCourseTerm, MockCourseVersionSection
    ):
        mock_session = MagicMock()
        mock_query = mock_session.query.return_value
        mock_query.outerjoin.return_value = mock_query
        mock_query.group_by.return_value = mock_query

        mock_result = [MagicMock(instructor_id=1, enrollment_count=5), MagicMock(instructor_id=2, enrollment_count=3)]
        mock_query.all.return_value = mock_result

        result = get_instructor_loads(mock_session)

        expected_result = {1: 5, 2: 3}

        self.assertEqual(result, expected_result)
        mock_query.outerjoin.assert_called()
        mock_query.group_by.assert_called_once_with(CourseVersionSection.instructor_id)
        mock_query.all.assert_called_once()

    @patch("propus.helpers.sql_calbright.enrollment.get_instructor_loads", autospec=True)
    @patch("propus.calbright_sql.program_version_course.ProgramVersionCourse", autospec=True)
    @patch("propus.calbright_sql.course_version_section.CourseVersionSection", autospec=True)
    @patch("propus.calbright_sql.course_version.CourseVersion", autospec=True)
    @patch("propus.calbright_sql.enrollment.LMS", autospec=True)
    def test_get_instructors_to_assign(
        self, MockLMS, MockCourseVersion, MockCourseVersionSection, MockProgramVersionCourse, mock_get_instructor_loads
    ):
        mock_session = MagicMock()

        mock_get_instructor_loads.return_value = {1: 5, 2: 3}

        mock_program_version_course = MagicMock()
        mock_program_version_course.course_version.course.course_instructor = [MagicMock(instructor=MagicMock(id=2))]
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [
            mock_program_version_course
        ]

        mock_course_version_section = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_course_version_section

        result = get_instructors_to_assign(mock_session)

        expected_result = {mock_program_version_course.id: mock_course_version_section}

        self.assertEqual(result, expected_result)

    @patch("propus.helpers.sql_calbright.enrollment.get_instructors_to_assign", autospec=True)
    def test_assign_enrollment_course_term_sections(self, mock_get_instructors_to_assign):
        mock_session = MagicMock()

        mock_section = MagicMock()
        mock_get_instructors_to_assign.return_value = {1: mock_section}

        mock_enrollment_course_term = MagicMock(spec=EnrollmentCourseTerm)
        mock_enrollment_course_term.course_version_id = 1
        mock_enrollment_course_term.course_version_section = None  # Ensure it starts as None
        mock_enrollment_course_term.enrollment.program_version.program_course_version = [
            MagicMock(course_version_id=1, id=1)
        ]

        result = assign_enrollment_course_term_sections(mock_session, [mock_enrollment_course_term])

        self.assertTrue(result)
        self.assertIs(mock_enrollment_course_term.course_version_section, mock_section)
        mock_session.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
