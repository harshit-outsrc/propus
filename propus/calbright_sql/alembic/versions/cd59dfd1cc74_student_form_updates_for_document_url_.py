"""student form updates for document url and form id

Revision ID: cd59dfd1cc74
Revises: 7b10e50b05df
Create Date: 2024-06-13 19:40:38.488584

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cd59dfd1cc74"
down_revision = "7b10e50b05df"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f("ix_student_contact_method_ccc_id"), "student_contact_method", ["ccc_id"], unique=False)
    op.create_index(
        op.f("ix_student_contact_method_contact_method_id"),
        "student_contact_method",
        ["contact_method_id"],
        unique=False,
    )
    op.create_index(op.f("ix_student_contact_time_ccc_id"), "student_contact_time", ["ccc_id"], unique=False)
    op.create_index(
        op.f("ix_student_contact_time_contact_time_id"), "student_contact_time", ["contact_time_id"], unique=False
    )
    op.add_column("student_form", sa.Column("form_id", sa.VARCHAR(length=50), nullable=False))
    op.add_column("student_form", sa.Column("document_url", sa.VARCHAR(length=250), nullable=True))
    op.create_index(op.f("ix_student_form_form_id"), "student_form", ["form_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_student_form_form_id"), table_name="student_form")
    op.drop_column("student_form", "document_url")
    op.drop_column("student_form", "form_id")
    op.drop_index(op.f("ix_student_contact_time_contact_time_id"), table_name="student_contact_time")
    op.drop_index(op.f("ix_student_contact_time_ccc_id"), table_name="student_contact_time")
    op.drop_index(op.f("ix_student_contact_method_contact_method_id"), table_name="student_contact_method")
    op.drop_index(op.f("ix_student_contact_method_ccc_id"), table_name="student_contact_method")
