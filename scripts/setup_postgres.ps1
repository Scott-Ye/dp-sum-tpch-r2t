$env:PGHOST="localhost"
$env:PGPORT="5432"
$env:PGUSER="postgres"
$env:PGPASSWORD=""
$env:PGDATABASE="tpch"
python -m r2t.tpch_schema
python -m r2t.synthetic_load
