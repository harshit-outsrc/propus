from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.ethnicity import Ethnicity
from propus.calbright_sql.student import Student


class StudentEthnicity(Base):
    __tablename__ = "student_ethnicity"

    student_id = mapped_column(
        VARCHAR,
        ForeignKey("student.ccc_id"),
        index=True,
        nullable=False,
        primary_key=True,
    )
    student = relationship("Student", backref="student_ethnicity", primaryjoin=student_id == Student.ccc_id)

    ethnicity_id = mapped_column(UUID(), ForeignKey("ethnicity.id"), index=True)
    ethnicity = relationship(
        "Ethnicity",
        backref="ethnicity_student",
        primaryjoin=ethnicity_id == Ethnicity.id,
    )
    __table_args__ = (UniqueConstraint("student_id", "ethnicity_id", name="uniq_student_ethnicity"),)

    def __repr__(self) -> str:
        return f"<StudentEthnicity: {self.student_id} - {self.ethnicity_id}>"
