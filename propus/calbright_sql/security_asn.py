import csv
import os

from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.etl import get_bool_or_none, get_int_or_none, get_string_or_none
from propus.helpers.sql_alchemy import update_or_create


class ASN(Base):
    __tablename__ = "security_asn"
    asn = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    flag = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.asn}>"

    def seed_data(self, session, **kwargs):
        seed_file = f"{os.path.dirname(os.path.abspath(__file__))}/seed_data/ASN-Export-2023-05-31.csv"

        rows = []
        with open(seed_file, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = {
                    "asn": get_int_or_none(row.get("ASN")),
                    "flag": get_bool_or_none(row.get("Flag")),
                    "created_at": get_string_or_none(row.get("Added")),
                }
                record = update_or_create(
                    session,
                    ASN,
                    row,
                    asn=row.get("asn"),
                )
                rows.append(record[0])
        self.session_commit_with_rollback_on_unique(session)
