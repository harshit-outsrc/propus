from sqlalchemy import ForeignKey, VARCHAR, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.event import Event
from propus.calbright_sql.staff import Staff


class ScheduledEvent(Base):
    """
    Table to map the static event with calendly data (i.e. title, description) to the specific event with a date
    and time, which then can be attributed to a user who has signed up to attend
    """

    __tablename__ = "scheduled_event"

    event_id = mapped_column(UUID, ForeignKey("event.id"), nullable=False, index=True)
    event = relationship("Event", backref="scheduled_event_event", primaryjoin=event_id == Event.id)

    event_reference_id = mapped_column(VARCHAR(250), index=True)  # ID reference from calendar provider (i.e.  zoom id)

    host_id = mapped_column(UUID, ForeignKey("staff.id"))
    host = relationship("Staff", backref="scheduled_event_host", primaryjoin=host_id == Staff.id)

    start_time = mapped_column(TIMESTAMP, nullable=False, index=True)
    end_time = mapped_column(TIMESTAMP, nullable=False, index=True)
    subject = mapped_column(VARCHAR(50))
    scheduled_event_metadata = mapped_column(JSON)  # Host this event specific data (i.e. zoom meeting info)
