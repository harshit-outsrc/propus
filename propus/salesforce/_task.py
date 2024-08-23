import json
from typing import AnyStr


def create_task(self, salesforce_id: AnyStr, **kwargs):
    payload = {"WhoId": salesforce_id}

    kwarg_dict = {
        "activity_date": "ActivityDate",
        "description": "Description",
        "subject": "Subject",
        "owner_id": "OwnerId",
        "status": "Status",
        "type": "Type",
    }
    for key, val in kwarg_dict.items():
        if kwargs.get(key):
            payload[val] = kwargs.get(key)

    url = self._get_endpoint("create_task")
    return self.make_request(url, data=json.dumps(payload), req_type="post")
