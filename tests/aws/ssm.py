import boto3
from botocore.exceptions import ClientError
from moto import mock_ssm
import unittest

from propus.aws.ssm import AWS_SSM


class TestSSM(unittest.TestCase):
    ssm_mock = mock_ssm()
    text_data = "ssm string data"
    json_data = '{"key": {"ssm_key": "ssm_value"}}'

    def setUp(self):
        self.ssm_mock.start()
        self.ssm_client = boto3.client("ssm", "us-west-2")
        self.ssm_client.put_parameter(Name="/foo/name1", Value=self.text_data, Type="String")
        self.ssm_client.put_parameter(
            Name="/foo/name2",
            Value=self.text_data,
            Type="SecureString",
            KeyId="alias/aws/ssm",
        )
        self.ssm_client.put_parameter(
            Name="/foo/name3",
            Value=self.json_data,
            Type="SecureString",
            KeyId="alias/aws/ssm",
        )
        self.ssm_module = AWS_SSM(self.ssm_client)

    def tearDown(self):
        self.ssm_mock.stop()

    def test_retrieve_string_ssm(self):
        response = self.ssm_module.get_param("/foo/name1")
        self.assertEqual(response, self.text_data)
        response = self.ssm_module.get_param("/foo/name2")
        self.assertEqual(response, self.text_data)
        response = self.ssm_module.get_param("/foo/name3", "json")
        self.assertEqual(response.get("key").get("ssm_key"), "ssm_value")

    def test_bad_key(self):
        error_caught = None
        try:
            self.ssm_module.get_param("WHAT_KEY")
        except ClientError as err:
            error_caught = "ParameterNotFound" in str(err)
            pass
        self.assertIsNotNone(error_caught)


if __name__ == "__main__":
    unittest.main()
