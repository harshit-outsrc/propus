from sqlalchemy import DATE, VARCHAR
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.user import User  # noqa:F401


class Student(Base):
    __tablename__ = "student"

    ccc_id = mapped_column(VARCHAR(12), unique=True, primary_key=True, index=True, nullable=False)
    user = relationship("User", uselist=False, back_populates="student")

    ssn = mapped_column(VARCHAR(9))
    tax_id = mapped_column(VARCHAR)
    date_of_birth = mapped_column(DATE(), index=True)
    mobile_number = mapped_column(VARCHAR(10))
    home_phone_number = mapped_column(VARCHAR(10))

    def __repr__(self) -> str:
        return f"<Student: {self.ccc_id}>"
