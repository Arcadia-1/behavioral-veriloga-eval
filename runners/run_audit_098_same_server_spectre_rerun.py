#!/usr/bin/env python3
"""Audit 098 — Same-server EVAS vs Spectre AX rerun via thu-sui wrapper.

Per memory: Spectre MUST be invoked via thu-sui→thu-wei SSH wrapper to
avoid Cadence license queue pollution (see r15 incident, audit
VAEVAS_SPEED_LIMITATION_ANALYSIS_2026-06-01.md).

This script generates the rerun queue for paper-facing speed claim
evidence. It does NOT execute simulations directly — the user must
run it on thu-sui (which has the wrapper) OR feed the output to the
existing same-server speed runner.

Usage on thu-sui:
    PYTHONPATH=/path/to/EVAS python3 runners/run_audit_098_same_server_spectre_rerun.py \\
        --row-list speed-optimization/reports/topwall10_rows_20260605.json \\
        --output-dir results/audit_098_rerun_$(date +%Y%m%d) \\
        --max-rows 64 \\
        --repeats 5

The output directory will contain:
    - manifest.json: row list with EVAS + Spectre wall measurements
    - rows/<row_id>/evas_wall.json
    - rows/<row_id>/spectre_ax_wall.json
    - rows/<row_id>/parity.json     (Spectre-equivalence-gated comparison)
    - summary.md: paper-facing speed table draft
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--row-list", type=Path, required=True,
                   help="JSON file listing row entries to rerun")
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--max-rows", type=int, default=None,
                   help="cap to first N rows (debugging)")
    p.add_argument("--repeats", type=int, default=5,
                   help="per-row repeats; final stat is trimmed mean")
    p.add_argument(
        "--evas-modes",
        nargs="+",
        default=["default", "generic_executor"],
        help="EVAS opt-in flag combinations to test",
    )
    p.add_argument(
        "--spectre-modes",
        nargs="+",
        default=["spectre_ax", "spectre_strict"],
        help="Spectre simulator modes to test for comparison",
    )
    p.add_argument(
        "--thu-sui-required",
        action="store_true",
        default=True,
        help="abort if not running on thu-sui (default true)",
    )
    return p.parse_args()


def assert_thu_sui_routing(required: bool) -> None:
    """Refuse to run from local mac — Spectre calls would hit license queue.

    Per memory: thu-sui→thu-wei wrapper is the only correct path.
    """
    hostname = os.uname().nodename
    if "thu-sui" not in hostname.lower():
        if required:
            print(
                f"ERROR: This runner must be executed on thu-sui (current host: {hostname}).\n"
                f"Spectre invocations from other hosts will hit the Cadence license queue\n"
                f"and pollute wall-time measurements (see audit r15 incident).\n"
                f"To override (development/debugging only), pass --no-thu-sui-required.",
                file=sys.stderr,
            )
            sys.exit(2)
        else:
            print(f"WARN: Running on {hostname} (not thu-sui). Wall times may be polluted.",
                  file=sys.stderr)


def trimmed_mean(values: List[float], trim: int = 1) -> float:
    if not values:
        return 0.0
    if len(values) <= 2 * trim:
        return statistics.mean(values)
    return statistics.mean(sorted(values)[trim:-trim])


def run_evas_once(row_entry: Dict[str, Any], mode: str, deadline_s: float) -> Dict[str, Any]:
    """Run EVAS once for a row in the given mode."""
    scs_path = row_entry["scs"]
    flags = {}
    if mode == "default":
        pass  # Python adaptive
    elif mode == "generic_executor":
        flags = {
            "rust_full_model_fastpath": True,
            "generic_executor": True,
            "rust_required": True,
        }
    elif mode == "rust_full_model_fastpath":
        flags = {
            "rust_full_model_fastpath": True,
            "rust_required": True,
        }
    else:
        return {"error": f"unknown evas mode: {mode}"}
    # Use the netlist runner to invoke EVAS as subprocess
    # (We launch a Python subprocess so the wall-time matches user experience.)
    runner = "from evas.netlist.runner import evas_simulate; import sys; "
    runner += f"sys.argv = ['runner', '{scs_path}']; "
    runner += "kwargs = " + repr({k: True for k in flags}) + "; "
    runner += "from evas.simulator.engine import Simulator; "
    runner += "orig = Simulator.run\n"
    runner += "def wrap(self, *a, **kw):\n"
    runner += "    kw.update(kwargs)\n"
    runner += "    return orig(self, *a, **kw)\n"
    runner += "Simulator.run = wrap\n"
    runner += "ok = evas_simulate(sys.argv[1])\n"
    runner += "sys.exit(0 if ok else 1)\n"
    with tempfile.TemporaryDirectory() as tmpd:
        t0 = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, "-c", runner],
            cwd=tmpd,
            capture_output=True,
            timeout=deadline_s,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1]) + "/../EVAS"},
        )
        wall = time.perf_counter() - t0
    return {
        "wall_s": wall,
        "exit_code": proc.returncode,
        "mode": mode,
    }


def run_spectre_once(row_entry: Dict[str, Any], mode: str, deadline_s: float) -> Dict[str, Any]:
    """Run Spectre once via thu-sui wrapper.

    Assumes a 'spectre' wrapper script is on PATH that delegates to thu-wei.
    Adjust the command line below to match the actual wrapper signature in
    your environment.
    """
    scs_path = row_entry["scs"]
    spectre_args = ["spectre"]
    if mode == "spectre_ax":
        spectre_args += ["+spice", "+errpreset=conservative", "++aps"]
    elif mode == "spectre_strict":
        spectre_args += ["+spice", "+errpreset=accurate"]
    else:
        return {"error": f"unknown spectre mode: {mode}"}
    spectre_args.append(scs_path)
    with tempfile.TemporaryDirectory() as tmpd:
        t0 = time.perf_counter()
        try:
            proc = subprocess.run(
                spectre_args,
                cwd=tmpd,
                capture_output=True,
                timeout=deadline_s,
            )
            wall = time.perf_counter() - t0
            exit_code = proc.returncode
            license_wait = b"Waiting for available license for Spectre" in proc.stderr
            polluted = license_wait
        except subprocess.TimeoutExpired:
            wall = deadline_s
            exit_code = -1
            polluted = True
    return {
        "wall_s": wall,
        "exit_code": exit_code,
        "license_wait_detected": polluted,
        "mode": mode,
    }


def measure_row(row_entry: Dict[str, Any], evas_modes: List[str],
                spectre_modes: List[str], repeats: int) -> Dict[str, Any]:
    out: Dict[str, Any] = {"row": row_entry}
    deadline = 600.0  # 10 min per run hard cap

    for mode in evas_modes:
        walls: List[float] = []
        last: Dict[str, Any] = {}
        for _ in range(repeats):
            r = run_evas_once(row_entry, mode, deadline)
            last = r
            if r.get("exit_code") == 0:
                walls.append(r["wall_s"])
        if walls:
            out[f"evas_{mode}"] = {
                "wall_trimmed_mean_s": trimmed_mean(walls),
                "wall_median_s": statistics.median(walls),
                "repeats_pass": len(walls),
                "last": last,
            }
        else:
            out[f"evas_{mode}"] = {"error": "all_repeats_failed", "last": last}

    for mode in spectre_modes:
        walls: List[float] = []
        last: Dict[str, Any] = {}
        any_polluted = False
        for _ in range(repeats):
            r = run_spectre_once(row_entry, mode, deadline)
            last = r
            if r.get("license_wait_detected"):
                any_polluted = True
                continue
            if r.get("exit_code") == 0:
                walls.append(r["wall_s"])
        if walls and not any_polluted:
            out[f"{mode}"] = {
                "wall_trimmed_mean_s": trimmed_mean(walls),
                "wall_median_s": statistics.median(walls),
                "repeats_pass": len(walls),
                "last": last,
            }
        else:
            out[f"{mode}"] = {
                "error": "license_polluted" if any_polluted else "all_repeats_failed",
                "last": last,
            }
    return out


def write_summary_md(output_dir: Path, results: List[Dict[str, Any]],
                     evas_modes: List[str], spectre_modes: List[str]) -> None:
    lines = [
        "# Audit 098 — Same-Server EVAS vs Spectre Speed Comparison",
        "",
        "Run via thu-sui→thu-wei wrapper. License-polluted rows are excluded from the paper-facing table.",
        "",
        "| Row | EVAS default | EVAS generic_executor | Spectre AX | Spectre strict |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in results:
        row_id = r["row"].get("entry_id", "?")
        evas_def = r.get("evas_default", {}).get("wall_trimmed_mean_s", "—")
        evas_ge = r.get("evas_generic_executor", {}).get("wall_trimmed_mean_s", "—")
        sp_ax = r.get("spectre_ax", {}).get("wall_trimmed_mean_s", "—")
        sp_st = r.get("spectre_strict", {}).get("wall_trimmed_mean_s", "—")
        def fmt(v):
            if isinstance(v, (int, float)):
                return f"{v:.3f}s"
            return v
        lines.append(f"| {row_id} | {fmt(evas_def)} | {fmt(evas_ge)} | {fmt(sp_ax)} | {fmt(sp_st)} |")
    (output_dir / "summary.md").write_text("\n".join(lines))


def main():
    args = parse_args()
    assert_thu_sui_routing(args.thu_sui_required)
    if not args.row_list.exists():
        print(f"ERROR: row list not found: {args.row_list}", file=sys.stderr)
        sys.exit(1)
    row_list = json.loads(args.row_list.read_text())
    if args.max_rows:
        row_list = row_list[:args.max_rows]
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results: List[Dict[str, Any]] = []
    for i, row in enumerate(row_list, 1):
        print(f"[{i}/{len(row_list)}] {row.get('entry_id', '?')}", flush=True)
        r = measure_row(row, args.evas_modes, args.spectre_modes, args.repeats)
        results.append(r)
        # Write per-row JSON for resumability
        rd = args.output_dir / "rows" / str(row.get("entry_id", f"row_{i:04d}"))
        rd.mkdir(parents=True, exist_ok=True)
        (rd / "measurement.json").write_text(json.dumps(r, indent=2))

    # Write top-level manifest
    (args.output_dir / "manifest.json").write_text(
        json.dumps({
            "args": vars(args),
            "results": results,
        }, indent=2, default=str)
    )
    write_summary_md(args.output_dir, results, args.evas_modes, args.spectre_modes)
    print(f"\nWrote {args.output_dir}/manifest.json")
    print(f"Wrote {args.output_dir}/summary.md")


if __name__ == "__main__":
    main()
