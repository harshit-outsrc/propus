import asyncio

from sqlalchemy import String, INTEGER
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Pronoun(Base):
    __tablename__ = "pronoun"

    pronoun = mapped_column(String(20), nullable=False, unique=True)
    anthology_id = mapped_column(INTEGER, unique=True)

    @staticmethod
    def col_names():
        return ["id", "pronoun", "anthology_id", "created_at"]

    def seed_data(self, session, anthology, **kwargs):
        pronouns = asyncio.run(anthology.fetch_configurations("pronoun"))
        if not pronouns.get("value"):
            raise Exception("No Pronouns Returned from Anthology")
        for pronoun in pronouns.get("value"):
            row = {"pronoun": pronoun.get("Name"), "anthology_id": pronoun.get("Id")}
            update_or_create(
                session,
                Pronoun,
                row,
                pronoun=row.get("pronoun"),
                anthology_id=row.get("anthology_id"),
            )
        self.session_commit_with_rollback_on_unique(session)
