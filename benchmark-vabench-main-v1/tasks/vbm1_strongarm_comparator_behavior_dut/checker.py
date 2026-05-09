#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


ALIASES = {
    "out_p": ("out_p", "outp", "dcmp_p", "dcmpp"),
    "out_n": ("out_n", "outn", "dcmp_n", "dcmpn"),
    "inp": ("inp", "vinp"),
    "inn": ("inn", "vinn"),
}


def _rows(csv_path):
    rows = []
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            row = {k.lower(): float(v) for k, v in raw.items() if v not in ("", None)}
            for target, names in ALIASES.items():
                if target not in row:
                    for name in names:
                        if name in row:
                            row[target] = row[name]
                            break
            rows.append(row)
    return rows


def _has(row, names):
    return all(name in row for name in names)


def _check_reset_priority(rows):
    required = {"time", "rst", "inp", "inn", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing reset-priority columns"
    threshold = 0.45
    reset_window = [r for r in rows if r["rst"] > threshold]
    active_window = [r for r in rows if r["time"] >= 24e-9 and r["rst"] < threshold]
    if not reset_window or not active_window:
        return False, "insufficient_reset_or_active_window"
    reset_outp_max = max(r["out_p"] for r in reset_window)
    reset_outn_max = max(r["out_n"] for r in reset_window)
    high_rows = [r for r in active_window if r["inp"] > r["inn"] + 5e-3]
    low_rows = [r for r in active_window if r["inp"] + 5e-3 < r["inn"]]
    if not high_rows or not low_rows:
        return False, "missing_post_reset_polarity_windows"
    high_outp = sum(1 for r in high_rows if r["out_p"] > threshold) / len(high_rows)
    high_outn = sum(1 for r in high_rows if r["out_n"] < threshold) / len(high_rows)
    low_outp = sum(1 for r in low_rows if r["out_p"] < threshold) / len(low_rows)
    low_outn = sum(1 for r in low_rows if r["out_n"] > threshold) / len(low_rows)
    ok = reset_outp_max < 0.1 and reset_outn_max < 0.1 and high_outp > 0.75 and high_outn > 0.75 and low_outp > 0.75 and low_outn > 0.75
    return ok, f"reset_outp_max={reset_outp_max:.3f} reset_outn_max={reset_outn_max:.3f} high_outp={high_outp:.3f} high_outn={high_outn:.3f} low_outp={low_outp:.3f} low_outn={low_outn:.3f}"


def _check_clocked_comparator(rows):
    required = {"time", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out_p/out_n"
    threshold = 0.45
    out_p = [r["out_p"] for r in rows]
    out_n = [r["out_n"] for r in rows]
    out_p_span = max(out_p) - min(out_p)
    out_n_span = max(out_n) - min(out_n)
    if out_p_span < threshold or out_n_span < threshold:
        return False, f"insufficient_toggle out_p_span={out_p_span:.3f} out_n_span={out_n_span:.3f}"
    pre = [r["out_p"] for r in rows if 0.6e-9 < r["time"] < 2.0e-9]
    post = [r["out_p"] for r in rows if 2.5e-9 < r["time"] < 4.0e-9]
    if not pre or not post:
        return False, "insufficient_polarity_windows"
    pre_high_frac = sum(1 for v in pre if v > threshold) / len(pre)
    post_low_frac = sum(1 for v in post if v < threshold) / len(post)
    ok = pre_high_frac >= 0.4 and post_low_frac >= 0.4
    return ok, f"pre_high_frac={pre_high_frac:.3f} post_low_frac={post_low_frac:.3f}"


def check_csv(csv_path):
    rows = _rows(csv_path)
    if not rows:
        return {"pass": False, "score": 0.0, "notes": ["empty_csv"]}
    if _has(rows[0], {"rst", "inp", "inn", "out_p", "out_n"}):
        ok, note = _check_reset_priority(rows)
    else:
        ok, note = _check_clocked_comparator(rows)
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": [note]}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
