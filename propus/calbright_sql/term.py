import asyncio
from sqlalchemy import String, DATE, INTEGER
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base
from propus.helpers.sql_alchemy import update_or_create


class Term(Base):
    __tablename__ = "term"

    term_name = mapped_column(String(16), nullable=False, unique=True)
    start_date = mapped_column(DATE, nullable=False, unique=True)
    end_date = mapped_column(DATE, nullable=False, unique=True)
    add_drop_date = mapped_column(DATE, unique=True)
    anthology_id = mapped_column(INTEGER, nullable=False, unique=True)

    def seed_data(self, session, anthology, **kwargs):
        from datetime import datetime

        academic_terms = asyncio.run(anthology.fetch_configurations("term"))
        if not academic_terms.get("value"):
            raise Exception("No Terms Returned from Anthology")
        start_date, end_date, add_drop = None, None, None
        for term in academic_terms.get("value"):
            if not (
                term.get("Code")
                and term.get("StartDate")  # noqa: W503
                and term.get("EndDate")  # noqa: W503
                and term.get("Id")  # noqa: W503
            ):
                continue
            if term.get("Code") == "TEST":
                continue
            if start_date is not None and term.get("Code") != "2020-21-TERM-01":
                for key, value in {
                    "StartDate": start_date,
                    "EndDate": end_date,
                    "AddDropDate": add_drop,
                }.items():
                    assert (
                        datetime.strptime(term.get(key).split("T")[0], "%Y-%m-%d") - value  # noqa: W503
                    ).days == 7, f'{term.get("Code")} has an error with it\'s {key}'
                assert (add_drop - start_date).days == 30
            start_date = datetime.strptime(term.get("StartDate").split("T")[0], "%Y-%m-%d")
            assert start_date.weekday() == 1
            end_date = datetime.strptime(term.get("EndDate").split("T")[0], "%Y-%m-%d")
            assert end_date.weekday() == 0 or "BETA" in term.get("Code")
            add_drop = term.get("AddDropDate")
            if add_drop:
                add_drop = datetime.strptime(add_drop.split("T")[0], "%Y-%m-%d")
                assert add_drop.weekday() == 3

            row = {
                "term_name": term.get("Code"),
                "start_date": start_date,
                "end_date": end_date,
                "add_drop_date": add_drop,
                "anthology_id": term.get("Id"),
            }

            update_or_create(
                session,
                Term,
                row,
                term_name=row.get("term_name"),
                anthology_id=row.get("anthology_id"),
            )
        self.session_commit_with_rollback_on_unique(session)
