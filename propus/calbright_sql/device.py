import enum
from sqlalchemy import VARCHAR, Enum, TEXT
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base


class DeviceType(enum.Enum):
    chromebook = "Chromebook"
    hotspot = "Hotspot"
    windows = "Windows"
    mac = "Mac"


class Device(Base):
    __tablename__ = "device"

    device_type = mapped_column(Enum(DeviceType), nullable=False)
    asset_id = mapped_column(VARCHAR(100), nullable=False, unique=True)
    model = mapped_column(VARCHAR(150), nullable=False)
    serial_number = mapped_column(VARCHAR(100), nullable=False, unique=True)
    imei = mapped_column(VARCHAR(22), nullable=False, unique=True)
    notes = mapped_column(TEXT)
