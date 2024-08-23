"""is_test_user and kickoff_scheduled columns added

Revision ID: 9d06068a2874
Revises: e59a4041103c
Create Date: 2024-06-24 16:18:27.540369

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "9d06068a2874"
down_revision = "e59a4041103c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("enrollment", sa.Column("kickoff_scheduled", sa.BOOLEAN(), nullable=True))
    op.add_column("user", sa.Column("is_test_user", sa.BOOLEAN(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "is_test_user")
    op.drop_column("enrollment", "kickoff_scheduled")
