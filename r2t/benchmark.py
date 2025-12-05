import argparse
import time
import random
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import csv
from .q3 import baseline_sum, join_rows
from .r2t_lp import r2t_estimate, tau_grid_from_contribs
from .db import execute

def simulate_updates(n, workers=1):
    if workers <= 1:
        for _ in range(n):
            li = random.randint(1, 10)
            execute("UPDATE lineitem SET l_extendedprice = l_extendedprice * 1.0001 WHERE l_linenumber = $1;", (li,))
    else:
        per = max(1, n // workers)
        def task(w):
            for _ in range(per):
                li = random.randint(1, 10)
                execute(
                    "UPDATE lineitem SET l_extendedprice = l_extendedprice * 1.0001 WHERE l_linenumber = $1 AND mod(l_orderkey, $2) = $3;",
                    (li, workers, w)
                )
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(task, w) for w in range(workers)]
            for f in futs:
                f.result()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mktsegment", default="BUILDING")
    p.add_argument("--cutoff", default="1995-03-15")
    p.add_argument("--epsilon", type=float, default=1.0)
    p.add_argument("--updates", type=int, default=20000)
    p.add_argument("--snapshots", type=int, default=10)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--log_csv", default="")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--sample_frac", type=float, default=1.0)
    p.add_argument("--max_orders", type=int, default=0)
    p.add_argument("--grid_k", type=int, default=64)
    args = p.parse_args()

    df0 = join_rows(args.mktsegment, args.cutoff)
    if args.sample_frac < 1.0:
        df0 = df0.sample(frac=max(min(args.sample_frac, 1.0), 0.0), random_state=123)
    contribs0 = df0.groupby("orderkey")["revenue"].sum().values.tolist()
    if args.max_orders and args.max_orders > 0:
        g0 = df0.groupby("orderkey")["revenue"].sum().sort_values(ascending=False)
        keys0 = set(g0.head(args.max_orders).index.tolist())
        contribs0 = [v for k, v in zip(g0.index.tolist(), g0.values.tolist()) if k in keys0]
    tau_values = tau_grid_from_contribs(contribs0, args.grid_k)
    rng = np.random.default_rng(123)
    base0 = baseline_sum(args.mktsegment, args.cutoff)

    total = args.updates
    step = max(1, total // args.snapshots)
    start = time.time()
    done = 0
    rows = []
    try:
        from tqdm import tqdm
        snapshot_iter = tqdm(range(args.snapshots), desc="Snapshots") if args.verbose else range(args.snapshots)
    except Exception:
        snapshot_iter = range(args.snapshots)
    for s in snapshot_iter:
        simulate_updates(step, args.workers)
        done += step
        base = baseline_sum(args.mktsegment, args.cutoff)
        df1 = join_rows(args.mktsegment, args.cutoff)
        if args.sample_frac < 1.0:
            df1 = df1.sample(frac=max(min(args.sample_frac, 1.0), 0.0), random_state=123+s)
        contribs1 = df1.groupby("orderkey")["revenue"].sum().values.tolist()
        if args.max_orders and args.max_orders > 0:
            g1 = df1.groupby("orderkey")["revenue"].sum().sort_values(ascending=False)
            keys1 = set(g1.head(args.max_orders).index.tolist())
            contribs1 = [v for k, v in zip(g1.index.tolist(), g1.values.tolist()) if k in keys1]
        dp_out, _ = r2t_estimate(contribs1, args.epsilon, tau_values, rng, verbose=False)
        err = abs(dp_out - base) / max(base, 1e-9)
        rate = done / max(time.time() - start, 1e-6)
        print(f"progress={done}/{total} rate={rate:.1f}/s baseline={base:.4f} dp_out={dp_out:.4f} rel_err={err:.4%}")
        rows.append({"snapshot": s+1, "done": done, "rate": rate, "baseline": base, "dp_out": dp_out, "rel_err": err})
    if args.log_csv:
        with open(args.log_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["snapshot","done","rate","baseline","dp_out","rel_err"]) 
            w.writeheader()
            w.writerows(rows)
        print(f"saved {args.log_csv}")

if __name__ == "__main__":
    main()
