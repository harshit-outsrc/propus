from alembic_utils.pg_function import PGFunction

invoke_trigger_system_lambda = PGFunction(
    schema="public",
    signature="invoke_trigger_system_lambda()",
    definition="""
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
   IF cardinality(TG_ARGV)!=3 OR TG_ARGV IS NULL THEN
      RAISE EXCEPTION 'Expected 3 parameters to invoke_trigger_system_lambda function but got %', cardinality(TG_ARGV);
   ELSEIF TG_ARGV[0]='' THEN
      RAISE EXCEPTION 'Lambda function name is empty';
   ELSEIF TG_ARGV[1]='' THEN
      RAISE EXCEPTION 'Lambda AWS region is empty';
   ELSEIF TG_ARGV[2]='' THEN
      RAISE EXCEPTION 'Lambda trigger name is empty';
   ELSE
      PERFORM * FROM aws_lambda.invoke(aws_commons.create_lambda_function_arn(TG_ARGV[0], TG_ARGV[1]),
                                        CONCAT('{"psql_trigger_type": "', TG_ARGV[2], '", "id": "', NEW.id, '",
                                        "created_at": "', NEW.created_at, '",
                                        "trigger_op": "', TG_OP, '"}')::json, 'Event');
      RETURN NULL;
   END IF;
END
$$;
""",
)
