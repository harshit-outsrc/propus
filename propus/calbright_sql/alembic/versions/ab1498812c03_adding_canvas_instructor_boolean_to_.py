"""adding canvas instructor boolean to instructor_course_table

Revision ID: ab1498812c03
Revises: e8833a11ed0a
Create Date: 2024-07-12 16:44:41.988568

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from propus.calbright_sql.seed_data.staff_ingestion import ingest_staff_data


# revision identifiers, used by Alembic.
revision = "ab1498812c03"
down_revision = "e8833a11ed0a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("instructor_course", sa.Column("canvas_instructor", sa.BOOLEAN(), nullable=True))
    ingest_staff_data(Session(bind=op.get_bind()))


def downgrade() -> None:
    op.drop_column("instructor_course", "canvas_instructor")
