"""adding instructor course table

Revision ID: 39c844923a6c
Revises: 9d06068a2874
Create Date: 2024-06-27 09:44:50.394201

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.session import Session

from propus.calbright_sql.seed_data.staff_ingestion import ingest_staff_data

# revision identifiers, used by Alembic.
revision = "39c844923a6c"
down_revision = "9d06068a2874"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sa.Enum("primary", "adjunct", name="instructortype").create(op.get_bind())
    op.create_table(
        "instructor_course",
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("instructor_id", sa.UUID(), nullable=True),
        sa.Column(
            "instructor_type",
            postgresql.ENUM("primary", "adjunct", name="instructortype", create_type=False),
            nullable=False,
        ),
        sa.Column("active", sa.BOOLEAN(), nullable=True),
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=True),
        sa.Column("modified_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["instructor_id"],
            ["staff.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("course_id", "instructor_id", name="uniq_course_instructor"),
    )
    op.create_index(op.f("ix_instructor_course_course_id"), "instructor_course", ["course_id"], unique=False)
    op.create_index(op.f("ix_instructor_course_id"), "instructor_course", ["id"], unique=False)
    ingest_staff_data(Session(bind=op.get_bind()))


def downgrade() -> None:
    op.drop_index(op.f("ix_instructor_course_id"), table_name="instructor_course")
    op.drop_index(op.f("ix_instructor_course_course_id"), table_name="instructor_course")
    op.drop_table("instructor_course")
    sa.Enum("primary", "adjunct", name="instructortype").drop(op.get_bind())
