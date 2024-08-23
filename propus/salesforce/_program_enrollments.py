import json


@staticmethod
def _fetch_program_enrollment_data(args):
    kwarg_dict = {
        "enrollment_status": "Enrollment_Status__c",
        "program_name": "Program_Name__c",
        "date_of_enrollment": "Date_of_Enrollment__c",
        "contact": "Contact__c",
        "program_version": "Program_Version__c",
    }
    return {val: args.get(key) for key, val in kwarg_dict.items() if args.get(key)}


def create_program_enrollment_record(self, **kwargs):
    data = self._fetch_program_enrollment_data(kwargs)
    url = self._get_endpoint("create_program_enrollment_record")
    return self.make_request(url, data=json.dumps(data), req_type="post")


def delete_program_enrollment_record(self, enrollment_id):
    url = self._get_endpoint("delete_program_enrollment_record", {"<enrollment_id>": enrollment_id})
    self.make_request(url, req_type="delete")


def update_program_enrollment_record(self, enrollment_id, **kwargs):
    url = self._get_endpoint("update_program_enrollment_record", {"<enrollment_id>": enrollment_id})
    self.make_request(url, data=json.dumps(kwargs), req_type="patch")
