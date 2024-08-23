from sqlalchemy import ForeignKey, VARCHAR, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.student import Student
from propus.calbright_sql.preferred_contact_time import PreferredContactTime


class StudentContactTime(Base):
    __tablename__ = "student_contact_time"

    contact_time_id = mapped_column(
        UUID, ForeignKey("preferred_contact_time.id"), nullable=False, primary_key=True, index=True
    )
    preferred_contact_time = relationship(
        "PreferredContactTime",
        backref="preferred_contact_time_student",
        primaryjoin=contact_time_id == PreferredContactTime.id,
    )

    ccc_id = mapped_column(VARCHAR(12), ForeignKey("student.ccc_id"), nullable=False, primary_key=True, index=True)
    student = relationship(
        "Student",
        backref="student_preferred_contact_time",
        primaryjoin=ccc_id == Student.ccc_id,
    )

    __table_args__ = (UniqueConstraint("contact_time_id", "ccc_id", name="uniq_student_contact_time"),)

    def __repr__(self) -> str:
        return f"<StudentContactTime: {self.contact_time_id} - {self.ccc_id}>"
