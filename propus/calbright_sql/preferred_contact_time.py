from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class PreferredContactTime(Base):
    __tablename__ = "preferred_contact_time"

    preferred_contact_time = mapped_column(String, nullable=False, unique=True)

    def seed_data(self, session, **kwargs):
        preferred_contact_time_list = [
            "Weekday Mornings (8am - 12pm)",
            "Weekday Afternoons (12pm - 5pm)",
            "Weekday Evenings (5pm - 8pm)",
            "Weekends (10am - 4pm)",
        ]
        for preferred_contact_time in preferred_contact_time_list:
            row = {"preferred_contact_time": preferred_contact_time}
            update_or_create(
                session,
                PreferredContactTime,
                row,
                preferred_contact_time=row.get("preferred_contact_time"),
            )
        self.session_commit_with_rollback_on_unique(session)
