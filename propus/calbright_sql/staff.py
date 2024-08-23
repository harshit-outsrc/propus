import enum
from sqlalchemy import VARCHAR, Enum, Boolean
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base


class StaffTitle(enum.Enum):
    instructor = "Instructor"
    counselor = "Success Counselor"
    student_support = "Student Support"
    dean_of_enrollment_services = "Dean of Enrollment Services"
    automation = "Automation Account"


class StaffRole(enum.Enum):
    accessability = "Accessability Services"
    veteran = "Veteran Services"


class Staff(Base):
    """
    Staff table will host all Calbright staff information (Student services, Instructors, etc.)
    """

    __tablename__ = "staff"
    user = relationship("User", uselist=False, back_populates="staff")

    staff_title = mapped_column(Enum(StaffTitle), nullable=False)
    staff_role = mapped_column(Enum(StaffRole))
    calendly_link = mapped_column(VARCHAR(250), unique=True)
    staff_slack_link = mapped_column(VARCHAR(100))
    availability = mapped_column(VARCHAR(30))
    active_staff = mapped_column(Boolean, nullable=False, default=True)
