import boto3
from botocore.exceptions import ClientError
from moto import mock_s3
import unittest

from propus.aws.s3 import AWS_S3


class TestS3(unittest.TestCase):
    mock_s3 = mock_s3()

    def setUp(self):
        self.aws_default_region = "us-west-2"
        self.mock_s3.start()
        self.s3_client = boto3.client("s3", self.aws_default_region)
        self.s3_resource = boto3.resource("s3", self.aws_default_region)

        # Create Mock Bucket
        self.bucket = "test_bucket"
        self.other_bucket = "another_bucket"
        self.s3_resource.create_bucket(
            Bucket=self.bucket,
            CreateBucketConfiguration={"LocationConstraint": self.aws_default_region},
        )
        self.s3_resource.create_bucket(
            Bucket=self.other_bucket,
            CreateBucketConfiguration={"LocationConstraint": self.aws_default_region},
        )

        # Create File (Until we build out this functionality in s3 module)
        self.key = "test_key.csv"
        self.body = "Some Test Data in CSV Format!"
        self.s3_client.put_object(Bucket=self.bucket, Key=self.key, Body=self.body)

        self.s3_module = AWS_S3(self.s3_resource, self.s3_client)

    def tearDown(self):
        self.mock_s3.stop()

    def test_write_to_s3(self):
        content = "Test Content"
        key = "test_write.txt"
        self.s3_module.write_to_s3(self.bucket, key, content)
        exists = self.s3_module.s3_file_exists(self.bucket, key)
        self.assertTrue(exists)
        read_from_s3 = self.s3_module.read_from_s3(bucket=self.bucket, key=key)
        self.assertEqual(read_from_s3, content)

    def test_read_from_s3(self):
        read_from_s3 = self.s3_module.read_from_s3(bucket=self.bucket, key=self.key)
        self.assertEqual(read_from_s3, self.body)
        with self.assertRaises(ClientError):
            _ = self.s3_module.read_from_s3(bucket=self.bucket, key="BAD_READ")

    def test_file_exists(self):
        valid_file = self.s3_module.s3_file_exists(bucket=self.bucket, key=self.key)
        self.assertTrue(valid_file)
        invalid_file = self.s3_module.s3_file_exists(bucket=self.bucket, key="bad_file")
        self.assertFalse(invalid_file)
        invalid_file = self.s3_module.s3_file_exists(bucket="bad_bucket", key=self.key)
        self.assertFalse(invalid_file)

    def test_download_file(self):
        resp = self.s3_module.download(self.bucket, self.key, "/tmp/test_file")
        self.assertTrue(resp)
        resp = self.s3_module.download(self.bucket, "unkown_key.csv", "/tmp/test_file")
        self.assertFalse(resp)

    def test_upload_file(self):
        resp = self.s3_module.upload("/tmp/test_file", self.bucket, "new_file")
        self.assertTrue(resp)
        resp = self.s3_module.upload("/tmp/test_file", "bad_bucket", "new_file")
        self.assertFalse(resp)

    def test_list_objects(self):
        found_file = False
        for obj in self.s3_module.list_objects(bucket=self.bucket, prefix=""):
            if obj.get("Key") == self.key:
                found_file = True
        self.assertTrue(found_file)

    def test_delete_objects(self):
        errors = self.s3_module.delete_objects(bucket=self.bucket, keys=[self.key])
        self.assertTrue(len(errors) == 0)

    def test_copy_file(self):
        source = {"Bucket": self.bucket, "Key": self.key}
        destination = {"Bucket": self.other_bucket, "Key": "destination_key"}
        self.assertTrue(self.s3_module.copy_file(source, destination))


if __name__ == "__main__":
    unittest.main()
