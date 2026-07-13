#!/usr/bin/env python3
"""Flatten data/latency/history.json into data/latency/latency_history.csv.

One row per (date, venue) with p50/p95 in ms. Used to give dataset-platform
viewers (Kaggle preview table, Hugging Face dataset viewer + Parquet indexing)
a tabular file. Rerun after each sync to keep the CSV fresh.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "latency" / "history.json"
OUT = ROOT / "data" / "latency" / "latency_history.csv"


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    rows = []
    for day in data.get("history", []):
        date = day.get("date")
        for venue, stats in day.get("venues", {}).items():
            rows.append(
                {
                    "date": date,
                    "venue": venue,
                    "p50_ms": stats.get("p50"),
                    "p95_ms": stats.get("p95"),
                }
            )
    rows.sort(key=lambda r: (r["date"], r["venue"]))
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "venue", "p50_ms", "p95_ms"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
