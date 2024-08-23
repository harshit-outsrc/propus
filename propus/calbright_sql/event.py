import enum
from sqlalchemy import VARCHAR, Enum, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.event_type import EventType
from propus.calbright_sql.user import User


class EventSource(enum.Enum):
    strut = "Strut"
    trailhead = "Trailhead"
    canvas = "Canvas"
    skillsway = "Skillsway"
    calendly = "Calendly"
    dialpad = "Dialpad"
    twilio = "Twilio"
    zoom = "Zoom"
    gcal = "GCal"


class Event(Base):
    __tablename__ = "event"

    user_id = mapped_column(UUID, ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="user_event", primaryjoin=user_id == User.id)

    enrollment_id = mapped_column(UUID, ForeignKey("enrollment.id"), index=True)
    enrollment = relationship("Enrollment", backref="enrollment_Event", primaryjoin=enrollment_id == Enrollment.id)

    event_id = mapped_column(VARCHAR(100), nullable=False, unique=True)
    event_source = mapped_column(Enum(EventSource), nullable=False)

    event_type_id = mapped_column(UUID, ForeignKey("event_type.id"), index=True)
    event_type = relationship("EventType", backref="event_type", primaryjoin=event_type_id == EventType.id)

    event_date = mapped_column(TIMESTAMP, nullable=False, index=True)
    event_metadata = mapped_column(JSON)
