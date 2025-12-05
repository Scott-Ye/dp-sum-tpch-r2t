import argparse
import numpy as np
from .q3 import baseline_sum, join_rows
from .r2t_lp import r2t_estimate, tau_grid_from_contribs
from .baselines import naive_laplace_sum, local_sensitivity_bound, smooth_like_laplace_sum

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mktsegment", default="BUILDING")
    p.add_argument("--cutoff", default="1995-03-15")
    p.add_argument("--epsilon", type=float, default=1.0)
    p.add_argument("--tau_grid", type=int, default=64)
    p.add_argument("--sample_frac", type=float, default=1.0)
    p.add_argument("--max_orders", type=int, default=0)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--with_baselines", action="store_true")
    args = p.parse_args()

    df = join_rows(args.mktsegment, args.cutoff)
    if args.sample_frac < 1.0:
        df = df.sample(frac=max(min(args.sample_frac, 1.0), 0.0), random_state=args.seed)
    contribs = df.groupby("orderkey")["revenue"].sum().values.tolist()
    if args.max_orders and args.max_orders > 0:
        g = df.groupby("orderkey")["revenue"].sum().sort_values(ascending=False)
        keys = set(g.head(args.max_orders).index.tolist())
        contribs = [v for k, v in zip(g.index.tolist(), g.values.tolist()) if k in keys]
    tau_values = tau_grid_from_contribs(contribs, args.tau_grid)
    rng = np.random.default_rng(args.seed)
    dp_out, all_est = r2t_estimate(contribs, args.epsilon, tau_values, rng, verbose=args.verbose)
    base = baseline_sum(args.mktsegment, args.cutoff)
    print(f"baseline={base:.4f}")
    print(f"dp_out={dp_out:.4f}")
    print(f"tau_values={len(tau_values)}")
    if args.with_baselines:
        tau_bound = max(tau_values)
        naive = naive_laplace_sum(base, args.epsilon, tau_bound, rng)
        ls_bound = local_sensitivity_bound(contribs)
        smooth = smooth_like_laplace_sum(base, args.epsilon, contribs, rng)
        print(f"naive_laplace={naive:.4f} (scale={tau_bound/args.epsilon:.4f})")
        print(f"local_sens_bound={ls_bound:.4f}")
        print(f"smooth_like={smooth:.4f}")

if __name__ == "__main__":
    main()
