import argparse
import csv
from pathlib import Path
import matplotlib.pyplot as plt
from .fig_utils import set_style, save_fig

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--out_prefix", default="report/snapshots")
    args = p.parse_args()

    rows = []
    with open(args.csv, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append({
                "snapshot": int(row["snapshot"]),
                "done": int(row["done"]),
                "rate": float(row["rate"]),
                "baseline": float(row["baseline"]),
                "dp_out": float(row["dp_out"]),
                "rel_err": float(row["rel_err"]),
            })
    if not rows:
        print("no data")
        return

    Path("report").mkdir(parents=True, exist_ok=True)
    xs = [r["done"] for r in rows]
    rate = [r["rate"] for r in rows]
    err = [r["rel_err"] for r in rows]
    base = [r["baseline"] for r in rows]
    dp = [r["dp_out"] for r in rows]

    set_style()
    plt.figure(figsize=(7, 4))
    plt.plot(xs, rate, marker="o")
    plt.xlabel("updates done")
    plt.ylabel("updates per second")
    plt.grid(True, linestyle=":")
    out1 = f"{args.out_prefix}_rate.png"
    save_fig(out1)
    print(f"saved {out1} and {out1.replace('.png', '.svg')}")

    plt.figure(figsize=(7, 4))
    plt.plot(xs, err, marker="o")
    plt.xlabel("updates done")
    plt.ylabel("relative error")
    plt.grid(True, linestyle=":")
    out2 = f"{args.out_prefix}_error.png"
    save_fig(out2)
    print(f"saved {out2} and {out2.replace('.png', '.svg')}\n")

    # Overlay baseline vs dp_out
    plt.figure(figsize=(7, 4))
    plt.plot(xs, base, marker="o", label="baseline (SUM)")
    plt.plot(xs, dp, marker="s", label="dp_out (R2T)")
    plt.xlabel("updates done")
    plt.ylabel("value")
    plt.grid(True, linestyle=":")
    plt.legend()
    out3 = f"{args.out_prefix}_values.png"
    save_fig(out3)
    print(f"saved {out3} and {out3.replace('.png', '.svg')}")

if __name__ == "__main__":
    main()
