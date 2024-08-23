from typing import AnyStr

import googleapiclient.discovery
from google.oauth2 import service_account

from propus.logging_utility import Logging
from propus.helpers.input_validations import validate_email
from propus.gsuite.constants import (
    GSE_PRODUCT_ID,
    GSE_SKU_ID,
)
from propus.gsuite.exceptions import LicensingException


class Licensing:
    """
    Wrapper class for interacting with Google Admin SDK Licensing API to manage licenses.

    Args:
        client: An initialized Google Admin SDK Licensing API client.

    Attributes:
        client: Google Admin SDK Licensing API client.
        logger: Logger instance for logging.

    Methods:
        build: Factory method to create an instance of Licensing with the provided service account information.

        fetch_profile_picture(user_key):
            Fetches the profile picture of a user from Google Admin SDK Licensing API.

    """

    def __init__(self, client):
        """
        Initializes the Licensing instance.

        Args:
            client: An initialized Google Admin SDK Licensing API client.

        """
        self.domain = "calbrightcollege.org"
        self.client = client
        self.logger = Logging.get_logger("propus/gsuite/licensing.py")

    @staticmethod
    def build(service_account_info):
        """
        Factory method to create an instance of Licensing with the provided service account information.

        Args:
            service_account_info: Information needed to create Google Admin SDK Licensing API credentials.

        Returns:
            An instance of Licensing.

        """
        credentials = service_account.Credentials.from_service_account_info(service_account_info).with_subject(
            "svc-engineering@calbrightcollege.org"
        )
        scope = [
            "https://www.googleapis.com/auth/apps.licensing",
        ]
        creds_with_scope = credentials.with_scopes(scope)
        return Licensing(googleapiclient.discovery.build("licensing", "v1", credentials=creds_with_scope))

    def get_license(self, calbright_email: AnyStr, product_id: AnyStr = GSE_PRODUCT_ID, sku_id: AnyStr = GSE_SKU_ID):
        """
        Get GSuite license assignments for a user.

        Args:
            calbright_email (str): Email address of the user.
            product_id (str): Product ID
                Defaults to "101031"
            sku_id (str): SKU ID
                Defaults to "1010310003"

        Returns:
            response (dict): Google API Client LicenseAssignment object.
                returns empty dictionary if user does not have the specified license.

        Raises:
            InvalidEmail: Raised if calbright_email fails validate_email
            LicensingException: Raised if Google API Client returns an error outside of license not found.
        """
        validate_email(calbright_email)
        try:
            response = (
                self.client.licenseAssignments()
                .get(productId=product_id, skuId=sku_id, userId=calbright_email)
                .execute()
            )
            self.logger.info(
                f"Google license assignments for productId {product_id} skuId {sku_id} userId {calbright_email}: {response}"  # noqa: E501
            )
            return response
        except googleapiclient.errors.HttpError as e:
            if e.status_code == 404 and "User does not have a license for specified sku and product" in str(e):
                return {}
            raise e
        except Exception as e:
            self.logger.error(
                f"Google license assignments for productId {product_id} skuId {sku_id} userId {calbright_email}: {e}"
            )
            raise LicensingException(
                msg=e,
                method="get_license",
                calbright_email=calbright_email,
                product_id=product_id,
                sku_id=sku_id,
            )

    def delete_license(self, calbright_email, product_id=GSE_PRODUCT_ID, sku_id=GSE_SKU_ID):
        """
        Delete GSuite license assignments for a user.

        Args:
            calbright_email (str): Email address of the user.
            product_id (str): Product ID
                Defaults to "101031"
            sku_id (str): SKU ID
                Defaults to "1010310003"

        Returns:
            response: 200 (OK) if successful

        Raises:
            InvalidEmail: Raised if calbright_email fails validate_email
            LicensingException: Raised if Google API Client returns an error.
        """
        validate_email(calbright_email)
        try:
            delete_response = (
                self.client.licenseAssignments()
                .delete(productId=product_id, skuId=sku_id, userId=calbright_email)
                .execute()
            )
            self.logger.info(
                f"Google license delete for productId {product_id} skuId {sku_id} userId {calbright_email}: {delete_response}"  # noqa: E501
            )
            return delete_response
        except Exception as e:
            self.logger.error(
                f"Google license delete for productId {product_id} skuId {sku_id} userId {calbright_email}: {e}"
            )
            raise LicensingException(
                msg=e,
                method="delete_license",
                calbright_email=calbright_email,
                product_id=product_id,
                sku_id=sku_id,
            )
