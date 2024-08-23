import enum
from sqlalchemy import ForeignKey, UniqueConstraint, Enum, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.course import Course
from propus.calbright_sql.staff import Staff


class InstructorType(enum.Enum):
    primary = "Primary"
    adjunct = "Adjunct"


class InstructorCourse(Base):
    __tablename__ = "instructor_course"

    course_id = mapped_column(UUID, ForeignKey("course.id"), index=True, nullable=False)
    course = relationship("Course", backref="course_instructor", primaryjoin=course_id == Course.id)

    instructor_id = mapped_column(UUID, ForeignKey("staff.id"))
    instructor = relationship("Staff", backref="instructor_course", primaryjoin=instructor_id == Staff.id)

    instructor_type = mapped_column(Enum(InstructorType), nullable=False)
    active = mapped_column(BOOLEAN, default=True)
    canvas_instructor = mapped_column(BOOLEAN, default=True)

    __table_args__ = (UniqueConstraint("course_id", "instructor_id", name="uniq_course_instructor"),)
