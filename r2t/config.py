import os

def pg_dsn():
    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "5432")),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", ""),
        "dbname": os.getenv("PGDATABASE", "tpch"),
    }

def epsilon_default():
    return float(os.getenv("EPSILON", "1.0"))
