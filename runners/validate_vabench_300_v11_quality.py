#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from simulate_evas import run_case


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "benchmark-vabench-release-v1" / "vabench-300-expansion"
MANIFEST = EXPANSION / "VABENCH_300_MANIFEST.json"
EVIDENCE_JSON = EXPANSION / "v11_task_specific_quality_evidence.json"
EVIDENCE_MD = EXPANSION / "v11_task_specific_quality_evidence.md"
PROVISIONAL_STATUS = "provisional_v1.1_management"
CERTIFIED_STATUS = "certified_v1.1_promoted"
V11_STATUSES = {PROVISIONAL_STATUS, CERTIFIED_STATUS}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def task_dir_for(row: dict[str, Any]) -> Path:
    return (ROOT / str(row["release_task_manifest"])).parent


def choose_gold(task_dir: Path) -> tuple[Path, Path]:
    gold_dir = task_dir / "gold"
    va = next(iter(sorted(gold_dir.glob("*.va"))), None)
    tb = next(iter(sorted(gold_dir.glob("tb*.scs"))), None)
    if va is None or tb is None:
        raise FileNotFoundError(f"missing gold .va or tb*.scs under {gold_dir}")
    return va, tb


def compile_sim_pass(raw: dict[str, Any]) -> bool:
    scores = raw.get("scores")
    if not isinstance(scores, dict):
        return False
    return (
        float(scores.get("dut_compile", 0.0)) >= 1.0
        and float(scores.get("tb_compile", 0.0)) >= 1.0
        and any("returncode=0" == str(note) for note in raw.get("notes", []))
    )


def stage_negative_task(task_dir: Path, gold_va: Path, gold_tb: Path, negative_va: Path) -> tempfile.TemporaryDirectory[str]:
    temp_ctx = tempfile.TemporaryDirectory(prefix=f"v11_neg_{task_dir.name}_")
    staged_task = Path(temp_ctx.name)
    staged_gold = staged_task / "gold"
    staged_gold.mkdir(parents=True)
    for name in ("meta.json", "checks.yaml", "prompt.md"):
        src = task_dir / name
        if src.exists():
            shutil.copy2(src, staged_task / name)
    shutil.copy2(gold_tb, staged_gold / gold_tb.name)
    shutil.copy2(negative_va, staged_gold / gold_va.name)
    return temp_ctx


def run_gold(row: dict[str, Any], output_root: Path, timeout_s: int) -> dict[str, Any]:
    task_id = str(row["task_id"])
    task_dir = task_dir_for(row)
    gold_va, gold_tb = choose_gold(task_dir)
    started = time.perf_counter()
    raw = run_case(
        task_dir,
        gold_va,
        gold_tb,
        output_root=output_root / "gold" / task_id.replace(":", "__"),
        timeout_s=timeout_s,
        checker_task_id_override=task_id,
    )
    return {
        "task_id": task_id,
        "release_task_manifest": row["release_task_manifest"],
        "raw_status": raw.get("status"),
        "compile_sim_pass": compile_sim_pass(raw),
        "behavior_checker_pass": raw.get("status") == "PASS",
        "scores": raw.get("scores", {}),
        "notes": [str(note) for note in raw.get("notes", [])],
        "wall_time_s": round(time.perf_counter() - started, 6),
    }


def run_negative(
    row: dict[str, Any],
    negative: dict[str, Any],
    output_root: Path,
    timeout_s: int,
) -> dict[str, Any]:
    task_id = str(row["task_id"])
    task_dir = task_dir_for(row)
    gold_va, gold_tb = choose_gold(task_dir)
    negative_va = ROOT / str(negative["source"])
    started = time.perf_counter()
    temp_ctx = stage_negative_task(task_dir, gold_va, gold_tb, negative_va)
    try:
        staged_task = Path(temp_ctx.name)
        staged_gold = staged_task / "gold"
        raw = run_case(
            staged_task,
            staged_gold / gold_va.name,
            staged_gold / gold_tb.name,
            output_root=output_root
            / "negative"
            / task_id.replace(":", "__")
            / str(negative["id"]),
            timeout_s=timeout_s,
            checker_task_id_override=task_id,
        )
    finally:
        temp_ctx.cleanup()
    scores = raw.get("scores") if isinstance(raw.get("scores"), dict) else {}
    sim_correct = float(scores.get("sim_correct", 0.0))
    full_checker_fail = compile_sim_pass(raw) and sim_correct < 1.0
    return {
        "task_id": task_id,
        "negative_id": negative["id"],
        "kind": negative["kind"],
        "source": negative["source"],
        "raw_status": raw.get("status"),
        "compile_sim_pass": compile_sim_pass(raw),
        "full_checker_fail": full_checker_fail,
        "scores": raw.get("scores", {}),
        "notes": [str(note) for note in raw.get("notes", [])],
        "wall_time_s": round(time.perf_counter() - started, 6),
    }


def update_negative_manifests(rows: list[dict[str, Any]], negative_results: list[dict[str, Any]]) -> None:
    by_task_negative = {
        (str(result["task_id"]), str(result["negative_id"])): result for result in negative_results
    }
    for row in rows:
        manifest_path = ROOT / str(row["negative_manifest"])
        manifest = read_json(manifest_path)
        changed = False
        for negative in manifest.get("negatives", []):
            result = by_task_negative.get((str(row["task_id"]), str(negative.get("id"))))
            if result is None:
                continue
            negative["validation_evidence"] = {
                "static_shallow_shape": "pass",
                "simulator_shallow_lane": "pass" if result["compile_sim_pass"] else "fail",
                "full_checker_lane": "pass" if result["full_checker_fail"] else "fail",
                "publication_status": "evas_full_checker_verified_spectre_pending"
                if result["full_checker_fail"]
                else "failed_local_evas_quality_gate",
            }
            negative["validation_result"] = {
                "raw_status": result["raw_status"],
                "compile_sim_pass": result["compile_sim_pass"],
                "full_checker_fail": result["full_checker_fail"],
                "notes": result["notes"][-4:],
            }
            changed = True
        if changed:
            write_json(manifest_path, manifest)


def update_manifest(summary: dict[str, Any]) -> None:
    manifest = read_json(MANIFEST)
    manifest["v11_task_specific_quality_evidence"] = rel(EVIDENCE_JSON)
    gold_pass_ids = {
        str(row["task_id"])
        for row in summary.get("gold_results", [])
        if row.get("behavior_checker_pass")
    }
    for row in manifest.get("tasks", []):
        if row.get("expansion_status") not in V11_STATUSES:
            continue
        if str(row.get("task_id")) in gold_pass_ids:
            row["evas"] = "pass"
        if row.get("spectre") != "pass":
            row["spectre"] = "pending_fresh_spectre_after_task_specific_rebuild"
    manifest.setdefault("summary", {})["task_specific_v11_gold_pass_count"] = summary[
        "gold_behavior_checker_pass_count"
    ]
    manifest.setdefault("summary", {})["task_specific_v11_negative_full_checker_fail_count"] = summary[
        "negative_full_checker_fail_count"
    ]
    manifest.setdefault("summary", {})["negative_simulator_shallow_verified_count"] = summary[
        "negative_compile_sim_pass_count"
    ]
    manifest.setdefault("summary", {})["negative_full_checker_fail_verified_count"] = summary[
        "negative_full_checker_fail_count"
    ]
    write_json(MANIFEST, manifest)


def write_markdown(summary: dict[str, Any]) -> None:
    lines = [
        "# vaBench 300 v1.1 Task-Specific Quality Evidence",
        "",
        f"- status: `{summary['status']}`",
        f"- engine: `{summary['engine']}`",
        f"- task-specific v1.1 rows: {summary['task_count']}",
        f"- gold behavior checker pass: {summary['gold_behavior_checker_pass_count']}/{summary['task_count']}",
        f"- negative compile/sim pass: {summary['negative_compile_sim_pass_count']}/{summary['negative_count']}",
        f"- negative full-checker fail: {summary['negative_full_checker_fail_count']}/{summary['negative_count']}",
        f"- output root: `{summary['output_root']}`",
        "",
        "This is local EVAS evidence for the rebuilt v1.1 task-specific assets.",
        "It is not itself Spectre certification. Fresh Spectre certification and",
        "score-denominator admission are recorded separately in",
        "`benchmark-vabench-release-v1/reports/vabench_300_v11_fresh_spectre_rerun.json`",
        "and `benchmark-vabench-release-v1/reports/vabench_300_v11_score_admission.json`.",
        "",
    ]
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate vaBench 300 v1.1 task-specific quality with EVAS.")
    ap.add_argument("--output-root", default=str(ROOT / "results" / "vabench-300-v11-quality"))
    ap.add_argument("--timeout-s", type=int, default=45)
    ap.add_argument("--engine", default="evas-rust", choices=("python", "evas-rust", "evas2", "rust2"))
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    os.environ["VAEVAS_DEFAULT_EVAS_ENGINE"] = args.engine
    os.environ.pop("EVAS_ENGINE", None)
    manifest = read_json(MANIFEST)
    rows = [row for row in manifest["tasks"] if row.get("expansion_status") in V11_STATUSES]
    if args.limit:
        rows = rows[: args.limit]
    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    output_root.mkdir(parents=True, exist_ok=True)

    gold_results: list[dict[str, Any]] = []
    negative_results: list[dict[str, Any]] = []
    started_at = datetime.now().isoformat(timespec="seconds")
    for index, row in enumerate(rows, start=1):
        gold = run_gold(row, output_root, args.timeout_s)
        gold_results.append(gold)
        print(
            f"[gold {index}/{len(rows)}] {gold['task_id']} status={gold['raw_status']} "
            f"checker={'pass' if gold['behavior_checker_pass'] else 'fail'}",
            flush=True,
        )
        negatives = read_json(ROOT / str(row["negative_manifest"]))["negatives"]
        for negative in negatives:
            result = run_negative(row, negative, output_root, args.timeout_s)
            negative_results.append(result)
            print(
                f"[neg {len(negative_results)}] {result['task_id']} {result['negative_id']} "
                f"compile={'pass' if result['compile_sim_pass'] else 'fail'} "
                f"full_fail={'pass' if result['full_checker_fail'] else 'fail'}",
                flush=True,
            )

    negative_count = len(negative_results)
    summary = {
        "status": "pass"
        if all(row["behavior_checker_pass"] for row in gold_results)
        and all(row["compile_sim_pass"] and row["full_checker_fail"] for row in negative_results)
        else "fail",
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "engine": args.engine,
        "output_root": rel(output_root),
        "task_count": len(rows),
        "negative_count": negative_count,
        "gold_behavior_checker_pass_count": sum(1 for row in gold_results if row["behavior_checker_pass"]),
        "gold_behavior_checker_fail_count": sum(1 for row in gold_results if not row["behavior_checker_pass"]),
        "negative_compile_sim_pass_count": sum(1 for row in negative_results if row["compile_sim_pass"]),
        "negative_full_checker_fail_count": sum(1 for row in negative_results if row["full_checker_fail"]),
        "spectre_status": "recorded_separately_in_vabench_300_v11_fresh_spectre_rerun",
        "claim_boundary": [
            "This validates task-specific v1.1 gold and negative behavior with EVAS only.",
            "This artifact is not itself Spectre certification; fresh Spectre certification and score admission are recorded in the release reports.",
            "A negative full-checker pass means the negative compiled and simulated but failed sim_correct.",
        ],
        "gold_results": gold_results,
        "negative_results": negative_results,
    }
    write_json(output_root / "summary.json", summary)
    if not args.limit:
        write_json(EVIDENCE_JSON, summary)
        write_markdown(summary)
        update_negative_manifests(rows, negative_results)
        update_manifest(summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in {"gold_results", "negative_results"}}, indent=2, sort_keys=True))
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
