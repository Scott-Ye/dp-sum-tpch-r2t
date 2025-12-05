CREATE TABLE IF NOT EXISTS region (
    r_regionkey INTEGER PRIMARY KEY,
    r_name TEXT,
    r_comment TEXT
);

CREATE TABLE IF NOT EXISTS nation (
    n_nationkey INTEGER PRIMARY KEY,
    n_name TEXT,
    n_regionkey INTEGER REFERENCES region(r_regionkey),
    n_comment TEXT
);

CREATE TABLE IF NOT EXISTS customer (
    c_custkey INTEGER PRIMARY KEY,
    c_name TEXT,
    c_address TEXT,
    c_nationkey INTEGER REFERENCES nation(n_nationkey),
    c_phone TEXT,
    c_acctbal NUMERIC,
    c_mktsegment TEXT,
    c_comment TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    o_orderkey INTEGER PRIMARY KEY,
    o_custkey INTEGER REFERENCES customer(c_custkey),
    o_orderstatus CHAR(1),
    o_totalprice NUMERIC,
    o_orderdate DATE,
    o_orderpriority TEXT,
    o_clerk TEXT,
    o_shippriority INTEGER,
    o_comment TEXT
);

CREATE TABLE IF NOT EXISTS lineitem (
    l_orderkey INTEGER REFERENCES orders(o_orderkey),
    l_partkey INTEGER,
    l_suppkey INTEGER,
    l_linenumber INTEGER,
    l_quantity NUMERIC,
    l_extendedprice NUMERIC,
    l_discount NUMERIC,
    l_tax NUMERIC,
    l_returnflag CHAR(1),
    l_linestatus CHAR(1),
    l_shipdate DATE,
    l_commitdate DATE,
    l_receiptdate DATE,
    l_shipinstruct TEXT,
    l_shipmode TEXT,
    l_comment TEXT,
    PRIMARY KEY (l_orderkey, l_linenumber)
);
