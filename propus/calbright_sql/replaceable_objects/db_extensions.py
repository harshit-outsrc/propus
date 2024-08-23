from alembic_utils.pg_extension import PGExtension


create_uuid_ossp = PGExtension(schema="public", signature="uuid-ossp")
create_aws_commons = PGExtension(schema="public", signature="aws_commons")
create_aws_lambda = PGExtension(schema="public", signature="aws_lambda")
# create_plpgsql = PGExtension(schema="public", signature="plpgsql")
