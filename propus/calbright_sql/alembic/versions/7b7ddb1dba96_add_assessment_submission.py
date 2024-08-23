"""add assessment submission

Revision ID: 7b7ddb1dba96
Revises: 7e395b9452af
Create Date: 2024-06-18 15:02:35.904680

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7b7ddb1dba96"
down_revision = "7e395b9452af"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sa.Enum("submitted", "passed", "failed", name="assessmentsubmissionstatus").create(op.get_bind())
    op.create_table(
        "assessment_submission",
        sa.Column("enrollment_id", sa.UUID(), nullable=False),
        sa.Column("assessment_id", sa.UUID(), nullable=False),
        sa.Column("attempt", sa.INTEGER(), nullable=False),
        sa.Column("score", sa.FLOAT(), nullable=True),
        sa.Column("grade", sa.VARCHAR(length=10), nullable=True),
        sa.Column("submission_timestamp", sa.TIMESTAMP(), nullable=False),
        sa.Column("lms", postgresql.ENUM("strut", "trailhead", "canvas", name="lms", create_type=False), nullable=True),
        sa.Column("lms_id", sa.VARCHAR(length=100), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM("submitted", "passed", "failed", name="assessmentsubmissionstatus", create_type=False),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=True),
        sa.Column("modified_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["enrollment_id"],
            ["enrollment.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_assessment_submission_assessment_id"), "assessment_submission", ["assessment_id"], unique=False
    )
    op.create_index(
        op.f("ix_assessment_submission_enrollment_id"), "assessment_submission", ["enrollment_id"], unique=False
    )
    op.create_index(op.f("ix_assessment_submission_id"), "assessment_submission", ["id"], unique=False)
    op.create_index(op.f("ix_assessment_submission_lms_id"), "assessment_submission", ["lms_id"], unique=True)
    op.create_index(op.f("ix_assessment_submission_status"), "assessment_submission", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_assessment_submission_status"), table_name="assessment_submission")
    op.drop_index(op.f("ix_assessment_submission_lms_id"), table_name="assessment_submission")
    op.drop_index(op.f("ix_assessment_submission_id"), table_name="assessment_submission")
    op.drop_index(op.f("ix_assessment_submission_enrollment_id"), table_name="assessment_submission")
    op.drop_index(op.f("ix_assessment_submission_assessment_id"), table_name="assessment_submission")
    op.drop_table("assessment_submission")
    sa.Enum("submitted", "passed", "failed", name="assessmentsubmissionstatus").drop(op.get_bind())
