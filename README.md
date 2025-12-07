# Instance-Optimal Differential Privacy for SUM (TPC-H Q3)

- Single-aggregate SUM (no GROUP BY) pipeline: join extraction → LP-based truncated sum → Laplace noise → max over a geometric τ-grid
- PostgreSQL by default, switchable to DuckDB; accuracy referenced to the PostgreSQL baseline SUM

## Reproducibility and Running

- Prerequisites: Python 3.10+; PostgreSQL accessible via `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`
- Install (Windows):
  - `python -m venv .venv`
  - `.venv\Scripts\pip install -r requirements.txt`

### Option A: Quick demo (no large data)
- Initialize schema: `python -m r2t.tpch_schema`
- Load small synthetic data: `python -m r2t.synthetic_load`
- Run: `python -m r2t.run_r2t --mktsegment MACHINERY --cutoff 1994-01-01 --epsilon 1.0 --tau_grid 128 --with_baselines`

### Option B: Full reproduction (TPC-H SF=1)
- Generate `.tbl` via DuckDB: `python db/generate_tbl_duckdb.py`
- Load into PostgreSQL: `python db/load_data.py`
- Run: same command as Option A

Note: Large TPC-H datasets are not distributed; generate locally with Option B, or use Option A to validate the pipeline.

## Backends
- `DB_BACKEND=postgres` (default) or `duckdb`
- For DuckDB, set `DUCKDB_PATH` to your local `db/tpch.duckdb`

## Repository Layout

- `r2t/`
  - `db.py`: DB adapter (PostgreSQL/DuckDB); `fetch_df`, `execute`, `execute_many`
  - `q3.py`: Q3 (no group) SQL runners — `baseline_sum`, `join_rows`
  - `r2t_lp.py`: truncated-sum LP (OR-Tools), Laplace mechanism, τ-grid — `truncated_sum_lp`, `r2t_estimate`, `tau_grid_from_contribs`
  - `baselines.py`: Naive Laplace and Smooth-like approximations; local sensitivity helpers
  - `run_r2t.py`: CLI entry — builds contributions, τ-grid, runs R2T and baselines, prints results
  - `benchmark.py`: incremental-update snapshot benchmark (engineering utility, optional)
  - `tpch_schema.py`: initialize tables from `db/schema.sql`
  - `synthetic_load.py`: populate a small runnable dataset for quick demo
- `db/`
  - `schema.sql`: table definitions (adapted for Q3 without grouping)
  - `load_data.py`: import `.tbl` into PostgreSQL
  - `generate_tbl_duckdb.py`: create TPC-H `.tbl` via DuckDB (SF=1)
- `queries/`
  - `q3_no_group.sql`: Q3 SUM without grouping
  - `q3_join_only.sql`: join-only rows used to construct per-order contributions
- `scripts/`
  - `setup_postgres.ps1`: helper for local PostgreSQL setup
- Root
  - `requirements.txt`: Python dependencies
  - `LICENSE`: license
  - `README.md`

## References
- TPC-H Benchmark Specification, Version 3.0.1, Transaction Processing Performance Council (TPC)
- Dong et al., “Instance-Optimal Algorithms for Differentially Private Query Release,” SIGMOD 2022
- Fang et al., “Shifted Inverse Sensitivity for Extremal Queries under User-Level DP,” CCS 2022
