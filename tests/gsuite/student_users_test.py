import unittest
import re

from unittest.mock import MagicMock, Mock, patch

from propus.aws.ssm import AWS_SSM
from propus.gsuite.student_users import fetch_student_photo, fetch_student_photo_url


class TestStudentUsersHelpers(unittest.TestCase):
    def setUp(self):
        # Mocking SSM build and get_param
        self.mock_ssm_build = MagicMock()
        self.mock_ssm_get_param = Mock(return_value={"param_key": "param_value"})
        self.mock_ssm_build.get_param = self.mock_ssm_get_param

        # Mocking S3 build
        self.mock_s3 = MagicMock()
        self.mock_s3_build = Mock(return_value=self.mock_s3)
        self.mock_s3.write_to_s3 = Mock(return_value={})
        self.mock_s3_client = MagicMock()
        self.mock_s3.s3_client = self.mock_s3_client
        self.mock_s3_meta = MagicMock()
        self.mock_s3_client.meta = self.mock_s3_meta
        self.mock_s3_meta.region_name = "us-w"

    @patch("propus.gsuite.student_users.UserDirectory.build")
    def test_fetch_student_photo_success(self, mock_user_directory_build):
        # Mocking UserDirectory fetch_profile_picture
        mock_user_directory = MagicMock()
        mock_user_directory.fetch_profile_picture.return_value = {"mock_key": "mock_value"}
        mock_user_directory_build.return_value = mock_user_directory
        AWS_SSM.build = Mock(return_value=self.mock_ssm_build)

        # Call the fetch_student_photo method
        result = fetch_student_photo("mock_user_id")

        # Assertions
        self.assertEqual(result, {"mock_key": "mock_value"})
        self.mock_ssm_get_param.assert_called_once_with("gsuite.calbright-student.users", param_type="json")
        mock_user_directory_build.assert_called_once_with({"param_key": "param_value"})
        mock_user_directory.fetch_profile_picture.assert_called_once_with("mock_user_id")

    @patch("propus.gsuite.student_users.UserDirectory.build")
    @patch("propus.gsuite.student_users.AWS_S3.build")
    def test_fetch_student_photo_url_success(self, mock_user_directory_build, mock_s3_build):
        # Mocking S3 s3_file_exists
        self.mock_s3.s3_file_exists.side_effect = [False, False]  # Simulate files not existing initially
        mock_s3_build.return_value = self.mock_s3

        # Mocking fetch_student_photo
        mock_fetch_student_photo = Mock(return_value={"photoData": "BASE64_ENCODED_DATA", "mimeType": "image/jpeg"})
        with patch("propus.gsuite.student_users.fetch_student_photo", mock_fetch_student_photo):
            # Call the fetch_student_photo_url method
            result = fetch_student_photo_url("mock_user_email", "mock_ccc_id")

        pattern = r"^https://s3\..*\.amazonaws\.com/static\.calbrightcollege\.org/assets/students/thumbnails/mock_ccc_id\.png$"
        # Assertions
        self.assertTrue(re.match(pattern, result))

    @patch("propus.gsuite.student_users.UserDirectory.build")
    def test_fetch_student_photo_url_default_avatar(self, mock_user_directory_build):
        # Mocking S3 s3_file_exists, simulating file not existing
        self.mock_s3.s3_file_exists.return_value = False

        # Mocking fetch_student_photo to raise an exception
        with patch("propus.gsuite.student_users.fetch_student_photo", side_effect=Exception("Mocked error")):
            result = fetch_student_photo_url("mock_user_email", "mock_ccc_id")

        # Assertions
        self.assertEqual(result, AWS_SSM.build().get_param("student.default_user_avatar"))


if __name__ == "__main__":
    unittest.main()
