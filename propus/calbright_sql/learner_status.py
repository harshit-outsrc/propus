import asyncio

from sqlalchemy import String, INTEGER
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class LearnerStatus(Base):
    __tablename__ = "learner_status"

    status = mapped_column(String(100), nullable=False, unique=True)
    anthology_id = mapped_column(INTEGER, unique=True)

    def seed_data(self, session, anthology, **kwargs):
        learner_status_to_anthology_status = {
            "Expressed Interest": None,
            "App Started": None,
            "App Submitted": None,
            "Ready for Onboarding": None,
            "Started Orientation": None,
            "Completed Orientation": None,
            "Completed Ed Plan": None,
            "Completed CSEP": None,
            "Enrolled in Essentials": None,
            "Completed Essentials": None,
            "Met w/Program Director": None,
            "Enrolled in Program Pathway": "NDS - Enrolled in Program Pathway",
            "Started Program Pathway": "NDS-Started Program Pathway",
            "Completed Program Pathway": "NDS-Completed",
            "Completed Industy Certificate": None,
            "Paid Apprenticeship": None,
            "Full-Time Employment": None,
            "Dropped": "NDS-Dropped",
            "Suspended by IT (pre-enrollment)": "NDS-Administrative Withdrawal",
            "Withdrawn": "NDS-Withdrawn",
        }

        anthology_resp = asyncio.run(anthology.fetch_configurations("school_status"))
        if not anthology_resp.get("value"):
            raise Exception("No Statuses Returned from Anthology")
        school_statuses = {status.get("Name"): status.get("Id") for status in anthology_resp.get("value")}

        for status, anthology_status in learner_status_to_anthology_status.items():
            row = {"status": status, "anthology_id": school_statuses.get(anthology_status)}
            update_or_create(
                session,
                LearnerStatus,
                row,
                status=row.get("status"),
                anthology_id=row.get("anthology_id"),
            )
        self.session_commit_with_rollback_on_unique(session)
