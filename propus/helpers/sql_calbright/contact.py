from typing import List

from propus.helpers.etl import fetch_county
from propus.helpers.sql_alchemy import create_field_map_from_composite_key

from propus.calbright_sql.address import Address
from propus.calbright_sql.preferred_contact_method import PreferredContactMethod
from propus.calbright_sql.preferred_contact_time import PreferredContactTime
from propus.calbright_sql.student import Student
from propus.calbright_sql.student_address import StudentAddress
from propus.calbright_sql.student_contact_method import StudentContactMethod
from propus.calbright_sql.student_contact_time import StudentContactTime


def update_address(session, student: Student, address_data: dict):
    """
    This function is used to update the address for a student. It takes in
    the session, student, and address data as arguments. It loops through
    the student's addresses and compares them to the address data. If the
    address data matches an existing address, it sets the current flag to
    True. If the address data does not match an existing address, it creates
    a new address and adds it to the database. Finally, it commits the changes
    to the database.

    Args:
        session (SQLAlchemy Session): active session connection to the database
        student (Student): student object to update the address for
        address_data (dict): dictionary containing the address data to update

    """
    if not address_data or len(address_data) < 3:
        return

    current_address = None
    for address in student.student_address:
        if address.current:
            current_address = address
        same_address = True
        for k, val in address_data.items():
            if getattr(address.address, k) != val:
                same_address = False
                address.current = False
                break
        if not same_address:
            continue
        if same_address and current_address:
            return

    # Create Student Address
    address = Address(
        address1=address_data.get("address1"),
        city=address_data.get("city"),
        state=address_data.get("state"),
        zip=address_data.get("zip"),
        county=fetch_county(address_data.get("city"), address_data.get("zip")),
        country=address_data.get("country"),
    )
    session.add(address)
    session.add(StudentAddress(student_id=student.ccc_id, address=address))


def update_contact_preferences(session, student: Student, new_data: List, req_type: str):
    """
    This function is used to update the preferred contact method and time
    for a student. It takes in the session, student, new data, and request
    type as arguments. The request type is used to determine which table to
    update. If the request type is "method", it will update the
    student_preferred_contact_method table. If the request type is "time", it
    will update the student_preferred_contact_time table. The function uses
    the create_field_map_from_composite_key function to create a lookup map
    from the new data. It then loops through the new data and checks if the
    item is in the lookup map. If the item is not in the lookup map, it will
    add a new item to the database. If the item is in the lookup map, it will
    delete the item from the database. Finally, it will commit the changes to
    the database.

    Args:
        session (SQLAlchemy Session): active session connection to the database
        student (Student): student object to update the preferred contact method and time for
        new_data (list): list of new data to update the preferred contact method and time for
        req_type (str): type of request to update the preferred contact method and time for (method or time)

    Raises:
        Exception raised if mapping cannot be found tied to model instance
    """
    lookup_map = create_field_map_from_composite_key(
        session,
        PreferredContactMethod if req_type == "method" else PreferredContactTime,
        map_from="preferred_contact_method" if req_type == "method" else "preferred_contact_time",
    )

    student_table = "student_preferred_contact_method"
    key_name = "preferred_contact_method"
    model = StudentContactMethod
    model_key = "contact_method_id"
    if req_type == "time":
        student_table = "student_preferred_contact_time"
        key_name = "preferred_contact_time"
        model = StudentContactTime
        model_key = "contact_time_id"

    stored_items = {getattr(item, key_name).id: item for item in getattr(student, student_table)}
    new_items = set(lookup_map.get(item) for item in new_data.split(";") if lookup_map.get(item))
    for item in new_items - set(stored_items.keys()):
        session.add(model(**{"ccc_id": student.ccc_id, model_key: item}))
    for item in set(stored_items.keys()) - new_items:
        session.delete(stored_items.get(item))
