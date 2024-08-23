"""adding lms field to program version course

Revision ID: 7b10e50b05df
Revises: 89ef553a69c8
Create Date: 2024-06-11 18:37:48.739729

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7b10e50b05df"
down_revision = "89ef553a69c8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("program_version_course", sa.Column("is_first_course_in_program", sa.BOOLEAN(), nullable=True))
    op.add_column(
        "program_version_course",
        sa.Column("lms", postgresql.ENUM("strut", "trailhead", "canvas", name="lms", create_type=False), nullable=True),
    )
    op.add_column("program_version_course", sa.Column("lms_id", sa.VARCHAR(length=100), nullable=True))
    op.create_index(op.f("ix_program_version_course_lms_id"), "program_version_course", ["lms_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_program_version_course_lms_id"), table_name="program_version_course")
    op.drop_column("program_version_course", "lms_id")
    op.drop_column("program_version_course", "lms")
    op.drop_column("program_version_course", "is_first_course_in_program")
