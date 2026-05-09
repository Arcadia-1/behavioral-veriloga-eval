#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _weighted_high_fraction(rows, col, threshold):
    high_dt = 0.0
    total_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        total_dt += dt
        if 0.5 * (rows[idx - 1][col] + rows[idx][col]) > threshold:
            high_dt += dt
    return high_dt / max(total_dt, 1e-18)


def _rising_edges(rows, col, threshold):
    edges = []
    prev = rows[0][col]
    for row in rows[1:]:
        cur = row[col]
        if prev < threshold <= cur:
            edges.append(row["time"])
        prev = cur
    return edges


def _window(rows, start, end):
    return [r for r in rows if start <= r["time"] <= end]


def check_csv(csv_path):
    rows = _rows(csv_path)
    required = {"time", "ref", "div", "up", "dn"}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing time/ref/div/up/dn"]}
    vth = max(r["ref"] for r in rows) * 0.5
    first = _window(rows, 20e-9, 120e-9)
    second = _window(rows, 160e-9, 260e-9)
    if len(first) < 4 or len(second) < 4:
        return {"pass": False, "score": 0.0, "notes": ["insufficient_window_samples"]}
    up_first = _weighted_high_fraction(first, "up", vth)
    dn_first = _weighted_high_fraction(first, "dn", vth)
    up_second = _weighted_high_fraction(second, "up", vth)
    dn_second = _weighted_high_fraction(second, "dn", vth)
    up_pulses_first = len(_rising_edges(first, "up", vth))
    dn_pulses_second = len(_rising_edges(second, "dn", vth))
    overlap_dt = 0.0
    total_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        total_dt += dt
        up_mid = 0.5 * (rows[idx - 1]["up"] + rows[idx]["up"])
        dn_mid = 0.5 * (rows[idx - 1]["dn"] + rows[idx]["dn"])
        if up_mid > vth and dn_mid > vth:
            overlap_dt += dt
    overlap_frac = overlap_dt / max(total_dt, 1e-18)
    ok = (
        0.001 <= up_first <= 0.08
        and dn_first <= 0.01
        and 0.001 <= dn_second <= 0.08
        and up_second <= 0.01
        and up_pulses_first >= 4
        and dn_pulses_second >= 4
        and overlap_frac <= 0.01
    )
    note = (
        f"up_first={up_first:.4f} dn_first={dn_first:.4f} "
        f"up_second={up_second:.4f} dn_second={dn_second:.4f} "
        f"up_pulses_first={up_pulses_first} dn_pulses_second={dn_pulses_second} "
        f"overlap_frac={overlap_frac:.4f}"
    )
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": [note]}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
