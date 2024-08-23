from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Grade(Base):
    __tablename__ = "grade"

    grade = mapped_column(VARCHAR(50), nullable=False, unique=True)
    title = mapped_column(VARCHAR(50), nullable=False, unique=True)

    def seed_data(self, session, **kwargs):
        grade_map = {
            "NP": "Not Passed",
            "SP": "Satisfactory Progress",  # Anthology has it as "Satisfactory Progres" due to character limit
            "P": "Pass",
            "D": "Dropped",
            "W": "Withdrawn",
            "I": "Incomplete",
            "EW": "Excused Withdrawal",
            "MW": "Military Withdrawal",
        }

        for g, t in grade_map.items():
            row = {"grade": g, "title": t}
            update_or_create(
                session,
                Grade,
                row,
                grade=row.get("grade"),
                title=row.get("title"),
            )
        self.session_commit_with_rollback_on_unique(session)
