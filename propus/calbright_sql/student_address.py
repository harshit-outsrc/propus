from sqlalchemy import BOOLEAN, ForeignKey, VARCHAR, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.address import Address
from propus.calbright_sql.student import Student


class StudentAddress(Base):
    __tablename__ = "student_address"

    student_id = mapped_column(
        VARCHAR,
        ForeignKey("student.ccc_id"),
        index=True,
        nullable=False,
    )
    student = relationship("Student", backref="student_address", primaryjoin=student_id == Student.ccc_id)

    address_id = mapped_column(UUID, ForeignKey("address.id"), index=True, nullable=False, primary_key=True)
    address = relationship("Address", backref="address_student", primaryjoin=address_id == Address.id)

    current = mapped_column(BOOLEAN, nullable=False, default=True)
    valid = mapped_column(BOOLEAN, nullable=False, default=True)
    address_type = mapped_column(VARCHAR(25), nullable=False, default="MailingAddress")

    __table_args__ = (UniqueConstraint("address_id", "valid", name="uniq_student_valid"),)

    def __repr__(self) -> str:
        return f"<StudentAddress: {self.student_id} - {self.address_id}>"
