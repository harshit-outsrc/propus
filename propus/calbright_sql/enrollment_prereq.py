from sqlalchemy import ForeignKey, TIMESTAMP, TEXT, Enum, INTEGER
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment import PreReqStatus
from propus.calbright_sql.staff import Staff
from propus.calbright_sql.user import User
from propus.calbright_sql.program import Program


class EnrollmentPreReq(Base):
    __tablename__ = "enrollment_prereq"

    user_id = mapped_column(UUID, ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="user_enrollmentprereq", primaryjoin=user_id == User.id)

    program_id = mapped_column(UUID, ForeignKey("program.id"), index=True, nullable=False)
    program = relationship("Program", backref="program_enrollmentprereq", primaryjoin=program_id == Program.id)

    status = mapped_column(Enum(PreReqStatus), nullable=True, default=PreReqStatus.pending)
    response = mapped_column(TEXT)
    prereq_denied_reason = mapped_column(TEXT)
    prereq_denied_response = mapped_column(TEXT)
    assigned_team = mapped_column(TEXT)

    reviewer_id = mapped_column(UUID, ForeignKey("staff.id"))
    reviewer = relationship("Staff", backref="enrollment_reviewer", primaryjoin=reviewer_id == Staff.id)
    review_timestamp = mapped_column(TIMESTAMP)

    cert_submission_attempts = mapped_column(INTEGER)
    exp_proof_submission_attempts = mapped_column(INTEGER)
