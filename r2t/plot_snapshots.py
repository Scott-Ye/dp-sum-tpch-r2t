import argparse
import csv
from pathlib import Path
import matplotlib.pyplot as plt

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

    plt.figure()
    plt.plot(xs, rate, marker="o")
    plt.xlabel("updates done")
    plt.ylabel("updates per second")
    plt.grid(True)
    out1 = f"{args.out_prefix}_rate.png"
    plt.savefig(out1, dpi=200)
    print(f"saved {out1}")

    plt.figure()
    plt.plot(xs, err, marker="o")
    plt.xlabel("updates done")
    plt.ylabel("relative error")
    plt.grid(True)
    out2 = f"{args.out_prefix}_error.png"
    plt.savefig(out2, dpi=200)
    print(f"saved {out2}")

if __name__ == "__main__":
    main()
