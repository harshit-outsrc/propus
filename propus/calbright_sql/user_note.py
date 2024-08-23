from sqlalchemy import ForeignKey, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.user import User


class UserNote(Base):
    __tablename__ = "user_note"
    # Using user.id here and in the next id because we want to track back and forth between students and staff
    author_id = mapped_column(UUID, ForeignKey("user.id"), nullable=False, index=True)
    author = relationship("User", backref="author_user", primaryjoin=author_id == User.id)

    recipient_id = mapped_column(UUID, ForeignKey("user.id"), index=True)
    recipient = relationship("User", backref="recipient_user", primaryjoin=recipient_id == User.id)

    note = mapped_column(TEXT, nullable=False)
