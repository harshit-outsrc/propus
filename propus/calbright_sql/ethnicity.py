import asyncio
from sqlalchemy import String, INTEGER
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Ethnicity(Base):
    __tablename__ = "ethnicity"

    ethnicity = mapped_column(String(50), nullable=False, unique=True)
    anthology_id = mapped_column(INTEGER, unique=True)

    def seed_data(self, session, anthology, **kwargs):
        ethnicity_anthology_map = {
            "Hispanic, Latino": "Hispanic or Latinix",
            "American Indian / Alaskan Native": "American Indian or Alaska Native",
            "Pacific Islander Other": "Native Hawaiian or Other Pacific Islander",
        }

        ccc_apply_ethnicity = [
            "Hispanic, Latino",
            "Mexican, Mexican-American, Chicano",
            "Central American",
            "South American",
            "Hispanic Other",
            "Asian Indian",
            "Asian Chinese",
            "Asian Japanese",
            "Asian Korean",
            "Asian Laotian",
            "Asian Cambodian",
            "Asian Vietnamese",
            "Asian Filipino",
            "Asian Other",
            "Black or African American",
            "American Indian / Alaskan Native",
            "Pacific Islander Guamanian",
            "Pacific Islander Hawaiian",
            "Pacific Islander Samoan",
            "Pacific Islander Other",
            "White",
        ]

        ethnicities = asyncio.run(anthology.fetch_configurations("ethnicity"))
        if not ethnicities.get("value"):
            raise Exception("No Ethnicities Returned from Anthology")
        anthology_ethnicities = {
            ethnicity.get("Name").replace(":", ""): ethnicity.get("Id") for ethnicity in ethnicities.get("value")
        }

        for ethnicity in ccc_apply_ethnicity:
            if anthology_ethnicities.get(ethnicity):
                anthology_id = anthology_ethnicities.get(ethnicity)
            elif ethnicity_anthology_map.get(ethnicity):
                anthology_id = anthology_ethnicities.get(ethnicity_anthology_map.get(ethnicity))
            else:
                #  We do not want to insert this ethnicity as it is not an option from CCCApply
                continue
            row = {"ethnicity": ethnicity, "anthology_id": anthology_id}
            update_or_create(
                session,
                Ethnicity,
                row,
                ethnicity=row.get("ethnicity"),
                anthology_id=row.get("anthology_id"),
            )
        self.session_commit_with_rollback_on_unique(session)
