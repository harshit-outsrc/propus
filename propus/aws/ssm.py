import backoff
import boto3
from botocore.exceptions import ClientError
import json
import logging
from typing import AnyStr, Dict

from propus.logging_utility import Logging
from propus.aws.exceptions import Non200Exception
from ssm_cache import SSMParameter


boto3.set_stream_logger("botocore.credentials", logging.CRITICAL)


class AWS_SSM(object):
    _default_region = "us-west-2"
    _kms_key_id = "69776fb9-cbe2-489c-8efe-1dd896aeab68"

    def __init__(self, ssm_client, cache_client=None):
        self.logger = Logging.get_logger("propus/aws/ssm")
        self.ssm_client = ssm_client
        self.ssm_cache = cache_client
        self.max_cache_age = 3600  # 1 hour

    @staticmethod
    def build(region: AnyStr = None, use_cache=False):
        if region is None:
            region = AWS_SSM._default_region
        client = boto3.client("ssm", region_name=region)
        return AWS_SSM(client, cache_client=SSMParameter if use_cache else None)

    @backoff.on_exception(backoff.expo, exception=(ClientError), max_tries=5)
    def get_param(self, parameter_name: AnyStr, param_type: AnyStr = None):
        """
        Retrieves the parameter from SSM and if the param_type is set return correctly (i.e. json to dictionary)

        Args:
            parameter_name (AnyStr): Parameter name of the SSM to retrieve
            param_type (AnyStr, optional): Param Type [string, json]. If json is specified JSON.loads will be returned

        :return: SSM Data (either Dict or String)
        """

        try:
            if self.ssm_cache:
                data = self.ssm_cache(parameter_name, max_age=self.max_cache_age)
                return json.loads(data.value) if param_type == "json" else data.value

            parameter = self.ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
            if parameter.get("ResponseMetadata", {}).get("HTTPStatusCode", 0) != 200:
                raise Non200Exception()
            if param_type == "json":
                return json.loads(parameter.get("Parameter", {}).get("Value", {}))
            return parameter.get("Parameter", {}).get("Value", {})
        except Exception as err:
            self.logger.error(f"Error during get_param: {err}")
            raise err

    @backoff.on_exception(backoff.expo, exception=(ClientError), max_tries=5)
    def put_param(self, parameter_name: AnyStr, value: AnyStr, overwrite: bool = False, **kwargs) -> Dict:
        """
        Puts the parameter data up to AWS SSM. Only parameter_name and value is required

        Args:
            parameter_name (AnyStr): Parameter name of the SSM to retrieve
            value (AnyStr): parameter data
            overwrite (bool): Default to False, must be set to true for updates to parameter
            kwargs: Additional arguments that can be added. They can be found on AWS Documentation:
                https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/put_parameter.html
                Current Supported Args are:
                  - description
                  - type
                  - key_id

        Raises:
            err: upon error from the AWS API, the same error will be returned to the caller

        :return: (Dict) SSM Data
        """
        try:
            payload = {
                "Name": parameter_name,
                "Value": value,
                "Type": "SecureString",
                "Overwrite": overwrite,
                "KeyId": self._kms_key_id,
                "Tags": [{"Key": "Name", "Value": parameter_name}],
                "Tier": "Standard",
            }
            if overwrite:
                del payload["Tags"]
            if kwargs.get("description"):
                payload["Description"] = kwargs.get("description")
            if kwargs.get("type"):
                payload["Type"] = kwargs.get("type")
                del payload["KeyId"]
            if kwargs.get("key_id"):
                payload["KeyId"] = kwargs.get("key_id")

            resp = self.ssm_client.put_parameter(**payload)
            self.logger.info(f"Successfully put_param: {parameter_name}")
            return resp
        except Exception as err:
            self.logger.error(f"Error during put_param: {err}")
            raise err
