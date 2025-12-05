from pathlib import Path
from .db import fetch_df

def baseline_sum(mktsegment: str, cutoff_date: str):
    sql = Path("queries/q3_no_group.sql").read_text(encoding="utf-8")
    df = fetch_df(sql, (mktsegment, cutoff_date))
    return float(df.loc[0, "revenue"]) if len(df) else 0.0

def join_rows(mktsegment: str, cutoff_date: str):
    sql = Path("queries/q3_join_only.sql").read_text(encoding="utf-8")
    return fetch_df(sql, (mktsegment, cutoff_date))
