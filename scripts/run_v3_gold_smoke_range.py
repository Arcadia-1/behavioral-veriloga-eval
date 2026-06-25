#!/usr/bin/env python3
"""Run EVAS gold smoke for a numbered v3 task range."""

from __future__ import annotations

import argparse
import ast
import json
import re
import time
from pathlib import Path

from simulate_evas import read_task_artifact_targets, run_case


def task_number(task_dir: Path) -> int | None:
    try:
        return int(task_dir.name[:3])
    except ValueError:
        return None


def task_toml_id(task_dir: Path) -> str | None:
    task_toml = task_dir / "task.toml"
    if not task_toml.exists():
        return None
    match = re.search(
        r'(?m)^\s*id\s*=\s*(".*?"|\'.*?\')\s*$',
        task_toml.read_text(encoding="utf-8", errors="ignore"),
    )
    if not match:
        return None
    try:
        value = ast.literal_eval(match.group(1))
    except (SyntaxError, ValueError):
        return None
    return str(value) if value else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="benchmark-vabench-release-v3/tasks")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--out", required=True)
    parser.add_argument(
        "--variant",
        help="Optional candidate subdirectory under negative_variants to run instead of solution.",
    )
    args = parser.parse_args()

    root = Path(args.root)
    rows = []
    for task in sorted(p for p in root.iterdir() if p.is_dir()):
        number = task_number(task)
        if number is None or number < args.start or number > args.end:
            continue
        targets = read_task_artifact_targets(task)
        if not targets:
            row = {
                "task_id": task.name,
                "status": "FAIL_NO_TARGET",
                "notes": ["missing task.toml artifacts.target"],
            }
            rows.append(row)
            print(task.name, row["status"], flush=True)
            continue
        dut_root = task / "negative_variants" / args.variant if args.variant else task / "solution"
        dut = dut_root / targets[0]
        if not dut.exists():
            fallback_candidates = sorted(dut_root.glob("*.va"))
            if len(fallback_candidates) == 1:
                dut = fallback_candidates[0]
            else:
                row = {
                    "task_id": task_toml_id(task) or task.name,
                    "status": "FAIL_NO_DUT",
                    "notes": [f"missing candidate artifact {dut}"],
                }
                rows.append(row)
                print(task.name, row["status"], flush=True)
                continue
        tb = task / "test_hidden" / "hidden.scs"
        if not tb.exists():
            tb_candidates = sorted((task / "test_hidden" / "tests").glob("*.scs"))
            if len(tb_candidates) == 1:
                tb = tb_candidates[0]
            else:
                row = {
                    "task_id": task_toml_id(task) or task.name,
                    "status": "FAIL_NO_TB",
                    "notes": [f"missing hidden.scs and unique test_hidden/tests/*.scs in {task}"],
                }
                rows.append(row)
                print(task.name, row["status"], flush=True)
                continue
        start = time.perf_counter()
        result = run_case(
            task,
            dut,
            tb,
            timeout_s=args.timeout,
            keep_run_dir=False,
            task_id_override=task_toml_id(task),
        )
        result["wall_s"] = time.perf_counter() - start
        rows.append(result)
        print(
            task.name,
            result.get("status"),
            result.get("checker_task_id"),
            f"{result['wall_s']:.2f}s",
            result.get("notes", [])[:6],
            flush=True,
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "tasks": len(rows),
                "pass": sum(1 for row in rows if row.get("status") == "PASS"),
                "rows": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("REPORT", out)
    return 0 if all(row.get("status") == "PASS" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
