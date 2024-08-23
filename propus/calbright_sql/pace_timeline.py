from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from propus.calbright_sql import Base
from propus.calbright_sql.program import Program
from propus.helpers.sql_alchemy import update_or_create


class PaceTimeline(Base):
    __tablename__ = "pace_timeline"

    timeline_name = mapped_column(String(25), nullable=False, unique=True)
    common_name = mapped_column(String(30), nullable=False)
    program_id = mapped_column(UUID(), ForeignKey("program.id"), index=True, nullable=False)
    program = relationship("Program", backref="pace_timeline_program", primaryjoin=program_id == Program.id)

    def seed_data(self, session, **kwargs):
        timeline_seed_data = [
            {
                "name": "CRM 60 Day",
                "common_name": "60 Day",
                "program_name": "Transition to Technology - Customer Relationship Management Platform Administration",
            },
            {
                "name": "CRM 90 Day",
                "common_name": "90 Day",
                "program_name": "Transition to Technology - Customer Relationship Management Platform Administration",
            },
            {
                "name": "CRM 120 Day",
                "common_name": "120 Day",
                "program_name": "Transition to Technology - Customer Relationship Management Platform Administration",
            },
            {
                "name": "CRM 180 Day",
                "common_name": "180 Day",
                "program_name": "Transition to Technology - Customer Relationship Management Platform Administration",
            },
            {
                "name": "CRM 365 Day",
                "common_name": "395 Day",
                "program_name": "Transition to Technology - Customer Relationship Management Platform Administration",
            },
            {
                "name": "Cybersecurity 4 Month",
                "common_name": "4 Month",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Cybersecurity 4 Month WF",
                "common_name": "4 Month WF",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Cybersecurity 8 Month",
                "common_name": "8 Month",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Cybersecurity 8 Month WF",
                "common_name": "8 Month WF",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Cybersecurity 12 Month",
                "common_name": "12 Month",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Cybersecurity 12 Month WF",
                "common_name": "12 Month WF",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Cybersecurity 18 Month",
                "common_name": "18 Month",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Cybersecurity 18 Month WF",
                "common_name": "18 Month WF",
                "program_name": "Cybersecurity",
            },
            {
                "name": "Data Analysis 3 Month",
                "common_name": "3 Month",
                "program_name": "Introduction to Data Analysis",
            },
            {
                "name": "Data Analysis 6 Month",
                "common_name": "6 Month",
                "program_name": "Introduction to Data Analysis",
            },
            {
                "name": "Data Analysis 10 Month",
                "common_name": "10 Month",
                "program_name": "Introduction to Data Analysis",
            },
            {
                "name": "Data Analysis 14 Month",
                "common_name": "14 Month",
                "program_name": "Introduction to Data Analysis",
            },
        ]
        rows = []
        for timeline in timeline_seed_data:
            row = {
                "timeline_name": timeline.get("name"),
                "program_id": Base.program_name_to_id.get(timeline.get("program_name")),
                "common_name": timeline.get("common_name"),
            }
            record = update_or_create(
                session,
                PaceTimeline,
                row,
                timeline_name=row.get("timeline_name"),
                program_id=row.get("program_id"),
            )
            rows.append(record[0])
        self.session_commit_with_rollback_on_unique(session)
        Base.pact_timeline_name_to_id = {row.timeline_name: row.id for row in rows}
