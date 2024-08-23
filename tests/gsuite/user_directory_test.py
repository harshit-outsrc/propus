import unittest
import googleapiclient.discovery

from google.oauth2 import service_account
from unittest.mock import MagicMock, Mock

from propus.gsuite.user_directory import UserDirectory
from propus.logging_utility import Logging

from propus.gsuite.exceptions import (
    UserUpdateMissingFields,
    UserCreateRequestsReached,
    UserAttemptingToCreateExists,
)


class TestUserDirectory(unittest.TestCase):
    def setUp(self):
        # Mock the necessary components
        self.mock_client = MagicMock()
        self.mock_logger = Mock()
        Logging.get_logger = Mock(return_value=self.mock_logger)

        # Create an instance of UserDirectory for testing
        self.user_directory = UserDirectory(self.mock_client)
        self.mock_response = {"mock_key": "mock_value"}

    def test_build(self):
        # Mock the necessary components
        mock_credentials = MagicMock()
        mock_credentials.with_subject = Mock(return_value=mock_credentials)
        mock_credentials.with_scopes = Mock(return_value=mock_credentials)
        service_account.Credentials.from_service_account_info = Mock(return_value=mock_credentials)

        # Mock the return value of googleapiclient.discovery.build
        googleapiclient.discovery.build = Mock(return_value=MagicMock())

        # Call the build method
        user_directory = UserDirectory.build({"service_account": "mocked"})

        # Assertions
        self.assertIsInstance(user_directory, UserDirectory)
        service_account.Credentials.from_service_account_info.assert_called_once_with({"service_account": "mocked"})
        mock_credentials.with_subject.assert_called_once_with("svc-engineering@calbrightcollege.org")
        mock_credentials.with_scopes.assert_called_once_with(
            ["https://www.googleapis.com/auth/admin.directory.user.readonly"]
        )
        googleapiclient.discovery.build.assert_called_once_with("admin", "directory_v1", credentials=mock_credentials)

    def test_fetch_profile_picture_success(self):
        # Mock the response from the API
        self.mock_client.users().photos().get().execute.return_value = self.mock_response

        # Call the fetch_profile_picture method
        result = self.user_directory.fetch_profile_picture("mock_user_key")

        # Assertions
        self.assertEqual(result, self.mock_response)
        self.mock_logger.error.assert_not_called()

    def test_fetch_profile_picture_error(self):
        # Mock an exception when calling the API
        self.mock_client.users().photos().get().execute.side_effect = Exception("Mocked error")

        # Call the fetch_profile_picture method
        with self.assertRaises(Exception) as context:
            self.user_directory.fetch_profile_picture("mock_user_key")

        # Assertions
        self.mock_logger.error.assert_called_once_with("Error fetching user photo: Mocked error")
        self.assertEqual(str(context.exception), "Mocked error")

    def test_fetch_user(self):
        # Mock the response from the API
        self.mock_client.users().get().execute.return_value = self.mock_response

        # Call the fetch_profile_picture method
        result = self.user_directory.fetch_user("mock_user_key")

        # Assertions
        self.assertEqual(result, self.mock_response)
        self.mock_logger.error.assert_not_called()

    def test_fetch_all_users(self):
        self.mock_client.users().list().execute.side_effect = [
            {"users": [{"email": "user1@example.com", "suspended": False}], "nextPageToken": "token1"},
            {"users": [{"email": "user2@example.com", "suspended": True}], "nextPageToken": None},
        ]
        result = self.user_directory.fetch_all_users()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["email"], "user1@example.com")
        self.assertEqual(result[0]["suspended"], False)
        self.assertEqual(result[1]["email"], "user2@example.com")
        self.assertEqual(result[1]["suspended"], True)

    def test_create_user(self):
        self.mock_client.users().get().execute.return_value = self.mock_response
        self.mock_client.users().insert().execute.return_value = self.mock_response

        with self.assertRaises(UserAttemptingToCreateExists):
            result = self.user_directory.create_user(
                "test@test.com",
                "MOCK123",
                "Mocker",
                "Mockington",
                "(555) 555-5555",
                calbright_email="testing@testcollege.org",
            )

        with self.assertRaises(UserCreateRequestsReached):
            result = self.user_directory.create_user(
                "test@test.com", "MOCK123", "Mocker", "Mockington", "(555) 555-5555"
            )

        self.mock_client.users().get().execute.side_effect = Exception("Test No User")
        result = self.user_directory.create_user("test@test.com", "MOCK123", "Mocker", "Mockington", "(555) 555-5555")
        self.assertEqual(result, self.mock_response)

    def test_update_user(self):
        user_test = {
            "agreed_to_terms": True,
            "suspended": False,
            "first_name": "Testing",
            "last_name": "Testerton",
            "personal_email": "test@test.com",
            "phone_number": "(555) 555-5555",
            "org_unit_path": "/Some OU",
        }

        mock_data = {
            "primaryEmail": "testing@testcollege.org",
            "password": "Super Secret Password",
            "agreedToTerms": False,
            "suspended": False,
            "changePasswordAtNextLogin": True,
            "name": {"familyName": "Some Last Name", "givenName": "Some First Name"},
            "emails": [
                {"address": "testing@testcollege.org", "primary": True},
                {"address": "test@test.com", "type": "home", "primary": False},
            ],
            "addresses": [{"region": "CA"}],
            "phones": [{"value": f"+11111111111", "type": "work"}],
            "includeInGlobalAddressList": False,
            "customSchemas": {"custom_attributes": {"role": "student", "cid": "MOCK123"}},
            "orgUnitPath": "/Original OU",
            "recoveryEmail": "test@test.com",
            "recoveryPhone": f"+11111111111",
        }

        self.mock_client.users().get().execute.return_value = mock_data
        self.mock_client.users().update().execute.return_value = self.mock_response
        result = self.user_directory._update_user("mock_user_key", **user_test)
        self.assertEqual(result, self.mock_response)

        with self.assertRaises(UserUpdateMissingFields):
            result = self.user_directory._update_user("mock_user_key", **{"Bad Data": "Bad Value"})

    def test_update_user_org_unit(self):
        # Mock the response from the API
        self.mock_client.users().get().execute.return_value = self.mock_response
        self.mock_client.users().update().execute.return_value = self.mock_response

        # Call the fetch_profile_picture method
        result = self.user_directory.update_user_org_unit("mock_user_key", "mock_org_unit")

        # Assertions
        self.assertEqual(result, self.mock_response)
        self.mock_logger.error.assert_not_called()

    def test_check_existing_email(self):
        self.mock_client.users().get().execute.return_value = self.mock_response
        result = self.user_directory.check_existing_email("mock_user_key")
        self.assertEqual(result, True)

        self.mock_client.users().get().execute.side_effect = Exception("Test No User")
        result = self.user_directory.check_existing_email("mock_user_key")
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
