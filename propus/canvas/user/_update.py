import json
from typing import Literal, Optional


async def update_user(
    self,
    user_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    time_zone: Optional[str] = None,
    email_address: Optional[str] = None,
    locale: Optional[str] = None,
    avatar_token: Optional[str] = None,
    avatar_url: Optional[str] = None,
    avatar_state: Optional[Literal["none", "submitted", "approved", "locked", "reported", "re_reported"]] = None,
    title: Optional[str] = None,
    bio: Optional[str] = None,
    pronouns: Optional[str] = None,
    event: Optional[Literal["suspend", "unsuspend"]] = None,
    override_sis_stickiness: bool = True,
) -> dict:
    """
    Update a user. This is a wrapper around the Canvas API endpoint for updating a user.
    Docs: https://canvas.instructure.com/doc/api/users.html#method.users.update
    :param self:
    :param user_id: The canvas user ID to update
    :param first_name: used to set name, short name, and sortable name. Both first and last are required to update.
    :param last_name: used to set name, short name, and sortable name. Both first and last are required to update.
    :param time_zone: The tz for the user. Allowed tz are IANA time zones or friendlier Ruby on Rails time zones.
    :param email: The default email address of the user.
    :param locale: The user’s preferred language, from the list of languages Canvas supports. In RFC-5646 format.
    :param avatar_token: A unique representation of the avatar record to assign as the user’s current avatar.
        This token can be obtained from the user avatars endpoint.
        This supersedes the user [avatar] [url] argument, and if both are included the url will be ignored.
        It should be consumed with this api endpoint and used in the user update endpoint,
        and should not be constructed by the client.
    :param avatar_url: To set the user’s avatar to point to an external url, do not include a token and instead
        pass the url here. Warning: For maximum compatibility, please use 128 px square images.
    :param avatar_state: To set the state of user’s avatar. Only valid for account administrator.
    :param title: Sets a title on the user profile. Profiles must be enabled on the root account.
    :param bio: Sets a bio on the user profile. Profiles must be enabled on the root account.
    :param pronouns: Sets pronouns on the user profile. Passing an empty string will empty the user’s pronouns.
        Only Available Pronouns set on the root account are allowed.
        Adding and changing pronouns must be enabled on the root account.
    :param event: Suspends or unsuspends all logins for this user that the calling user has permission to
    :param override_sis_stickiness: Default is true. If false, any fields containing “sticky” changes will not be
        updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness
    :return: The updated user object
    """
    payload = {
        "override_sis_stickiness": override_sis_stickiness,
        "user": {"avatar": {}},
        "communication_channel": {},
    }
    if first_name and last_name:
        payload["user"]["name"] = first_name + " " + last_name
        payload["user"]["sortable_name"] = last_name + ", " + first_name
        payload["user"]["short_name"] = first_name + " " + last_name
    if time_zone is not None:
        payload["user"]["time_zone"] = time_zone
    if email_address is not None:
        payload["user"]["email"] = email_address
    if locale is not None:
        payload["user"]["locale"] = locale
    if avatar_token is not None:
        payload["user"]["avatar"]["token"] = avatar_token
    if avatar_url is not None:
        payload["user"]["avatar"]["url"] = avatar_token
    if avatar_state is not None:
        payload["user"]["avatar"]["state"] = avatar_state
    if title is not None:
        payload["user"]["title"] = title
    if bio is not None:
        payload["user"]["bio"] = bio
    if pronouns is not None:
        payload["user"]["pronouns"] = pronouns
    if event is not None:
        payload["user"]["event"] = event

    return self.make_request(
        req_type="put",
        url=self._get_endpoint("update_user", {"<user_id>": user_id}),
        data=json.dumps(payload),
    )
