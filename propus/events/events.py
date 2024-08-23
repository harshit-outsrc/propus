import json
from propus.aws.sqs import AWS_SQS
from propus.events.exceptions import InvalidEventType, MissingRequiredData
from propus.logging_utility import Logging


class Events:
    def __init__(self, sqs, env):
        self.sqs_client = sqs
        self.events = self.__build_event_library()
        self.events_queue = f"calbright_events_{env}"
        self.logger = Logging.get_logger("propus/events")

    @staticmethod
    def build(env="dev"):
        return Events(AWS_SQS.build(), env)

    def __build_event_library(self):
        return {
            "csep_completed": {"required": ["calbright_email", "date_completed"]},
            "veteran_intake_compeleted": {},
        }

    def send_event(self, event_type, **kwargs):
        event_data = self.events.get(event_type)
        if not event_data:
            raise InvalidEventType(event_type)

        for required_field in event_data.get("required"):
            if not kwargs.get(required_field):
                raise MissingRequiredData(event_type, event_data.get("required"))
        kwargs["event_type"] = event_type
        msg = json.dumps(kwargs)
        self.logger.info(f"sending message to {self.events_queue}: {msg}")
        self.sqs_client.send_message(queue_name=self.events_queue, message=msg)
