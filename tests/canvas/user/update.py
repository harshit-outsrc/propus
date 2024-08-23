import asyncio
import unittest
from tests.api_client import TestAPIClient
from propus.canvas import Canvas


class TestCanvasUserUpdate(TestAPIClient):
    def setUp(self) -> None:
        super().setUp()
        auth_providers = {"okta": 105, "google": 105}
        self.canvas = Canvas(
            application_key=self.application_key,
            base_url=self.url,
            additional_headers=None,
            auth_providers=auth_providers,
        )
        self.canvas.request_service = self._req_mock
        self.test_data = {
            "user_id": 1234,
            "first_name": "Johnny",
            "last_name": "Trombono",
            "time_zone": "America/New_York",
            "email": "j.trombono@trombonesuperstore.net",
            "bio": "I am a trombone enthusiast and I love to play jazz music.",
            "pronouns": "they/them",
        }
        self.test_urls = {
            "update_user": f"{self.url}/api/v1/users/{self.test_data['user_id']}",
        }

    def test_update_user(self):
        self.test_name = "update_user"
        self.assertEqual(
            asyncio.run(
                self.canvas.update_user(
                    user_id=self.test_data.get("user_id"),
                    first_name=self.test_data.get("first_name"),
                    last_name=self.test_data.get("last_name"),
                    time_zone=self.test_data.get("time_zone"),
                    email_address=self.test_data.get("email"),
                )
            ),
            self.success_response,
        )


if __name__ == "__main__":
    unittest.main()
