#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys

TASK_DIR = Path(__file__).resolve().parent


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _val(row, name):
    return row.get(name.lower(), 0.0)


def check_csv(csv_path):
    rows = _rows(csv_path)
    if len(rows) < 4:
        return {"pass": False, "score": 0.0, "notes": ["too_few_rows"]}

    decisions = []
    prev_clk = _val(rows[0], "CLK")
    for idx, row in enumerate(rows[1:], start=1):
        clk = _val(row, "CLK")
        if prev_clk <= 0.45 and clk > 0.45:
            target_t = _val(row, "time") + 0.15e-9
            sample = min(rows[idx:], key=lambda r: abs(_val(r, "time") - target_t))
            diff = _val(row, "VINP") - _val(row, "VINN")
            out = _val(sample, "OUT_P")
            decisions.append((diff, out))
        prev_clk = clk

    high_ok = any(diff > 1.2e-3 and out > 0.6 for diff, out in decisions)
    low_ok = any(diff < -1.2e-3 and out < 0.3 for diff, out in decisions)
    wrong_high = any(diff > 1.2e-3 and out < 0.3 for diff, out in decisions)
    wrong_low = any(diff < -1.2e-3 and out > 0.6 for diff, out in decisions)
    ok = high_ok and low_ok and not wrong_high and not wrong_low
    notes = [
        f"clock_decisions={len(decisions)}",
        f"high_ok={int(high_ok)}",
        f"low_ok={int(low_ok)}",
    ]
    if wrong_high:
        notes.append("wrong_high_decision")
    if wrong_low:
        notes.append("wrong_low_decision")
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": notes}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
