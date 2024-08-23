from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class EventType(Base):
    __tablename__ = "event_type"

    name = mapped_column(String(25), nullable=False, unique=True)

    def seed_data(self, session, **kwargs):
        event_types = ["LMS-Login", "LMS-SAA", "Meeting-Scheduled", "Meeting-Canceled"]
        for et in event_types:
            row = {"name": et}
            update_or_create(
                session,
                EventType,
                row,
                name=row.get("name"),
            )
        self.session_commit_with_rollback_on_unique(session)
