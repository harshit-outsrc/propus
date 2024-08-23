"""Add Intended Program To User Table

Revision ID: e389c455df91
Revises: d689708501de
Create Date: 2024-07-11 14:15:50.855648

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e389c455df91"
down_revision = "d689708501de"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("intended_program_id", sa.UUID(), nullable=True))
    op.create_foreign_key(None, "user", "program", ["intended_program_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "user", type_="foreignkey")
    op.drop_column("user", "intended_program_id")
