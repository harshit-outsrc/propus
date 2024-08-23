import csv
import os
from sqlalchemy import String, INTEGER, DATE, VARCHAR, FLOAT
from sqlalchemy.orm import mapped_column
from propus.helpers.sql_alchemy import update_or_create

from propus.calbright_sql import Base


class Course(Base):
    __tablename__ = "course"

    course_name = mapped_column(String, nullable=False, unique=True)
    status = mapped_column(String(25), nullable=False)

    # Coci Data Columns
    course_id = mapped_column(INTEGER, nullable=False, unique=True, index=True)
    control_number = mapped_column(String(25), nullable=False, unique=True, index=True)
    course_code = mapped_column(String(10), nullable=False)
    department_name = mapped_column(String(5), nullable=False)
    department_number = mapped_column(INTEGER, nullable=False)
    course_classification_status = mapped_column(VARCHAR(1), nullable=False)

    top_code = mapped_column(String, nullable=False)
    last_updated_by_college = mapped_column(DATE, nullable=False)
    minimum_course_contact_hours = mapped_column(FLOAT, nullable=False)
    maximum_course_contact_hours = mapped_column(FLOAT, nullable=False)

    anthology_course_id = mapped_column(INTEGER)

    def seed_data(self, session, **kwargs):
        anthology_id_map = {
            "WF-500": 2,
            "IT-500": 3,
            "IT-510": 4,
            "MC-500": 5,
            "IT-520": 6,
            "IT-525": 7,
            "HC-500": 8,
            "HC-501": 9,
            "HC-502": 10,
            "IT-532": 11,
            "IT-533": 12,
            "WF-510": 13,
            "BUS-500": 14,
            "BUS-501": 15,
            "IT-500CPL": 20,
            "IT-100": 21,
            "WF-100": 22,
            "BUS-520": 16,
            "BUS-521": 17,
            "BUS-522": 18,
        }
        seed_file = f"{os.path.dirname(os.path.abspath(__file__))}/seed_data/COCI-Course-Export-2024-06-27.csv"

        rows = []
        with open(seed_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = {
                    "course_name": row.get("TITLE (CB02)"),
                    "status": row.get("STATUS"),
                    "course_id": row.get("COURSE ID"),
                    "control_number": row.get("CONTROL NUMBER (CB00)"),
                    "department_name": row.get("DEPARTMENT NAME (CB01A)"),
                    "department_number": row.get("DEPARTMENT NUMBER (CB01B)"),
                    "course_code": row.get("DEPARTMENT NAME (CB01A)") + row.get("DEPARTMENT NUMBER (CB01B)"),
                    "course_classification_status": row.get("COURSE CLASSIFICATION STATUS (CB11)"),
                    "top_code": row.get("TOP CODE (CB03)"),
                    "last_updated_by_college": row.get("LAST UPDATED BY COLLEGE"),
                    "minimum_course_contact_hours": row.get("MINIMUM COURSE CONTACT HOURS"),
                    "maximum_course_contact_hours": row.get("MAXIMUM COURSE CONTACT HOURS"),
                    "anthology_course_id": anthology_id_map.get(
                        f"{row.get('DEPARTMENT NAME (CB01A)')}-{row.get('DEPARTMENT NUMBER (CB01B)')}"
                    ),
                }

                record = update_or_create(
                    session,
                    Course,
                    row,
                    course_id=row.get("course_id"),
                    course_code=row.get("course_code"),
                )
                rows.append(record[0])
        self.session_commit_with_rollback_on_unique(session)
        Base.course_name_to_id = {f"{r.department_name}{r.department_number}": r.id for r in rows}
