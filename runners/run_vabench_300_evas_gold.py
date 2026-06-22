#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from simulate_evas import run_case


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "benchmark-vabench-release-v1" / "vabench-300-expansion"
MANIFEST = EXPANSION / "VABENCH_300_MANIFEST.json"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / "vabench-300-evas-gold"
SUMMARY_JSON = EXPANSION / "evas_gold_summary.json"
SUMMARY_MD = EXPANSION / "evas_gold_summary.md"
PROMOTED_STATUS = "certified_v1.1_promoted"


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


def choose_gold_source(gold_dir: Path) -> tuple[Path | None, Path | None]:
    fixed = gold_dir / "dut_fixed.va"
    va = fixed if fixed.exists() else next(iter(sorted(gold_dir.glob("*.va"))), None)
    preferred_tb = sorted(gold_dir.glob("tb*_ref.scs"))
    if preferred_tb:
        tb = preferred_tb[0]
    else:
        tb = next(iter(sorted(gold_dir.glob("tb*.scs"))), None)
    return va, tb


def ahdl_includes(tb: Path) -> list[str]:
    text = tb.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r'^\s*ahdl_include\s+"([^"]+)"', text, flags=re.MULTILINE)


def staged_bugfix_task_dir(task_dir: Path, va: Path, tb: Path) -> tempfile.TemporaryDirectory[str] | None:
    if va.name != "dut_fixed.va":
        return None
    missing = [name for name in ahdl_includes(tb) if not (tb.parent / name).exists()]
    if not missing:
        return None
    temp_ctx = tempfile.TemporaryDirectory(prefix=f"{task_dir.name}_evas_gold_")
    staged_task_dir = Path(temp_ctx.name)
    staged_gold = staged_task_dir / "gold"
    staged_gold.mkdir(parents=True)
    for src in task_dir.iterdir():
        if src.name == "gold" or src.is_dir():
            continue
        (staged_task_dir / src.name).write_bytes(src.read_bytes())
    for src in tb.parent.iterdir():
        if src.is_file():
            (staged_gold / src.name).write_bytes(src.read_bytes())
    for name in missing:
        alias = staged_gold / Path(name).name
        if not alias.exists():
            alias.write_bytes(va.read_bytes())
    return temp_ctx


def compile_sim_pass(raw: dict[str, Any]) -> bool:
    scores = raw.get("scores")
    if not isinstance(scores, dict):
        return False
    return (
        float(scores.get("dut_compile", 0.0)) >= 1.0
        and float(scores.get("tb_compile", 0.0)) >= 1.0
        and any("returncode=0" == str(note) for note in raw.get("notes", []))
    )


def run_one(row: dict[str, Any], output_root: Path, timeout_s: int) -> dict[str, Any]:
    task_id = str(row["task_id"])
    task_dir = task_dir_for(row)
    gold_dir = task_dir / "gold"
    va, tb = choose_gold_source(gold_dir)
    result_root = output_root / task_id.replace(":", "__")
    started = time.perf_counter()
    if va is None or tb is None:
        raw = {
            "task_id": task_id,
            "status": "FAIL_INFRA",
            "backend_used": "evas",
            "scores": {"dut_compile": 0.0, "tb_compile": 0.0, "sim_correct": 0.0},
            "notes": ["missing gold .va or tb*.scs"],
        }
    else:
        temp_ctx = staged_bugfix_task_dir(task_dir, va, tb)
        effective_task_dir = Path(temp_ctx.name) if temp_ctx is not None else task_dir
        effective_gold_dir = effective_task_dir / "gold"
        effective_va = effective_gold_dir / va.name
        effective_tb = effective_gold_dir / tb.name
        try:
            raw = run_case(
                effective_task_dir,
                effective_va,
                effective_tb,
                output_root=result_root,
                timeout_s=timeout_s,
            )
        except subprocess.TimeoutExpired as exc:
            raw = {
                "task_id": task_id,
                "status": "FAIL_TIMEOUT",
                "backend_used": "evas",
                "evas_engine_used": os.environ.get("VAEVAS_DEFAULT_EVAS_ENGINE", ""),
                "scores": {"dut_compile": 0.0, "tb_compile": 0.0, "sim_correct": 0.0},
                "notes": [f"evas_timeout>{timeout_s}s", f"cmd={getattr(exc, 'cmd', '')}"],
                "stdout_tail": ((exc.stdout or "") + "\n" + (exc.stderr or ""))[-1200:],
            }
        finally:
            if temp_ctx is not None:
                temp_ctx.cleanup()
    notes = [str(note) for note in raw.get("notes", [])]
    checker_missing = any("no behavior check implemented" in note for note in notes)
    return {
        "task_id": task_id,
        "topic_id": row.get("topic_id"),
        "legacy_task_id": row.get("legacy_task_id"),
        "legacy_entry_id": row.get("legacy_entry_id"),
        "release_task_manifest": row["release_task_manifest"],
        "expansion_status": row.get("expansion_status"),
        "form": row.get("form"),
        "family": row.get("family"),
        "gold_dir": rel(gold_dir),
        "result_root": rel(result_root),
        "wall_time_s": round(time.perf_counter() - started, 6),
        "raw_task_id": raw.get("task_id"),
        "checker_task_id": raw.get("checker_task_id"),
        "evas_engine": raw.get("evas_engine_used"),
        "raw_status": raw.get("status"),
        "compile_sim_pass": compile_sim_pass(raw),
        "behavior_checker_pass": raw.get("status") == "PASS",
        "behavior_checker_missing": checker_missing,
        "scores": raw.get("scores", {}),
        "notes": notes,
        "stdout_tail": raw.get("stdout_tail", "")[-1200:],
    }


def summarize(rows: list[dict[str, Any]], *, started_at: str, output_root: Path, engine: str) -> dict[str, Any]:
    compile_pass_count = sum(1 for row in rows if row["compile_sim_pass"])
    checker_pass_count = sum(1 for row in rows if row["behavior_checker_pass"])
    checker_missing_count = sum(1 for row in rows if row["behavior_checker_missing"])
    promoted = [row for row in rows if row["expansion_status"] == PROMOTED_STATUS]
    return {
        "status": "pass" if compile_pass_count == len(rows) else "fail",
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "engine": engine,
        "engine_label": "evas-rust" if engine in {"evas-rust", "evas2", "rust2"} else engine,
        "output_root": rel(output_root),
        "task_count": len(rows),
        "compile_sim_pass_count": compile_pass_count,
        "compile_sim_fail_count": len(rows) - compile_pass_count,
        "behavior_checker_pass_count": checker_pass_count,
        "behavior_checker_nonpass_count": len(rows) - checker_pass_count,
        "behavior_checker_missing_count": checker_missing_count,
        "promoted_v11_task_count": len(promoted),
        "promoted_v11_compile_sim_pass_count": sum(1 for row in promoted if row["compile_sim_pass"]),
        "promoted_v11_behavior_checker_missing_count": sum(
            1 for row in promoted if row["behavior_checker_missing"]
        ),
        "claim_boundary": [
            "This report is an EVAS gold run over the vaBench 300 expansion assets.",
            "compile_sim_pass means EVAS compiled the DUT, executed the testbench, returned 0, and produced simulation output.",
            "behavior_checker_pass additionally requires an implemented repository checker to pass.",
        "Rows with behavior_checker_missing are not behavior-certified by this EVAS-only run.",
        ],
        "results": rows,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    lines = [
        "# vaBench 300 EVAS Gold Summary",
        "",
        f"- status: `{summary['status']}`",
        f"- engine: `{summary.get('engine_label', summary['engine'])}`",
        f"- raw engine selector: `{summary['engine']}`",
        f"- tasks: {summary['task_count']}",
        f"- compile/sim pass: {summary['compile_sim_pass_count']}",
        f"- compile/sim fail: {summary['compile_sim_fail_count']}",
        f"- behavior checker pass: {summary['behavior_checker_pass_count']}",
        f"- behavior checker missing: {summary['behavior_checker_missing_count']}",
        f"- output root: `{summary['output_root']}`",
        "",
        "This is EVAS-only evidence. The 300-task certification source of truth is the full EVAS/Spectre closure report.",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def update_manifest(summary: dict[str, Any]) -> None:
    manifest = read_json(MANIFEST)
    manifest.setdefault("summary", {})["evas_gold_compile_sim_pass_count"] = summary[
        "compile_sim_pass_count"
    ]
    manifest.setdefault("summary", {})["evas_gold_behavior_checker_pass_count"] = summary[
        "behavior_checker_pass_count"
    ]
    manifest.setdefault("summary", {})["evas_gold_behavior_checker_missing_count"] = summary[
        "behavior_checker_missing_count"
    ]
    manifest["evas_gold_summary"] = rel(SUMMARY_JSON)
    write_json(MANIFEST, manifest)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run EVAS over vaBench 300 expansion gold assets.")
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    ap.add_argument("--timeout-s", type=int, default=90)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--task", action="append", default=[])
    ap.add_argument("--engine", default="python", choices=("python", "evas-rust", "evas2", "rust2"))
    ap.add_argument("--resume-partial", action="store_true")
    args = ap.parse_args()

    os.environ["VAEVAS_DEFAULT_EVAS_ENGINE"] = args.engine
    os.environ.pop("EVAS_ENGINE", None)
    manifest = read_json(MANIFEST)
    tasks = list(manifest["tasks"])
    if args.task:
        selected = set(args.task)
        tasks = [
            row
            for row in tasks
            if row["task_id"] in selected
            or row.get("legacy_task_id") in selected
            or row.get("topic_id") in selected
            or row.get("legacy_entry_id") in selected
        ]
    if args.limit:
        tasks = tasks[: args.limit]
    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    output_root.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now().isoformat(timespec="seconds")
    partial_path = output_root / "summary.partial.json"
    rows: list[dict[str, Any]] = []
    completed_ids: set[str] = set()
    if args.resume_partial and partial_path.exists():
        partial = read_json(partial_path)
        rows = list(partial.get("results", []))
        completed_ids = {str(row.get("task_id")) for row in rows}
        tasks = [row for row in tasks if str(row["task_id"]) not in completed_ids]
        print(f"resuming from partial: completed={len(rows)} remaining={len(tasks)}", flush=True)

    total_planned = len(rows) + len(tasks)
    for offset, row in enumerate(tasks, start=1):
        index = len(rows) + 1
        result = run_one(row, output_root, args.timeout_s)
        rows.append(result)
        partial = summarize(rows, started_at=started_at, output_root=output_root, engine=args.engine)
        partial["status"] = "running"
        partial["tasks_total_planned"] = total_planned
        partial["tasks_completed"] = index
        write_json(partial_path, partial)
        print(
            f"[{index}/{total_planned}] {result['task_id']} "
            f"compile_sim={'pass' if result['compile_sim_pass'] else 'fail'} "
            f"status={result['raw_status']}",
            flush=True,
        )

    summary = summarize(rows, started_at=started_at, output_root=output_root, engine=args.engine)
    write_json(output_root / "summary.json", summary)
    if not args.task and not args.limit and summary["task_count"] == 300:
        write_json(SUMMARY_JSON, summary)
        write_markdown(summary)
        update_manifest(summary)
    if partial_path.exists():
        partial_path.unlink()
    print(json.dumps({k: summary[k] for k in summary if k != "results"}, indent=2, sort_keys=True))
    return 0 if summary["compile_sim_fail_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
