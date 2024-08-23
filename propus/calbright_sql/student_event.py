import enum
from sqlalchemy import ForeignKey, JSON, VARCHAR, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.student import Student
from propus.calbright_sql.scheduled_event import ScheduledEvent


class EventAttendance(enum.Enum):
    scheduled = "Scheduled"
    attended = "Attended"
    no_show = "No Show"
    cancel = "Cancel"


class StudentEvent(Base):
    __tablename__ = "student_event"

    ccc_id = mapped_column(VARCHAR(12), ForeignKey("student.ccc_id"), nullable=False, index=True)
    student = relationship("Student", backref="student_event_student", primaryjoin=ccc_id == Student.ccc_id)

    scheduled_event_id = mapped_column(UUID, ForeignKey("scheduled_event.id"), nullable=False, index=True)
    scheduled_event = relationship(
        "ScheduledEvent", backref="student_event_scheduled_event", primaryjoin=scheduled_event_id == ScheduledEvent.id
    )

    student_event_attendance = mapped_column(Enum(EventAttendance), nullable=False, default=EventAttendance.scheduled)

    # student_event_metadata can contain items like poll responses during the meeting or Q&A when scheduled
    student_event_metadata = mapped_column(JSON)
