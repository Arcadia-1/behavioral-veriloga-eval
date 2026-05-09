#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _nearest(rows, t):
    return min(rows, key=lambda r: abs(r["time"] - t))


def check_csv(csv_path):
    rows = _rows(csv_path)
    required = {"time", "vin", "clk", "vout"}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing time/vin/clk/vout"]}
    vth = 0.45
    edges = []
    for i in range(1, len(rows)):
        if rows[i - 1]["clk"] <= vth < rows[i]["clk"]:
            edges.append(rows[i]["time"])
    if len(edges) < 5:
        return {"pass": False, "score": 0.0, "notes": [f"too_few_edges={len(edges)}"]}
    mismatches = 0
    checked = 0
    taperture = 200e-12
    settle = 1.0e-9
    for edge_t in edges[:6]:
        vin_sample = _nearest(rows, edge_t + taperture)["vin"]
        vout_settled = _nearest(rows, edge_t + taperture + settle)["vout"]
        checked += 1
        if abs(vout_settled - vin_sample) > 0.045:
            mismatches += 1
    hold_failures = 0
    for a, b in zip(edges[:4], edges[1:5]):
        window = [r["vout"] for r in rows if a + 2e-9 <= r["time"] <= b - 2e-9]
        if len(window) >= 2 and max(window) - min(window) > 0.04:
            hold_failures += 1
    ok = checked >= 5 and mismatches <= 1 and hold_failures == 0
    return {
        "pass": ok,
        "score": 1.0 if ok else 0.0,
        "notes": [f"edges={len(edges)} checked={checked} mismatches={mismatches} hold_failures={hold_failures}"],
    }


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
