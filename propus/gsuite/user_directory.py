import random
from typing import AnyStr

import googleapiclient.discovery

from google.oauth2 import service_account

from propus.logging_utility import Logging

from propus.helpers.input_validations import (
    validate_email,
    validate_phone_number,
    validate_string_length,
)

from propus.helpers.etl import clean_phone, generate_password

from propus.gsuite.exceptions import (
    UserUpdateMissingFields,
    UserCreateRequestsReached,
    UserAttemptingToCreateExists,
)

from propus.gsuite.constants import USER_KEY_MAPPING


class UserDirectory:
    """
    Wrapper class for interacting with Google Admin SDK Directory API to fetch user information.

    Args:
        client: An initialized Google Admin SDK Directory API client.

    Attributes:
        client: Google Admin SDK Directory API client.
        logger: Logger instance for logging.

    Methods:
        build: Factory method to create an instance of UserDirectory with the provided service account information.

        fetch_profile_picture(user_key):
            Fetches the profile picture of a user from Google Admin SDK Directory API.

    """

    def __init__(self, client):
        """
        Initializes the UserDirectory instance.

        Args:
            client: An initialized Google Admin SDK Directory API client.

        """
        self.domain = "calbrightcollege.org"
        self.client = client
        self.calbright_college_customer_id = "C00mo6spc"
        self.logger = Logging.get_logger("propus/gsuite/user_directory.py")

    @staticmethod
    def build(service_account_info, readonly=True):
        """
        Factory method to create an instance of UserDirectory with the provided service account information.

        Args:
            service_account_info: Information needed to create Google Admin SDK Directory API credentials.

        Returns:
            An instance of UserDirectory.
        """
        credentials = service_account.Credentials.from_service_account_info(service_account_info).with_subject(
            "svc-engineering@calbrightcollege.org"
        )

        scope = ["https://www.googleapis.com/auth/admin.directory.user.readonly"]
        if not readonly:
            scope = ["https://www.googleapis.com/auth/admin.directory.user"]
        creds_with_scope = credentials.with_scopes(scope)
        return UserDirectory(googleapiclient.discovery.build("admin", "directory_v1", credentials=creds_with_scope))

    def fetch_profile_picture(self, user_key):
        """
        Fetches the profile picture of a user from Google Admin SDK Directory API.

        Args:
            user_key: Key identifying the user whose profile picture is to be fetched.

        Returns:
            Dictionary containing user photo information.

        Raises:
            Exception: If there is an error fetching the user photo.

        """
        try:
            response = self.client.users().photos().get(userKey=user_key).execute()
            return response
        except Exception as err:
            self.logger.error(f"Error fetching user photo: {err}")
            # Return URL for default profile picture
            raise err

    def fetch_user(self, user_key: AnyStr):
        """Fetch user data that exists within GSuite

        Args:
            user_key (AnyStr): User Key can be primary email address, alias email address, or unique user ID.

        Raises:
            err: If there is an error fetching the user

        Returns:
            dict: Dictionary with user data found
        """
        try:
            response = self.client.users().get(userKey=user_key).execute()
            return response
        except Exception as err:
            self.logger.error(f"Error fetching user: {err}")
            raise err

    def fetch_all_users(self, active=True, suspended=False):
        """
        Fetches a list of all users from the Google Admin SDK Directory API.

        Args:
            show_suspended (bool, optional): Whether to include suspended users in the
                results. Defaults to False.

        Returns:
            list: A list of dictionaries representing user details for all users in
                the customer's Google Workspace domain. Each dictionary contains
                basic user information such as email, name, and suspended status.

        This method uses the Google Admin SDK Directory API to retrieve a list of
        all users in the customer's domain. It handles pagination by making
        multiple API requests if necessary, until all users have been fetched.
        The results are filtered based on the `show_suspended` parameter.
        """
        all_users = []
        next_token = "first_iteration"

        query = ""
        if active and not suspended:
            query = "isSuspended=False"
        elif suspended and not active:
            query = "isSuspended=True"

        while next_token:
            list_args = {
                "customer": self.calbright_college_customer_id,
                "query": query,
                "maxResults": 100,
                "orderBy": "email",
                "viewType": "admin_view",
                "projection": "basic",
                "showDeleted": False,
            }
            if next_token != "first_iteration":
                list_args["pageToken"] = next_token
            results = self.client.users().list(**list_args).execute()
            all_users += results.get("users")
            next_token = results.get("nextPageToken")
        return all_users

    def create_user(
        self,
        personal_email: AnyStr,
        ccc_id: AnyStr,
        first_name: AnyStr,
        last_name: AnyStr,
        phone_number: AnyStr,
        org_unit_path: AnyStr = None,
        calbright_email: AnyStr = None,
        password: AnyStr = None,
        max_attempts=10,
    ):
        """Creates a new GSuite user based on provided variables

        Args:
            personal_email (AnyStr): student supplied personal email
            ccc_id (AnyStr): student id coming from CCCApply
            first_name (AnyStr): student first name
            last_name (AnyStr): student last name
            phone_number (AnyStr): US phone number as it will be cleaned and +1 applied to follow E.164 format
            org_unit_path (AnyStr, optional): organizational unit that applies permissions and apps. Defaults to None.
            calbright_email (AnyStr, optional): if passed, will attempt to create student email with passed calbright
                email. Defaults to None.
            password (AnyStr, optional): if passed, will use as the first password for login and then user will reset
                on first login. If not, then a newly generated password will be applied. Defaults to None.
            max_attempts (Integer, optional): max number of tries to setup a new user email. Defaults to 10

        Raises:
            UserCreateRequestsReached: If max attempts is reached for creating a new user, raises this exception
            UserAttemptingToCreateExists: Exception if calbright email is passed, but student is already existing
            err: Exception if error occurred during the attempt of creating new GSuite user

        Returns:
            dict: response of student that was newly created
        """

        try:
            phone_number = clean_phone(phone_number)
            validate_string_length(ccc_id, "ccc_id", max_len=8)
            validate_string_length(first_name, "first_name", max_len=100)
            validate_string_length(last_name, "last_name", max_len=100)
            validate_phone_number(phone_number, "NNNNNNNNNN")
            validate_email(personal_email)

            if not password:
                password = generate_password()
            else:
                validate_string_length(password, "password", min_len=8, max_len=36)

            if not calbright_email:
                calbright_email = f"{first_name}.{last_name}".lower()

                check_email = f"{calbright_email}@{self.domain}"
                for i in range(max_attempts):
                    if self.check_existing_email(check_email):
                        check_email = f"{calbright_email}{random.randint(0, 100)}@{self.domain}"
                    else:
                        calbright_email = check_email
                        break

                    if i == 9:
                        raise UserCreateRequestsReached
            else:
                validate_email(calbright_email)
                if self.check_existing_email(calbright_email):
                    raise UserAttemptingToCreateExists

            if not org_unit_path:
                org_unit_path = "/Pre-enrolled Students"

            user_payload = {
                "primaryEmail": calbright_email,
                "password": password,
                "agreedToTerms": False,
                "suspended": False,
                "changePasswordAtNextLogin": True,
                "name": {"familyName": last_name, "givenName": first_name},
                "emails": [
                    {"address": calbright_email, "primary": True},
                    {"address": personal_email, "type": "home", "primary": False},
                ],
                "addresses": [{"region": "CA"}],
                "phones": [{"value": f"+1{phone_number}", "type": "work"}],
                "includeInGlobalAddressList": False,
                "customSchemas": {"custom_attributes": {"role": "student", "cid": ccc_id}},
                "orgUnitPath": org_unit_path,
                "recoveryEmail": personal_email,
                "recoveryPhone": f"+1{phone_number}",  # Format for google api
            }

            response = self.client.users().insert(body=user_payload).execute()
            return response
        except Exception as err:
            self.logger.error(f"Error creating user: {err}")
            raise err

    def _update_user(self, calbright_email: AnyStr, **kwargs):
        """Update specific user based on dictionary of data passed

            Example of mapping used for data passed:
            USER_KEY_MAPPING = {
                "agreed_to_terms": "agreedToTerms",
                "suspended": "suspended",
                "first_name": "givenName",
                "last_name": "familyName",
                "personal_email": "address",
                "phone_number": "value",
                "org_unit_path": "orgUnitPath",
            }

        Args:
            calbright_email (AnyStr): The student email tied to the GSuite used as user_key

        Raises:
            UserUpdateMissingFields: Passed data didn't contain any of the mapped fields and no update was performed
            err: Exception if error occurred during updating of the GSuite account

        Returns:
            dict: response of student that was newly updated
        """

        try:
            user_payload = self.fetch_user(calbright_email)

            fields_updated = False

            for key, value in kwargs.items():
                if not USER_KEY_MAPPING.get(key):
                    continue

                if key == "first_name" or key == "last_name":
                    validate_string_length(value, "first_name", max_len=100)
                    user_payload["name"][USER_KEY_MAPPING.get(key)] = value
                elif key == "phone_number":
                    value = clean_phone(value)
                    validate_phone_number(value, "NNNNNNNNNN")
                    value = f"+1{value}"
                    if not any(phone.get("value") == value for phone in user_payload["phones"]):
                        user_payload["phones"].append({"value": value, "type": "home"})
                elif key == "personal_email":
                    validate_email(value)
                    if not any(email.get("address") == value for email in user_payload["emails"]):
                        user_payload["emails"].append({"address": value, "type": "home", "primary": False})
                else:
                    user_payload[USER_KEY_MAPPING.get(key)] = value

                fields_updated = True

            if not fields_updated:
                raise UserUpdateMissingFields

            response = self.client.users().update(userKey=calbright_email, body=user_payload).execute()
            return response
        except Exception as err:
            self.logger.error(f"Error updating user: {err}")
            raise err

    def update_user_org_unit(self, calbright_email: AnyStr, org_unit_path: AnyStr, suspended=False):
        """Update user organizational unit that contains the permissions and apps

        Args:
            calbright_email (AnyStr): The student email tied to the GSuite used as user_key
            org_unit_path (AnyStr): The path to the organizational unit to apply.
                Example of OU Paths:
                    "/Enrolled Students",
                    "/Enrolled Students/CRM Platform Admin Program",
                    "/Pre-enrolled Students",
                    "/Suspended"
            suspended (bool, optional): Determines if the student should be suspended with OU update. Defaults to False.

        Returns:
            dict: response of student that was newly updated
        """
        user_data = {
            "suspended": suspended,
            "org_unit_path": org_unit_path,
        }

        return self._update_user(calbright_email, **user_data)

    def check_existing_email(self, calbright_email: AnyStr):
        """Checks if email exists or not

        Args:
            calbright_email (AnyStr): The student email tied to the GSuite used as user_key

        Returns:
            bool: Returns True if existing user found, False if an user wasn't found
        """
        try:
            self.fetch_user(calbright_email)
            return True
        except Exception as err:
            self.logger.info(f"Couldn't find existing user: {err}")
            return False
