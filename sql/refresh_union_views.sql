CREATE OR REPLACE FUNCTION refresh_union_view(table_name text) RETURNS void AS $$
DECLARE
  schema RECORD;
  field RECORD;
  result RECORD;
  fields TEXT := '';
  sql TEXT := '';
BEGIN
  FOR field IN EXECUTE
    format(
      'SELECT column_name FROM information_schema.columns WHERE table_schema = ''onepercent'' AND table_name = ''%I''',
        table_name
    )
  LOOP
    fields := fields || format('%I, ', field.column_name);
  END LOOP;
  FOR schema IN EXECUTE
    format(
      'SELECT id, schema_name FROM public.clients_client where schema_name != ''goodup_demo'''
    )
  LOOP
    sql := sql || 'SELECT ' || fields || format('%L AS tenant  FROM %I.%I UNION ALL ', schema.schema_name, schema.schema_name, table_name);
  END LOOP;

  EXECUTE
    format('CREATE OR REPLACE VIEW %I AS ', 'all_' || table_name) || left(sql, -11);
END
$$ LANGUAGE plpgsql;