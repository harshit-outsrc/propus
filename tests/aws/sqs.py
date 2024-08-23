import boto3
from botocore.exceptions import ClientError
from moto import mock_sqs
import unittest

from propus.aws.sqs import AWS_SQS


class TestSQS(unittest.TestCase):
    mock_sqs = mock_sqs()

    def setUp(self):
        self.mock_sqs.start()
        self.sqs_client = boto3.client("sqs", "us-west-2")
        self.sqs_resource = boto3.resource("sqs", "us-west-2")
        self.queue_url = self.sqs_client.create_queue(QueueName="mock_test")["QueueUrl"]
        self.q_name = "mock_test"
        self.sqs_module = AWS_SQS(self.sqs_resource, self.sqs_client)

    def tearDown(self):
        self.mock_sqs.stop()

    def test_sqs_send_receive(self):
        msg = "THIS IS A TEST MSG"
        message_id = self.sqs_module.send_message(self.q_name, msg)
        self.assertTrue(type(message_id) == str)
        resp = self.sqs_module.receive_messages(self.q_name, num_messages=1)
        self.assertEqual(len(resp.get("Messages")), 1)
        self.assertEqual(resp.get("Messages")[0].get("MessageId"), message_id)
        self.assertEqual(resp.get("Messages")[0].get("Body"), msg)

    def test_sqs_receive_args(self):
        """assert our SQS.receive_messages method will forward any additional kwargs to boto3's receive_message"""
        with unittest.mock.patch.object(self.sqs_module.sqs_client, "receive_message") as mock_receive_msg:
            self.sqs_module.receive_messages(self.q_name, WaitTimeSeconds=20)
            _, args, kwargs = mock_receive_msg.mock_calls[0]
            self.assertTrue(kwargs.get("WaitTimeSeconds"), 20)

    def test_failed_send(self):
        try:
            error_caught = False
            _ = self.sqs_module.send_message("failed", "failed")
        except ClientError as err:
            error_caught = "NonExistentQueue" in str(err)
            pass
        self.assertTrue(error_caught)

    def test_sqs_delete_message(self):
        msg = "THIS IS A TEST MSG"
        message_id = self.sqs_module.send_message(self.q_name, msg)
        self.assertTrue(type(message_id) == str)
        resp = self.sqs_module.receive_messages(self.q_name, num_messages=1)
        receipt_handle = resp.get("Messages")[0].get("ReceiptHandle")
        self.assertEqual(len(resp.get("Messages")), 1)
        self.sqs_module.delete_message(self.q_name, receipt_handle=receipt_handle)
        resp = self.sqs_module.receive_messages(self.q_name, num_messages=1)
        self.assertEqual(resp.get("Messages"), None)


if __name__ == "__main__":
    unittest.main()
