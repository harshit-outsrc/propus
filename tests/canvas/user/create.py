import asyncio
import unittest
from tests.api_client import TestAPIClient
from propus.canvas import Canvas
from propus.helpers.exceptions import InvalidEmail
from propus.canvas.user._exceptions import UserIdTaken


class TestCanvasUserCreate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(application_key=self.application_key, base_url=self.url, auth_providers=auth_providers)
        self.canvas.request_service = self._req_mock
        self.test_data = {
            "first_name": "Tony",
            "last_name": "Pizza",
            "email_address": "tonypizza@tonypizzaspizzablog.biz",
            "sis_user_id": "pizzaman",
            "integration_id": "tpizza",
            "timezone": "America/Los_Angeles",
            "locale": "sp",
            "destination": "https://tonypizzaspizzablog.biz/welcome",
            "initial_enrollment_type": "observer",
            "pairing_code": "p1234",
            "terms_of_use": True,
            "send_confirmation": True,
            "skip_registration": False,
            "force_self_registration": False,
            "confirmation_url": True,
            "skip_confirmation": False,
            "force_validations": False,
            "enable_sis_reactivation": False,
            "bad_email": "tonypizzaman.hero",
        }
        self.test_urls = {
            "create_user": (f"{self.url}/api/v1/accounts/1/users"),
            "create_user_expanded": (f"{self.url}/api/v1/accounts/1/users"),
            "create_user_bad_email": (f"{self.url}/api/v1/accounts/1/users"),
            "create_user_id_taken": (f"{self.url}/api/v1/accounts/1/users"),
        }

    def test_minimum_create_user(self):
        self.test_name = "create_user"
        self.assertEqual(
            asyncio.run(
                self.canvas.create_user(
                    user_type="student",
                    first_name=self.test_data["first_name"],
                    last_name=self.test_data["last_name"],
                    email_address=self.test_data["email_address"],
                    sis_user_id=self.test_data["sis_user_id"],
                )
            ),
            self.success_response,
        )

    def test_expanded_create_user(self):
        self.test_name = "create_user_expanded"
        self.assertEqual(
            asyncio.run(
                self.canvas.create_user(
                    user_type="staff",
                    first_name=self.test_data["first_name"],
                    last_name=self.test_data["last_name"],
                    email_address=self.test_data["email_address"],
                    sis_user_id=self.test_data["sis_user_id"],
                    integration_id=self.test_data["integration_id"],
                    timezone=self.test_data["timezone"],
                    locale=self.test_data["locale"],
                    destination=self.test_data["destination"],
                    initial_enrollment_type=self.test_data["initial_enrollment_type"],
                    pairing_code=self.test_data["pairing_code"],
                    terms_of_use=self.test_data["terms_of_use"],
                    send_confirmation=self.test_data["send_confirmation"],
                    skip_registration=self.test_data["skip_registration"],
                    force_self_registration=self.test_data["force_self_registration"],
                    confirmation_url=self.test_data["confirmation_url"],
                    skip_confirmation=self.test_data["skip_confirmation"],
                    force_validations=self.test_data["force_validations"],
                    enable_sis_reactivation=self.test_data["enable_sis_reactivation"],
                )
            ),
            self.success_response,
        )

    def test_bad_email(self):
        self.test_name = "create_user_bad_email"
        with self.assertRaises(InvalidEmail) as context:
            asyncio.run(
                self.canvas.create_user(
                    user_type="staff",
                    first_name=self.test_data["first_name"],
                    last_name=self.test_data["last_name"],
                    email_address=self.test_data["bad_email"],
                    sis_user_id=self.test_data["sis_user_id"],
                )
            )
        self.assertEqual(
            str(context.exception),
            f'email "{self.test_data["bad_email"]}" is an invalid email',
        )

    #
    def test_user_id_taken(self):
        self.test_name = "create_user_id_taken"
        with self.assertRaises(UserIdTaken) as context:
            raise UserIdTaken(self.test_data["sis_user_id"], "staff")
        self.assertEqual(
            str(context.exception),
            f"SIS ID '{self.test_data['sis_user_id']}' for user type 'staff' is already in use.",
        )


if __name__ == "__main__":
    unittest.main()
