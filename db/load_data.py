from pathlib import Path
from r2t.db import get_conn

TABLES = [
    ("region", ["r_regionkey","r_name","r_comment"]),
    ("nation", ["n_nationkey","n_name","n_regionkey","n_comment"]),
    ("customer", ["c_custkey","c_name","c_address","c_nationkey","c_phone","c_acctbal","c_mktsegment","c_comment"]),
    ("orders", ["o_orderkey","o_custkey","o_orderstatus","o_totalprice","o_orderdate","o_orderpriority","o_clerk","o_shippriority","o_comment"]),
    ("lineitem", ["l_orderkey","l_partkey","l_suppkey","l_linenumber","l_quantity","l_extendedprice","l_discount","l_tax","l_returnflag","l_linestatus","l_shipdate","l_commitdate","l_receiptdate","l_shipinstruct","l_shipmode","l_comment"]),
]

def main(dbgen_dir="dbgen"):
    with get_conn() as conn:
        with conn.cursor() as cur:
            for name, cols in TABLES:
                tbl = Path(dbgen_dir) / f"{name}.tbl"
                if not tbl.exists():
                    continue
                cur.execute(f"TRUNCATE {name} CASCADE;")
                with tbl.open('rb') as f:
                    cur.copy(
                        f"COPY {name} ({','.join(cols)}) FROM STDIN WITH (FORMAT csv, DELIMITER '|')",
                        f,
                    )

if __name__ == "__main__":
    main()
