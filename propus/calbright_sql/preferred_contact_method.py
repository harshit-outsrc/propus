from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class PreferredContactMethod(Base):
    __tablename__ = "preferred_contact_method"

    preferred_contact_method = mapped_column(String, nullable=False, unique=True)

    def seed_data(self, session, **kwargs):
        preferred_contact_method_list = ["Text Message", "Phone Call", "Email"]
        for preferred_contact_method in preferred_contact_method_list:
            row = {"preferred_contact_method": preferred_contact_method}
            update_or_create(
                session,
                PreferredContactMethod,
                row,
                preferred_contact_method=row.get("preferred_contact_method"),
            )
        self.session_commit_with_rollback_on_unique(session)
