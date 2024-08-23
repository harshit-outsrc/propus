from typing import AnyStr

from propus.logging_utility import Logging


class Slack:
    def __init__(
        self,
        client,
        ssm=None,
        base_url="https://api.slack.com",
        version="v1",
    ):
        self.base_url = base_url
        self.ssm = ssm
        self.version = version
        self.client = client
        self.logger = Logging.get_logger("propus/slack.py")

        self.endpoints = {
            "users": f"/scim/{self.version}/Users/",
            "user": (f"/scim/{self.version}/Users/<user_id>", ["<user_id>"]),
            "group": (f"/scim/{self.version}/Groups/<group_id>", ["<group_id>"]),
            "token_url_v2": "/oauth.v2.access",
            "token_url_v1": "/oauth.access",
            "token_base_url": "https://slack.com/api",
        }

    @staticmethod
    def build(ssm):
        """
        Build method for the Slack class

        Returns:
            class(Slack): Class Initialization of Slack
        """
        from slack_sdk import WebClient
        import ssl
        import certifi

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        web_client = WebClient(token=ssm.get("calbright-bot").get("bot_user_oauth_token"), ssl=ssl_context)

        return Slack(web_client)

    def send_message(self, channel: AnyStr, message: AnyStr, markdown: bool = True):
        """
        This method will send a message to a Slack channel

        Args:
            channel (string): channel to receive the message in slack
            message (string): message to be sent in slack
            markdown (boolean): determine if slack api should post with markdown syntax available. Defaults to True
        """
        try:
            response = self.client.chat_postMessage(channel=channel, text=message, mrkdwn=markdown)
            assert response.get("message", {}).get("text") == message
        except Exception as e:
            self.logger.error(f"Failed attempt to send Slack message: {e}")

    def add_user_to_channel(self, channel_ids: list, email: AnyStr, team_id: AnyStr):
        """
        This method will add a user to a Slack channel

        Args:
            channel_ids (list): list of channel ids to add the user
            email (string): user email
            team_id (string): team id
        """
        try:
            self.client.admin_users_invite(channel_ids=channel_ids, email=email, team_id=team_id)
        except Exception as e:
            self.logger.error(f"Failed attempt to add user to a channel: {e}")

    def create_user(self, username: AnyStr, email: AnyStr):
        """
        This method will create a user through the Slack SCIM API

        Args:
            username (string): username
            email (string): user email
        """
        url = self._get_endpoint("users")
        data = {
            "schemas": [
                "urn:scim:schemas:core:1.0",
                "urn:scim:schemas:extension:enterprise:1.0",
            ],
            "userName": username,
            "emails": [{"value": email, "type": "work", "primary": True}],
        }
        return self._make_request(url, data, req_type="post")

    def add_user_to_group(self, user_id: AnyStr, group_id: AnyStr):
        """
        This method will add a user to a group through the Slack SCIM API

        Args:
            user_id (string): user id
            group_id (string): user email
        """
        url = self._get_endpoint("group", {"group_id": group_id})
        data = {
            "schemas": ["urn:scim:schemas:core:1.0"],
            "members": [{"value": user_id}],
        }
        return self._make_request(url, data=data, req_type="patch")

    def delete_user(self, user_id: AnyStr):
        """
        This method will delete a user through the Slack SCIM API

        Args:
            user_id (string): user id
        """
        url = self._get_endpoint("user", {"user_id": user_id})
        return self._make_request(url, req_type="delete")
