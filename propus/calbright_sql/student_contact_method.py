from sqlalchemy import ForeignKey, VARCHAR, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.student import Student
from propus.calbright_sql.preferred_contact_method import PreferredContactMethod


class StudentContactMethod(Base):
    __tablename__ = "student_contact_method"

    contact_method_id = mapped_column(
        UUID, ForeignKey("preferred_contact_method.id"), nullable=False, primary_key=True, index=True
    )
    preferred_contact_method = relationship(
        "PreferredContactMethod",
        backref="preferred_contact_method_student",
        primaryjoin=contact_method_id == PreferredContactMethod.id,
    )

    ccc_id = mapped_column(VARCHAR(12), ForeignKey("student.ccc_id"), nullable=False, primary_key=True, index=True)
    student = relationship("Student", backref="student_preferred_contact_method", primaryjoin=ccc_id == Student.ccc_id)

    __table_args__ = (UniqueConstraint("contact_method_id", "ccc_id", name="uniq_student_contact_method"),)

    def __repr__(self) -> str:
        return f"<StudentContactMethod: {self.contact_method_id} - {self.ccc_id}>"
