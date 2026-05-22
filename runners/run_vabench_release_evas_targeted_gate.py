#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from run_gold_suite import run_gold_case


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
MANIFEST_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_staging_manifest.json"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / "vabench-release-v1-evas-targeted-gate"

DEFAULT_ENTRIES = (
    "vbr1_l1_calibration_deadband_controller",
    "vbr1_l1_charge_pump_abstraction",
    "vbr1_l1_dac_mismatch_unit_weighting_model",
    "vbr1_l1_event_pulse_stretcher",
    "vbr1_l1_loop_filter_abstraction",
    "vbr1_l2_amplifier_filter_chain",
)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_or_abs(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def normalize_output_root(path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path


def selected_bundles(
    manifest: dict[str, object],
    *,
    entries: set[str],
    forms: set[str] | None,
    variants: set[str] | None,
) -> list[dict[str, object]]:
    bundles: list[dict[str, object]] = []
    for record in manifest.get("bundles", []):
        if not isinstance(record, dict) or record.get("status") != "ready":
            continue
        if str(record.get("entry_id")) not in entries:
            continue
        if forms and str(record.get("form")) not in forms:
            continue
        if variants and str(record.get("variant")) not in variants:
            continue
        bundles.append(record)
    return sorted(bundles, key=lambda row: (str(row["entry_id"]), str(row["form"]), str(row["variant"])))


def evas_expected_met(raw_result: dict[str, object], expected_result: str) -> bool:
    status = str(raw_result.get("status", "UNKNOWN"))
    if expected_result == "pass":
        return status == "PASS"
    if expected_result == "fail":
        return status == "FAIL_SIM_CORRECTNESS"
    return False


def run_gate(
    bundles: list[dict[str, object]],
    *,
    output_root: Path,
    timeout_s: int,
) -> dict[str, object]:
    results: list[dict[str, object]] = []
    started_at = datetime.now().isoformat(timespec="seconds")
    partial_path = output_root / "summary.partial.json"
    summary_path = output_root / "summary.json"

    for index, record in enumerate(bundles, start=1):
        task_dir = ROOT / str(record["staged_task_dir"])
        result_root = output_root / str(record["entry_id"]) / str(record["form"]) / str(record["variant"])
        t0 = time.perf_counter()
        raw_result = run_gold_case(task_dir, result_root, timeout_s)
        expected_result = str(record["expected_result"])
        row = {
            "entry_id": record["entry_id"],
            "form": record["form"],
            "variant": record["variant"],
            "expected_result": expected_result,
            "expected_result_met": evas_expected_met(raw_result, expected_result),
            "staged_task_dir": record["staged_task_dir"],
            "result_root": rel_or_abs(result_root),
            "wall_time_s": time.perf_counter() - t0,
            "raw_result": raw_result,
        }
        results.append(row)
        partial = {
            "status": "running",
            "started_at": started_at,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "tasks_total": len(bundles),
            "tasks_completed": index,
            "expected_met_count": sum(1 for item in results if item["expected_result_met"] is True),
            "expected_miss_count": sum(1 for item in results if item["expected_result_met"] is False),
            "results": results,
        }
        partial_path.write_text(json.dumps(partial, indent=2) + "\n", encoding="utf-8")

    summary = {
        "status": "pass" if all(row["expected_result_met"] for row in results) else "fail",
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "tasks_total": len(results),
        "pass_count": sum(1 for row in results if row["raw_result"].get("status") == "PASS"),
        "nonpass_count": sum(1 for row in results if row["raw_result"].get("status") != "PASS"),
        "expected_met_count": sum(1 for row in results if row["expected_result_met"] is True),
        "expected_miss_count": sum(1 for row in results if row["expected_result_met"] is False),
        "results": results,
        "notes": [
            "EVAS-only targeted gate: buggy variants are expected to fail behavior in EVAS.",
            "Spectre buggy-fail confirmation is handled by the dual rerun smoke gate.",
        ],
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if partial_path.exists():
        partial_path.unlink()
    return summary


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run EVAS-only targeted checks for modified vaBench release tasks.")
    ap.add_argument("--manifest", default=str(MANIFEST_JSON), help="Staging manifest JSON.")
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Output directory.")
    ap.add_argument("--timeout-s", type=int, default=90, help="Per-task EVAS timeout.")
    ap.add_argument("--entry", action="append", help="Restrict to release entry id; may be repeated.")
    ap.add_argument("--form", action="append", choices=("dut", "tb", "bugfix", "e2e"), help="Restrict by form.")
    ap.add_argument("--variant", action="append", choices=("gold", "fixed", "buggy"), help="Restrict by variant.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    output_root = normalize_output_root(args.output_root)
    entries = set(args.entry) if args.entry else set(DEFAULT_ENTRIES)
    bundles = selected_bundles(
        read_json(manifest_path),
        entries=entries,
        forms=set(args.form) if args.form else None,
        variants=set(args.variant) if args.variant else None,
    )
    summary = run_gate(bundles, output_root=output_root, timeout_s=args.timeout_s)
    print(json.dumps(summary, indent=2))
    return 0 if summary["expected_miss_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
