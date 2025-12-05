# Instance-Optimal DP for SUM Queries over TPC-H (R2T)

- Implements an R2T-style pipeline on PostgreSQL + Python for a single-aggregate SUM over TPC-H Q3 (without GROUP BY).
- Pipeline: join extraction → LP-based truncated sum → Laplace noise → max selection over τ-grid.
- Includes accuracy benchmarking vs PostgreSQL baseline and simple throughput tests with synthetic updates.

## Quick Start

- Set PostgreSQL env vars: `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`.
- Create a virtualenv and install: `python -m venv .venv && .venv\\Scripts\\pip install -r requirements.txt`.
- Initialize schema: `python -m r2t.tpch_schema` (creates TPC-H tables) and optionally load synthetic dev data: `python -m r2t.synthetic_load`.
- Run baseline and R2T DP: `python -m r2t.run_r2t --epsilon 1.0 --tau_grid 64`.
- Run benchmarks: `python -m r2t.benchmark --epsilon 1.0`.

## Publish to GitHub

- Initialize: `git init && git add . && git commit -m "R2T TPCH Q3 DP"`.
- Create a remote on GitHub and push: `git remote add origin <your_repo_url>` then `git push -u origin main`.

## Layout

- `r2t/`: Python package for DB access, query extraction, R2T mechanism, and benchmarks.
- `queries/`: SQL definitions for TPC-H Q3 (modified).
- `db/`: Schema DDL and helper scripts.
- `report/`: Draft report (Markdown) and figures.

## Notes

- No secrets are stored; configure PostgreSQL via environment.
- For real data, use official TPC-H Tools v3.0.1 to generate scale=1 and load:
  - Download TPC-H Tools v3.0.1 and build `dbgen`.
  - Run `dbgen -s 1` to produce `.tbl` files.
  - Place `.tbl` files under `dbgen/` in this repo.
  - Run `python db/load_data.py` to `COPY` into PostgreSQL.
