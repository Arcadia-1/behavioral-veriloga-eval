#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from bridge_preflight import bridge_preflight, resolve_cadence_cshrc
from run_gold_dual_suite import default_bridge_repo, run_dual_case
from run_gold_suite import benchmark_root


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
MANIFEST_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_staging_manifest.json"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / "vabench-release-v1-dual-rerun"
PRIMARY_VARIANTS = {"gold", "fixed"}


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
        path = benchmark_root() / path
    path.mkdir(parents=True, exist_ok=True)
    return path


def bundle_task_dir(record: dict[str, object]) -> Path:
    task_dir = ROOT / str(record["staged_task_dir"])
    if not task_dir.exists():
        raise FileNotFoundError(f"staged task dir missing: {task_dir}")
    return task_dir


def select_bundles(
    *,
    manifest: dict[str, object],
    include_buggy: bool,
    entry: set[str] | None,
    form: set[str] | None,
    variant: set[str] | None,
    limit: int | None,
) -> list[dict[str, object]]:
    bundles = []
    for record in manifest.get("bundles", []):
        if not isinstance(record, dict) or record.get("status") != "ready":
            continue
        record_variant = str(record["variant"])
        if not include_buggy and record_variant not in PRIMARY_VARIANTS:
            continue
        if entry and str(record["entry_id"]) not in entry:
            continue
        if form and str(record["form"]) not in form:
            continue
        if variant and record_variant not in variant:
            continue
        bundles.append(record)
    bundles.sort(key=lambda row: (str(row["entry_id"]), str(row["form"]), str(row["variant"])))
    if limit is not None:
        bundles = bundles[:limit]
    return bundles


def expected_result_met(raw_result: dict[str, object], expected_result: str) -> bool:
    raw_status = str(raw_result.get("status", "UNKNOWN"))
    if expected_result == "pass":
        return raw_status == "PASS"
    if expected_result == "fail":
        evas = raw_result.get("evas")
        spectre = raw_result.get("spectre")
        if not isinstance(evas, dict) or not isinstance(spectre, dict):
            return False
        if evas.get("status") != "FAIL_SIM_CORRECTNESS":
            return False
        if not spectre.get("ok"):
            return False
        try:
            spectre_behavior_score = float(spectre.get("behavior_score", 1.0))
        except (TypeError, ValueError):
            return False
        if spectre_behavior_score >= 1.0:
            return False
        if raw_status in {"PASS", "FAIL_INFRA", "FAIL_SPECTRE", "FAIL_TB_COMPILE", "FAIL_DUT_COMPILE"}:
            return False
        return raw_status in {"FAIL_EVAS", "FAIL_SPECTRE_BEHAVIOR"}
    return False


def dry_run_raw_result(task_dir: Path) -> dict[str, object]:
    meta_path = task_dir / "meta.json"
    meta = read_json(meta_path) if meta_path.exists() else {}
    task_id = meta.get("task_id") or meta.get("id") or task_dir.name
    checker_task_id = meta.get("checker_task_id") or meta.get("source_checker_task_id") or task_id
    return {
        "task_id": task_id,
        "checker_task_id": checker_task_id,
        "status": "DRY_RUN",
        "notes": ["dry run: simulator calls skipped"],
    }


def write_summary(path: Path, summary: dict[str, object]) -> None:
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def run_bundles(
    *,
    bundles: list[dict[str, object]],
    output_root: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    dry_run: bool,
) -> dict[str, object]:
    results: list[dict[str, object]] = []
    started = datetime.now().isoformat(timespec="seconds")
    summary_path = output_root / "summary.json"
    partial_path = output_root / "summary.partial.json"
    for idx, record in enumerate(bundles, start=1):
        task_dir = bundle_task_dir(record)
        result_root = output_root / str(record["entry_id"]) / str(record["form"]) / str(record["variant"])
        expected_result = str(record["expected_result"])
        bundle_started_at = datetime.now().isoformat(timespec="seconds")
        bundle_t0 = time.perf_counter()
        if dry_run:
            raw_result = dry_run_raw_result(task_dir)
        else:
            raw_result = run_dual_case(
                task_dir=task_dir,
                output_root=result_root,
                bridge_repo=bridge_repo,
                cadence_cshrc=cadence_cshrc,
                timeout_s=timeout_s,
            )
        bundle_wall_time_s = time.perf_counter() - bundle_t0
        raw_status = str(raw_result.get("status", "UNKNOWN"))
        result = {
            "entry_id": record["entry_id"],
            "form": record["form"],
            "variant": record["variant"],
            "expected_result": expected_result,
            "expected_result_met": expected_result_met(raw_result, expected_result) if not dry_run else None,
            "started_at": bundle_started_at,
            "finished_at": datetime.now().isoformat(timespec="seconds"),
            "wall_time_s": bundle_wall_time_s,
            "staged_task_dir": record["staged_task_dir"],
            "result_root": rel_or_abs(result_root),
            "raw_result": raw_result,
        }
        results.append(result)
        partial = {
            "status": "running",
            "started_at": started,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "tasks_total": len(bundles),
            "tasks_completed": idx,
            "pass_expected_met_count": sum(1 for item in results if item["expected_result_met"] is True),
            "expected_miss_count": sum(1 for item in results if item["expected_result_met"] is False),
            "results": results,
        }
        write_summary(partial_path, partial)

    final = {
        "status": "complete" if not dry_run else "dry_run",
        "started_at": started,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "tasks_total": len(bundles),
        "total_wall_time_s": sum(float(item.get("wall_time_s", 0.0)) for item in results),
        "pass_count": sum(1 for item in results if item["raw_result"].get("status") == "PASS"),
        "nonpass_count": sum(1 for item in results if item["raw_result"].get("status") != "PASS"),
        "expected_met_count": sum(1 for item in results if item["expected_result_met"] is True),
        "expected_miss_count": sum(1 for item in results if item["expected_result_met"] is False),
        "dry_run": dry_run,
        "results": results,
    }
    write_summary(summary_path, final)
    if partial_path.exists():
        partial_path.unlink()
    return final


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run EVAS/Spectre dual rerun on staged vaBench release bundles.")
    ap.add_argument("--manifest", default=str(MANIFEST_JSON), help="dual rerun staging manifest JSON.")
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Output directory for rerun results.")
    ap.add_argument(
        "--bridge-repo",
        default=os.environ.get("VAEVAS_BRIDGE_REPO", str(default_bridge_repo())),
        help="Path to virtuoso-bridge-lite.",
    )
    ap.add_argument(
        "--cadence-cshrc",
        default=os.environ.get("VB_CADENCE_CSHRC", ""),
        help="Remote Cadence cshrc path used to expose spectre on PATH.",
    )
    ap.add_argument("--timeout-s", type=int, default=180, help="Per-bundle simulator timeout.")
    ap.add_argument("--limit", type=int, default=None, help="Optional maximum number of bundles to run.")
    ap.add_argument("--entry", action="append", help="Restrict to one release entry; may be repeated.")
    ap.add_argument("--form", action="append", choices=["dut", "tb", "bugfix", "e2e"], help="Restrict by form.")
    ap.add_argument("--variant", action="append", help="Restrict by staged variant: gold, fixed, or buggy.")
    ap.add_argument("--include-buggy", action="store_true", help="Also run bugfix buggy companion bundles.")
    ap.add_argument("--dry-run", action="store_true", help="Check selection and output shape without simulator calls.")
    ap.add_argument("--skip-bridge-preflight", action="store_true", help="Skip bridge health checks.")
    ap.add_argument("--require-virtuoso-daemon", action="store_true", help="Treat CIW daemon disconnect as a hard blocker.")
    ap.add_argument("--allow-direct-run", action="store_true", help="Allow direct execution outside scripts/run_with_bridge.sh.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = read_json(manifest_path)
    bundles = select_bundles(
        manifest=manifest,
        include_buggy=args.include_buggy,
        entry=set(args.entry) if args.entry else None,
        form=set(args.form) if args.form else None,
        variant=set(args.variant) if args.variant else None,
        limit=args.limit,
    )
    output_root = normalize_output_root(args.output_root)

    if args.dry_run:
        summary = run_bundles(
            bundles=bundles,
            output_root=output_root,
            bridge_repo=Path(args.bridge_repo),
            cadence_cshrc=args.cadence_cshrc or None,
            timeout_s=args.timeout_s,
            dry_run=True,
        )
        print(json.dumps(summary, indent=2))
        return 0

    via_wrapper = os.environ.get("VAEVAS_BRIDGE_WRAPPER") == "1"
    if not via_wrapper and not args.allow_direct_run:
        bridge_failure_reason = os.environ.get("VAEVAS_BRIDGE_FAILURE_REASON", "").strip()
        summary = {
            "status": "blocked",
            "reason": bridge_failure_reason or "direct invocation blocked; use scripts/run_with_bridge.sh",
            "tasks_total": len(bundles),
            "bridge_profile": os.environ.get("VAEVAS_BRIDGE_PROFILE", "") or os.environ.get("BRIDGE_PROFILE", ""),
            "direct_invocation_blocked": True,
            "remediation": [
                "./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py",
                "or add --allow-direct-run if this is an intentional local smoke run",
            ],
        }
        write_summary(output_root / "summary.json", summary)
        print(json.dumps(summary, indent=2))
        return 2

    bridge_repo = Path(args.bridge_repo).resolve()
    if not bridge_repo.exists():
        summary = {"status": "blocked", "reason": f"bridge repo not found: {bridge_repo}", "tasks_total": len(bundles)}
        write_summary(output_root / "summary.json", summary)
        print(json.dumps(summary, indent=2))
        return 2

    bridge_profile = os.environ.get("VAEVAS_BRIDGE_PROFILE") or os.environ.get("BRIDGE_PROFILE", "")
    effective_cshrc = resolve_cadence_cshrc(bridge_repo, args.cadence_cshrc, bridge_profile or None)
    if args.skip_bridge_preflight:
        preflight = {"status": "skipped", "bridge_repo": str(bridge_repo), "cadence_cshrc": effective_cshrc}
    else:
        preflight = bridge_preflight(
            bridge_repo,
            cadence_cshrc=effective_cshrc,
            require_daemon=args.require_virtuoso_daemon,
            profile=bridge_profile or None,
        )
        if preflight.get("status") == "blocked":
            summary = {
                "status": "blocked",
                "reason": preflight.get("reason", "bridge preflight failed"),
                "tasks_total": len(bundles),
                "bridge_repo": str(bridge_repo),
                "bridge_profile": bridge_profile,
                "cadence_cshrc": effective_cshrc,
                "bridge_preflight": preflight,
            }
            write_summary(output_root / "summary.json", summary)
            print(json.dumps(summary, indent=2))
            return 2

    summary = run_bundles(
        bundles=bundles,
        output_root=output_root,
        bridge_repo=bridge_repo,
        cadence_cshrc=effective_cshrc or None,
        timeout_s=args.timeout_s,
        dry_run=False,
    )
    summary["bridge_repo"] = str(bridge_repo)
    summary["bridge_profile"] = bridge_profile
    summary["cadence_cshrc"] = effective_cshrc
    summary["bridge_preflight"] = preflight
    write_summary(output_root / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary["expected_miss_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
