from propus.helpers.sql_alchemy import create_field_map


# Map out string values to object ID for ingestion
def create_contact_method_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.preferred_contact_method import PreferredContactMethod

    contact_method_map = create_field_map(session, PreferredContactMethod, map_from="preferred_contact_method")
    return contact_method_map


def create_contact_method_map_sf(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.helpers.salesforce import SF_CONTACT_METHOD_MAP

    contact_method_map = {}
    _contact_method_map = create_contact_method_map(session)
    for k, v in SF_CONTACT_METHOD_MAP.items():
        contact_method_map[k] = _contact_method_map[v]
    return contact_method_map


def create_contact_time_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.preferred_contact_time import PreferredContactTime

    contact_time_map = create_field_map(session, PreferredContactTime, map_from="preferred_contact_time")
    return contact_time_map


def create_ethnicity_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.ethnicity import Ethnicity

    ethnicity_map = create_field_map(session, Ethnicity, map_from="ethnicity")
    return ethnicity_map


def create_ethnicity_map_sf(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.helpers.salesforce import SF_ETHNICITY_MAP

    _ethnicity_map = create_ethnicity_map(session)
    ethnicity_map = {}
    for k, v in SF_ETHNICITY_MAP.items():
        ethnicity_map[k] = _ethnicity_map[v]
    ethnicity_map["N"] = None
    ethnicity_map[0] = None
    return ethnicity_map


def create_gender_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.gender import Gender

    gender_map = create_field_map(session, Gender, map_from="gender")
    gender_map[None] = gender_map.get("No selection")
    return gender_map


def create_lead_source_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.lead_source import LeadSource

    return create_field_map(session, LeadSource, map_from="lead_source")


def create_learner_status_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.learner_status import LearnerStatus

    learner_status_map = create_field_map(session, LearnerStatus, map_from="status")
    return learner_status_map


def create_program_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.program import Program

    return create_field_map(session, Program, map_from="short_name")


def create_program_map_sf(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.helpers.salesforce import SF_PROGRAMS_OF_INTEREST_MAP

    _program_map = create_program_map(session)
    return {k: _program_map.get(v, None) for k, v in SF_PROGRAMS_OF_INTEREST_MAP.items()}


def create_pronoun_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.pronoun import Pronoun

    pronoun_map = create_field_map(session, Pronoun, map_from="pronoun")
    return pronoun_map


def create_pronoun_map_sf(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.helpers.salesforce import SF_PRONOUN_MAP

    pronoun_map = {}
    _pronoun_map = create_pronoun_map(session)
    for k, v in SF_PRONOUN_MAP.items():
        pronoun_map[k] = _pronoun_map[v]
    return pronoun_map


def create_salutation_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.salutation import Salutation

    salutation_map = create_field_map(session, Salutation, map_from="salutation")
    return salutation_map


def create_suffix_map(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.calbright_sql.suffix import Suffix

    suffix_map = create_field_map(session, Suffix, map_from="suffix")
    return suffix_map


def create_suffix_map_sf(session):
    """Creates mapping of strings to ID fields.

    Arguments:
        session: SQL Alchemy Session

    Returns:
        map_dict: Dictionary of keys (typically `name` or the name of the model)
            mapped to ID fields of the model.
    """
    from propus.helpers.salesforce import SF_SUFFIX_MAP

    suffix_map = {}
    _suffix_map = create_suffix_map(session)
    for k, v in SF_SUFFIX_MAP.items():
        suffix_map[k] = _suffix_map[v]
    return suffix_map


def extract_data_based_on_mapping(data, dict_to_column_mapping):
    """
    Extracts data from the incoming dictionary based on the provided mapping.

    Args:
        data (dict): Incoming data as dictionary
        dict_to_column_mapping (dict): Mapping of dictionary keys to
                                             database column names

    Returns:
        dict: A dictionary containing extracted data dictionaries, with section
              names as keys

    Example use:
    from propus.helpers.field_maps import extract_data_based_on_mapping

    data = {
        "FirstName": "John",
        "LastName": "Doe",
        "Email": "john.doe@example.com",
        "Phone": "1234567890",
        "Address": {
            "City": "New York",
            "ZipCode": "10001"
        }
    }
    dict_to_column_mapping = {
        "student": {
            "Email": "personal_email",
            "Phone": "phone_number"
        },
        "name": {
            "FirstName": "first_name",
            "LastName": "last_name"
        },
        "location": {
            "Address.City": "city",
            "Address.ZipCode": "zip_code"
        }
    }

    result = extract_data_based_on_mapping(
            self.data,
            self.dict_to_column_mapping
        )

    In above example:
    result = {
        "student": {
            "personal_email": "john.doe@example.com",
            "phone_number": "1234567890"
        },
        "name": {
            "first_name": "John",
            "last_name": "Doe"
        },
        "location": {
            "city": "New York",
            "zip_code": "10001"
        }
    }
    """
    data_mapping = {}
    for section, mapping in dict_to_column_mapping.items():
        data_mapping.setdefault(section, {})
        for key, column_name in mapping.items():
            current_data = data
            for sub_key in key.split("."):
                current_data = current_data.get(sub_key)
                if current_data is None:
                    break
            if current_data is not None:
                data_mapping[section][column_name] = current_data
    return data_mapping
