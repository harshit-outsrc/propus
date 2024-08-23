import enum
from sqlalchemy import ForeignKey, VARCHAR, TIMESTAMP, FLOAT, INTEGER, Enum, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, backref

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment_status import EnrollmentStatus
from propus.calbright_sql.program_version import ProgramVersion
from propus.calbright_sql.student import Student
from propus.calbright_sql.term import Term
from propus.calbright_sql.pace_timeline import PaceTimeline


class LMS(enum.Enum):
    strut = "Strut"
    trailhead = "Trailhead"
    canvas = "Canvas"


class PreReqStatus(enum.Enum):
    waiting_support = "Waiting Support"
    pending = "Pending"
    approved = "Approved"
    denied = "Denied"


class Enrollment(Base):
    __tablename__ = "enrollment"

    sis_enrollment_id = mapped_column(INTEGER, index=True, unique=True)
    ccc_id = mapped_column(VARCHAR(12), ForeignKey("student.ccc_id"), nullable=False, index=True)
    student = relationship(
        "Student",
        backref=backref("enrollment_student", order_by="Enrollment.created_at.desc()"),
        primaryjoin=ccc_id == Student.ccc_id,
    )
    program_version_id = mapped_column(UUID, ForeignKey("program_version.id"), nullable=False)
    program_version = relationship(
        "ProgramVersion", backref="enrollment_program_version", primaryjoin=program_version_id == ProgramVersion.id
    )
    first_term_id = mapped_column(UUID, ForeignKey("term.id"), nullable=False, index=True)
    first_term = relationship("Term", backref="enrollment_term", primaryjoin=first_term_id == Term.id)
    enrollment_status_id = mapped_column(UUID, ForeignKey("enrollment_status.id"), nullable=False)
    enrollment_status = relationship(
        "EnrollmentStatus",
        backref="enrollment_status",
        primaryjoin=enrollment_status_id == EnrollmentStatus.id,
    )

    salesforce_course_version = mapped_column(VARCHAR(500))

    enrollment_salesforce_id = mapped_column(VARCHAR(25), unique=True, index=True)
    prereq_status = mapped_column(Enum(PreReqStatus))
    lms = mapped_column(Enum(LMS), nullable=False)

    kickoff_scheduled = mapped_column(BOOLEAN, default=False)

    first_saa = mapped_column(TIMESTAMP)
    last_saa = mapped_column(TIMESTAMP)
    first_lms_login = mapped_column(TIMESTAMP)
    last_lms_login = mapped_column(TIMESTAMP)

    progress = mapped_column(FLOAT, default=0.0)
    pace_timeline_id = mapped_column(UUID(), ForeignKey("pace_timeline.id"), index=True)
    pace_timeline = relationship(
        "PaceTimeline",
        backref="enrollment_pace_timeline",
        primaryjoin=pace_timeline_id == PaceTimeline.id,
    )
    enrollment_date = mapped_column(TIMESTAMP)
    drop_date = mapped_column(TIMESTAMP)
    completion_date = mapped_column(TIMESTAMP)
    withdrawn_date = mapped_column(TIMESTAMP)
