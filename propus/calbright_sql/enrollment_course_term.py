import enum
from sqlalchemy import ForeignKey, TIMESTAMP, UniqueConstraint, Enum, VARCHAR, INTEGER, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.course_version_section import CourseVersionSection
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.grade import Grade
from propus.calbright_sql.staff import Staff
from propus.calbright_sql.term import Term


class GradeStatus(enum.Enum):
    not_graded = "Not Graded"
    submitted = "Submitted"
    certified = "Certified"
    dropped = "Dropped"


class EnrollmentCourseTerm(Base):
    __tablename__ = "enrollment_course_term"

    enrollment_id = mapped_column(UUID, ForeignKey("enrollment.id"), index=True, nullable=False)
    enrollment = relationship(
        "Enrollment", backref="enrollment_enrollment_course_term", primaryjoin=enrollment_id == Enrollment.id
    )

    course_version_id = mapped_column(UUID, ForeignKey("course_version.id"), index=True, nullable=False)
    course_version = relationship(
        "CourseVersion",
        backref="course_version",
        primaryjoin=course_version_id == CourseVersion.id,
    )

    anthology_course_id = mapped_column(INTEGER, unique=True, index=True)
    grade_salesforce_id = mapped_column(VARCHAR(25), unique=True, index=True)
    progress = mapped_column(FLOAT, default=0.0)

    term_id = mapped_column(UUID, ForeignKey("term.id"), index=True, nullable=False)
    term = relationship("Term", backref="enrollment_course_term", primaryjoin=term_id == Term.id)

    grade_status = mapped_column(Enum(GradeStatus), nullable=False, index=True, default=GradeStatus.not_graded)

    instructor_id = mapped_column(UUID, ForeignKey("staff.id"), index=True)
    instructor = relationship("Staff", backref="enrollment_staff", primaryjoin=instructor_id == Staff.id)

    certified_by_id = mapped_column(UUID, ForeignKey("staff.id"), index=True)
    certified_by = relationship("Staff", backref="enrollment_certifier", primaryjoin=certified_by_id == Staff.id)

    grade_id = mapped_column(UUID, ForeignKey("grade.id"), index=True)
    grade = relationship("Grade", backref="enrollment_course_grade", primaryjoin=grade_id == Grade.id)

    withdraw_date = mapped_column(TIMESTAMP)
    drop_date = mapped_column(TIMESTAMP)
    grade_date = mapped_column(TIMESTAMP)
    certified_date = mapped_column(TIMESTAMP)

    course_version_section_id = mapped_column(UUID, ForeignKey("course_version_section.id"), index=True, nullable=True)
    course_version_section = relationship(
        "CourseVersionSection",
        backref="enrollment_course_term_section",
        primaryjoin=course_version_section_id == CourseVersionSection.id,
    )

    __table_args__ = (UniqueConstraint("enrollment_id", "course_version_id", "term_id", name="uniq_enrollment_course"),)
