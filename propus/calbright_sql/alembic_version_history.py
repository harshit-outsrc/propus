import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base


class AlembicVersionHistoryRevisionType(enum.Enum):
    """
    Alembic Version History Revision Type populated whenever an upgrade or downgrade revision is carried out
    """

    downgrade = "downgrade"
    upgrade = "upgrade"


class AlembicVersionHistory(Base):
    __tablename__ = "alembic_version_history"

    version_number = mapped_column(String(32), nullable=False)
    revision_type = mapped_column(Enum(AlembicVersionHistoryRevisionType), nullable=False)
    message = mapped_column(String)
