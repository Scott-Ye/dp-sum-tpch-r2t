SELECT o.o_orderkey AS orderkey,
       l.l_extendedprice * (1 - l_discount) AS revenue
FROM customer c
JOIN orders o ON o.o_custkey = c.c_custkey
JOIN lineitem l ON l.l_orderkey = o.o_orderkey
WHERE c.c_mktsegment = $1
  AND o.o_orderdate < CAST($2 AS DATE)
  AND l.l_shipdate > CAST($2 AS DATE);
