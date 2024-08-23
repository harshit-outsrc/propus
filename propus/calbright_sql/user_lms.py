from sqlalchemy import VARCHAR, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment import LMS
from propus.calbright_sql.user import User


class UserLms(Base):
    __tablename__ = "user_lms"

    lms = mapped_column(Enum(LMS), nullable=False, index=True)
    lms_id = mapped_column(VARCHAR(100), index=True)
    user_id = mapped_column(UUID(), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="user_lms", primaryjoin=user_id == User.id)

    __table_args__ = (UniqueConstraint("lms", "lms_id", name="uniq_lms_lms_id"),)
