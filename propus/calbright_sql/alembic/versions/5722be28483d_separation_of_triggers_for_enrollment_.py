"""separation of triggers for enrollment_course_term

Revision ID: 5722be28483d
Revises: ab1498812c03
Create Date: 2024-07-19 14:41:41.576327

"""

import os
from alembic import op
from alembic_utils.pg_trigger import PGTrigger

# revision identifiers, used by Alembic.
revision = "5722be28483d"
down_revision = "ab1498812c03"
branch_labels = None
depends_on = None


def upgrade() -> None:

    env = os.environ.get("ENV")
    public_enrollment_course_term_update_create_grade_trigger = PGTrigger(
        schema="public",
        signature="update_create_grade_trigger",
        on_entity="public.enrollment_course_term",
        is_constraint=False,
        definition=f"AFTER UPDATE OF grade_status, grade_id\n    ON enrollment_course_term\n    FOR EACH ROW\n    WHEN (new.grade_id IS NOT NULL and new.grade_status = 'certified' and old.grade_status <> new.grade_status)\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',\n                                                        'update_create_grade_trigger')",  # noqa: E501
    )
    op.replace_entity(public_enrollment_course_term_update_create_grade_trigger)

    public_enrollment_course_term_insert_create_grade_trigger = PGTrigger(
        schema="public",
        signature="insert_create_grade_trigger",
        on_entity="public.enrollment_course_term",
        is_constraint=False,
        definition=f"AFTER INSERT ON public.enrollment_course_term FOR EACH ROW EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2', 'update_create_grade_trigger')",  # noqa: E501
    )
    op.create_entity(public_enrollment_course_term_insert_create_grade_trigger)


def downgrade() -> None:

    env = os.environ.get("ENV")
    public_enrollment_course_term_insert_create_grade_trigger = PGTrigger(
        schema="public",
        signature="insert_create_grade_trigger",
        on_entity="public.enrollment_course_term",
        is_constraint=False,
        definition=f"AFTER INSERT ON public.enrollment_course_term FOR EACH ROW EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2', 'update_create_grade_trigger')",  # noqa: E501
    )
    op.drop_entity(public_enrollment_course_term_insert_create_grade_trigger)

    public_enrollment_course_term_update_create_grade_trigger = PGTrigger(
        schema="public",
        signature="update_create_grade_trigger",
        on_entity="public.enrollment_course_term",
        is_constraint=False,
        definition=f"AFTER INSERT OR UPDATE OF grade_status, grade_id\n    ON enrollment_course_term\n    FOR EACH ROW\n    WHEN (new.grade_id IS NOT NULL and new.grade_status = 'certified')\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2', 'update_create_grade_trigger')",  # noqa: E501
    )
    op.replace_entity(public_enrollment_course_term_update_create_grade_trigger)
