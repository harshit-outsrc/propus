"""adding course_version_section table

Revision ID: 20481bc8a72b
Revises: 8fd7cef7183d
Create Date: 2024-06-05 15:36:04.139048

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20481bc8a72b"
down_revision = "8fd7cef7183d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "course_version_section",
        sa.Column("course_version_id", sa.UUID(), nullable=False),
        sa.Column("instructor_id", sa.UUID(), nullable=False),
        sa.Column("section_id", sa.VARCHAR(length=100), nullable=True),
        sa.Column("section_name", sa.VARCHAR(length=200), nullable=True),
        sa.Column("lms", postgresql.ENUM("strut", "trailhead", "canvas", name="lms", create_type=False), nullable=True),
        sa.Column("lms_id", sa.VARCHAR(length=100), nullable=True),
        sa.Column("sis_id", sa.VARCHAR(length=100), nullable=True),
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=True),
        sa.Column("modified_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["course_version_id"],
            ["course_version.id"],
        ),
        sa.ForeignKeyConstraint(
            ["instructor_id"],
            ["staff.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_course_version_section_course_version_id"),
        "course_version_section",
        ["course_version_id"],
        unique=False,
    )
    op.create_index(op.f("ix_course_version_section_id"), "course_version_section", ["id"], unique=False)
    op.create_index(
        op.f("ix_course_version_section_instructor_id"), "course_version_section", ["instructor_id"], unique=False
    )
    op.create_index(op.f("ix_course_version_section_lms_id"), "course_version_section", ["lms_id"], unique=True)
    op.create_index(
        op.f("ix_course_version_section_section_id"), "course_version_section", ["section_id"], unique=False
    )
    op.create_index(
        op.f("ix_course_version_section_section_name"), "course_version_section", ["section_name"], unique=True
    )
    op.create_index(op.f("ix_course_version_section_sis_id"), "course_version_section", ["sis_id"], unique=True)
    op.add_column("enrollment_course_term", sa.Column("course_version_section_id", sa.UUID(), nullable=True))
    op.create_index(
        op.f("ix_enrollment_course_term_course_version_section_id"),
        "enrollment_course_term",
        ["course_version_section_id"],
        unique=False,
    )
    op.create_foreign_key(
        None, "enrollment_course_term", "course_version_section", ["course_version_section_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint(None, "enrollment_course_term", type_="foreignkey")
    op.drop_index(op.f("ix_enrollment_course_term_course_version_section_id"), table_name="enrollment_course_term")
    op.drop_column("enrollment_course_term", "course_version_section_id")
    op.drop_index(op.f("ix_course_version_section_sis_id"), table_name="course_version_section")
    op.drop_index(op.f("ix_course_version_section_section_name"), table_name="course_version_section")
    op.drop_index(op.f("ix_course_version_section_section_id"), table_name="course_version_section")
    op.drop_index(op.f("ix_course_version_section_lms_id"), table_name="course_version_section")
    op.drop_index(op.f("ix_course_version_section_instructor_id"), table_name="course_version_section")
    op.drop_index(op.f("ix_course_version_section_id"), table_name="course_version_section")
    op.drop_index(op.f("ix_course_version_section_course_version_id"), table_name="course_version_section")
    op.drop_table("course_version_section")
