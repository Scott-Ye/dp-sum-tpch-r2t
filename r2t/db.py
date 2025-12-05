import os
import re
import pandas as pd

BACKEND = os.getenv("DB_BACKEND", "postgres").lower()

def _translate_pg_params(sql):
    return re.sub(r"\$\d+", "?", sql)
def _expand_params(sql, params):
    if params is None:
        return ()
    idxs = [int(m.group()[1:]) for m in re.finditer(r"\$\d+", sql)]
    vals = []
    for i in idxs:
        vals.append(params[i-1])
    return tuple(vals)

if BACKEND == "duckdb":
    import duckdb
    from pathlib import Path
    DBPATH = os.getenv("DUCKDB_PATH", str(Path("db/tpch.duckdb").resolve()))
    _cached_con = None

    def get_conn():
        global _cached_con
        if _cached_con is None:
            _cached_con = duckdb.connect(DBPATH)
        return _cached_con

    def execute(sql, params=None):
        con = get_conn()
        con.execute(_translate_pg_params(sql), _expand_params(sql, params))

    def execute_many(sql, params_list):
        con = get_conn()
        if not params_list:
            return
        sql_t = _translate_pg_params(sql)
        con.executemany(sql_t, [ _expand_params(sql, p) for p in params_list ])

    def fetch_df(sql, params=None):
        con = get_conn()
        rel = con.execute(_translate_pg_params(sql), _expand_params(sql, params))
        return rel.df()
else:
    import psycopg
    from .config import pg_dsn
    _PG_PARAM_RE = re.compile(r"\$\d+")
    def _translate_pg_params_pg(sql: str) -> str:
        return _PG_PARAM_RE.sub("%s", sql)
    def _expand_params_pg(sql: str, params):
        if params is None:
            return ()
        idxs = [int(m.group()[1:]) for m in _PG_PARAM_RE.finditer(sql)]
        return tuple(params[i-1] for i in idxs)

    def get_conn():
        return psycopg.connect(**pg_dsn())

    def execute(sql, params=None):
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(_translate_pg_params_pg(sql), _expand_params_pg(sql, params))

    def execute_many(sql, params_list):
        if not params_list:
            return
        with get_conn() as conn:
            with conn.cursor() as cur:
                sql_t = _translate_pg_params_pg(sql)
                for p in params_list:
                    cur.execute(sql_t, _expand_params_pg(sql, p))

    def fetch_df(sql, params=None):
        with get_conn() as conn:
            sql_t = _translate_pg_params_pg(sql)
            return pd.read_sql_query(sql_t, conn, params=_expand_params_pg(sql, params))
