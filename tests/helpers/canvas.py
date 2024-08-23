import unittest
from unittest.mock import AsyncMock, patch
from mock_alchemy.mocking import AlchemyMagicMock

from propus.calbright_sql.enrollment import LMS, Enrollment
from propus.calbright_sql.user_lms import UserLms

from propus.helpers.canvas import (
    create_canvas_user,
    create_course_sections,
    get_canvas_id_from_user_lms_list,
    get_student_enrollment,
    create_initial_course_enrollment,
    create_subsequent_course_enrollment,
    enroll_instructors_in_sections,
    conclude_student_enrollments,
)
from propus.calbright_sql.user import User


class TestCanvasHelpers(unittest.TestCase):
    def setUp(self) -> None:
        self.test_user_data = {
            "first_name": "Tony",
            "last_name": "Pizza",
            "email_address": "tony.pizza@calbright.org",
            "ccc_id": "a1",
        }
        self.test_user_object = User(
            first_name=self.test_user_data["first_name"],
            last_name=self.test_user_data["last_name"],
            calbright_email=self.test_user_data["email_address"],
            ccc_id=self.test_user_data["ccc_id"],
        )
        self.canvas_user_data = {"canvas_id": 1234, "ccc_id": 5678}
        self.test_user_lms_list = [
            UserLms(
                user_id=self.canvas_user_data["ccc_id"],
                lms_id=self.canvas_user_data["canvas_id"],
                lms=LMS("Canvas"),
            ),
            UserLms(user_id=self.canvas_user_data["canvas_id"], lms_id=910, lms=LMS("Strut")),
        ]
        self.test_enrollment = Enrollment(
            ccc_id=self.canvas_user_data["ccc_id"],
        )
        self.session = AlchemyMagicMock()
        self.canvas = AsyncMock()
        self.canvas.create_user = AsyncMock()

    # TODO: Revisit these tests to ensure they are testing the correct things

    def test_create_canvas_user(self):
        self.test_name = "create_canvas_user"
        self.canvas.create_user.return_value = {"id": 1234}
        user_id = create_canvas_user(
            user_type="student",
            first_name=self.test_user_data["first_name"],
            last_name=self.test_user_data["last_name"],
            email_address=self.test_user_data["email_address"],
            sis_user_id=self.test_user_data["ccc_id"],
            session=self.session,
            canvas=self.canvas,
        )

        self.assertEqual(user_id["canvas_id"], self.canvas_user_data["canvas_id"])

    def test_create_canvas_user_with_user_object(self):
        self.test_name = "create_canvas_user_with_user_object"
        self.canvas.create_user.return_value = {"id": 1234}
        user_id = create_canvas_user(
            user_type="student",
            first_name=self.test_user_data["first_name"],
            last_name=self.test_user_data["last_name"],
            email_address=self.test_user_data["email_address"],
            sis_user_id=self.test_user_data["ccc_id"],
            session=self.session,
            canvas=self.canvas,
            user_object=self.test_user_object,
        )
        self.assertEqual(user_id["canvas_id"], self.canvas_user_data["canvas_id"])

    def test_create_course_sections(self):
        self.test_name = "create_course_sections"
        sections_created = create_course_sections(
            session=self.session,
            canvas=self.canvas,
        )
        self.assertFalse(sections_created)

    def test_get_canvas_id_from_user_lms_list(self):
        self.test_name = "get_canvas_id_from_user_lms_list"
        canvas_id = get_canvas_id_from_user_lms_list(self.test_user_lms_list)
        self.assertEqual(canvas_id, self.canvas_user_data["canvas_id"])

    def test_get_student_enrollment(self):
        self.test_name = "get_student_enrollment"
        enrollment = get_student_enrollment(
            ccc_id=self.test_user_data["ccc_id"],
            session=self.session,
        )
        self.assertTrue(enrollment)

    def test_create_initial_course_enrollment(self):
        self.test_name = "create_initial_course_enrollment"
        initial_enrollment = create_initial_course_enrollment(
            ccc_id=self.test_user_data["ccc_id"],
            session=self.session,
            canvas=self.canvas,
            orientation_course_section_id=23,
        )
        self.assertFalse(initial_enrollment)

    def test_create_subsequent_course_enrollment(self):
        self.test_name = "create_subsequent_course_enrollment"
        subsequent_enrollment = create_subsequent_course_enrollment(
            current_course_id=23,
            ccc_id=self.test_user_data["ccc_id"],
            canvas_user_id=self.canvas_user_data["canvas_id"],
            session=self.session,
            canvas=self.canvas,
        )
        self.assertFalse(subsequent_enrollment)

    def test_enroll_instructors_in_sections(self):
        self.test_name = "enroll_instructors_in_sections"
        enrolled_instructors = enroll_instructors_in_sections(
            session=self.session,
            canvas=self.canvas,
        )
        self.assertFalse(enrolled_instructors)

    @patch("propus.helpers.canvas.get_canvas_id_from_user_lms_list", return_value=1234)
    def test_conclude_student_enrollments(self, mock_get_canvas_id_from_user_lms_list):
        self.test_name = "conclude_student_enrollments"
        concluded_enrollments = conclude_student_enrollments(
            ccc_id=self.test_user_data["ccc_id"],
            session=self.session,
            canvas=self.canvas,
        )
        self.assertTrue(concluded_enrollments)


if __name__ == "__main__":
    unittest.main()
