from unittest.mock import MagicMock

from propus.slack import Slack
from tests.api_client import TestAPIClient


class TestSlack(TestAPIClient):
    def setUp(self) -> None:
        self.version = "v1"
        self.slack = Slack.build(bot_token=self.bot_token)
        self.slack.client = MagicMock()
        self.slack.request_service = self._req_mock()
        self.user_id = "userid"
        self.user_email = "email@email.com"
        self.channel_ids = ["channelid1", "channelid2"]
        self.group_id = "groupid"
        self.team_id = "teamid"
        self.username = "username"

    def test_succesfully_send_message(self):
        channel = "random channel"
        message = "random message"

        self.slack.send_message(channel, message)
        assert self.slack.client.chat_postMessage.assert_called_with("#" + channel, message)

    def test_create_user(self):
        self.slack.create_user(self.username, self.user_email)
        assert self.slack._make_request.assert_called_with(
            url=f"https://api.slack.com/scim/{self.version}/Users/",
            req_type="post",
            data={
                "schemas": [
                    "urn:scim:schemas:core:1.0",
                    "urn:scim:schemas:extension:enterprise:1.0",
                ],
                "userName": self.username,
                "emails": [{"value": self.user_email, "type": "work", "primary": True}],
            },
        )

    def test_delete_user(self):
        self.slack.delete_user(self.user_id)
        assert self.slack._make_request.assert_called_with(
            url=f"https://api.slack.com/scim/{self.version}/Users/{self.user_id}",
            req_type="delete",
        )

    def test_add_user_to_group(self):
        self.slack.add_user_to_group(self.user_id, self.group_id)
        assert self.slack._make_request.assert_called_with(
            url=f"https://api.slack.com/scim/{self.version}/Users/{self.user_id}",
            req_type="patch",
            data={
                "schemas": ["urn:scim:schemas:core:1.0"],
                "members": [{"value": self.user_id}],
            },
        )

    def test_add_user_to_channel(self):
        self.slack.add_user_to_channel(channel_ids=self.channel_ids, email=self.user_email, team_id=self.team_id)
        assert self.client.admin_users_invite.assert_called_with(
            channel_ids=self.channel_ids, email=self.user_email, team_id=self.team_id
        )

    def get_successful_response(self, message):
        return {"ok": True, "message": {"text": message}}


if __name__ == "__main__":
    import unittest

    unittest.main()
