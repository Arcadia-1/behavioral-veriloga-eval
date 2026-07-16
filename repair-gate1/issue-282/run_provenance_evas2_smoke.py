#!/usr/bin/env python3
"""Run issue #282 provenance-local EVAS2 smoke for families 041-050."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "runners"))

from runners.simulate_evas import (  # noqa: E402
    effective_evas_engine,
    evaluate_behavior_with_timeout,
    parse_evas_performance_counters,
    parse_evas_timing,
    required_trace_signals_for_checker,
    run_evas,
)


SOURCE_ROOT = (
    REPO
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)
DEFAULT_OUTPUT = REPO / "repair-gate1" / "issue-282" / "evas2-provenance-smoke-041-050.json"
DEFAULT_WORK_ROOT = Path("/tmp/v4-repair-batch-282-evas2-work")
FAMILIES = [f"{value:03d}" for value in range(41, 51)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def family_dir(family_id: str) -> Path:
    matches = sorted(SOURCE_ROOT.glob(f"{family_id}-*"))
    if len(matches) != 1:
        raise RuntimeError(f"{family_id}: expected one family dir, found {len(matches)}")
    return matches[0]


def denominator_active_mutations() -> dict[str, list[str]]:
    manifest = read_json(SOURCE_ROOT / "score_denominator_manifest.json")
    rows = {str(row.get("canonical_dut_id")): row for row in manifest.get("tasks", [])}
    selected: dict[str, list[str]] = {}
    for family_id in FAMILIES:
        row = rows[family_id]
        selected[family_id] = [
            str(item.get("mutation_id") or item.get("id"))
            for item in row.get("active_mutations", [])
        ]
    return selected


def copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def overlay_mutation(mutation_dir: Path, dut_dir: Path) -> list[str]:
    changed: list[str] = []
    for source in sorted(mutation_dir.rglob("*")):
        if not source.is_file() or source.name == "certification.json":
            continue
        relative = source.relative_to(mutation_dir)
        target = dut_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        changed.append(relative.as_posix())
    return changed


def backend_source() -> dict[str, Any]:
    source_root = Path("/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS")
    commit = None
    status = None
    if source_root.exists():
        rev = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        if rev.returncode == 0:
            commit = rev.stdout.strip()
        stat = subprocess.run(
            ["git", "-C", str(source_root), "status", "--short", "--branch"],
            capture_output=True,
            text=True,
            check=False,
        )
        if stat.returncode == 0:
            status = stat.stdout.strip()

    version = "unknown"
    probe = subprocess.run(
        ["python3", "-c", "import evas; print(getattr(evas, '__version__', 'unknown'))"],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(source_root)},
    )
    if probe.returncode == 0:
        version = probe.stdout.strip() or "unknown"

    evas_frontend = shutil.which("evas")
    return {
        "frontend_path": evas_frontend,
        "frontend_realpath": str(Path(evas_frontend).resolve()) if evas_frontend else None,
        "source_root": str(source_root),
        "source_git_commit": commit,
        "source_git_status_short_branch": status,
        "evas_python_package_version": version,
    }


def run_case(
    *,
    task: Path,
    checker_task_id: str,
    family_id: str,
    case_id: str,
    mutation_id: str | None,
    work_root: Path,
    timeout_s: int,
) -> dict[str, Any]:
    case_dir = work_root / family_id / case_id
    if case_dir.exists():
        shutil.rmtree(case_dir)
    case_dir.mkdir(parents=True)
    dut_dir = case_dir / "dut"
    copy_tree(task / "evaluator" / "solution", dut_dir)
    changed: list[str] = []
    if mutation_id is not None:
        mutation_dir = task / "evaluator" / "mutation_bundles" / mutation_id
        changed = overlay_mutation(mutation_dir, dut_dir)
        if not changed:
            raise RuntimeError(f"{task.name}/{mutation_id}: no changed mutation artifacts")

    tb_source = task / "evaluator" / "score_tb.scs"
    tb_path = case_dir / "score_tb.scs"
    shutil.copy2(tb_source, tb_path)
    out_dir = case_dir / "output"
    required_signals = required_trace_signals_for_checker(checker_task_id)
    started = time.perf_counter()
    proc = run_evas(
        case_dir,
        tb_path,
        out_dir,
        timeout_s,
        required_trace_signals=required_signals,
    )
    wall_s = time.perf_counter() - started
    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    csv_path = out_dir / "tran.csv"
    simulator_ok = proc.returncode == 0 and csv_path.is_file()
    checker_ok = False
    checker_notes: list[str] = []
    if simulator_ok:
        checker_score, checker_notes = evaluate_behavior_with_timeout(
            checker_task_id,
            csv_path,
            timeout_s=timeout_s,
        )
        checker_ok = bool(checker_score)
    checker_infrastructure_error = any(
        note.startswith(("behavior_eval_timeout", "behavior_eval_error", "no behavior check implemented"))
        for note in checker_notes
    )

    if mutation_id is None:
        status = "reference_pass" if simulator_ok and checker_ok else "reference_fail"
    elif not simulator_ok or checker_infrastructure_error:
        status = "infrastructure_error"
    elif checker_ok:
        status = "mutation_survived"
    else:
        status = "mutation_killed"

    return {
        "case_id": case_id,
        "mutation_id": mutation_id,
        "status": status,
        "simulator_ok": simulator_ok,
        "checker_ok": checker_ok,
        "returncode": proc.returncode,
        "changed_artifacts": changed,
        "score_tb_sha256": file_sha(tb_path),
        "required_trace_signal_count": len(required_signals - {"time"}) if required_signals else 0,
        "checker_notes": checker_notes,
        "evas_engine": effective_evas_engine(),
        "timing": parse_evas_timing(combined),
        "performance_counters": parse_evas_performance_counters(combined),
        "wall_time_s": round(wall_s, 6),
        "stdout_tail": combined[-2000:],
    }


def run_smoke(*, output: Path, work_root: Path, timeout_s: int) -> dict[str, Any]:
    if work_root.exists():
        shutil.rmtree(work_root)
    work_root.mkdir(parents=True)
    active = denominator_active_mutations()
    results = []
    for family_id in FAMILIES:
        task = family_dir(family_id)
        record = read_json(task / "evaluator" / "task_record.json")
        checker_task_id = str(record["checker_task_id"])
        cases = [
            run_case(
                task=task,
                checker_task_id=checker_task_id,
                family_id=family_id,
                case_id="gold",
                mutation_id=None,
                work_root=work_root,
                timeout_s=timeout_s,
            )
        ]
        for mutation_id in active[family_id]:
            cases.append(
                run_case(
                    task=task,
                    checker_task_id=checker_task_id,
                    family_id=family_id,
                    case_id=mutation_id,
                    mutation_id=mutation_id,
                    work_root=work_root,
                    timeout_s=timeout_s,
                )
            )

        reference_pass = cases[0]["status"] == "reference_pass"
        mutation_kill_count = sum(1 for case in cases[1:] if case["status"] == "mutation_killed")
        mutation_count = len(cases) - 1
        infrastructure_error_count = sum(
            1 for case in cases if case["status"] in {"reference_fail", "infrastructure_error"}
        )
        mutation_survivor_count = sum(1 for case in cases[1:] if case["status"] == "mutation_survived")
        results.append(
            {
                "family_id": family_id,
                "task_dir": task.name,
                "checker_task_id": checker_task_id,
                "active_mutations_source": "score_denominator_manifest.json",
                "reference_pass": reference_pass,
                "mutation_kill_count": mutation_kill_count,
                "mutation_count": mutation_count,
                "infrastructure_error_count": infrastructure_error_count,
                "mutation_survivor_count": mutation_survivor_count,
                "status": "pass"
                if reference_pass
                and mutation_kill_count == mutation_count
                and infrastructure_error_count == 0
                and mutation_survivor_count == 0
                else "fail",
                "cases": cases,
            }
        )

    report = {
        "schema_version": "issue-282-provenance-evas2-smoke-v1",
        "issue": 282,
        "batch": "05/40",
        "families": FAMILIES,
        "source_root": str(SOURCE_ROOT),
        "work_root": str(work_root),
        "command": (
            "EVAS_ENGINE=evas2 VAEVAS_DEFAULT_EVAS_ENGINE=evas2 PYTHONPATH=runners "
            "python3 repair-gate1/issue-282/run_provenance_evas2_smoke.py"
        ),
        "evas_engine_used": effective_evas_engine(),
        "python_fallback_evidence_claimed": False,
        "backend_source": backend_source(),
        "task_count": len(results),
        "pass_count": sum(1 for row in results if row["status"] == "pass"),
        "fail_count": sum(1 for row in results if row["status"] != "pass"),
        "reference_pass_count": sum(1 for row in results if row["reference_pass"]),
        "mutation_kill_count": sum(row["mutation_kill_count"] for row in results),
        "mutation_count": sum(row["mutation_count"] for row in results),
        "status": "pass" if all(row["status"] == "pass" for row in results) else "fail",
        "results": results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--work-root", type=Path, default=DEFAULT_WORK_ROOT)
    parser.add_argument("--timeout-s", type=int, default=120)
    args = parser.parse_args()
    report = run_smoke(
        output=args.output.expanduser().resolve(),
        work_root=args.work_root.expanduser().resolve(),
        timeout_s=args.timeout_s,
    )
    summary = {
        key: report[key]
        for key in [
            "schema_version",
            "status",
            "task_count",
            "pass_count",
            "fail_count",
            "reference_pass_count",
            "mutation_kill_count",
            "mutation_count",
            "evas_engine_used",
        ]
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
