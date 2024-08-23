import json
from typing import AnyStr

from propus.salesforce.exceptions import CreateCaseMissingFields, CreateCaseUnknownRecordType


def fetch_case_details_record_by_case_number(self, case_number):
    return self.custom_query(
        f"""SELECT Subject, Description, Status, Priority, CaseNumber, ContactId,
    CreatedDate, ClosedDate, LastModifiedById, AssetId, Reason, Case_Resolved_Date__c
    FROM Case WHERE CaseNumber = '{case_number}'"""
    )


def fetch_case_record_by_sf_id(self, salesforce_id):
    url = self._get_endpoint("case_by_sfid", {"<sfid>": salesforce_id})
    return self.make_request(url)


def update_case_record(self, salesforce_id: AnyStr, **kwargs):
    url = self._get_endpoint("update_case", {"<sfid>": salesforce_id})
    self.make_request(url, data=json.dumps(kwargs), req_type="patch")


def create_case_record(self, record_type: AnyStr, **kwargs) -> dict:
    """
    Method used to create a case record in Salesforce

    Returns:
        Dict: response from Salesforce including the new case Id
    """

    record_type_map = {
        "Academic Success Counselor Case": "0123k0000014TpNAAU",
        "Academic Support Services Case": "0125G000000uJHkQAM",
        "Accessibility Case": "0123k0000014TpSAAU",
        "Admissions Case": "0123k000000XUaXAAW",
        "Career Services Case": "0125G000000bJpqQAE",
        "Instruction Team Case": "0123k0000014TpXAAU",
        "IT Security": "0123k0000014SeIAAU",
        "End User Support": "0123k000001MT3RAAW",
        "Proactive Outreach": "0125G000000uJZfQAM",
        "Welcome Services Case": "0123k000001YdiuAAC",
    }
    record_type_id = record_type_map.get(record_type)
    if not record_type_id:
        raise CreateCaseUnknownRecordType(record_type)

    # Validate required fields
    required_fields = ["issue__c", "Issue_Description__c", "Preventing_Student_Access__c"] + (
        ["Issue_Title__c"] if kwargs.get("issue__c") == "Other" else []
    )
    for field in required_fields:
        if not kwargs.get(field):
            raise CreateCaseMissingFields(field, record_type)

    url = self._get_endpoint("create_case")
    kwargs["RecordTypeId"] = record_type_id
    return self.make_request(url, data=json.dumps(kwargs), req_type="post")
