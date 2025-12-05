from .db import execute, execute_many, get_conn
import random

def main():
    execute("DELETE FROM lineitem;")
    execute("DELETE FROM orders;")
    execute("DELETE FROM customer;")
    execute("DELETE FROM nation;")
    execute("DELETE FROM region;")
    try:
        from tqdm import tqdm
        bar = True
    except Exception:
        bar = False
    params_region = [ (r, f"R{r}") for r in range(3) ]
    execute_many("INSERT INTO region(r_regionkey,r_name) VALUES($1,$2);", params_region)
    params_nation = [ (n, f"N{n}", n % 3) for n in range(5) ]
    execute_many("INSERT INTO nation(n_nationkey,n_name,n_regionkey) VALUES($1,$2,$3);", params_nation)
    params_customer = []
    for c in range(100):
        seg = random.choice(["AUTOMOBILE","BUILDING","HOUSEHOLD","FURNITURE","MACHINERY"])
        params_customer.append((c, f"C{c}", "addr", c % 5, "ph", 0.0, seg, ""))
    execute_many(
        "INSERT INTO customer(c_custkey,c_name,c_address,c_nationkey,c_phone,c_acctbal,c_mktsegment,c_comment) VALUES($1,$2,$3,$4,$5,$6,$7,$8);",
        params_customer
    )
    oid = 0
    order_params = []
    line_params = []
    cust_iter = range(100)
    if bar:
        from tqdm import tqdm
        cust_iter = tqdm(cust_iter, desc="orders/lineitems")
    for c in cust_iter:
        for _ in range(random.randint(3, 8)):
            oid += 1
            order_params.append((oid, c, "O", 0.0, "1995-01-01", "1-URGENT", "clerk", 0, ""))
            for li in range(1, random.randint(2, 10)):
                qty = random.randint(1, 10)
                price = random.uniform(10, 100)
                disc = random.choice([0.0, 0.05, 0.1])
                line_params.append((oid, 0, 0, li, qty, price * qty, disc, 0.0, "N", "O", "1996-04-01", "1995-03-30", "1996-04-10", "", "MAIL", ""))
        if len(order_params) >= 2000:
            execute_many(
                "INSERT INTO orders(o_orderkey,o_custkey,o_orderstatus,o_totalprice,o_orderdate,o_orderpriority,o_clerk,o_shippriority,o_comment) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9);",
                order_params
            )
            order_params = []
        if len(line_params) >= 5000:
            execute_many(
                "INSERT INTO lineitem(l_orderkey,l_partkey,l_suppkey,l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax,l_returnflag,l_linestatus,l_shipdate,l_commitdate,l_receiptdate,l_shipinstruct,l_shipmode,l_comment) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16);",
                line_params
            )
            line_params = []
    if order_params:
        execute_many(
            "INSERT INTO orders(o_orderkey,o_custkey,o_orderstatus,o_totalprice,o_orderdate,o_orderpriority,o_clerk,o_shippriority,o_comment) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9);",
            order_params
        )
    if line_params:
        execute_many(
            "INSERT INTO lineitem(l_orderkey,l_partkey,l_suppkey,l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax,l_returnflag,l_linestatus,l_shipdate,l_commitdate,l_receiptdate,l_shipinstruct,l_shipmode,l_comment) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16);",
            line_params
        )

if __name__ == "__main__":
    main()
