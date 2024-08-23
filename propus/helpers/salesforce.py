from propus.logging_utility import Logging
from propus.helpers.etl import clean_phone, clean_ssn
from propus.helpers.field_maps import (
    create_contact_method_map_sf,
    create_contact_time_map,
    create_ethnicity_map_sf,
    create_gender_map,
    create_learner_status_map,
    create_pronoun_map_sf,
    create_salutation_map,
    create_suffix_map_sf,
    create_program_map_sf,
)
from propus.helpers.exceptions import InvalidDataAttribute

logger = Logging.get_logger("propus/helpers/salesforce")

# Address fields in student contact record
SF_ADDRESS_FIELDS = [
    "MailingAddress",
    "OtherAddress",
    "Device_Shipping_Address__c",
    "hed__Current_Address__c",
]

SF_ADDRESS_FIELD_MAP = {
    "street": "address1",
    "city": "city",
    "state": "state",
    "postalCode": "zip",
}

SF_CURRENT_ADDRESS_FIELD_MAP = {
    "hed__MailingStreet__c": "address1",
    "hed__MailingStreet2__c": "address2",
    "hed__MailingCity__c": "city",
    "hed__MailingState__c": "state",
    "hed__MailingPostalCode__c": "zip",
}

SF_USER_MAP = {
    "Id": "salesforce_id",
    "FirstName": "first_name",
    "MiddleName": "middle_name",
    "LastName": "last_name",
    "Email": "personal_email",
    "Phone": "phone_number",
    "cfg_Calbright_Email__c": "calbright_email",
    "hed__Former_Last_Name__c": "maiden_name",
    "Chosen_First_Name__c": "preferred_first_name",
    "Chosen_Last_Name__c": "preferred_last_name",
}

# Foreign key relationships between Postgres / SF.
# I.e., the field values are the same between databases,
# but in Postgres the Student record stores a foreign key
# to another table that contains the value.
SF_USER_FK_MAP = {
    "Salutation": (create_salutation_map, "salutation_id"),
    "Suffix": (create_suffix_map_sf, "suffix_id"),
    "Preferred_Pronouns__c": (create_pronoun_map_sf, "pronoun_id"),
    "cfg_Learner_Status__c": (create_learner_status_map, "learner_status_id"),
    "hed__Gender__c": (create_gender_map, "gender_id"),
}

SF_STUDENT_MAP = {
    "cfg_CCC_ID__c": "ccc_id",
    "hed__Social_Security_Number__c": "ssn",
    "HomePhone": "home_phone_number",
    "MobilePhone": "mobile_number",
    "IP_Lookup_Link__c": "ip_address",
}

SF_CONTACT_METHOD_MAP = {
    "Text Message": "Text Method",
    "Phone Call": "Phone call",
    "Email": "Email",
}

SF_ENROLLMENT_MAP = {"Assigned_Academic_Counselor_Email__c": "counselor_email"}

SF_ETHNICITY_MAP = {
    "AA": "Black or African American",
    "ACA": "Asian Cambodian",
    "ACH": "Asian Chinese",
    "AFI": "Asian Filipino",
    "AI": "Asian Indian",
    "AIN": "American Indian / Alaskan Native",
    "AJA": "Asian Japanese",
    "AKO": "Asian Korean",
    "ALA": "Asian Laotian",
    "AOTH": "Asian Other",
    "AVI": "Asian Vietnamese",
    "CAM": "Central American",
    "H": "Hispanic, Latino",
    "HOTH": "Hispanic Other",
    "MMAC": "Mexican, Mexican-American, Chicano",
    "PIGU": "Pacific Islander Guamanian",
    "PIHI": "Pacific Islander Hawaiian",
    "PIOTH": "Pacific Islander Other",
    "PISA": "Pacific Islander Samoan",
    "SAM": "South American",
    "W": "White",
}

SF_EXPRESS_INTEREST_MAP = {
    "Pre_Application_Browser_Type__c": "browser_type",
    "cfg_Landing_Page_URL__c": "landing_page",
    "cfg_UTM_Medium__c": "utm_medium",
    "cfg_UTM_Term__c": "utm_term",
    "cfg_UTM_Source__c": "utm_source",
    "cfg_UTM_Content__c": "utm_content",
    "cfg_UTM_Campaign__c": "utm_campaign",
    "cfg_Referrer_URL__c": "referrer_url",
    "LeadSource": "lead_source_picklist",
}

SF_PROGRAMS_OF_INTEREST_MAP = {
    "Data Analysis": "Data Analysis",
    "IT Support": "IT Support",
    "T2T CRM Admin": "Customer Relationship Management",
    "Cybersecurity": "Cybersecurity",
    "HC DEI": "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion",  # noqa: E501
    "Medical Coding": "Medical Coding",
    "Career Readiness": "",  # Might not get released as individual program and may need to adjust
    "T2T Intro to Networks": "T2T Intro to Networks",
    "Project Management": "Project Management",
    "Other": "",  # Undetermined and result of previous architecture
}

SF_LEARNER_STATUS_MAP = {
    # Current_Learner_Status_Number__c: cfg_Current_Learner_Status__c
    -2.0: "Suspended by IT (pre-enrollment)",
    0.0: "Dropped",
    1.0: "Expressed Interest",
    2.0: "App Started",
    3.0: "App Submitted",
    4.0: "Started Orientation",
    5.0: "Completed Orientation",
    6.0: "Completed Ed Plan",
    6.5: "Completed CSEP",
    7.0: "Enrolled in Essentials",
    8.0: "Completed Essentials",
    9.0: "Met w/Program Director",
    10.0: "Enrolled in Program Pathway",
    11.0: "Started Program Pathway",
    12.0: "Completed Program Pathway",
    13.0: "Completed Industry Certification",
    14.0: "Paid Apprenticeship",
    15.0: "Full-Time Employment",
}

SF_PRONOUN_MAP = {
    "He/him/his": "He/Him/His",
    "She/her/hers": "She/Her/Hers",
    "They/them/theirs": "They/Them/Theirs",
}

SF_SUFFIX_MAP = {
    "II": "II",
    "III": "III",
    "IV": "IV",
    "Jr": "Jr.",
    "Jr.": "Jr.",
    "Sr.": "Sr.",
}

SF_API_NAME_TO_CALBRIGHT_SHORT_NAME = {
    "T2T CRM Admin": "Customer Relationship Management",
    "HC DEI": "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion",
}


def create_express_interest_per_program_of_interest(session, express_interest_args, programs_of_interest_list):
    """Create new expressed interest record per program of interest received

    Args:
        session: Sql Alchemy database session
        express_interest_args (Dict): Dictionary of arguments that will be applied to express interest records
        programs_of_interest_list (List): List of programs that will create an express interest record for each program
    """
    from propus.calbright_sql.expressed_interest import ExpressInterest

    if express_interest_args is None:
        raise TypeError("Error: Express Interest Args are 'None'")

    programs_of_interest_map = create_program_map_sf(session)
    for program_of_interest in programs_of_interest_list:
        if program_of_interest not in programs_of_interest_map:
            logger.warning(f"Error: program {program_of_interest} not found / mapped.")
            continue
        else:
            program_of_interest_id = programs_of_interest_map[program_of_interest]
            express_interest_args["program_interest_id"] = program_of_interest_id
            session.add(ExpressInterest(**express_interest_args))


def create_student_addresses(session, student, addresses_dict, geolocator=None, salesforce=None):
    from propus.calbright_sql.address import Address
    from propus.calbright_sql.student_address import StudentAddress

    if not geolocator or not salesforce:
        from propus.aws.ssm import SSM

        ssm = SSM.build()

    current_address = addresses = mailing_address = device_shipping_address = other_address = {}

    # Set the current address if provided from the extract file, or
    # fetch from Salesforce if provided in the addresses_dict
    if "address" in addresses_dict:
        current_address = addresses_dict.pop("address")
        addresses["Current"] = current_address
    elif "hed__Current_Address__c" in addresses_dict:
        if not salesforce:
            from propus.salesforce import Salesforce

            salesforce = Salesforce.build(**ssm.get_param(parameter_name="salesforce.propus.stage", param_type="json"))
        sf_table = "hed__Address__c"
        sf_fields = ", ".join([k for k, v in SF_CURRENT_ADDRESS_FIELD_MAP.items()])

        address_id = addresses_dict.pop("hed__Current_Address__c")
        custom_qry = f"SELECT {sf_fields} FROM {sf_table} where id = '{address_id}'"
        current_result = salesforce.custom_query(custom_qry)
        if current_result["totalSize"] == 1:
            _current_address = current_result["records"][0]
            _ = _current_address.pop("attributes")
            current_address = {
                SF_CURRENT_ADDRESS_FIELD_MAP[k]: v
                for k, v in _current_address.items()
                if k in SF_CURRENT_ADDRESS_FIELD_MAP and v not in [None, ""]
            }
        current_address["country"] = "US"
        addresses["Current"] = current_address

    _mailing_address = addresses_dict.pop("MailingAddress") if addresses_dict.get("MailingAddress") else {}
    _device_shipping_address = (
        addresses_dict.pop("Device_Shipping_Address__c") if addresses_dict.get("Device_Shipping_Address__c") else ""
    )
    _other_address = addresses_dict.pop("OtherAddress") if addresses_dict.get("OtherAddress") else {}

    if _mailing_address:
        mailing_address = {
            SF_ADDRESS_FIELD_MAP[k]: v
            for k, v in _mailing_address.items()
            if k in SF_ADDRESS_FIELD_MAP and v not in [None, ""]
        }
        mailing_address["country"] = "US"
        is_new = current_address != mailing_address
        if is_new:
            addresses["Mailing"] = mailing_address
    if _device_shipping_address:
        if not geolocator:
            from propus.geolocator import Geolocator

            geolocator = Geolocator.build(config=ssm.get_param("google_maps.propus.stage", "json"))

        device_shipping_address = geolocator.get(_device_shipping_address)
        device_shipping_address["country"] = "US"
        is_new = (device_shipping_address != current_address) and (device_shipping_address != mailing_address)
        if is_new:
            addresses["Device Shipping"] = device_shipping_address
    if _other_address:
        other_address = {
            SF_ADDRESS_FIELD_MAP[k]: v
            for k, v in _other_address.items()
            if k in SF_ADDRESS_FIELD_MAP and v not in [None, ""]
        }
        other_address["country"] = "US"
        is_new = (
            (other_address != current_address)
            and (other_address != mailing_address)  # noqa: W503
            and (other_address != device_shipping_address)  # noqa: W503
        )
        if is_new:
            addresses["Other"] = other_address

    for address_type, address in addresses.items():
        try:
            is_current = True if address_type == "Current" else False
            # Device shipping addresses are said to have been validated prior to shipment
            is_valid = True if address == device_shipping_address else False
            if (
                not address.get("address1")
                or not address.get("city")  # noqa: W503
                or not address.get("state")  # noqa: W503
                or not address.get("zip")  # noqa: W503
                or not address.get("country")  # noqa: W503
            ):
                logger.info(f"{student}: Skipping {address_type} address because it is incomplete ({address})")
                continue
            new_address = Address(**address)
            session.add(new_address)
            new_student_address = StudentAddress(
                student=student,
                address=new_address,
                current=is_current,
                valid=is_valid,
                address_type=address_type,
            )
            session.add(new_student_address)
        except Exception as e:
            logger.error(e)


def create_student_contact_method(session, student, contact_method_str):
    from propus.calbright_sql.student_contact_method import StudentContactMethod

    contact_method_map = create_contact_method_map_sf(session)
    contact_methods = contact_method_str.split(";")
    for contact_method in contact_methods:
        contact_method_id = contact_method_map[contact_method]
        student_contact_method_args = {
            "contact_method_id": contact_method_id,
            "ccc_id": student.ccc_id,
        }
        new_student_contact_method = StudentContactMethod(**student_contact_method_args)
        session.add(new_student_contact_method)


def create_student_contact_time(session, student, contact_time_str):
    from propus.calbright_sql.student_contact_time import StudentContactTime

    contact_time_map = create_contact_time_map(session)
    contact_times = contact_time_str.split(";")
    for contact_time in contact_times:
        contact_time_id = contact_time_map[contact_time]
        student_contact_time_args = {
            "contact_time_id": contact_time_id,
            "ccc_id": student.ccc_id,
        }
        new_student_contact_time = StudentContactTime(**student_contact_time_args)
        session.add(new_student_contact_time)


def create_student_ethnicity(session, student, ethnicity_list):
    from propus.calbright_sql.student_ethnicity import StudentEthnicity

    ethnicity_map = create_ethnicity_map_sf(session)
    for ethnicity in ethnicity_list:
        if ethnicity not in ethnicity_map:
            logger.warning(f"Error: ethnicity {ethnicity} not found / mapped.")
            continue
        else:
            ethnicity_id = ethnicity_map[ethnicity]
        # `N` (no ethnicity) is a possible ethnicity code that should be skipped if encountered
        if ethnicity_id:
            student_ethnicity_args = {
                "student_id": student.ccc_id,
                "ethnicity_id": ethnicity_id,
            }
            new_student_ethnicity = StudentEthnicity(**student_ethnicity_args)
            session.add(new_student_ethnicity)


def validate_data_attribute_type(data, attribute_type):
    """
    Validates the attribute type of incoming data.
    Every Salesforce object contains a `type` field that contains the attribute of the object. This helps to validate
    that attribute type is correct for the given object.

    Args:
        data (dict): Incoming data
        attribute_type (str): Name of the attribute

    Raises:
        InvalidAPIUsage: If the attribute type is missing or invalid
    """
    try:
        if data["type"] != attribute_type:
            raise InvalidDataAttribute(attribute_type)
    except KeyError:
        raise InvalidDataAttribute(attribute_type, True)


# Functions to clean SalesForce data prior to saving.
# E.g., remove unwanted characters, etc.
SF_CLEAN_FIELD_FUNCTIONS = {
    "phone_number": clean_phone,
    "mobile_number": clean_phone,
    "other_number": clean_phone,
    "ssn": clean_ssn,
}

# Intermediary foreign key relationships, e.g., there is a StudentContactMethod object
# between Student and PreferredContactMethod objects.
SF_FK_INTERMEDIARY_MAP = {
    "Preferred_Contact_Method__c": create_student_contact_method,
    "Preferred_Contact_Time__c": create_student_contact_time,
}

# # Foreign key relationships between Postgres / SF for Express Interest.
SF_FK_EXPRESS_INTEREST_MAP = {
    "cfg_Learner_Status__c": (create_learner_status_map, "learner_status_id"),
}


# Mapping is part of creating multiple Express Interest records
SF_FK_EXPRESS_INTEREST_MULTI_MAP = {
    "cfg_Programs_of_Interest__c": (create_program_map_sf, "program_interest_id"),
}
