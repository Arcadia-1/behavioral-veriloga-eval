#!/usr/bin/env python3
"""Replay formal tri-form reference testbenches through the feedback adapter.

This is a lightweight dynamic audit for testbench-form tasks.  It exports a
runtime for each selected task, submits the sealed reference testbench as the
candidate artifact, and checks that the public feedback adapter reports:

    FEEDBACK_TB_PASS killed=5/5

The audit is intentionally separate from raw simulator evidence.  It records a
compact JSON summary with task status, elapsed time, and the final feedback tail
needed for triage.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from typing import Any


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
REPO = PACKAGE.parent
DEFAULT_RELEASE = PACKAGE / "release" / "tri-form-v4-1200-final"
EXPORTER = HERE / "export_tri_form_runtime.py"
FEEDBACK_ADAPTER = PACKAGE / "operations" / "calibration_pilot" / "feedback_adapter.py"
PASS_MARKER = "FEEDBACK_TB_PASS killed=5/5"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_task_rows(release: Path, requested: list[str]) -> list[dict[str, Any]]:
    rows = read_json(release / "TASK_INDEX.json")["tasks"]
    testbench_rows = [row for row in rows if row.get("form") == "testbench"]
    if not requested:
        return testbench_rows
    by_id = {str(row["task_id"]): row for row in testbench_rows}
    missing = [task_id for task_id in requested if task_id not in by_id]
    if missing:
        raise SystemExit(f"unknown testbench task id(s): {', '.join(missing)}")
    return [by_id[task_id] for task_id in requested]


def compact_tail(text: str, limit: int) -> str:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[-limit:])


def audit_one(
    *,
    release: Path,
    row: dict[str, Any],
    mode: str,
    working_token_budget: int,
    timeout_s: int,
    tail_lines: int,
) -> dict[str, Any]:
    task_id = str(row["task_id"])
    started = time.time()
    try:
        with tempfile.TemporaryDirectory(prefix=f"{task_id}_reference_tb_") as td:
            runtime = Path(td) / "runtime"
            export = subprocess.run(
                [
                    "python3",
                    str(EXPORTER),
                    "--release",
                    str(release),
                    "--task",
                    task_id,
                    "--mode",
                    mode,
                    "--output",
                    str(runtime),
                    "--working-token-budget",
                    str(working_token_budget),
                    "--force",
                ],
                cwd=REPO,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=90,
                check=False,
            )
            if export.returncode != 0:
                return {
                    "task_id": task_id,
                    "status": "EXPORT_FAIL",
                    "elapsed_s": round(time.time() - started, 3),
                    "tail": compact_tail(export.stdout or "", tail_lines),
                }

            task_dir = release / str(row["task_dir"])
            submission = runtime / "public" / "submission"
            submission.mkdir(parents=True, exist_ok=True)
            shutil.copy2(task_dir / "evaluator" / "reference_tb.scs", submission / "testbench.scs")

            env = os.environ.copy()
            env["VABENCH_RUNTIME_DIR"] = str(runtime)
            feedback = subprocess.run(
                ["python3", str(FEEDBACK_ADAPTER)],
                cwd=REPO,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                timeout=timeout_s,
                check=False,
            )
            stdout = feedback.stdout or ""
            passed = feedback.returncode == 0 and PASS_MARKER in stdout
            return {
                "task_id": task_id,
                "status": "PASS" if passed else "FAIL",
                "returncode": feedback.returncode,
                "elapsed_s": round(time.time() - started, 3),
                "tail": compact_tail(stdout, tail_lines),
            }
    except subprocess.TimeoutExpired as exc:
        return {
            "task_id": task_id,
            "status": "TIMEOUT",
            "elapsed_s": round(time.time() - started, 3),
            "tail": str(exc)[-2000:],
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--task-id", action="append", default=[], help="Restrict to one task id; may repeat.")
    parser.add_argument("--mode", default="G0")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout-s", type=int, default=240)
    parser.add_argument("--working-token-budget", type=int, default=60000)
    parser.add_argument("--tail-lines", type=int, default=40)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    release = args.release.expanduser().resolve()
    rows = resolve_task_rows(release, args.task_id)
    workers = max(1, min(args.workers, len(rows) or 1))
    started_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    results: list[dict[str, Any]] = []
    with futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(
                audit_one,
                release=release,
                row=row,
                mode=args.mode,
                working_token_budget=args.working_token_budget,
                timeout_s=args.timeout_s,
                tail_lines=args.tail_lines,
            ): row
            for row in rows
        }
        for future in futures.as_completed(future_map):
            result = future.result()
            results.append(result)
            print(f"{result['task_id']} {result['status']} {result['elapsed_s']}s", flush=True)

    order = {str(row["task_id"]): index for index, row in enumerate(rows)}
    results.sort(key=lambda item: order.get(str(item["task_id"]), 10**9))
    pass_count = sum(1 for result in results if result["status"] == "PASS")
    summary = {
        "schema_version": "v4-reference-tb-feedback-audit-v1",
        "started_at": started_at,
        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "release": str(release),
        "mode": args.mode,
        "timeout_s": args.timeout_s,
        "workers": workers,
        "task_count": len(results),
        "pass_count": pass_count,
        "fail_count": len(results) - pass_count,
        "results": results,
    }
    if args.output:
        write_json(args.output.expanduser().resolve(), summary)
    print(json.dumps({key: summary[key] for key in ("task_count", "pass_count", "fail_count")}, sort_keys=True))
    return 0 if pass_count == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
