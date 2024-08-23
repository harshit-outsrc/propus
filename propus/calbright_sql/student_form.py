import enum
from sqlalchemy import ForeignKey, JSON, VARCHAR, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.student import Student


class FormStatus(enum.Enum):
    draft = "draft"
    awaiting_signature = "awaiting_signature"
    completed = "completed"


class FormType(enum.Enum):
    csep = "CSEP"
    dpau = "DPAU"


class StudentForm(Base):
    __tablename__ = "student_form"
    form_id = mapped_column(VARCHAR(50), nullable=False, primary_key=True, index=True)

    ccc_id = mapped_column(VARCHAR(12), ForeignKey("student.ccc_id"), nullable=False)
    student = relationship("Student", backref="student_form_student", primaryjoin=ccc_id == Student.ccc_id)

    enrollment_id = mapped_column(UUID, ForeignKey("enrollment.id"), index=True)
    enrollment = relationship("Enrollment", backref="enrollment_csep", primaryjoin=enrollment_id == Enrollment.id)

    form_type = mapped_column(Enum(FormType), nullable=False)
    form_status = mapped_column(Enum(FormStatus), nullable=False)
    document_url = mapped_column(VARCHAR(250))
    form_metadata = mapped_column(JSON)
