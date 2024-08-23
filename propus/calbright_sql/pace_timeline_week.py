import csv
import os
from sqlalchemy import INTEGER, ForeignKey, VARCHAR
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from propus.calbright_sql import Base
from propus.calbright_sql.competency import Competency
from propus.calbright_sql.pace_timeline import PaceTimeline
from propus.helpers.sql_alchemy import update_or_create


class PaceTimelineWeek(Base):
    __tablename__ = "pace_timeline_week"

    completion_order = mapped_column(INTEGER, nullable=False)
    week_to_complete = mapped_column(INTEGER, nullable=False)
    timeline_id = mapped_column(UUID(), ForeignKey("pace_timeline.id"), index=True, nullable=False)
    timeline = relationship(
        "PaceTimeline",
        backref="pace_timeline_week_timeline",
        primaryjoin=timeline_id == PaceTimeline.id,
    )

    competency_id = mapped_column(UUID(), ForeignKey("competency.id"), index=True)
    competency = relationship(
        "Competency",
        backref="pace_timeline_week_competency",
        primaryjoin=competency_id == Competency.id,
    )
    lesson_name = mapped_column(VARCHAR(250))

    __table_args__ = (UniqueConstraint("competency_id", "timeline_id", name="_uniq_competency_timeline"),)

    def seed_data(self, session, **kwargs):
        seed_file = f"{os.path.dirname(os.path.abspath(__file__))}/seed_data/CompetencyToTimelineWeeks.csv"
        with open(seed_file) as csvfile:
            reader = csv.DictReader(csvfile)
            competency_names = None
            for row in reader:
                if competency_names is None:
                    competency_names = list(row.keys())[2:]
                for competency in competency_names:
                    if not row.get(competency):
                        continue
                    pace_timeline_week_record = {
                        "completion_order": row.get("Competency Completion Order"),
                        "week_to_complete": row.get(competency),
                        "timeline_id": Base.pact_timeline_name_to_id.get(competency),
                        "competency_id": (
                            Base.competency_name_to_id.get(row.get("Competency Name"))
                            if row.get("Competency Name")
                            else None
                        ),
                        "lesson_name": (
                            None
                            if Base.competency_name_to_id.get(row.get("Competency Name"))
                            else row.get("Competency Name")
                        ),
                    }
                    update_or_create(
                        session,
                        PaceTimelineWeek,
                        pace_timeline_week_record,
                        timeline_id=pace_timeline_week_record.get("timeline_id"),
                        competency_id=pace_timeline_week_record.get("competency_id"),
                    )
        self.session_commit_with_rollback_on_unique(session)
