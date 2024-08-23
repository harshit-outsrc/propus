from propus.api_client import RestAPIClient
import json
from typing import AnyStr, Dict


class WPWebhook(RestAPIClient):
    def __init__(self, api_key, base_url, wh_env):
        super().__init__(base_url=base_url)
        self.default_params = {"wpwhpro_action": wh_env, "wpwhpro_api_key": api_key}
        self.base_url = base_url
        self.timeout = 10

    @staticmethod
    def build(
        api_key: AnyStr, base_url: AnyStr = "https://beta.calbrightcollege.org/", wh_env: AnyStr = "beta-student-portal"
    ):
        """
        Singleton to build the WPWebhook Client.
        Args:
            wh_env (AnyStr): Environment that shall match one setup in Student Portal
            api_key (AnyStr): API key used to hit the webhook
            base_url (AnyStr): : base url for WP Webhooks API
               - Defaults to https://beta.calbrightcollege.org/

        Returns:
            An instance of WPWebhook Class
        """
        return WPWebhook(wh_env=wh_env, api_key=api_key, base_url=base_url)

    def update_user(self, user_meta: Dict, user_email: AnyStr = None, user_id: AnyStr = None) -> Dict:
        """Update students on their Wordpress Portal. user_id has higher priority over the user email on lookup.

        Args:
            user_meta (Dict): metadata fields attempting to update on Wordpress
            user_email (AnyStr, optional): user email of the existing account that needs updating. Defaults to None.
            user_id (AnyStr, optional): user id of the existing account that needs updating. Defaults to None.

        Raises:
            Exception: If User ID or User Email is not provided throws an exception

        Returns:
            Dict: returns the response received from WPWebhooks.
        """

        if not any((user_id, user_email)):
            raise Exception("At least an user id or email must be given.")

        user_info = dict()

        if user_id:
            user_info["user_id"] = user_id
        if user_email:
            user_info["user_email"] = user_email

        payload = {**user_info, "action": "update_user", "user_meta": json.dumps(user_meta)}

        resp = self._make_request(
            url=self.base_url,
            data=payload,
            params=self.default_params,
            req_type="post",
            headers={
                "User-Agent": "CalbrightCastor",
            },
        )

        return resp
