import csv
import os

from sqlalchemy import String, INTEGER, DATE
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Program(Base):
    __tablename__ = "program"

    program_name = mapped_column(String, nullable=False, unique=True)
    short_name = mapped_column(String, unique=True)
    status = mapped_column(String(25), nullable=False, default="Not-Offered")

    # Coci Data Columns
    control_number = mapped_column(INTEGER, nullable=False, unique=True, index=True)
    top_code = mapped_column(String, nullable=False)
    cip_code = mapped_column(String, nullable=False)
    approved_date = mapped_column(DATE, nullable=False)

    anthology_program_id = mapped_column(INTEGER)
    anthology_program_version_id = mapped_column(INTEGER)

    certificates_offered = mapped_column(String())

    def seed_data(self, session, **kwargs):
        data_map = {
            "38571": {
                "short_name": "Medical Coding",
                "anthology_program_id": 7,
                "anthology_program_version_id": 9,
            },
            "38572": {
                "short_name": "Cybersecurity",
                "anthology_program_id": 6,
                "anthology_program_version_id": 6,
                "status": "Offered",
            },
            "38573": {
                "short_name": "IT Support",
                "anthology_program_id": 6,
                "anthology_program_version_id": 8,
                "status": "Offered",
            },
            "40597": {
                "short_name": "Customer Relationship Management",
                "anthology_program_id": 6,
                "anthology_program_version_id": 10,
                "status": "Offered",
            },
            "41214": {
                "short_name": "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion",
                "anthology_program_id": 7,
                "anthology_program_version_id": 11,
            },
            "41516": {
                "short_name": "T2T Intro to Networks",
                "anthology_program_id": 6,
                "anthology_program_version_id": 12,
            },
            "42338": {
                "short_name": "Data Analysis",
                "anthology_program_id": 9,
                "anthology_program_version_id": 15,
                "status": "Pilot",
            },
            "43231": {
                "short_name": "Project Management",
                "anthology_program_id": 9,
                "anthology_program_version_id": 16,
                "status": "Pilot",
            },
        }
        seed_file = f"{os.path.dirname(os.path.abspath(__file__))}/seed_data/COCI-Program-Export-2024-06-27.csv"

        with open(seed_file) as csvfile:
            reader = csv.DictReader(csvfile)
            rows = []
            for row in reader:
                new_data = {
                    "program_name": row.get("TITLE"),
                    "control_number": row.get("CONTROL NUMBER"),
                    "top_code": row.get("TOP CODE"),
                    "cip_code": row.get("CIP CODE"),
                    "approved_date": row.get("APPROVED DATE"),
                }
                new_data.update(data_map.get(row.get("CONTROL NUMBER"), {}))
                record = update_or_create(
                    session,
                    Program,
                    new_data,
                    program_name=new_data.get("program_name"),
                    control_number=new_data.get("control_number"),
                )
                rows.append(record[0])
        self.session_commit_with_rollback_on_unique(session)
        Base.program_name_to_id = {row.program_name: row.id for row in rows}
