import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from .q3 import baseline_sum, join_rows
from .r2t_lp import r2t_estimate, tau_grid_from_contribs
from .baselines import naive_laplace_sum, smooth_like_laplace_sum, local_sensitivity_bound

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
    errs_r2t = []
    errs_naive = []
    errs_smooth = []
    rng = np.random.default_rng(777)
    tau_bound = max(tau_values) if len(tau_values) else 1.0
    ls_bound = local_sensitivity_bound(contribs)
    for e in xs:
        dp_out, _ = r2t_estimate(contribs, e, tau_values, rng)
        naive = naive_laplace_sum(base, e, tau_bound, rng)
        smooth = smooth_like_laplace_sum(base, e, contribs, rng)
        errs_r2t.append(abs(dp_out - base) / max(base, 1e-9))
        errs_naive.append(abs(naive - base) / max(base, 1e-9))
        errs_smooth.append(abs(smooth - base) / max(base, 1e-9))

    plt.style.use("seaborn-v0_8")
    plt.figure(figsize=(7, 4))
    plt.plot(xs, errs_r2t, marker="o", label="R2T-LP")
    plt.plot(xs, errs_naive, marker="s", label="Naive Laplace")
    plt.plot(xs, errs_smooth, marker="^", label="Smooth-like")
    plt.xlabel("epsilon")
    plt.ylabel("relative error")
    plt.grid(True, linestyle=":")
    plt.legend()
    Path("report").mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig("report/error_epsilon.png", dpi=200)
    plt.savefig("report/error_epsilon.svg")
    print("saved report/error_epsilon.png and .svg")

if __name__ == "__main__":
    main()
