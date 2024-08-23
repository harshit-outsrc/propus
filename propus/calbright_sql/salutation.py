import asyncio
from sqlalchemy import String, INTEGER
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Salutation(Base):
    __tablename__ = "salutation"

    salutation = mapped_column(String(5), nullable=False, unique=True)
    anthology_id = mapped_column(INTEGER, unique=True)

    def seed_data(self, session, anthology, **kwargs):
        titles = asyncio.run(anthology.fetch_configurations("title"))
        if not titles.get("value"):
            raise Exception("No Salutations Returned from Anthology")
        for title in titles.get("value"):
            row = {"salutation": title.get("Name"), "anthology_id": title.get("Id")}
            update_or_create(
                session,
                Salutation,
                row,
                salutation=row.get("salutation"),
                anthology_id=row.get("anthology_id"),
            )
        self.session_commit_with_rollback_on_unique(session)
