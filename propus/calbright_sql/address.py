from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base


class Address(Base):
    __tablename__ = "address"

    address1 = mapped_column(String, nullable=False)
    address2 = mapped_column(String)
    city = mapped_column(String, nullable=False)
    state = mapped_column(String, nullable=False)
    zip = mapped_column(String, nullable=False)
    county = mapped_column(String)
    country = mapped_column(String, nullable=False, default="USA")
