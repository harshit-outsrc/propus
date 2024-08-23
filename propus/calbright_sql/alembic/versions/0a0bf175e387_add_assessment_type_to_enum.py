"""add assessment type to enum

Revision ID: 0a0bf175e387
Revises: 7b7ddb1dba96
Create Date: 2024-06-18 17:42:33.113318

"""

import sqlalchemy as sa
from alembic import op
from alembic_postgresql_enum import TableReference
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0a0bf175e387"
down_revision = "93a519766633"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.sync_enum_values(
        "public",
        "assessmenttype",
        ["summative", "formative", "final_grade", "pre_assessment", "milestone", "observable_skill", "discussion"],
        [TableReference(table_schema="public", table_name="assessment", column_name="assessment_type")],
        enum_values_to_rename=[],
    )
    sa.Enum("assignment", "quiz", "discussion", name="lmstype").create(op.get_bind())
    op.add_column(
        "assessment",
        sa.Column(
            "lms_type",
            postgresql.ENUM("assignment", "quiz", "discussion", name="lmstype", create_type=False),
            nullable=True,
        ),
    )
    sa.Enum("competency", "durable_skill", "final_grade", "observable_skill", name="competencytype").create(
        op.get_bind()
    )
    op.add_column("assessment", sa.Column("active", sa.BOOLEAN(), nullable=True))
    op.drop_index("ix_assessment_lms_id", table_name="assessment")
    op.create_index(op.f("ix_assessment_lms_id"), "assessment", ["lms_id"], unique=False)
    op.create_unique_constraint("uniq_lms_id_lms_type", "assessment", ["lms_id", "lms_type"])
    op.add_column(
        "competency",
        sa.Column(
            "competency_type",
            postgresql.ENUM(
                "competency",
                "durable_skill",
                "final_grade",
                "observable_skill",
                name="competencytype",
                create_type=False,
            ),
            nullable=True,
        ),
    )
    op.create_unique_constraint(
        "uniq_instructor_program_version_course",
        "course_version_section",
        ["program_version_course_id", "instructor_id"],
    )


def downgrade() -> None:
    op.sync_enum_values(
        "public",
        "assessmenttype",
        ["summative", "formative", "final_grade"],
        [TableReference(table_schema="public", table_name="assessment", column_name="assessment_type")],
        enum_values_to_rename=[],
    )
    op.drop_column("assessment", "lms_type")
    sa.Enum("assignment", "quiz", "discussion", name="lmstype").drop(op.get_bind())
    op.drop_column("competency", "competency_type")
    op.drop_constraint("uniq_lms_id_lms_type", "assessment", type_="unique")
    op.drop_index(op.f("ix_assessment_lms_id"), table_name="assessment")
    op.create_index("ix_assessment_lms_id", "assessment", ["lms_id"], unique=True)
    op.drop_column("assessment", "active")
    sa.Enum("competency", "durable_skill", "final_grade", "observable_skill", name="competencytype").drop(op.get_bind())
    op.drop_constraint("uniq_instructor_program_version_course", "course_version_section", type_="unique")
