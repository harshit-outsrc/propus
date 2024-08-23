"""change enrollment_prereq foreign key to user table

Revision ID: 38a60bb86098
Revises: dcb9d9452147
Create Date: 2024-08-01 13:47:19.121789

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "38a60bb86098"
down_revision = "dcb9d9452147"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("enrollment_prereq", sa.Column("user_id", sa.UUID(), nullable=False))
    op.add_column("enrollment_prereq", sa.Column("program_id", sa.UUID(), nullable=False))
    op.drop_index("ix_enrollment_prereq_enrollment_id", table_name="enrollment_prereq")
    op.create_index(op.f("ix_enrollment_prereq_program_id"), "enrollment_prereq", ["program_id"], unique=False)
    op.create_index(op.f("ix_enrollment_prereq_user_id"), "enrollment_prereq", ["user_id"], unique=False)
    op.drop_constraint("enrollment_prereq_enrollment_id_fkey", "enrollment_prereq", type_="foreignkey")
    op.create_foreign_key(None, "enrollment_prereq", "user", ["user_id"], ["id"])
    op.create_foreign_key(None, "enrollment_prereq", "program", ["program_id"], ["id"])
    op.drop_column("enrollment_prereq", "enrollment_id")


def downgrade() -> None:
    op.add_column("enrollment_prereq", sa.Column("enrollment_id", sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, "enrollment_prereq", type_="foreignkey")
    op.drop_constraint(None, "enrollment_prereq", type_="foreignkey")
    op.create_foreign_key(
        "enrollment_prereq_enrollment_id_fkey", "enrollment_prereq", "enrollment", ["enrollment_id"], ["id"]
    )
    op.drop_index(op.f("ix_enrollment_prereq_user_id"), table_name="enrollment_prereq")
    op.drop_index(op.f("ix_enrollment_prereq_program_id"), table_name="enrollment_prereq")
    op.create_index("ix_enrollment_prereq_enrollment_id", "enrollment_prereq", ["enrollment_id"], unique=False)
    op.drop_column("enrollment_prereq", "program_id")
    op.drop_column("enrollment_prereq", "user_id")
