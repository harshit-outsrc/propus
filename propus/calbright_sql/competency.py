import enum

from sqlalchemy import ForeignKey
from sqlalchemy import VARCHAR, TEXT, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.enrollment import LMS

from propus.calbright_sql.seed_data.competency import COMPETENTCY_TO_COURSE_VERSION, TRAILHEAD_DATA
from propus.helpers.sql_alchemy import update_or_create


class CompetencyType(enum.Enum):
    competency = "Competency"
    durable_skill = "Durable Skill"
    final_grade = "Final Grade"
    observable_skill = "Observable Skill"


class Competency(Base):
    __tablename__ = "competency"

    course_version_id = mapped_column(UUID, ForeignKey("course_version.id"), index=True, nullable=False)
    course_version_competency = relationship(
        "CourseVersion",
        backref="course_version_competency",
        primaryjoin=course_version_id == CourseVersion.id,
    )

    competency_name = mapped_column(VARCHAR(500), nullable=False)
    description = mapped_column(TEXT)
    state = mapped_column(VARCHAR(25), default="published")
    lms = mapped_column(Enum(LMS), nullable=False)
    lms_id = mapped_column(VARCHAR(50), index=True, unique=True)
    is_active = mapped_column(Boolean, index=True, default=True)
    competency_type = mapped_column(Enum(CompetencyType), nullable=True)

    @staticmethod
    def fetch_strut_competencies(strut):
        start = 0
        response = strut.fetch_competencies(start=start, shallow=False)
        return [
            {
                "lms": LMS.strut,
                "lms_id": str(c.get("id")),
                "state": c.get("state"),
                "description": c.get("description"),
                "competency_name": c.get("title"),
            }
            for c in response
            if c.get("state") in ["retired", "published"]
        ]

    def seed_data(self, session, **kwargs):
        competency_seed_data = self.fetch_strut_competencies(kwargs.get("strut"))
        for lms_id, competency in TRAILHEAD_DATA.items():
            competency_seed_data.append(
                {
                    "lms": LMS.trailhead,
                    "lms_id": lms_id,
                    "competency_name": competency.get("name"),
                    "course_version_id": Base.course_versions.get(competency.get("course_version")).id,
                }
            )
        rows = []
        for row in competency_seed_data:
            if not row.get("course_version_competency") and not COMPETENTCY_TO_COURSE_VERSION.get(row.get("lms_id")):
                continue
            row["course_version_id"] = Base.course_versions.get(COMPETENTCY_TO_COURSE_VERSION.get(row.get("lms_id"))).id
            record = update_or_create(
                session,
                Competency,
                row,
                competency_name=row.get("competency_name"),
                course_version_id=row.get("course_version_id"),
                lms_id=row.get("lms_id"),
            )
            rows.append(record[0])
        was_successful = self.session_commit_with_rollback_on_unique(session)
        if was_successful:
            Base.competency_name_to_id = {row.competency_name: row.id for row in rows}
