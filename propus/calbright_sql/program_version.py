from sqlalchemy import FLOAT, INTEGER, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.program import Program
from propus.helpers.sql_alchemy import update_or_create


class ProgramVersion(Base):
    __tablename__ = "program_version"

    program_id = mapped_column(UUID, ForeignKey("program.id"), index=True, nullable=False)
    program = relationship(
        "Program",
        backref="program_version_program",
        primaryjoin=program_id == Program.id,
    )
    version_id = mapped_column(FLOAT, nullable=False)
    product_id = mapped_column(INTEGER)
    completion_type = mapped_column(String(25), nullable=False)

    def seed_data(self, session, **kwargs):
        initial_versions = [
            {"version_id": 1.0, "completion_type": "sequential"},
            {"version_id": 1.5, "completion_type": "sequential"},
            {"version_id": 2.0, "completion_type": "co_enrollment"},
            {"version_id": 3.0, "completion_type": "co_enrollment"},
            {"version_id": 4.0, "completion_type": "co_enrollment"},
            {"version_id": 5.0, "completion_type": "co_enrollment"},
        ]
        program_version_data = {
            "Medical Coding for Physician Services": initial_versions,
            "Introduction to Information Technology Support (A+)": initial_versions,
            "Cybersecurity": initial_versions,
            "Transition to Technology - Customer Relationship Management Platform Administration": [
                {"version_id": 1.0, "completion_type": "co_enrollment"},
                {"version_id": 2.0, "completion_type": "co_enrollment"},
            ],
            "Transition to Technology: IT Help Desk Technician": [],
            "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion": [
                {"version_id": 1.0, "completion_type": "co_enrollment"},
                {"version_id": 2.0, "completion_type": "co_enrollment"},
            ],
            "Upskilling for Equitable Health Impacts: Interpersonal Skills": [],
            "Transition to Technology: Introduction to Networks": [
                {"version_id": 1.0, "product_id": 5, "completion_type": "co_enrollment"},
            ],
            "Introduction to Data Analysis": [
                {"version_id": 1.0, "completion_type": "co_enrollment"},
                {"version_id": 2.0, "completion_type": "co_enrollment"},
                {
                    "version_id": 3.0,
                    "product_id": 3,
                    "completion_type": "co_enrollment",
                },
            ],
            "Licensed Vocational Nursing (LVN) Program": [],
            "Project Management": [
                {"version_id": 1.0, "product_id": 7, "completion_type": "co_enrollment"},
            ],
        }

        program_versions = []
        for program_name, versions in program_version_data.items():
            p_id = Base.program_name_to_id.get(program_name)
            for version in versions:
                row = dict(**{"program_id": p_id}, **version)
                record = update_or_create(
                    session, ProgramVersion, row, program_id=row.get("program_id"), version_id=row.get("version_id")
                )
                program_versions.append(record[0])
        self.session_commit_with_rollback_on_unique(session)
        Base.program_version = program_versions
