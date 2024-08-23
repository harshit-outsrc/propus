from datetime import datetime
import json
from typing import AnyStr


def create_event(self, salesforce_id: AnyStr, start_time: datetime, duration: int, **kwargs):
    data = {
        "WhoId": salesforce_id,
        "DurationInMinutes": duration,
        "StartDateTime": start_time,
    }

    kwarg_dict = {
        "subject": "Subject",
        "description": "Description",
        "assignee_id": "OwnerId",
        "type": "Type",
    }
    for key, val in kwarg_dict.items():
        if kwargs.get(key):
            data[val] = kwargs.get(key)

    url = self._get_endpoint("create_event")
    return self.make_request(url, data=json.dumps(data), req_type="post")
