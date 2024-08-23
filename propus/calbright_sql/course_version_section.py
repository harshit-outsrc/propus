from sqlalchemy import ForeignKey, VARCHAR, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment import LMS
from propus.calbright_sql.program_version_course import ProgramVersionCourse
from propus.calbright_sql.staff import Staff


class CourseVersionSection(Base):
    __tablename__ = "course_version_section"

    program_version_course_id = mapped_column(
        UUID,
        ForeignKey("program_version_course.id"),
        index=True,
        nullable=False,
    )
    program_version_course = relationship(
        "ProgramVersionCourse",
        backref="section_program_version_course",
        primaryjoin=program_version_course_id == ProgramVersionCourse.id,
    )

    instructor_id = mapped_column(UUID, ForeignKey("staff.id"), index=True, nullable=False)
    instructor = relationship("Staff", backref="course_version_section_staff", primaryjoin=instructor_id == Staff.id)
    instructor_enrollment_lms_id = mapped_column(VARCHAR(100), index=True, unique=True, nullable=True)

    section_id = mapped_column(VARCHAR(100), index=True, unique=False)
    section_name = mapped_column(VARCHAR(200), index=True, unique=True)

    lms = mapped_column(Enum(LMS), nullable=True)
    lms_id = mapped_column(VARCHAR(100), index=True, unique=True, nullable=True)

    sis_id = mapped_column(VARCHAR(100), index=True, unique=True, nullable=True)  # i.e. Anthology section ID

    __table_args__ = (
        UniqueConstraint("program_version_course_id", "instructor_id", name="uniq_instructor_program_version_course"),
    )
