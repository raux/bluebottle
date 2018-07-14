CREATE OR REPLACE FUNCTION refresh_union_view(table_name text) RETURNS void AS $$
DECLARE
  schema RECORD;
  result RECORD;
  sql TEXT := '';
BEGIN
  FOR schema IN EXECUTE
    format(
      'SELECT id, schema_name FROM public.clients_client where schema_name != ''goodup_demo'''
    )
  LOOP
    sql := sql || format('SELECT (SELECT column_name FROM information_schema.columns WHERE table_schema = ''onepercent'' AND table_name  = ''%I''),  ''%I'' as tenant  FROM %I.%I UNION ALL ', table_name, schema.schema_name, schema.schema_name, table_name);
  END LOOP;

  EXECUTE
    format('CREATE OR REPLACE VIEW %I AS ', 'all_' || table_name) || left(sql, -11);
END
$$ LANGUAGE plpgsql;
