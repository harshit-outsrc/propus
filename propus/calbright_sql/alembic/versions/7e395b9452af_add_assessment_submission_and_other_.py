"""add assessment submission and other fields

Revision ID: 7e395b9452af
Revises: f7aa2b27565b
Create Date: 2024-06-18 09:05:52.797483

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7e395b9452af"
down_revision = "f7aa2b27565b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "assessment",
        sa.Column("lms", postgresql.ENUM("strut", "trailhead", "canvas", name="lms", create_type=False), nullable=True),
    )
    op.add_column("assessment", sa.Column("lms_id", sa.VARCHAR(length=100), nullable=True))
    op.add_column("assessment", sa.Column("required_percentage_to_pass", sa.FLOAT(), nullable=True))
    op.add_column("assessment", sa.Column("is_last_summative_of_course", sa.BOOLEAN(), nullable=True))
    op.create_index(op.f("ix_assessment_lms_id"), "assessment", ["lms_id"], unique=True)
    op.add_column(
        "course_version",
        sa.Column("lms", postgresql.ENUM("strut", "trailhead", "canvas", name="lms", create_type=False), nullable=True),
    )
    op.add_column("course_version", sa.Column("lms_id", sa.VARCHAR(length=100), nullable=True))
    op.create_index(op.f("ix_course_version_lms_id"), "course_version", ["lms_id"], unique=True)
    op.add_column("course_version_section", sa.Column("program_version_course_id", sa.UUID(), nullable=False))
    op.add_column(
        "course_version_section", sa.Column("instructor_enrollment_lms_id", sa.VARCHAR(length=100), nullable=True)
    )
    op.drop_index("ix_course_version_section_course_version_id", table_name="course_version_section")
    op.create_index(
        op.f("ix_course_version_section_instructor_enrollment_lms_id"),
        "course_version_section",
        ["instructor_enrollment_lms_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_course_version_section_program_version_course_id"),
        "course_version_section",
        ["program_version_course_id"],
        unique=False,
    )
    op.drop_constraint("course_version_section_course_version_id_fkey", "course_version_section", type_="foreignkey")
    op.create_foreign_key(
        None, "course_version_section", "program_version_course", ["program_version_course_id"], ["id"]
    )
    op.drop_column("course_version_section", "course_version_id")
    op.drop_index("ix_program_version_course_lms_id", table_name="program_version_course")
    op.drop_column("program_version_course", "lms_id")
    op.drop_column("program_version_course", "lms")


def downgrade() -> None:
    op.add_column(
        "program_version_course",
        sa.Column(
            "lms",
            postgresql.ENUM("strut", "trailhead", "canvas", name="lms", create_type=False),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "program_version_course", sa.Column("lms_id", sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    )
    op.create_index("ix_program_version_course_lms_id", "program_version_course", ["lms_id"], unique=True)
    op.add_column(
        "course_version_section", sa.Column("course_version_id", sa.UUID(), autoincrement=False, nullable=False)
    )
    op.drop_constraint(None, "course_version_section", type_="foreignkey")
    op.create_foreign_key(
        "course_version_section_course_version_id_fkey",
        "course_version_section",
        "course_version",
        ["course_version_id"],
        ["id"],
    )
    op.drop_index(op.f("ix_course_version_section_program_version_course_id"), table_name="course_version_section")
    op.drop_index(op.f("ix_course_version_section_instructor_enrollment_lms_id"), table_name="course_version_section")
    op.create_index(
        "ix_course_version_section_course_version_id", "course_version_section", ["course_version_id"], unique=False
    )
    op.drop_column("course_version_section", "instructor_enrollment_lms_id")
    op.drop_column("course_version_section", "program_version_course_id")
    op.drop_index(op.f("ix_course_version_lms_id"), table_name="course_version")
    op.drop_column("course_version", "lms_id")
    op.drop_column("course_version", "lms")
    op.drop_index(op.f("ix_assessment_lms_id"), table_name="assessment")
    op.drop_column("assessment", "is_last_summative_of_course")
    op.drop_column("assessment", "required_percentage_to_pass")
    op.drop_column("assessment", "lms_id")
    op.drop_column("assessment", "lms")
