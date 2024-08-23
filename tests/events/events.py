import json
import unittest
from unittest.mock import MagicMock, Mock

from propus.events.events import Events
from propus.events.exceptions import InvalidEventType, MissingRequiredData


class TestEventSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.env = "OurSQSQueue"
        sqs_client = MagicMock()
        sqs_client.send_message = Mock(side_effect=self.send_msg)
        self.event_system = Events(sqs_client, self.env)

        self.test_email = "you@calbright.org"
        self.test_date = "NOW!"

    def test_send_event(self):
        self.assertTrue(self.event_system.events_queue.endswith(self.env))
        self.assertEqual(
            self.event_system.events,
            {
                "csep_completed": {"required": ["calbright_email", "date_completed"]},
                "veteran_intake_compeleted": {},
            },
        )

        self.event_system.send_event(
            event_type="csep_completed",
            calbright_email=self.test_email,
            date_completed=self.test_date,
        )

    def send_msg(self, queue_name, message):
        self.assertTrue(queue_name.endswith(self.env))
        j_data = json.loads(message)
        self.assertEqual(j_data.get("calbright_email"), self.test_email)
        self.assertEqual(j_data.get("date_completed"), self.test_date)
        self.assertTrue(j_data.get("event_type") == "csep_completed")

    def test_errors(self):
        with self.assertRaises(InvalidEventType):
            self.event_system.send_event("event_type")

        with self.assertRaises(MissingRequiredData):
            self.event_system.send_event("csep_completed")


if __name__ == "__main__":
    unittest.main()
