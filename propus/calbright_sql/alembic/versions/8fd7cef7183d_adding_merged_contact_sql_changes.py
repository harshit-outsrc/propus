"""
Adding merged contact sql changes

Revision ID: 8fd7cef7183d
Revises: 605a6ef75c1f
Create Date: 2024-05-24 13:54:45.153599

"""

from alembic import op
import sqlalchemy as sa

from propus.calbright_sql.seed_data.views import student_info_view, student_enrollment_view


# revision identifiers, used by Alembic.
revision = "8fd7cef7183d"
down_revision = "605a6ef75c1f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP VIEW IF EXISTS student_enrollment;DROP VIEW IF EXISTS student_info;")
    op.alter_column(
        "student",
        "ip_address",
        existing_type=sa.VARCHAR(length=15),
        type_=sa.VARCHAR(length=50),
        existing_nullable=True,
    )
    op.add_column("user", sa.Column("is_duplicate_record", sa.BOOLEAN(), nullable=True))
    op.add_column("user", sa.Column("merged_user_id", sa.UUID(), nullable=True))
    op.create_index(op.f("ix_user_merged_user_id"), "user", ["merged_user_id"], unique=False)
    op.create_foreign_key("merged_user_id", "user", "user", ["merged_user_id"], ["id"])
    op.execute(student_info_view)
    op.execute(student_enrollment_view)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS student_enrollment;DROP VIEW IF EXISTS student_info;")
    op.drop_constraint("merged_user_id", "user", type_="foreignkey")
    op.drop_index(op.f("ix_user_merged_user_id"), table_name="user")
    op.drop_column("user", "merged_user_id")
    op.drop_column("user", "is_duplicate_record")
    op.alter_column(
        "student",
        "ip_address",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.VARCHAR(length=15),
        existing_nullable=True,
    )
    op.execute(student_info_view)
    op.execute(student_enrollment_view)
