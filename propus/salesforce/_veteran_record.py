import json


def fetch_contact_vet_record_by_ccc_id(self, ccc_id):
    return self.custom_query(
        f"""Select Id, firstname, lastname, (Select Id From Veteran_Service_Records__r)
    from Contact WHERE cfg_CCC_ID__c ='{ccc_id}'"""
    )


def fetch_vet_record_by_contact_data(self, ccc_id=None, email=None):
    where_query = ""
    if ccc_id is not None:
        where_query += f"Related_Student__r.cfg_CCC_ID__c = '{ccc_id}'"
    if email is not None:
        if len(where_query) > 0:
            where_query += " AND "
        where_query += f"Related_Student__r.cfg_Calbright_Email__c = '{email}'"
    return self.custom_query(
        f"""SELECT Id, Related_Student__r.Id, Intake_Form_Sent_Date__c,
    Intake_Form_Submitted_Date__c, Branch_of_Service__c, Do_You_Have_Any_Disabilities__c,
    Community_Support_Services_Interested_In__c, Status__c FROM Veteran_Service_Record__c
    WHERE {where_query}"""
    )


def fetch_vet_record_by_sf_id(self, salesforce_id):
    return self.custom_query(
        f"""SELECT Id, Intake_Form_Sent_Date__c, Intake_Form_Submitted_Date__c,
    Branch_of_Service__c, Do_You_Have_Any_Disabilities__c, Community_Support_Services_Interested_In__c, Status__c FROM
    Veteran_Service_Record__c WHERE Related_Student__c = '{salesforce_id}'"""
    )


@staticmethod
def _fetch_veteran_data(args):
    payload = {}

    kwarg_dict = {
        "intake_form_sent": "Intake_Form_Sent_Date__c",
        "intake_form_submitted": "Intake_Form_Submitted_Date__c",
        "status": "Status__c",
        "other_status": "Other_Status__c",
        "disabilities": "Do_You_Have_Any_Disabilities__c",
        "branch_of_service": "Branch_of_Service__c",
        "other_branch_of_service": "Other_Branch_of_Service__c",
        "student_supports": "Calbright_Student_Supports_Interested_In__c",
        "community_support": "Community_Support_Services_Interested_In__c",
        "program_of_study": "Intake_stated_Program_of_Study__c",
        "other_program_of_study": "Intake_stated_program_Other__c",
    }
    for key, val in kwarg_dict.items():
        if args.get(key):
            if key in ["branch_of_service", "student_supports", "community_support"]:
                payload[val] = ";".join(args.get(key))
                continue
            payload[val] = args.get(key)
    return payload


def create_vet_record(self, salesforce_id, **kwargs):
    data = self._fetch_veteran_data(kwargs)
    data["Related_Student__c"] = salesforce_id
    url = self._get_endpoint("create_vet_record")
    return self.make_request(url, data=json.dumps(data), req_type="post")


def update_vet_record(self, vet_record_id, **kwargs):
    url = self._get_endpoint("update_vet_record", {"<vet_id>": vet_record_id})
    self.make_request(url, data=json.dumps(self._fetch_veteran_data(kwargs)), req_type="patch")


def delete_vet_record(self, vet_record_id):
    url = self._get_endpoint("delete_vet_record", {"<vet_id>": vet_record_id})
    self.make_request(url, req_type="delete")
