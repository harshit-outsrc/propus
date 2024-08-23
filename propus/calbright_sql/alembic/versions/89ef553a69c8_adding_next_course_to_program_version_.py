"""adding next course to program_version_course

Revision ID: 89ef553a69c8
Revises: 20481bc8a72b
Create Date: 2024-06-10 15:43:47.314796

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "89ef553a69c8"
down_revision = "20481bc8a72b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE IF EXISTS public.program_version_course DROP CONSTRAINT IF EXISTS program_version_course_pkey;
        ALTER TABLE IF EXISTS public.program_version_course ADD PRIMARY KEY (id);
    """
    )

    op.add_column("program_version_course", sa.Column("next_program_version_course_id", sa.UUID(), nullable=True))
    op.create_index(
        op.f("ix_program_version_course_next_program_version_course_id"),
        "program_version_course",
        ["next_program_version_course_id"],
        unique=False,
    )
    op.create_unique_constraint(
        "uniq_program_course_version", "program_version_course", ["program_version_id", "course_version_id"]
    )
    op.create_foreign_key(
        "next_program_version_course_id",
        "program_version_course",
        "program_version_course",
        ["next_program_version_course_id"],
        ["id"],
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE IF EXISTS public.program_version_course DROP CONSTRAINT IF EXISTS program_version_course_pkey;
        ALTER TABLE IF EXISTS public.program_version_course ADD PRIMARY KEY (id, course_version_id, program_version_id);
    """
    )
    op.drop_constraint("next_program_version_course_id", "program_version_course", type_="foreignkey")
    op.drop_constraint("uniq_program_course_version", "program_version_course", type_="unique")
    op.drop_index(op.f("ix_program_version_course_next_program_version_course_id"), table_name="program_version_course")
    op.drop_column("program_version_course", "next_program_version_course_id")
