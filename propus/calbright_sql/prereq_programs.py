from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.program import Program
from propus.helpers.sql_alchemy import update_or_create


class PrereqProgram(Base):
    __tablename__ = "prereq_program"

    program_id = mapped_column(
        UUID(),
        ForeignKey("program.id"),
        index=True,
        primary_key=True,
    )
    program = relationship("Program", backref="program_prereq_program", primaryjoin=program_id == Program.id)

    # If student has completed the following program they are pre-approved to take te above program id
    # i.e. if prereq_program is IT Support student is pre-approved to take above program of Cyber
    prereq_program_id = mapped_column(
        UUID(),
        ForeignKey("program.id"),
        index=True,
        primary_key=True,
    )
    prereq_program = relationship(
        "Program", backref="prereq_program_program", primaryjoin=prereq_program_id == Program.id
    )

    __table_args__ = (UniqueConstraint("program_id", "prereq_program_id", name="uniq_prereq_program_id"),)

    def __repr__(self) -> str:
        return f"<PrereqProgram: {self.program_id} - {self.prereq_program_id}>"

    def seed_data(self, session, **kwargs):
        itspt = "Introduction to Information Technology Support (A+)"
        cyber = "Cybersecurity"
        netwrks = "Transition to Technology: Introduction to Networks"
        pre_reqs = {cyber: [itspt, netwrks], netwrks: [itspt, cyber]}

        for program, pre_approved_programs in pre_reqs.items():
            program_id = Base.program_name_to_id.get(program)
            for pre_approved in pre_approved_programs:
                prereq_program_id = Base.program_name_to_id.get(pre_approved)
                row = {"program_id": program_id, "prereq_program_id": prereq_program_id}
                update_or_create(
                    session,
                    PrereqProgram,
                    row,
                    program_id=row.get("program_id"),
                    prereq_program_id=row.get("prereq_program_id"),
                )
        self.session_commit_with_rollback_on_unique(session)
