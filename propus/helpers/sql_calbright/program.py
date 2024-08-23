from sqlalchemy import select

from propus.calbright_sql.program import Program


def fetch_courses_for_program(session, program_name, program_version_id=None):
    program = session.execute(select(Program).filter_by(short_name=program_name)).scalar_one()
    version_to_program = {p.id: p for p in program.program_version_program}
    program_version = version_to_program.get(
        program_version_id if program_version_id else max(version_to_program.keys())
    )

    return [
        pcv.course_version.course
        for pcv in program_version.program_course_version
        if pcv.course_version.course.status == "Active"
    ]
