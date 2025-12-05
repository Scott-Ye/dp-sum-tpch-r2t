from pathlib import Path
import duckdb

TABLES = [
    ("region", ["r_regionkey","r_name","r_comment"]),
    ("nation", ["n_nationkey","n_name","n_regionkey","n_comment"]),
    ("customer", ["c_custkey","c_name","c_address","c_nationkey","c_phone","c_acctbal","c_mktsegment","c_comment"]),
    ("orders", ["o_orderkey","o_custkey","o_orderstatus","o_totalprice","o_orderdate","o_orderpriority","o_clerk","o_shippriority","o_comment"]),
    ("lineitem", ["l_orderkey","l_partkey","l_suppkey","l_linenumber","l_quantity","l_extendedprice","l_discount","l_tax","l_returnflag","l_linestatus","l_shipdate","l_commitdate","l_receiptdate","l_shipinstruct","l_shipmode","l_comment"]),
]

def to_tbl_line(row):
    return "|".join(map(str, row)) + "|\n"

def main(out_dir="dbgen", scale=1):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    con.execute("INSTALL tpch;")
    con.execute("LOAD tpch;")
    con.execute("CALL dbgen(sf=?, children=1);", [scale])

    for name, cols in TABLES:
        rel = con.execute(f"SELECT {', '.join(cols)} FROM {name}")
        with (out_path / f"{name}.tbl").open("w", encoding="utf-8") as f:
            for r in rel.fetchall():
                f.write(to_tbl_line(r))

if __name__ == "__main__":
    main()

