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
    required = {"time", "rdy", "dp_dac_3", "dp_dac_0"}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing rdy/dp_dac_3/dp_dac_0"]}
    rdy_edges = _rising_edges(rows, "rdy")
    bit_activity = {}
    for bit in range(4):
        col = f"dp_dac_{bit}"
        if col not in rows[0]:
            return {"pass": False, "score": 0.0, "notes": [f"missing {col}"]}
        vals = [r[col] for r in rows]
        bit_activity[col] = max(vals) - min(vals)
    active_bits = sum(1 for span in bit_activity.values() if span > 0.4)
    ok = len(rdy_edges) >= 3 and active_bits >= 2
    return {
        "pass": ok,
        "score": 1.0 if ok else 0.0,
        "notes": [f"rdy_edges={len(rdy_edges)} active_bits={active_bits} spans={bit_activity}"],
    }


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
