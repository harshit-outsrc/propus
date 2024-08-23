import json
from typing import AnyStr

from propus.salesforce.exceptions import CreateContactMissingFields, CreateContactUnknownRecordType


def fetch_contact_details_record_by_ccc_id(self, ccc_id):
    return self.custom_query(
        f"""select cfg_Full_Name__c,Preferred_Contact_Method__c,
    Preferred_Pronouns__c,hed__PreferredPhone__c,
    Email,cfg_Programs_of_Interest__c,cfg_Calbright_Email__c,IT_Suspension_Reason__c,
    MobilePhone,
    HomePhone,Application_Hold_Reason__c,Phone,Enrollment_Status__c,
    Applicant_verified_by_phone__c,Who_Verified_Applicant_by_Phone__c
    from Contact WHERE cfg_CCC_ID__c ='{ccc_id}'"""
    )


def fetch_contact_accessibility_record_by_ccc_id(self, ccc_id):
    return self.custom_query(
        f"""select Related_Student__c,
    Accessibility_1st_AEC_Appointment_Set__c,Accessibility_1st_AEC_Sent_Date__c,Accessibility_1st_AEC_Signed_Date__c,
    Accessibility_2nd_AEC_Appointment_Set__c,Accessibility_2nd_AEC_Sent_Date__c,Accessibility_2nd_AEC_Signed_Date__c,
    Accessibility_AAP_Sent_Date__c,Accessibility_AAP_Signed_Date__c,Accessibility_Accom_Distributed_Date__c,
    Accessibility_Documents_Verified__c,Accessibility_Intake_Appointment_Date__c,Accessibility_Intake_Form_Signed_Date__c,
    Accessibility_Intake_Form_Submitted_Date__c,Disability_Verification_Received_Date__c,Contact_Date__c,
    Service_Provided__c,Service_Explanation__c
    from Contact WHERE cfg_CCC_ID__c ='{ccc_id}'"""
    )


def fetch_contact_record_by_sf_id(self, salesforce_id):
    url = self._get_endpoint("contact_by_sfid", {"<sfid>": salesforce_id})
    return self.make_request(url)


def fetch_salesforce_id_by_ccc_id(self, ccc_id):
    return (
        self.custom_query(f"""select id from Contact WHERE cfg_CCC_ID__c ='{ccc_id}' LIMIT 1""")
        .get("records")[0]
        .get("Id")
    )


def get_sf_id_by_user(self, user):
    """get_sf_id_by_user takes a User object and returns the Salesforce ID.

    If the Salesforce ID has not been set then Salesforce is queried by ccc_id to retrieve the ID.

    * Note that this is designed to work with Student Users, although it will return the salesforce_id
    for Staff if set. However, if a staff member does not have a salesforce_id it will not be queried for.

    Args:
        user (propus.sql.calbright.user.User): User object with the salesforce_id set or to be fetched / set.

    Returns:
        sf_id (str): Salesforce ID of the User (student / staff)

    """
    try:
        if user.salesforce_id:
            return user.salesforce_id
    except Exception:
        pass

    try:
        ccc_id = user.ccc_id
        sf_id = self.fetch_salesforce_id_by_ccc_id(ccc_id)
        user.salesforce_id = sf_id
        user.save()
        self.logger.info(f"Fetched and saved Salesforce ID {sf_id} for {user}")
        return sf_id

    except Exception as e:
        self.logger.error(f"Unable to find or fetch Salesforce ID for {user}: {e}")
        return None


def update_contact_record(self, salesforce_id: AnyStr, **kwargs):
    url = self._get_endpoint("update_contact", {"<sfid>": salesforce_id})
    self.make_request(url, data=json.dumps(kwargs), req_type="patch")


def create_contact_record(self, record_type: AnyStr, **kwargs) -> dict:
    """
    Method used to create a contact record in Salesforce
    Args:
        record_type (AnyStr): type of record to be created. Options are learner, visitor, vendor, or employer

    Returns:
        Dict: response from salesforce including the new contact Id
    """
    record_type_map = {
        "learner": "0123k000001MQDqAAO",
        "visitor": "0123k0000014U2oAAE",
        "vendors": "0123k0000014TX9AAM",
        "employer": "0123k000001MQDvAAO",
    }
    record_type_id = record_type_map.get(record_type)
    if not record_type_id:
        raise CreateContactUnknownRecordType(record_type)
    if record_type == "learner":
        for field in ["Email", "FirstName", "LastName", "cfg_Learner_Status__c", "Phone"]:
            if not kwargs.get(field):
                raise CreateContactMissingFields(field)
    url = self._get_endpoint("create_contact")
    kwargs["RecordTypeId"] = record_type_id
    return self.make_request(url, data=json.dumps(kwargs), req_type="post")
