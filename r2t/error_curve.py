import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from .q3 import baseline_sum, join_rows
from .r2t_lp import r2t_estimate, tau_grid_from_contribs

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mktsegment", default="BUILDING")
    p.add_argument("--cutoff", default="1995-03-15")
    p.add_argument("--epsilons", default="0.1,0.5,1,2")
    p.add_argument("--sample_frac", type=float, default=1.0)
    p.add_argument("--max_orders", type=int, default=0)
    p.add_argument("--grid_k", type=int, default=64)
    args = p.parse_args()

    df = join_rows(args.mktsegment, args.cutoff)
    if args.sample_frac < 1.0:
        df = df.sample(frac=max(min(args.sample_frac, 1.0), 0.0), random_state=777)
    contribs = df.groupby("orderkey")["revenue"].sum().values.tolist()
    if args.max_orders and args.max_orders > 0:
        g = df.groupby("orderkey")["revenue"].sum().sort_values(ascending=False)
        keys = set(g.head(args.max_orders).index.tolist())
        contribs = [v for k, v in zip(g.index.tolist(), g.values.tolist()) if k in keys]
    tau_values = tau_grid_from_contribs(contribs, args.grid_k)
    base = baseline_sum(args.mktsegment, args.cutoff)

    xs = [float(x) for x in args.epsilons.split(",")]
    errs = []
    rng = np.random.default_rng(777)
    for e in xs:
        dp_out, _ = r2t_estimate(contribs, e, tau_values, rng)
        errs.append(abs(dp_out - base) / max(base, 1e-9))

    plt.figure()
    plt.plot(xs, errs, marker="o")
    plt.xlabel("epsilon")
    plt.ylabel("relative error")
    plt.grid(True)
    Path("report").mkdir(parents=True, exist_ok=True)
    plt.savefig("report/error_epsilon.png", dpi=200)
    print("saved report/error_epsilon.png")

if __name__ == "__main__":
    main()
