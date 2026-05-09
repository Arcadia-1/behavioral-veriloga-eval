#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _rising_edges(rows, col, threshold=0.45):
    edges = []
    for i in range(1, len(rows)):
        if rows[i - 1][col] < threshold <= rows[i][col]:
            edges.append(rows[i]["time"])
    return edges


def check_csv(csv_path):
    rows = _rows(csv_path)
    required = {"time", "clk_in", "clk_out", "lock"} | {f"div_code_{i}" for i in range(8)}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing clk/divider columns"]}
    ratio = sum((1 << i) if rows[0][f"div_code_{i}"] > 0.45 else 0 for i in range(8)) or 1
    in_edges = _rising_edges(rows, "clk_in")
    out_edges = _rising_edges(rows, "clk_out")
    if len(in_edges) < max(12, ratio * 2) or len(out_edges) < 3:
        return {"pass": False, "score": 0.0, "notes": [f"not_enough_edges ratio={ratio} in={len(in_edges)} out={len(out_edges)}"]}
    intervals = []
    for a, b in zip(out_edges, out_edges[1:]):
        intervals.append(sum(1 for t in in_edges if a < t <= b))
    measured = intervals[1:] if len(intervals) > 2 else intervals
    mismatch = [n for n in measured if n != ratio]
    final_lock_high = rows[-1]["lock"] > 0.45
    high_seen = any(r["clk_out"] > 0.45 for r in rows)
    low_seen = any(r["clk_out"] <= 0.45 for r in rows)
    ok = not mismatch and final_lock_high and high_seen and low_seen
    return {
        "pass": ok,
        "score": 1.0 if ok else 0.0,
        "notes": [f"ratio={ratio} in_edges={len(in_edges)} out_edges={len(out_edges)} intervals={measured} lock={int(final_lock_high)}"],
    }


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
