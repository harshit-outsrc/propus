import enum
from sqlalchemy import ForeignKey, VARCHAR, JSON, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.student import Student
from propus.calbright_sql.device import Device


class RequestStatus(enum.Enum):
    requested = "Requested"
    pending = "Pending Shipment"
    shipped = "Shipped"
    delivered = "Delivered"
    return_requested = "Return Requested"
    returned = "Returned"
    lost = "Lost"
    stolen = "Stolen"
    end_of_life = "End of Life"


class DeviceRequest(Base):
    __tablename__ = "device_request"

    ccc_id = mapped_column(VARCHAR(12), ForeignKey("student.ccc_id"), nullable=False, index=True, primary_key=True)
    student = relationship("Student", backref="user_device_request", primaryjoin=ccc_id == Student.ccc_id)

    device_id = mapped_column(UUID, ForeignKey("device.id"), primary_key=True)
    device = relationship("Device", backref="device_request_device", primaryjoin=device_id == Device.id)

    request_status = mapped_column(Enum(RequestStatus), nullable=False, default=RequestStatus.pending)

    delivery_tracking_number = mapped_column(VARCHAR(100))
    return_tracking_number = mapped_column(VARCHAR(100))
    request_metadata = mapped_column(JSON())

    __table_args__ = (UniqueConstraint("ccc_id", "device_id", name="uniq_student_device_id"),)
