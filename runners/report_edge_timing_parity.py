#!/usr/bin/env python3
"""Diagnostic edge-timing parity report between an EVAS and a Spectre tran CSV.

Motivation (2026-06-11 triage, testspace/edge-timing-triage-20260611): a flat
picosecond gate on digital edge crossing times systematically over-flags when
the Spectre evidence was produced under the Spectre X `ax` preset, because `ax`
overrides testbench maxstep and the exported rows are sparse — the crossing
time is interpolated between rows, so its resolution is bounded by the local
row spacing. This tool therefore reports, for every digital signal:

  - max edge crossing-time delta (linear interpolation on native rows)
  - the local row spacing of BOTH waveforms around the worst edge
  - a row-spacing-aware verdict instead of a flat gate:
      pass                 delta <= gate
      fail_interp_limited  delta >  gate but < 0.5 * max(row spacings)
                           (NOT resolvable from this evidence; rerun strict)
      fail_parity          delta robust against row spacing (engine question)
      edge_structure_mismatch  edge count/direction differ (behavior question)

It NEVER changes scoring; it is a triage layer to attribute parity failures
before anyone edits engines or thresholds.

Usage:
  python3 runners/report_edge_timing_parity.py EVAS.csv SPECTRE.csv [--gate-ps 5]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def load_csv(path: Path) -> tuple[list[str], list[list[float]]]:
    with path.open() as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = []
        for raw in reader:
            try:
                rows.append([float(x) for x in raw])
            except ValueError:
                continue
    return header, rows


def column(header: list[str], rows: list[list[float]], name: str) -> list[float]:
    idx = header.index(name)
    return [r[idx] for r in rows]


def infer_digital(vals: list[float]) -> tuple[bool, float, float]:
    """Mirror of run_gold_dual_suite.compare_waveforms digital inference."""
    if not vals:
        return False, 0.0, 0.0
    lo, hi = min(vals), max(vals)
    span = hi - lo
    if span < 1e-6:
        return False, lo, hi
    if abs(lo) > max(0.10, 0.15 * span) or hi < 0.30:
        return False, lo, hi
    tol = max(0.15 * span, 0.05)
    near = sum(1 for v in vals if abs(v - lo) <= tol or abs(v - hi) <= tol)
    return (near / len(vals)) >= 0.95, lo, hi


def edges_with_spacing(
    times: list[float], vals: list[float], vth: float
) -> list[tuple[float, int, float]]:
    out = []
    for i in range(1, len(times)):
        a, b = vals[i - 1] - vth, vals[i] - vth
        if a == 0.0 and b == 0.0:
            continue
        if (a < 0.0 <= b) or (a > 0.0 >= b):
            dv = b - a
            frac = 0.0 if abs(dv) < 1e-30 else max(0.0, min(1.0, -a / dv))
            t = times[i - 1] + frac * (times[i] - times[i - 1])
            direction = 1 if b > a else -1
            out.append((t, direction, times[i] - times[i - 1]))
    return out


def compare_signal(
    et: list[float], ev: list[float],
    st: list[float], sv: list[float],
    gate_s: float,
) -> dict | None:
    de, lo_e, hi_e = infer_digital(ev)
    ds, lo_s, hi_s = infer_digital(sv)
    if not (de and ds):
        return None
    vth = 0.5 * (min(lo_e, lo_s) + max(hi_e, hi_s))
    e_edges = edges_with_spacing(et, ev, vth)
    s_edges = edges_with_spacing(st, sv, vth)
    if len(e_edges) != len(s_edges):
        return {"status": "edge_structure_mismatch",
                "reason": f"edge_count {len(e_edges)} vs {len(s_edges)}"}
    if any(e[1] != s[1] for e, s in zip(e_edges, s_edges)):
        return {"status": "edge_structure_mismatch", "reason": "edge_direction_mismatch"}
    if not e_edges:
        return None
    deltas = [abs(e[0] - s[0]) for e, s in zip(e_edges, s_edges)]
    worst = max(range(len(deltas)), key=deltas.__getitem__)
    delta = deltas[worst]
    spacing = max(e_edges[worst][2], s_edges[worst][2])
    if delta <= gate_s:
        status = "pass"
    elif delta < 0.5 * spacing:
        status = "fail_interp_limited"
    else:
        status = "fail_parity"
    return {
        "status": status,
        "max_delta_ps": round(delta * 1e12, 3),
        "worst_edge_time_s": e_edges[worst][0],
        "row_spacing_ps": round(spacing * 1e12, 2),
        "edge_count": len(e_edges),
        "gate_ps": round(gate_s * 1e12, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evas_csv", type=Path)
    parser.add_argument("spectre_csv", type=Path)
    parser.add_argument("--gate-ps", type=float, default=5.0)
    parser.add_argument("--json-out", type=Path, default=None)
    args = parser.parse_args()

    eh, er = load_csv(args.evas_csv)
    sh, sr = load_csv(args.spectre_csv)
    et, st = column(eh, er, "time"), column(sh, sr, "time")
    report = {}
    for sig in sorted((set(eh) & set(sh)) - {"time"}):
        res = compare_signal(
            et, column(eh, er, sig), st, column(sh, sr, sig),
            args.gate_ps * 1e-12,
        )
        if res is not None:
            report[sig] = res
    out = {
        "evas_csv": str(args.evas_csv),
        "spectre_csv": str(args.spectre_csv),
        "evas_rows": len(er),
        "spectre_rows": len(sr),
        "signals": report,
    }
    text = json.dumps(out, indent=1)
    if args.json_out:
        args.json_out.write_text(text)
    print(text)
    worst = {"pass": 0, "fail_interp_limited": 1,
             "edge_structure_mismatch": 2, "fail_parity": 3}
    rank = max((worst[r["status"]] for r in report.values()), default=0)
    return 0 if rank == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
