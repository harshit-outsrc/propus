"""ccc_application table adjustments

Revision ID: dcb9d9452147
Revises: f141bd683556
Create Date: 2024-08-01 09:06:57.898075

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dcb9d9452147"
down_revision = "f141bd683556"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "ccc_application", "term_id", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "major_id", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "college_count", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "hs_attendance", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application",
        "race_group",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.VARCHAR(length=80),
        existing_nullable=True,
    )
    op.alter_column(
        "ccc_application", "res_area_a", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "res_area_b", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "res_area_c", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "res_area_d", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "fraud_status", existing_type=sa.INTEGER(), type_=sa.DECIMAL(), existing_nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "ccc_application", "fraud_status", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "res_area_d", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "res_area_c", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "res_area_b", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "res_area_a", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application",
        "race_group",
        existing_type=sa.VARCHAR(length=80),
        type_=sa.VARCHAR(length=50),
        existing_nullable=True,
    )
    op.alter_column(
        "ccc_application", "hs_attendance", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "college_count", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "major_id", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
    op.alter_column(
        "ccc_application", "term_id", existing_type=sa.DECIMAL(), type_=sa.INTEGER(), existing_nullable=True
    )
