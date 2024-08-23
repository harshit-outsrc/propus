import inspect

import sqlalchemy
from sqlalchemy import text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.exc import IntegrityError

from propus import Logging

logger = Logging.get_logger("propus/sql/calbright")


class orm_mixin_class(object):
    """
    Additional functionality wanted in orm classes (that inherit from Base).
    Adapted from: https://stackoverflow.com/a/27947295
    Accessed 06/06/2023
    """

    @classmethod
    def col_names(cls):
        """
        Get info about the orm class (as opposed to the database table it is mapped to).

        Returns:
            list: orm class attribute names
        """
        column_names = []
        member_pairs = inspect.getmembers(cls)
        for name, type in member_pairs:
            try:
                inspected_type = sqlalchemy.inspection.inspect(type)
                if isinstance(inspected_type, sqlalchemy.orm.attributes.QueryableAttribute) and not isinstance(
                    inspected_type.property, sqlalchemy.orm.RelationshipProperty
                ):
                    column_names.append(name)
            except Exception:
                pass

        return column_names


class Base(DeclarativeBase, orm_mixin_class):
    __abstract__ = True

    id = mapped_column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, index=True)
    created_at = mapped_column(TIMESTAMP(), server_default=text("NOW()"))
    modified_at = mapped_column(TIMESTAMP(), server_default=text("NOW()"))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.id}>"

    def to_dict(self):
        return {k: getattr(self, k) for k in self.col_names()}

    @staticmethod
    def session_commit_with_rollback_on_unique(session) -> bool:
        """
        Run a session commit and rollback when the commit fails.

        Args:
            session (SQLAlchemy.session): session of the SQLAlchemy session connection

        Returns:
            bool: Returns True is commit was successful else Fals
        """
        try:
            session.commit()
        except IntegrityError as e:
            if "UniqueViolation" not in str(e):
                raise e
            session.rollback()  # clearing the session so the next commit does not fail
            logger.error(e)
            return False
        return True
