import enum
from typing import Dict

from sqlalchemy import inspect, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from propus.helpers.input_validations import validate_uuid
from propus.helpers.exceptions import MappingError, InvalidKeyList


def _extract_model_params(defaults, **kwargs):
    defaults = defaults or {}
    ret = {}
    ret.update(kwargs)
    ret.update(defaults)
    return ret


def _create_object_from_params(session, model, lookup, params, lock=False):
    obj = model(**params)
    session.add(obj)
    try:
        with session.begin_nested():
            session.flush()
    except IntegrityError:
        session.rollback()
        query = session.execute(select(model).filter_by(**lookup)).scalars()
        if lock:
            query = query.with_for_update(key_share=True)
        try:
            obj = query.one()
        except NoResultFound:
            raise
        else:
            return obj, False
    else:
        return obj, True


def get_or_create(session, model, defaults: Dict = None, **kwargs) -> (Dict, bool):
    """
    This function can be used to create an object if it does not exist.
    Source https://github.com/enricobarzetti/sqlalchemy_get_or_create

    Args:
        session: SQLAlchemy Session Connection
        model: SQLAlchemy Model Object
        defaults (Dict): This should a dictionary of data to be upserted. Defaults to None for empty inserts
        kwargs: dictionary of items to attempt a match on (i.e. {"id": "1234", "ccc_id": "56784"})

    Returns:
        Dict: SQLAlchemy of the object that was Upserted
        Boolean: True if item was created, False if item was updated
    """
    try:
        return session.execute(select(model).filter_by(**kwargs)).scalars().one(), False
    except NoResultFound:
        params = _extract_model_params(defaults, **kwargs)
        return _create_object_from_params(session, model, kwargs, params)


def update_or_create(session, model, defaults: Dict = None, **kwargs) -> (Dict, bool):
    """
    This function can be used to do an upsert.
    Source https://github.com/enricobarzetti/sqlalchemy_get_or_create

    Args:
        session: SQLAlchemy Session Connection
        model: SQLAlchemy Model Object
        defaults (Dict): This should be a dictionary of data to be upserted. Defaults to None for empty inserts
        kwargs: dictionary of items to attempt a match on (i.e. {"id": "1234", "ccc_id": "56784"})

    Returns:
        Dict: SQLAlchemy of the object that was Upserted
        Boolean: True if item was created, False if item was updated
    """
    defaults = defaults or {}
    with session.begin_nested():
        try:
            obj = session.execute(select(model).with_for_update(key_share=True).filter_by(**kwargs)).scalars().one()
        except NoResultFound:
            params = _extract_model_params(defaults, **kwargs)
            obj, created = _create_object_from_params(session, model, kwargs, params, lock=True)
            if created:
                return obj, created
        for k, v in defaults.items():
            setattr(obj, k, v)
        session.add(obj)
        session.flush()
    return obj, False


def upsert_changes(session, model, object, defaults, **kwargs) -> (Dict, bool):
    """
    This function checks if values in the defaults dictionary are different from
    existing values in the object, and if so upserts the changes.

    Args:
        model: SQLAlchemy Model Object
        object: SQLAlchemy object instance to be checked / upserted
        defaults (Dict): This should a dictionary of data to be upserted.
        kwargs: dictionary of items to attempt a match on (i.e. {"id": "1234", "ccc_id": "56784"})

    Returns:
        Dict: Dictionary of values that have been upserted.
        Boolean: True if object was upserted, False if object has not been changed
    """
    original_data = object.__dict__
    upserted = False
    upserts = {k: v for k, v in defaults.items() if original_data.get(k) != v}

    if upserts:
        _, upserted = update_or_create(session, model, upserts, **kwargs)
        upserted = True

    return upserts, upserted


def build_query(table, fields, filters=None):
    """Builds a query string, e.g., SELECT fields FROM table WHERE FILTERS

    Arguments:
        table: Database table to query
        fields: Fields string or list to return
        filters (optional): String or list of WHERE filters

    Returns:
        qry_string: string of the SQL query to execute
    """
    if not table:
        raise ValueError("'table' is required")

    # Fields requested
    if fields:
        if isinstance(fields, str):
            field_list = fields.split(",")
        elif isinstance(fields, list):
            field_list = fields
        else:
            raise ValueError("'fields' argument should be a string or list")
    else:
        raise ValueError("'fields' argument is required")

    if filters:
        if isinstance(filters, str):
            where_filters = filters.split(",")
        elif isinstance(filters, list):
            where_filters = filters
        else:
            raise ValueError("'filters' argument should be a string or list")

    if not filters:
        qry = f"""SELECT {', '.join(field_list)} FROM {table}"""
    else:
        qry = f"""SELECT {', '.join(field_list)} FROM {table} WHERE {' and '.join(where_filters)}"""

    return qry


def create_field_map(session, model, map_from="name", map_to="id", key_list=None, one_to_many=False):
    """
    Create a mapping from one field to another in a one-to-many relationship.

    This function generates a mapping dictionary where keys correspond to values in the
    'map_from' field of the 'model', and values correspond to the corresponding values
    in the 'map_to' field. The mapping can be performed for a specific set of keys
    provided in 'key_list', or for all records if 'key_list' is not provided.

    Args:
        session (object): Database session object.
        model (class): SQLAlchemy model class.
        map_from (str, optional): Field to map from. Defaults to "name".
        map_to (str, optional): Field to map to. Defaults to "id".
        key_list (list, optional): List of keys to create mappings for. If None, mappings
                                  will be generated for all records in 'model'. Defaults to None.
        one_to_many (bool, optional): Flag indicating if the relationship is one-to-many.
                                     If True, the mapping result will include lists of values for each key.
                                     If False, the mapping result will include a single value for each key.
                                     Defaults to False.

    Returns:
        dict: A mapping dictionary with keys from 'map_from' and values from 'map_to'.
              If one_to_many is True, values are lists; otherwise, values are single items.

    Raises:
        Exception: If there is an error during the mapping process.

    Example Usage:
    from my_models import MyModel  # Assuming 'MyModel' is your SQLAlchemy model class

    # Assuming 'MyModel' has fields 'field1' and 'field2'
    key_list = ["value1", "value2", "value3"]

    # Case 1: one_to_many=False
    mapping_single = create_field_map(session, MyModel, "field1", "field2", key_list, one_to_many=False)
    # 'mapping_single' will be a dictionary with keys from 'field1' and single 'field2' values

    # Case 2: one_to_many=True
    mapping_multiple = create_field_map(session, MyModel, "field1", "field2", key_list, one_to_many=True)
    # 'mapping_multiple' will be a dictionary with keys from 'field1' and lists of 'field2' values
    """
    map_dict = {}
    query_pk = True
    validation_function = get_validation_function_by_model_field(session, model, map_from)
    if not key_list:
        for obj in session.execute(select(model)).scalars().all():
            obj_dict = obj.__dict__
            k = obj_dict.get(map_from, None)
            if one_to_many:
                if k not in map_dict:
                    map_dict[k] = []
                map_dict[k].append(obj_dict.get(map_to, None))
            else:
                map_dict[k] = obj_dict.get(map_to, None)

        return map_dict

    for key in key_list:
        if not validation_function or validation_function(key) is None:
            filters = {map_from: key}
            if query_pk:
                try:
                    instance = session.execute(select(model).filter_by(**filters).limit(1)).scalars().first()
                except Exception:
                    query_pk = False

            if not query_pk:
                try:
                    if one_to_many:
                        instance = session.execute(select(model).filter_by(**filters)).scalars().all()
                    else:
                        instance = session.execute(select(model).filter_by(**filters).limit(1)).scalars().first()
                except Exception:
                    instance = {map_to: None}

            if isinstance(instance, model):
                map_dict[key] = instance.__dict__.get(map_to)
            elif isinstance(instance, dict):
                map_dict[key] = instance.get(map_to)
            elif isinstance(instance, list):
                for obj in instance:
                    if isinstance(obj, model):
                        map_dict[key] = map_dict[key] if key in map_dict else []
                        map_dict[key].append(obj.__dict__.get(map_to))
                    elif isinstance(obj, dict):
                        map_dict[key] = map_dict[key] if key in map_dict else []
                        map_dict[key].append(obj.get(map_to))
                    else:
                        raise Exception(f"Error mapping key {key}. Unable to map instance ({obj})")
            else:
                raise Exception(f"Error mapping key {key}. Unable to map instance ({instance})")
        else:
            map_dict[key] = [] if one_to_many else None

    return map_dict


def create_field_map_many_to_many(session, model, map_from=["name"], map_to=["id"], key_list=None):
    """
    Get values corresponding to composite keys from a database model.

    This function retrieves values from the 'map_to' array for composite keys formed
    by a list of fields specified in 'map_from'. The retrieval can be performed for
    a specific set of keys provided in 'key_list', or for all records if 'key_list'
    is not provided.

    Args:
        session (object): Database session object.
        model (class): SQLAlchemy model class.
        map_from (list, optional): List of fields to use for composite keys.
                                  Defaults to ["name"].
        map_to (list, optional): List of fields to retrieve values from. Defaults to ["id"].
        key_list (list, optional): List of composite keys to retrieve values for.
                                  If None, values will be retrieved for all records
                                  in 'model'. Defaults to None.

    Returns:
        dict: A mapping dictionary with composite keys as keys and values from 'map_to'
              as values.

    Raises:
        InvalidKeyList: If the KeyList is Invalid(the keys don't pass the validation check for the column type)

    Example Usage:
    key_list = [
        # ("course_name", "course_id")
        ('College and Career E...ial Skills', 388667),
        ('Introduction at Cybe...Security+)', 388668),
        ('Introduction to Info...pport (A+)', 388669),
        ('Medical Coding for P...l Services', 388670),
        ('Industry Training an...Experience', 400737)
    ]
    values_mapping = create_field_map_many_to_many(
        session, Course, ["course_name", "course_id"], ["department_name", "department_number"], key_list = key_list
    )

    # `values_mapping` will be a dictionary with composite keys as keys and corresponding `department_name`,
      `department_number` values
    values_mapping = {
        ('College and Career E...ial Skills', 388667): ['WF', 500]
        ('Introduction at Cybe...Security+)', 388668): ['IT', 510]
        ('Introduction to Info...pport (A+)', 388669): ['IT', 500]
        ('Medical Coding for P...l Services', 388670): ['MC', 500]
        ('Industry Training an...Experience', 400737): ['WF', 550]
    }
    """
    values_dict = {}
    query_pk = True

    if not key_list:
        # If key_list is not provided, retrieve values for all records
        for obj in session.scalars(select(model)).all():
            obj_dict = obj.__dict__
            k = tuple(obj_dict.get(field, None) for field in map_from)
            values_dict[k] = [obj_dict.get(field, None) for field in map_to]

        return values_dict

    # Fetch validation functions for each column
    validation_functions = [
        get_validation_function_by_model_field(session, model, column_name) for column_name in map_from
    ]

    # Validate keys using validation functions
    for composite_key in key_list:
        try:
            # Iterate over each key in the composite key and apply corresponding validation functions,
            # validation functions raise an exception on failure and return None if valid
            [
                validation_function(key)
                for key, validation_function in zip(composite_key, validation_functions)
                if validation_function
            ]
        except Exception:
            raise InvalidKeyList(composite_key)

    for composite_key in key_list:
        filters = {col: val for col, val in zip(map_from, composite_key)}
        if query_pk:
            try:
                instance = session.execute(select(model).filter_by(**filters).limit(1)).scalars().first()
            except Exception:
                query_pk = False

        if not query_pk:
            try:
                instance = session.execute(select(model).filter_by(**filters).limit(1)).scalars().first()
            except Exception:
                instance = {field: None for field in map_to}

        if isinstance(instance, model):
            values_dict[composite_key] = [instance.__dict__.get(field, None) for field in map_to]
        elif isinstance(instance, dict):
            values_dict[composite_key] = [instance.get(field, None) for field in map_to]

    return values_dict


def get_validation_function_by_model_field(session, model, field):
    """Return the validation function appropriate for a specified
    model and field. Currently limited to UUID fields because
    non-UUID values were breaking create_field_map when querying
    the db.

    Arguments:
        session: SQL Alchemy Session
        model: SQL Alchemy model to build the map from
        field: name of the column / attribute to be validated

    Returns:
        validation_function: Function appropriate for checking
        data prior to ingestion / querying into the model's field.
    """
    engine = session.get_bind()
    insp = inspect(engine)
    table_name = model.__table__.name
    columns_dict = {c["name"]: c["type"] for c in insp.get_columns(table_name)}
    column_type = columns_dict.get(field)
    if isinstance(column_type, UUID):
        return validate_uuid
    else:
        return None


def map_value_to_foreign_key(
    session,
    data,
    old_value_key,
    new_id_key,
    table_class,
    column_name,
    return_column="id",
):
    """
    Maps a value to its corresponding foreign key ID in a database table.

    Args:
        session (Session): The database session.
        data (dict): The data containing the value and foreign key.
        old_value_key (str): The key for the value to be mapped.
        new_id_key (str): The key for storing the foreign key ID.
        table_class (class): The SQLAlchemy model class for the target table.
        column_name (str): The name of the column in the target table to perform the mapping.

    Returns:
        dict: The updated data dictionary.

    Raises:
        ValueError: If the value is not found in the target table.
    """
    value = data.pop(old_value_key, None)
    if value is not None:
        item_id = (
            session.execute(select(getattr(table_class, return_column)).filter_by(**{column_name: value}))
            .scalars()
            .first()
        )
        if item_id is None:
            raise ValueError(f"{old_value_key} '{value}' not found in table '{table_class.__tablename__}'")
        else:
            item_id = item_id[0]
        data[new_id_key] = item_id
    else:
        data.pop(old_value_key, None)
    return data


def create_field_map_from_composite_key(session, model, map_from=["name"], map_to="id", key_list=None):
    """
    Create a mapping from composite keys to target fields in a database model.

    This function generates a mapping dictionary where keys are composite keys formed
    by a list of fields specified in 'map_from', and values correspond to the corresponding
    values in the 'map_to' field. The mapping can be performed for a specific set of keys
    provided in 'key_list', or for all records if 'key_list' is not provided.

    Args:
        session (object): Database session object.
        model (class): SQLAlchemy model class.
        map_from (list, optional): List of fields to use for composite keys.
                                  Defaults to ["name"].
        map_to (str, optional): Field to map to. Defaults to "id".
        key_list (list, optional): List of composite keys to create mappings for.
                                  If None, mappings will be generated for all records
                                  in 'model'. Defaults to None.

    Returns:
        dict: A mapping dictionary with composite keys as keys and values from 'map_to'
              as values.

    Raises:
        Exception: If there is an error during the mapping process.

    Example Usage:
    from sqlalchemy import create_engine, Session
    from my_models import MyModel  # Assuming 'MyModel' is your SQLAlchemy model class

    engine = create_engine('sqlite:///my_database.db')
    session = Session(engine)

    # Assuming 'MyModel' has fields 'field1' and 'field2'
    key_list = [("value1", "value2"), ("value3", "value4")]
    mapping = create_field_map_from_composite_key(session, MyModel, ["field1", "field2"], "id", key_list)

    # 'mapping' will be a dictionary with composite keys as keys and corresponding 'id' values

    """
    map_dict = {}
    query_pk = True

    if not key_list:
        for obj in session.scalars(select(model)).all():
            obj_dict = obj.__dict__
            k = obj_dict.get(map_from, None)
            map_dict[k] = obj_dict.get(map_to, None)

        return map_dict

    for keys in key_list:
        validation_function = get_validation_function_by_model_field(session, model, keys)
        valid_key_list = False
        if validation_function and (
            all(get_validation_function_by_model_field(session, model, key) for key in keys) is None
        ):
            valid_key_list = True

        if not validation_function or valid_key_list:
            filters = {col: val for col, val in zip(map_from, keys)}
            if query_pk:
                try:
                    instance = session.execute(select(model).filter_by(**filters).limit(1)).scalars().first()
                except Exception:
                    query_pk = False

            if not query_pk:
                try:
                    instance = session.execute(select(model).filter_by(**filters).limit(1)).scalars().first()
                except Exception:
                    instance = {map_to: None}

            if isinstance(instance, model):
                map_dict[keys] = instance.__dict__.get(map_to)
            elif isinstance(instance, dict):
                map_dict[keys] = instance.get(map_to)
        else:
            map_dict[keys] = None

    return map_dict


def resolve_mappings(
    session,
    data,
    old_key,
    new_key,
    model,
    map_from,
    map_to="id",
    return_map=False,
    replace_old_key=True,
    is_required=False,
    parent=None,
):
    """
    Maps old_key in data to the new_key based on map_from, map_to values of
    the model class.

    Args:
        session (object): Database session.
        data (list): List of dictionaries representing records.
        old_key (str): Key to be replaced.
        new_key (str): New key to be assigned.
        model (object): Database model for mapping.
        map_from (str): Field to map from.
        map_to (str, optional): Field to map to. Defaults to "id".
        return_map (bool, optional): Whether to return the mapping. Defaults to False.
        replace_old_key (bool, optional): If False, retains 'old_key' in 'record'. Defaults to True.
        is_required (bool, optional): If True, raises an error for missing mappings. Defaults to False.
        parent (str, optional): Parent key if the record is nested in a dictionary. Defaults to None.

    Returns:
        list or tuple: Updated data with resolved mappings and optional
        mapping dictionary.

    """
    map = create_field_map(session, model, map_from, map_to)
    failed_records = []
    for record in data:
        current_record = record
        if parent:
            for key in parent.split("."):
                record = record.get(key, None)
        try:
            if old_key in record:
                if replace_old_key:
                    value = record.pop(old_key)
                else:
                    value = record[old_key]
                id = map.get(value)
                if is_required and id is None:
                    raise MappingError(old_key, value, model.__tablename__)
                record[new_key] = id
        except Exception as e:
            failed_records.append({"record": current_record, "error": str(e)})
        if parent and new_key in record:
            current_record[new_key] = record[new_key]
            record = current_record
    for record in failed_records:
        data.remove(record.get("record"))
    if return_map:
        return data, failed_records, map
    else:
        return data, failed_records


def apply_mappings(session, data, mappings):
    """
    Applies mappings to incoming data. These old_key in data to the new_key
    based on map_from, map_to values of the model class.

    Args:
        session (object): Database session.
        data (list): List of dictionaries representing records.
        mappings (list): List of dictionaries containing mapping details.

    Example:
        data = {"cfg_Learner_Status__c": "Expressed Interest"}

        mappings=
            [
                {
                    'old_key': "cfg_Learner_Status__c",
                    'new_key': "learner_status_id",
                    'model': LearnerStatus,
                    'map_from': "status",
                    'map_to': "id",
                    'return_map': True
                }
            ]
        result = apply_mappings(session, data, mappings)
        expected_result = {"learner_status_id": <UUID>}

    Returns:
        tuple: Updated data with resolved mappings and mapping dictionary.

    """
    maps = {}
    failed_records = []
    for mapping in mappings:
        if mapping.get("return_map"):
            valid_data, failed_batch, map = resolve_mappings(session, data, **mapping)
            maps[mapping["new_key"]] = map
        else:
            valid_data, failed_batch = resolve_mappings(session, data, **mapping)
        failed_records.extend(failed_batch)
    return valid_data, failed_records, maps


def find_enum_value(enum: enum, value: str):
    """
    Fetches the enum ID from the supplied enum based on the provided value.

    Args:
        value (str): The lead source data to be converted to an enum ID.

    Returns:
        enum value: The instance of the matching enum
        None: No matching enum found
    """
    if not value:
        return None
    for key, enum in enum._value2member_map_.items():
        if key.lower() == value.lower():
            return enum
    return None
