import backoff
import boto3
from botocore.exceptions import ClientError, ParamValidationError
import logging
from typing import AnyStr, Dict, List

from propus.logging_utility import Logging

boto3.set_stream_logger("botocore.credentials", logging.CRITICAL)


class AWS_S3(object):
    _default_region = "us-west-2"

    def __init__(self, s3_resource, s3_client):
        self.s3_resource = s3_resource
        self.s3_client = s3_client
        self.logger = Logging.get_logger("aws/s3.py")

    @staticmethod
    def build(region: AnyStr = None, additional_params: Dict = {}):
        if region is None:
            region = AWS_S3._default_region
        s3_resource = boto3.resource("s3", region_name=region, **additional_params)
        s3_client = boto3.client("s3", region_name=region, **additional_params)
        return AWS_S3(s3_resource, s3_client)

    @backoff.on_exception(backoff.expo, exception=(ClientError, ParamValidationError), max_tries=5)
    def read_from_s3(self, bucket: AnyStr, key: AnyStr, **kwargs) -> AnyStr:
        """
        Given a bucket & key retrieve the file from S3 and return the object
        Returns empty string if the object file has been archived (stored in Glacier)
        :param bucket: String of the bucket the file is store in
        :param key: Full key of file being retrieved
        :kwargs can contain the following arguments:
            decode: Bool indicating if the response should be decoded (true) or left as byte array
        :return: Decoded text read from S3 object
        """
        obj = self.s3_resource.Object(bucket, key)
        body = obj.get()["Body"].read()
        if kwargs.get("decode", True):
            body = body.decode("utf-8")
        return body

    def download(self, bucket: AnyStr, key: AnyStr, download_location: AnyStr, extra_args={}) -> bool:
        """
        Wrapper around boto s3's download_file
        :param bucket: S3 Bucket
        :param key: S3 object key
        :param download_location: local location to download to
        :return: true/false on success of download
        """
        try:
            self.s3_client.download_file(bucket, key, download_location, ExtraArgs=extra_args)
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                self.logger.error(f"s3 - Failed download of file: {err}")
            return False
        except Exception as err:
            self.logger.error(f"s3 - Failed download of file: {err}")
            return False
        return True

    def upload(
        self,
        full_file_name: AnyStr,
        bucket: AnyStr,
        upload_path: AnyStr,
        extra_args: Dict = {},
    ) -> bool:
        """
        Upload wrapper around boto s3's upload_file
        :param full_file_name: Full file name location on localhost
        :param bucket: upload bucket
        :param upload_path: upload path
        :param extra_args: dictionary of any additional S3 args like content type, acl
        :return: true/false on success/failure
        """
        try:
            self.s3_client.upload_file(
                Filename=full_file_name,
                Bucket=bucket,
                Key=upload_path,
                ExtraArgs=extra_args,
            )
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                self.logger.info("The object does not exist.")
            return False
        except Exception as err:
            self.logger.error(f"s3 - Failed download of file: {err}")
            return False
        return True

    @backoff.on_exception(backoff.expo, exception=(ClientError, ParamValidationError), max_tries=5)
    def write_to_s3(self, bucket: AnyStr, key: AnyStr, body: AnyStr, **kwargs) -> Dict:
        """
        Stores body parameter into S3 bucket at a particular key
        :param bucket: String of the bucket the file will be stored in
        :param key: Full key of file being stored
        :param body: Content to store
        :param acl: Defines which AWS accounts or groups are granted access and the type of access
        :return:
            {
                'Expiration': 'string',
                'ETag': 'string',
                'ServerSideEncryption': 'AES256'|'aws:kms',
                'VersionId': 'string',
                'SSECustomerAlgorithm': 'string',
                'SSECustomerKeyMD5': 'string',
                'SSEKMSKeyId': 'string',
                'SSEKMSEncryptionContext': 'string',
                'RequestCharged': 'requester'
            }
        """
        obj = self.s3_resource.Object(bucket, key)
        response = obj.put(Body=body)

        acl = kwargs.get("acl")
        if acl:
            obj.Acl().put(ACL=acl)

        return response

    def head_obj(self, bucket: AnyStr, key: AnyStr):
        """
        This is a helper function that simply returns S3's head object response. This allows us to use this function
        within this class but also return a raw response. There is no error handling.
        :param bucket: (String) S3 Bucket
        :param key: (String) S3 Key to Lookup
        :return: S3 Head Object Response
        """
        return self.s3_client.head_object(Bucket=bucket, Key=key)

    def s3_file_exists(self, bucket: AnyStr, key: AnyStr) -> bool:
        """
        Simple function to query S3 and see if a given key exists
        :param bucket: (String) S3 Bucket
        :param key: (String) S3 Key to Lookup
        :return: Boolean True/False if File Exists
        """
        try:
            self.head_obj(bucket, key)
            return True
        except ClientError as err:
            if err.response.get("Error", {}).get("Code") in ["NoSuchBucket", "404"]:
                return False
            raise err

    def list_objects(self, bucket: AnyStr, prefix: AnyStr, additional_args: Dict = {}) -> Dict:
        """
        Returns a generator to loop through all possible items in a listed directory
        :param bucket: bucket of object
        :param prefix: object prefix to lookup for
        :param additional_args: Any additional arguments allowed by Boto3 API. See the following for request syntax:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
        :return: Dictionary is returned of the object data including key, last modified, etc.
        """
        list_args = {"Bucket": bucket, "Prefix": prefix, **additional_args}
        continuation_token = True
        while continuation_token:
            response = self.s3_client.list_objects_v2(**list_args)
            for item in response.get("Contents", []):
                yield item
            continuation_token = response.get("NextContinuationToken")
            list_args["ContinuationToken"] = continuation_token

    def delete_objects(self, bucket: AnyStr, keys: List, quiet: bool = True) -> List:
        """
        delete objects take a list of object (max 1000) and delete's the item at their S3 object path
        :param bucket: bucket of objects
        :param keys: list of items to delete
        :param quiet: enable quiet mode for the request.
        :return: list of any errors that occurred
        """
        try:
            response = self.s3_client.delete_objects(
                Bucket=bucket,
                Delete={"Objects": [{"Key": k} for k in keys], "Quiet": quiet},
            )
            return [e for e in response.get("Errors", [])]
        except Exception as err:
            self.logger.error(f"Bulk deleting objects failed. Error {err}")
            raise err

    def list_buckets(self):
        response = self.s3_client.list_buckets()
        for bucket in response.get("Buckets"):
            yield bucket

    @backoff.on_exception(backoff.expo, exception=(ClientError, ParamValidationError), max_tries=5)
    def copy_file(self, source, destination):
        """
        Copies file from source to destination. Returns true iff delete successful.
        :source dict: Dictionary in the format of {Bucket: '', Key: ''} to represent source of copy action.
        :destination dict: Dictionary in the format of {Bucket: '', Key: ''} to represent destination of copy action.
        :return: Boolean True/False if write successful
        """
        response = self.s3_client.copy_object(CopySource=source, **destination)
        return response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200
