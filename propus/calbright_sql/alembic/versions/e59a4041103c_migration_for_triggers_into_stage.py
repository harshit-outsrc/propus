"""migration for triggers into stage

Revision ID: e59a4041103c
Revises: 7b7ddb1dba96
Create Date: 2024-06-20 15:51:27.402181

"""

import os

from alembic import op
from alembic_utils.pg_extension import PGExtension
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

# revision identifiers, used by Alembic.
revision = "e59a4041103c"
down_revision = "7b7ddb1dba96"
branch_labels = None
depends_on = None


def upgrade() -> None:
    env = os.environ.get("ENV")
    if env == "stage" or env == "prod":
        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition="RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF cardinality(TG_ARGV)!=3 OR TG_ARGV IS NULL THEN\n      RAISE EXCEPTION 'Expected 3 parameters to invoke_trigger_system_lambda function but got %', cardinality(TG_ARGV);\n   ELSEIF TG_ARGV[0]='' THEN\n      RAISE EXCEPTION 'Lambda function name is empty';\n   ELSEIF TG_ARGV[1]='' THEN\n      RAISE EXCEPTION 'Lambda AWS region is empty';\n   ELSEIF TG_ARGV[2]='' THEN\n      RAISE EXCEPTION 'Lambda trigger name is empty';\n   ELSE\n      PERFORM * FROM aws_lambda.invoke(aws_commons.create_lambda_function_arn(TG_ARGV[0], TG_ARGV[1]),\n                                        CONCAT('{\"psql_trigger_type\"\\: \"', TG_ARGV[2], '\", \"id\"\\: \"', NEW.id, '\",\n                                        \"created_at\"\\: \"', NEW.created_at, '\"}')::json, 'Event');\n      RETURN NULL;\n   END IF;\nEND\n$$",  # noqa: E501
        )
        op.create_entity(public_invoke_trigger_system_lambda)

        public_aws_commons = PGExtension(schema="public", signature="aws_commons")
        op.create_entity(public_aws_commons)

        public_aws_lambda = PGExtension(schema="public", signature="aws_lambda")
        op.create_entity(public_aws_lambda)
    else:
        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition='RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF TG_ARGV[0]=\'\' THEN\n      RAISE EXCEPTION \'Lambda function name is empty\';\n   ELSE\n      RAISE INFO \'{"psql_trigger_type"\\: "%", "id"\\: "%", "created_at"\\: "%"}\', TG_ARGV[2], NEW.id, NEW.created_at;\n      RETURN NULL;\n   END IF;\nEND\n$$',  # noqa: E501
        )
        op.create_entity(public_invoke_trigger_system_lambda)

    public_ccc_application_new_ccc_application_trigger = PGTrigger(
        schema="public",
        signature="new_ccc_application_trigger",
        on_entity="public.ccc_application",
        is_constraint=False,
        definition=f"AFTER INSERT ON ccc_application\n    FOR EACH ROW\n    EXECUTE PROCEDURE invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',\n                                                        'new_ccc_application_trigger')",  # noqa: E501
    )
    op.create_entity(public_ccc_application_new_ccc_application_trigger)

    public_enrollment_new_enrollment_trigger = PGTrigger(
        schema="public",
        signature="new_enrollment_trigger",
        on_entity="public.enrollment",
        is_constraint=False,
        definition=f"AFTER INSERT ON enrollment\n    FOR EACH ROW\n    EXECUTE PROCEDURE invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',\n                                                        'new_enrollment_trigger')",  # noqa: E501
    )
    op.create_entity(public_enrollment_new_enrollment_trigger)

    public_enrollment_new_certificate_trigger = PGTrigger(
        schema="public",
        signature="new_certificate_trigger",
        on_entity="public.enrollment",
        is_constraint=False,
        definition=f"AFTER INSERT OR UPDATE OF completion_date, enrollment_status_id\n    ON enrollment\n    FOR EACH ROW\n    WHEN (new.completion_date IS NOT NULL and new.enrollment_status_id IS NOT NULL)\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2', 'new_certificate_trigger')",  # noqa: E501
    )
    op.create_entity(public_enrollment_new_certificate_trigger)

    public_enrollment_course_term_update_create_grade_trigger = PGTrigger(
        schema="public",
        signature="update_create_grade_trigger",
        on_entity="public.enrollment_course_term",
        is_constraint=False,
        definition=f"AFTER INSERT OR UPDATE OF grade_status, grade_id\n    ON enrollment_course_term\n    FOR EACH ROW\n    WHEN (new.grade_id IS NOT NULL and new.grade_status = 'certified')\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2', 'update_create_grade_trigger')",  # noqa: E501
    )
    op.create_entity(public_enrollment_course_term_update_create_grade_trigger)

    public_user_update_student_demographic_trigger = PGTrigger(
        schema="public",
        signature="update_student_demographic_trigger",
        on_entity="public.user",
        is_constraint=False,
        definition=f"AFTER UPDATE OF ccc_id, anthology_id, gender_id, pronoun_id, salutation_id, suffix_id, first_name, middle_name,\n      last_name, maiden_name, preferred_first_name, preferred_last_name, phone_number, calbright_email, personal_email\n    ON user\n    FOR EACH ROW\n    WHEN (new.ccc_id <> '' AND new.anthology_id IS NOT NULL AND new.staff_id IS NULL)\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',\n                                                     'update_student_demographic_trigger')",  # noqa: E501
    )
    op.create_entity(public_user_update_student_demographic_trigger)


def downgrade() -> None:
    env = os.environ.get("ENV")
    if env == "stage" or env == "prod":
        public_aws_lambda = PGExtension(schema="public", signature="aws_lambda")
        op.drop_entity(public_aws_lambda)

        public_aws_commons = PGExtension(schema="public", signature="aws_commons")
        op.drop_entity(public_aws_commons)

        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition="RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF cardinality(TG_ARGV)!=3 OR TG_ARGV IS NULL THEN\n      RAISE EXCEPTION 'Expected 3 parameters to invoke_trigger_system_lambda function but got %', cardinality(TG_ARGV);\n   ELSEIF TG_ARGV[0]='' THEN\n      RAISE EXCEPTION 'Lambda function name is empty';\n   ELSEIF TG_ARGV[1]='' THEN\n      RAISE EXCEPTION 'Lambda AWS region is empty';\n   ELSEIF TG_ARGV[2]='' THEN\n      RAISE EXCEPTION 'Lambda trigger name is empty';\n   ELSE\n      PERFORM * FROM aws_lambda.invoke(aws_commons.create_lambda_function_arn(TG_ARGV[0], TG_ARGV[1]),\n                                        CONCAT('{\"psql_trigger_type\"\\: \"', TG_ARGV[2], '\", \"id\"\\: \"', NEW.id, '\",\n                                        \"created_at\"\\: \"', NEW.created_at, '\"}')::json, 'Event');\n      RETURN NULL;\n   END IF;\nEND\n$$",  # noqa: E501
        )
        op.drop_entity(public_invoke_trigger_system_lambda)
    else:
        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition='RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF TG_ARGV[0]=\'\' THEN\n      RAISE EXCEPTION \'Lambda function name is empty\';\n   ELSE\n      RAISE INFO \'{"psql_trigger_type"\\: "%", "id"\\: "%", "created_at"\\: "%"}\', TG_ARGV[2], NEW.id, NEW.created_at;\n      RETURN NULL;\n   END IF;\nEND\n$$',  # noqa: E501
        )
        op.drop_entity(public_invoke_trigger_system_lambda)

    public_user_update_student_demographic_trigger = PGTrigger(
        schema="public",
        signature="update_student_demographic_trigger",
        on_entity="public.user",
        is_constraint=False,
        definition=f"AFTER UPDATE OF ccc_id, anthology_id, gender_id, pronoun_id, salutation_id, suffix_id, first_name, middle_name,\n      last_name, maiden_name, preferred_first_name, preferred_last_name, phone_number, calbright_email, personal_email\n    ON user\n    FOR EACH ROW\n    WHEN (new.ccc_id <> '' AND new.anthology_id IS NOT NULL AND new.staff_id IS NULL)\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',\n                                                     'update_student_demographic_trigger')",  # noqa: E501
    )
    op.drop_entity(public_user_update_student_demographic_trigger)

    public_enrollment_course_term_update_create_grade_trigger = PGTrigger(
        schema="public",
        signature="update_create_grade_trigger",
        on_entity="public.enrollment_course_term",
        is_constraint=False,
        definition=f"AFTER INSERT OR UPDATE OF grade_status, grade_id\n    ON enrollment_course_term\n    FOR EACH ROW\n    WHEN (new.grade_id IS NOT NULL and new.grade_status = 'certified')\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2', 'update_create_grade_trigger')",  # noqa: E501
    )
    op.drop_entity(public_enrollment_course_term_update_create_grade_trigger)

    public_enrollment_new_certificate_trigger = PGTrigger(
        schema="public",
        signature="new_certificate_trigger",
        on_entity="public.enrollment",
        is_constraint=False,
        definition=f"AFTER INSERT OR UPDATE OF completion_date, enrollment_status_id\n    ON enrollment\n    FOR EACH ROW\n    WHEN (new.completion_date IS NOT NULL and new.enrollment_status_id IS NOT NULL)\n    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2', 'new_certificate_trigger')",  # noqa: E501
    )
    op.drop_entity(public_enrollment_new_certificate_trigger)

    public_enrollment_new_enrollment_trigger = PGTrigger(
        schema="public",
        signature="new_enrollment_trigger",
        on_entity="public.enrollment",
        is_constraint=False,
        definition=f"AFTER INSERT ON enrollment\n    FOR EACH ROW\n    EXECUTE PROCEDURE invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',\n                                                        'new_enrollment_trigger')",  # noqa: E501
    )
    op.drop_entity(public_enrollment_new_enrollment_trigger)

    public_ccc_application_new_ccc_application_trigger = PGTrigger(
        schema="public",
        signature="new_ccc_application_trigger",
        on_entity="public.ccc_application",
        is_constraint=False,
        definition=f"AFTER INSERT ON ccc_application\n    FOR EACH ROW\n    EXECUTE PROCEDURE invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',\n                                                        'new_ccc_application_trigger')",  # noqa: E501
    )
    op.drop_entity(public_ccc_application_new_ccc_application_trigger)
