import enum

from sqlalchemy import ForeignKey, Enum, VARCHAR, INTEGER, FLOAT, UUID, TIMESTAMP
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.assessment import Assessment
from propus.calbright_sql.enrollment import Enrollment, LMS


class AssessmentSubmissionStatus(enum.Enum):
    submitted = "Submitted"
    passed = "Passed"
    failed = "Failed"


class AssessmentSubmission(Base):
    __tablename__ = "assessment_submission"

    enrollment_id = mapped_column(UUID, ForeignKey("enrollment.id"), index=True, nullable=False)
    enrollment = relationship(
        "Enrollment", backref="enrollment_assessment_submission", primaryjoin=enrollment_id == Enrollment.id
    )

    assessment_id = mapped_column(UUID, ForeignKey("assessment.id"), index=True, nullable=False)
    assessment = relationship(
        "Assessment", backref="assessment_assessment_submission", primaryjoin=assessment_id == Assessment.id
    )

    attempt = mapped_column(INTEGER, nullable=False)
    score = mapped_column(FLOAT, nullable=True)
    grade = mapped_column(VARCHAR(10), nullable=True)
    submission_timestamp = mapped_column(TIMESTAMP, nullable=False)

    lms = mapped_column(Enum(LMS), nullable=True)
    lms_id = mapped_column(VARCHAR(100), index=True, unique=True, nullable=True)
    # TODO: double check if this is globally unique or per student....

    status = mapped_column(Enum(AssessmentSubmissionStatus), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<AssessmentSubmission: {self.assessment_id} - {self.id}>"
