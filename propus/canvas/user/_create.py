import json
from typing import Literal, Optional

from propus.api_client import FailedRequest
from propus.canvas.user._exceptions import UserIdTaken
from propus.helpers.input_validations import validate_email


async def create_user(
    self,
    user_type: Literal["student", "staff"],
    first_name: str,
    last_name: str,
    email_address: str,
    sis_user_id: str,
    integration_id: Optional[str] = None,
    timezone: Optional[str] = "America/Los_Angeles",
    locale: Optional[str] = "en",
    destination: Optional[str] = None,
    initial_enrollment_type: Optional[str] = None,
    pairing_code: Optional[str] = None,
    terms_of_use: bool = False,
    send_confirmation: bool = False,
    skip_registration: bool = True,
    force_self_registration: bool = False,
    confirmation_url: bool = False,
    skip_confirmation: bool = True,
    force_validations: bool = False,
    enable_sis_reactivation: bool = True,
) -> dict:
    """
    Create a new student in the account. This is a wrapper around the Canvas API endpoint for creating a user.
    Docs: https://canvas.instructure.com/doc/api/users.html#method.users.create
    :param self:
    :param user_type: The type of user to create. Must be either 'student' or 'staff'.
    :param first_name: used to set name, short name, and sortable name. Both first and last are required to update.
    :param last_name: used to set name, short name, and sortable name. Both first and last are required to update.
    :param email_address: The default email address of the user.
    :param sis_user_id: SIS ID for the user’s account. To set this parameter, the caller must be able to
        manage SIS permissions.
    :param integration_id: Integration ID for the login. To set this parameter, the caller must be able to
        manage SIS permissions. The Integration ID is a secondary identifier useful for more complex SIS integrations.
    :param authentication_provider_id: The authentication provider this login is associated with. Logins associated
        with a specific provider can only be used with that provider. Legacy providers (LDAP, CAS, SAML) will search
        for logins associated with them, or unassociated logins. New providers will only search for logins explicitly
         associated with them. This can be the integer ID of the provider, or the type of the provider (in which case,
          it will find the first matching provider).
    :param timezone: The tz for the user. Allowed tz are IANA time zones or friendlier Ruby on Rails time zones.
    :param locale: The user’s preferred language, from the list of languages Canvas supports. In RFC-5646 format.
    :param destination: If you’re setting the password for the newly created user, you can provide this param with
        a valid URL pointing into this Canvas installation, and the response will include a destination field that’s a
        URL that you can redirect a browser to and have the newly created user automatically logged in. The URL is only
         valid for a short time, and must match the domain this request is directed to, and be for a well-formed path
          that Canvas can recognize.
    :param initial_enrollment_type: ‘observer` if doing a self-registration with a pairing code.
        This allows setting the password during user creation.
    :param pairing_code: If provided and valid, will link the new user as an observer to the
        students whose pairing code is given.
    :param terms_of_use: Whether the user accepts the terms of use. Required if this is a self-registration and this
        canvas instance requires users to accept the terms (on by default).
    :param send_confirmation:
    :param skip_registration: Automatically mark the user as registered. If this is true, it is recommended to set
        "pseudonym[send_confirmation]" to true as well. Otherwise, the user will not receive any messages about
        their account creation.
    :param force_self_registration: Send user a self-registration style email if true. Setting it means the users will
        get a notification asking them to “complete the registration process” by clicking it, setting a password,
        and letting them in. Will only be executed on if the user does not need admin approval. Defaults to false
        unless explicitly provided.
    :param confirmation_url: Only valid for account admins. If true, returns the new user account confirmation
        URL in the response.
    :param skip_confirmation: Only valid for site admins and account admins making requests; If true, the channel is
        automatically validated and no confirmation email or SMS is sent. Otherwise, the user must respond to a
        confirmation message to confirm the channel. If this is true, it is recommended to set
         "pseudonym[send_confirmation]" to true as well. Otherwise, the user will not receive any messages about
          their account creation.
    :param force_validations: If true, validations are performed on the newly created user (and their associated
        pseudonym) even if the request is made by a privileged user like an admin. When set to false, or not included
        in the request parameters, any newly created users are subject to validations unless the request is made by
        a user with a ‘manage_user_logins’ right. In which case, certain validations such as
        ‘require_acceptance_of_terms’ and ‘require_presence_of_name’ are not enforced. Use this parameter to return
         helpful json errors while building users with an admin request.
    :param enable_sis_reactivation: When true, will first try to re-activate a deleted user with matching sis_user_id
        if possible. This is commonly done with user and communication_channel so that the default
        communication_channel is also restored.

    :return: The created user object
    """

    validate_email(email_address, is_required=True)

    # Note - these auth providers are stored in SSM
    if user_type == "student":
        authentication_provider_id = self.auth_providers["google"]
    else:
        authentication_provider_id = self.auth_providers["okta"]

    payload = {
        "user": {
            "name": first_name + " " + last_name,
            "short_name": first_name + " " + last_name,
            "sortable_name": last_name + ", " + first_name,
            "terms_of_use": terms_of_use,
            "skip_registration": skip_registration,
        },
        "pseudonym": {
            "unique_id": email_address,
            "sis_user_id": sis_user_id,
            "send_confirmation": send_confirmation,
            "force_self_registration": force_self_registration,
            "authentication_provider_id": authentication_provider_id,
            # "password": "",  # leave blank, they are using SSO
        },
        "communication_channel": {
            "type": "email",
            "address": email_address,
            "confirmation_url": confirmation_url,
            "skip_confirmation": skip_confirmation,
        },
        "force_validations": force_validations,
        "enable_sis_reactivation": enable_sis_reactivation,
        # "pseudonym[password]": "",  # leave blank, they are using SSO
    }
    if timezone is not None:
        payload["user"]["time_zone"] = timezone
    if locale is not None:
        payload["user"]["locale"] = locale
    if destination is not None:
        payload["destination"] = destination
    if initial_enrollment_type is not None:
        payload["initial_enrollment_type"] = initial_enrollment_type
    if pairing_code is not None:
        payload["pairing_code[code]"] = pairing_code
    if integration_id is not None:
        payload["pseudonym"]["integration_id"] = integration_id

    try:
        return self.make_request(
            req_type="post",
            url=self._get_endpoint("create_user", {"<account_id>": self._account_id}),
            data=json.dumps(payload),
        )
    except FailedRequest as e:
        error_message = str(e)
        try:
            error_data = json.loads(error_message.split(":", 1)[1].strip())

            pseudonym_errors = error_data["errors"].get("pseudonym", {})

            if pseudonym_errors:
                unique_id_errors = pseudonym_errors.get("unique_id", [])
                sis_user_id_errors = pseudonym_errors.get("sis_user_id", [])

                if any(error["type"] == "taken" for error in unique_id_errors + sis_user_id_errors):
                    raise UserIdTaken(sis_user_id, user_type)

            user_pseudonym_errors = error_data["errors"].get("user", {}).get("pseudonyms", [])

            if any(error["type"] == "invalid" for error in user_pseudonym_errors):
                raise Exception("One or more of the user pseudonyms are invalid")

        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse error message: {e}")
