"""trigger operations adjustment

Revision ID: d689708501de
Revises: 0a0bf175e387
Create Date: 2024-07-11 12:19:38.119864

"""

import os
from alembic import op
from alembic_utils.pg_function import PGFunction

# revision identifiers, used by Alembic.
revision = "d689708501de"
down_revision = "0a0bf175e387"
branch_labels = None
depends_on = None


def upgrade() -> None:

    env = os.environ.get("ENV")
    if env == "stage" or env == "prod":
        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition="RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF cardinality(TG_ARGV)!=3 OR TG_ARGV IS NULL THEN\n      RAISE EXCEPTION 'Expected 3 parameters to invoke_trigger_system_lambda function but got %', cardinality(TG_ARGV);\n   ELSEIF TG_ARGV[0]='' THEN\n      RAISE EXCEPTION 'Lambda function name is empty';\n   ELSEIF TG_ARGV[1]='' THEN\n      RAISE EXCEPTION 'Lambda AWS region is empty';\n   ELSEIF TG_ARGV[2]='' THEN\n      RAISE EXCEPTION 'Lambda trigger name is empty';\n   ELSE\n      PERFORM * FROM aws_lambda.invoke(aws_commons.create_lambda_function_arn(TG_ARGV[0], TG_ARGV[1]),\n                                        CONCAT('{\"psql_trigger_type\"\\: \"', TG_ARGV[2], '\", \"id\"\\: \"', NEW.id, '\",\n                                        \"created_at\"\\: \"', NEW.created_at, '\",\n                                        \"trigger_op\"\\: \"', TG_OP, '\"}')::json, 'Event');\n      RETURN NULL;\n   END IF;\nEND\n$$",  # noqa: E501
        )
        op.replace_entity(public_invoke_trigger_system_lambda)
    else:
        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition='RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF TG_ARGV[0]=\'\' THEN\n      RAISE EXCEPTION \'Lambda function name is empty\';\n   ELSE\n      RAISE INFO \'{"psql_trigger_type"\\: "%", "id"\\: "%", "created_at"\\: "%", "trigger_op"\\: "%"}\', TG_ARGV[2], NEW.id, NEW.created_at, TG_OP;\n      RETURN NULL;\n   END IF;\nEND\n$$',  # noqa: E501
        )
        op.replace_entity(public_invoke_trigger_system_lambda)
    # ### end Alembic commands ###


def downgrade() -> None:

    env = os.environ.get("ENV")
    if env == "stage" or env == "prod":
        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition="RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF cardinality(TG_ARGV)!=3 OR TG_ARGV IS NULL THEN\n      RAISE EXCEPTION 'Expected 3 parameters to invoke_trigger_system_lambda function but got %', cardinality(TG_ARGV);\n   ELSEIF TG_ARGV[0]='' THEN\n      RAISE EXCEPTION 'Lambda function name is empty';\n   ELSEIF TG_ARGV[1]='' THEN\n      RAISE EXCEPTION 'Lambda AWS region is empty';\n   ELSEIF TG_ARGV[2]='' THEN\n      RAISE EXCEPTION 'Lambda trigger name is empty';\n   ELSE\n      PERFORM * FROM aws_lambda.invoke(aws_commons.create_lambda_function_arn(TG_ARGV[0], TG_ARGV[1]),\n                                        CONCAT('{\"psql_trigger_type\"\\: \"', TG_ARGV[2], '\", \"id\"\\: \"', NEW.id, '\",\n                                        \"created_at\"\\: \"', NEW.created_at, '\"}')::json, 'Event');\n      RETURN NULL;\n   END IF;\nEND\n$$",  # noqa: E501
        )
        op.replace_entity(public_invoke_trigger_system_lambda)
    else:
        public_invoke_trigger_system_lambda = PGFunction(
            schema="public",
            signature="invoke_trigger_system_lambda()",
            definition='RETURNS TRIGGER\n  LANGUAGE PLPGSQL\n  AS\n$$\nBEGIN\n   IF TG_ARGV[0]=\'\' THEN\n      RAISE EXCEPTION \'Lambda function name is empty\';\n   ELSE\n      RAISE INFO \'{"psql_trigger_type"\\: "%", "id"\\: "%", "created_at"\\: "%"}\', TG_ARGV[2], NEW.id, NEW.created_at;\n      RETURN NULL;\n   END IF;\nEND\n$$',  # noqa: E501
        )
        op.replace_entity(public_invoke_trigger_system_lambda)
    # ### end Alembic commands ###
