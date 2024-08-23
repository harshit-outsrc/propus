from sqlalchemy import select
from propus.calbright_sql.expressed_interest import ExpressInterest, LeadSource, BrowserType
from propus.calbright_sql.program import Program

from propus.helpers.sql_alchemy import find_enum_value


def fetch_programs_by_name(session, program_name_list):
    return session.scalars(select(Program).filter(Program.short_name.in_(program_name_list))).all()


def create_expressed_interest_record(session, user, expressed_interest_data: dict):
    """
    Create an expressed interest record.

    This function takes in a database session, user object, and expressed interest
    data dictionary to create a record of the user's expressed interest in a program.

    It first queries the database to get Program objects matching the program IDs
    in the data. It then checks if the user already has expressed interests and
    filters out any duplicate program IDs.

    The function handles populating enum fields like lead source and browser type.
    It also adds the user and program ID to the data before creating an
    ExpressInterest object and adding it to the database session.

    Args:
        session: SQLAlchemy database session
        expressed_interest_data (dict): Data for creating the
            expressed_interest record
    """
    if not expressed_interest_data.get("program_interest_id"):
        return
    programs_of_interest = fetch_programs_by_name(
        session, expressed_interest_data.get("program_interest_id").split(";")
    )
    if not programs_of_interest:
        return
    current_expressed_interests = [
        p.program_interest_id
        for p in user.expressed_interest_user
        if user.expressed_interest_user and p.program_interest_id
    ]

    new_programs = [p.id for p in programs_of_interest if p.id not in current_expressed_interests]
    if not new_programs:
        return
    lead_source = (
        find_enum_value(LeadSource, expressed_interest_data.get("lead_source"))
        if expressed_interest_data.get("lead_source")
        else LeadSource.other
    )
    expressed_interest_data["browser_type"] = (
        (BrowserType.mobile if expressed_interest_data.get("browser_type") == "Mobile" else BrowserType.desktop)
        if expressed_interest_data.get("browser_type")
        else None
    )
    expressed_interest_data["lead_source"] = lead_source
    expressed_interest_data["user"] = user
    for program in new_programs:
        expressed_interest_data["program_interest_id"] = program
    session.add(ExpressInterest(**expressed_interest_data))
