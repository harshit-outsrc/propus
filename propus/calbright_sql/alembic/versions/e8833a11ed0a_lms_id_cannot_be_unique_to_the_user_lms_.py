"""lms_id cannot be unique to the user lms table

Revision ID: e8833a11ed0a
Revises: e389c455df91
Create Date: 2024-07-12 09:17:43.789147

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "e8833a11ed0a"
down_revision = "e389c455df91"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("uniq_lms_id_for_user", "user_lms", type_="unique")
    op.drop_index("ix_user_lms_lms_id", table_name="user_lms")
    op.create_index(op.f("ix_user_lms_lms_id"), "user_lms", ["lms_id"], unique=False)
    op.create_index(op.f("ix_user_lms_lms"), "user_lms", ["lms"], unique=False)
    op.create_unique_constraint("uniq_lms_lms_id", "user_lms", ["lms", "lms_id"])


def downgrade() -> None:
    op.drop_constraint("uniq_lms_lms_id", "user_lms", type_="unique")
    op.drop_index(op.f("ix_user_lms_lms"), table_name="user_lms")
    op.drop_index(op.f("ix_user_lms_lms_id"), table_name="user_lms")
    op.create_index("ix_user_lms_lms_id", "user_lms", ["lms_id"], unique=True)
    op.create_unique_constraint("uniq_lms_id_for_user", "user_lms", ["lms", "lms_id", "user_id"])
