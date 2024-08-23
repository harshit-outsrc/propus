"""convert varchar to boolean for ccc_application

Revision ID: ffda5c32701e
Revises: 38a60bb86098
Create Date: 2024-08-01 14:25:01.544897

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ffda5c32701e"
down_revision = "38a60bb86098"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "ccc_application",
        "res_status_change",
        existing_type=sa.VARCHAR(length=1),
        type_=sa.BOOLEAN(),
        existing_nullable=True,
        postgresql_using="res_status_change::boolean",
    )


def downgrade() -> None:
    op.alter_column(
        "ccc_application",
        "res_status_change",
        existing_type=sa.BOOLEAN(),
        type_=sa.VARCHAR(length=1),
        existing_nullable=True,
        postgresql_using="res_status_change::varchar(1)",
    )
