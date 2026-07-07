#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


STATUSES = (
    "behavior_checked",
    "light_behavior",
    "compile_only_smoke",
    "missing_or_unknown",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def task_dirs(tasks_root: Path) -> list[Path]:
    return sorted(
        path
        for path in tasks_root.iterdir()
        if path.is_dir() and re.match(r"^\d{3}-", path.name)
    )


def classify_visible_smoke(script_path: Path) -> str:
    if not script_path.exists():
        return "missing_or_unknown"
    text = script_path.read_text(encoding="utf-8")
    if (
        "VISIBLE_BEHAVIOR_PASS" in text
        or "evaluate_behavior(" in text
        or re.search(r"checker_task_id\s*=\s*[\"']", text)
    ):
        return "behavior_checked"
    if any(
        marker in text
        for marker in (
            "csv.DictReader",
            "load_csv(",
            "rising_edges(",
            "sample_signal(",
            "required_trace_signals",
            "VISIBLE_BEHAVIOR_FAIL",
        )
    ):
        return "light_behavior"
    if (
        "Compiled Verilog-A module:" in text
        and "Transient Analysis" in text
        and "VISIBLE_SMOKE_PASS" in text
    ):
        return "compile_only_smoke"
    return "missing_or_unknown"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify v3 visible smoke tests by behavioral strength."
    )
    parser.add_argument("--list", action="store_true", help="print every task classification")
    parser.add_argument(
        "--status",
        choices=STATUSES,
        help="only list tasks with the selected classification",
    )
    parser.add_argument(
        "--fail-on-compile-only",
        action="store_true",
        help="exit nonzero if any compile-only visible smoke remains",
    )
    args = parser.parse_args()

    tasks_root = repo_root() / "benchmark-vabench-release-v3" / "tasks"
    rows: list[tuple[str, str]] = []
    for task_dir in task_dirs(tasks_root):
        script_path = task_dir / "test_visible" / "tests" / "run_visible_smoke.py"
        rows.append((task_dir.name, classify_visible_smoke(script_path)))

    counts = Counter(status for _, status in rows)
    print("visible_smoke_strength_summary")
    for status in STATUSES:
        print(f"{status}: {counts.get(status, 0)}")

    if args.list or args.status:
        for task_name, status in rows:
            if args.status and status != args.status:
                continue
            print(f"{task_name}: {status}")

    if args.fail_on_compile_only and counts.get("compile_only_smoke", 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
