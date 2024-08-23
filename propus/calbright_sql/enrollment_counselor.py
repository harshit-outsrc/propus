from sqlalchemy import BOOLEAN, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.staff import Staff


class EnrollmentCounselor(Base):
    __tablename__ = "enrollment_counselor"

    enrollment_id = mapped_column(UUID, ForeignKey("enrollment.id"), index=True, nullable=False)
    enrollment = relationship("Enrollment", backref="counselor_enrollment", primaryjoin=enrollment_id == Enrollment.id)

    counselor_id = mapped_column(UUID, ForeignKey("staff.id"))
    counselor = relationship("Staff", backref="enrollment_counselor", primaryjoin=counselor_id == Staff.id)

    current_counselor = mapped_column(BOOLEAN, nullable=False, default=True)

    __table_args__ = (UniqueConstraint("enrollment_id", "current_counselor", name="uniq_enrollment_counselor"),)

    def __repr__(self) -> str:
        return f"<EnrollmentCounselor: {self.enrollment_id} - {self.counselor_id}>"
