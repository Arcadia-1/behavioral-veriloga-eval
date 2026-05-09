#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _val(row, name):
    return row.get(name.lower(), 0.0)


def check_csv(csv_path):
    rows = _rows(csv_path)
    if len(rows) < 4:
        return {"pass": False, "score": 0.0, "notes": ["too_few_rows"]}
    # Ignore transition edges; sample the settled tail of each PWL plateau.
    probes = [20e-9, 45e-9, 70e-9, 95e-9, 115e-9]
    samples = [min(rows, key=lambda r: abs(_val(r, "time") - t)) for t in probes]
    expected = []
    for row in samples:
        x = _val(row, "raw_level")
        y = min(max(x, 0.18), 0.72)
        expected.append((x, _val(row, "clamped_level"), y))
    errors = [abs(y - ref) for _x, y, ref in expected]
    low_ok = any(x < 0.18 and abs(y - 0.18) < 0.035 for x, y, _ in expected)
    mid_ok = any(0.25 < x < 0.65 and abs(y - x) < 0.04 for x, y, _ in expected)
    high_ok = any(x > 0.72 and abs(y - 0.72) < 0.035 for x, y, _ in expected)
    max_err = max(errors) if errors else 1.0
    ok = low_ok and mid_ok and high_ok and max_err < 0.06
    notes = [
        f"low_clamp_ok={int(low_ok)}",
        f"mid_follow_ok={int(mid_ok)}",
        f"high_clamp_ok={int(high_ok)}",
        f"max_err={max_err:.4g}",
    ]
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": notes}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
