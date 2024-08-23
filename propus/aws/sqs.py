import backoff
import boto3
from botocore.exceptions import ClientError, ParamValidationError
import logging
from typing import List, Dict, AnyStr
import warnings

from propus.logging_utility import Logging

warnings.filterwarnings("ignore", category=FutureWarning, module="botocore.client")
boto3.set_stream_logger("botocore.credentials", logging.CRITICAL)


class AWS_SQS(object):
    _default_region = "us-west-2"

    def __init__(self, sqs_resource, sqs_client):
        self.sqs_resource = sqs_resource
        self.sqs_client = sqs_client
        self._queue_urls = {}
        self.default_visibility = 720
        self.logger = Logging.get_logger("propus/sqs")

    @staticmethod
    def build(region: AnyStr = None, additional_params: Dict = {}):
        if region is None:
            region = AWS_SQS._default_region
        sqs_resource = boto3.resource("sqs", region_name=region, **additional_params)
        sqs_client = boto3.client("sqs", region_name=region, **additional_params)
        return AWS_SQS(sqs_resource, sqs_client)

    def __get_queue_url(self, q_name: AnyStr) -> AnyStr:
        """
        Private function to retrieve the queue url. If it is stored in the class object then it is returned,
        otherwise it is returned from AWS and stored in the class object.

        Args:
            q_name (AnyStr): Queue Name as a string

        :return: Returns the URL of an existing Amazon SQS queue.
        """
        if not self._queue_urls.get(q_name):
            queue = self.sqs_resource.get_queue_by_name(QueueName=q_name)
            self._queue_urls[q_name] = queue.url
        return self._queue_urls.get(q_name)

    def receive_messages(
        self, queue_name: AnyStr, num_messages: int = 10, visibility: int = 720, **receive_msg_args
    ) -> List[Dict]:
        """
        Using the boto3 library this function retrieves a specific queue url and then retrieves a given number
        of messages. Boto3 receive messages limits the maximum number of messages to 10.

        Args:
            queue_name (AnyStr): Queue Name as a string
            num_messages (Int): Number of messages to retrieve from the queue
                - default = 10
            visibility (Int): Visibility timeout
                - default = 720 seconds

        :return: List of message dictionaries
        """
        if not visibility:
            visibility = self.default_visibility
        queue_url = self.__get_queue_url(queue_name)
        messages = self.sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=num_messages,
            VisibilityTimeout=visibility,
            **receive_msg_args,
        )
        return messages

    @backoff.on_exception(backoff.expo, exception=(ClientError, ParamValidationError), max_tries=5)
    def send_message(self, queue_name: AnyStr, message: AnyStr, message_attributes: Dict = {}, **kwargs) -> AnyStr:
        """
        Sends a message to a specific queue.

        Args:
            queue_name (AnyStr): The name of the queue to enqueue
            message (AnyStr): The message that you want enqueued
            message_attributes (Dict): Additional message_attributes if necessary

        :return <String> response: Message ID response after enqueueing
        """
        kwargs |= {"QueueUrl": self.__get_queue_url(queue_name), "MessageBody": message}
        if len(message_attributes) > 0:
            kwargs["MessageAttributes"] = message_attributes
        response = self.sqs_client.send_message(**kwargs)
        return response.get("MessageId")

    @backoff.on_exception(backoff.expo, exception=(ClientError, ParamValidationError), max_tries=5)
    def delete_message(self, queue_name: AnyStr, receipt_handle: AnyStr):
        """
        Sends a message to a specific queue.

        Args:
            queue_name (AnyStr): The name of the queue from where to delete the message
            receipt_handle (AnyStr): The handle to be deleted

        :return None
        """
        return self.sqs_client.delete_message(QueueUrl=self.__get_queue_url(queue_name), ReceiptHandle=receipt_handle)
