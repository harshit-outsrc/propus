import enum
from sqlalchemy import String, UUID, ForeignKey, Enum, VARCHAR, FLOAT, BOOLEAN, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.competency import Competency
from propus.calbright_sql.enrollment import LMS


class AssessmentType(enum.Enum):
    summative = "Summative"
    formative = "Formative"
    final_grade = "Final Grade"
    pre_assessment = "Pre-Assessment"
    milestone = "Milestone"
    observable_skill = "Observable Skill"
    discussion = "Discussion"


class LmsType(enum.Enum):
    assignment = "Assignment"
    quiz = "Quiz"
    discussion = "Discussion"


class Assessment(Base):
    __tablename__ = "assessment"

    competency_id = mapped_column(UUID, ForeignKey("competency.id"), index=True, nullable=False)
    competency_assessment = relationship(
        "Competency", backref="competency_assessment", primaryjoin=competency_id == Competency.id
    )

    name = mapped_column(String, nullable=False)
    assessment_type = mapped_column(Enum(AssessmentType), nullable=False)

    # LMS Info/ID
    lms = mapped_column(Enum(LMS), nullable=True)
    lms_id = mapped_column(VARCHAR(100), index=True, unique=False, nullable=True)
    lms_type = mapped_column(Enum(LmsType), nullable=True)

    # the required percentage for a student to be considered as having passed the assessment
    required_percentage_to_pass = mapped_column(FLOAT, default=0.0)

    # booleans for if this assignment is the final summative assignment of the course
    is_last_summative_of_course = mapped_column(BOOLEAN, default=False)

    active = mapped_column(BOOLEAN, default=True)

    __table_args__ = (UniqueConstraint("lms_id", "lms_type", name="uniq_lms_id_lms_type"),)
