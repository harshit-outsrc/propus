import asyncio
from sqlalchemy import String, INTEGER
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Gender(Base):
    __tablename__ = "gender"

    gender = mapped_column(String(50), nullable=False, unique=True)
    anthology_id = mapped_column(INTEGER)

    def seed_data(self, session, anthology, **kwargs):
        gender_anthology_map = {
            "Decline to state": "Not specified",
            "Non-binary": "Non-Binary",
        }

        ccc_apply_gender = [
            "Female",
            "Male",
            "Non-binary",
            "Decline to state",
        ]
        genders = asyncio.run(anthology.fetch_configurations("gender"))
        if not genders:
            raise Exception("No Genders Returned from Anthology")
        anthology_genders = {gender.get("Name").replace(":", ""): gender.get("Id") for gender in genders.get("value")}

        for gender in ccc_apply_gender:
            if anthology_genders.get(gender):
                anthology_id = anthology_genders.get(gender)
            elif gender_anthology_map.get(gender):
                anthology_id = anthology_genders.get(gender_anthology_map.get(gender))
            else:
                anthology_id = None
            row = {"gender": gender, "anthology_id": anthology_id}
            update_or_create(
                session,
                Gender,
                row,
                gender=row.get("gender"),
                anthology_id=row.get("anthology_id"),
            )
        self.session_commit_with_rollback_on_unique(session)
