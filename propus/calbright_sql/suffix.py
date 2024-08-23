import asyncio
from sqlalchemy import String, INTEGER
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Suffix(Base):
    __tablename__ = "suffix"

    suffix = mapped_column(String(20), nullable=False, unique=True)
    anthology_id = mapped_column(INTEGER, unique=True)

    def seed_data(self, session, anthology, **kwargs):
        suffixes = asyncio.run(anthology.fetch_configurations("suffix"))
        if not suffixes.get("value"):
            raise Exception("No Suffixes Returned from Anthology")
        for suffix in suffixes.get("value"):
            row = {"suffix": suffix.get("Code"), "anthology_id": suffix.get("Id")}
            update_or_create(session, Suffix, row, suffix=row.get("suffix"), anthology_id=row.get("anthology_id"))
        self.session_commit_with_rollback_on_unique(session)
