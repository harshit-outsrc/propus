"""Expressed Interest Changes

Revision ID: 93a519766633
Revises: 39c844923a6c
Create Date: 2024-07-08 14:29:30.854119

"""

from alembic import op
import sqlalchemy as sa

from propus.calbright_sql.seed_data.views import student_info_view, student_enrollment_view

# revision identifiers, used by Alembic.
revision = "93a519766633"
down_revision = "39c844923a6c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP VIEW IF EXISTS student_enrollment;DROP VIEW IF EXISTS student_info;")
    op.add_column("express_interest", sa.Column("ip_address", sa.VARCHAR(length=50), nullable=True))
    op.drop_column("student", "ip_address")
    op.add_column("user", sa.Column("call_opt_out", sa.BOOLEAN(), nullable=True))
    op.add_column("user", sa.Column("sms_opt_out", sa.BOOLEAN(), nullable=True))
    op.execute(student_info_view)
    op.execute(student_enrollment_view)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS student_enrollment;DROP VIEW IF EXISTS student_info;")
    op.drop_column("user", "sms_opt_out")
    op.drop_column("user", "call_opt_out")
    op.add_column("student", sa.Column("ip_address", sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column("express_interest", "ip_address")
    op.execute(student_info_view)
    op.execute(student_enrollment_view)
