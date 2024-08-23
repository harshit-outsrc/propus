from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class EnrollmentStatus(Base):
    __tablename__ = "enrollment_status"

    status = mapped_column(VARCHAR(25), nullable=False, unique=True)
    anthology_id = mapped_column(VARCHAR(50), unique=True)

    def seed_data(self, session, **kwargs):
        status_to_anthology = {
            "Enrolled": "NDS-Enrolled in Program Pathway",
            "Started": "NDS-Started Program Pathway",
            "Complete": "NDS-Completed",
            "Dropped": "NDS-Dropped",
            "Withdrawn": "NDS-Withdrawn",
        }

        for status, anthology_id in status_to_anthology.items():
            row = {"status": status, "anthology_id": anthology_id}
            update_or_create(
                session,
                EnrollmentStatus,
                row,
                status=row.get("status"),
                anthology_id=row.get("anthology_id"),
            )
        self.session_commit_with_rollback_on_unique(session)
