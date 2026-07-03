#!/usr/bin/env python3
"""Run EVAS AHDL-like lint preflight for vaBench v3 tasks."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from simulate_evas import evas_command_and_env, read_task_artifact_targets, read_task_index_id  # noqa: E402


LintRunner = Callable[[Path, float, int], tuple[int, list[dict[str, Any]], str]]


@dataclass(frozen=True)
class LintCase:
    case_id: str
    task_slug: str
    task_id: str
    source_kind: str
    lint_input: Path
    candidate_root: Path
    targets: tuple[str, ...]


def task_number(task_dir: Path) -> int | None:
    try:
        return int(task_dir.name.split("-", 1)[0])
    except ValueError:
        return None


def parse_task_filter(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def task_matches_filter(task_dir: Path, task_filter: set[str]) -> bool:
    if not task_filter:
        return True
    number = task_number(task_dir)
    return task_dir.name in task_filter or (number is not None and f"{number:03d}" in task_filter)


def task_in_requested_range(task_dir: Path, task_filter: set[str], start: int, end: int) -> bool:
    number = task_number(task_dir)
    if number is not None:
        return start <= number <= end
    return bool(task_filter) and task_dir.name in task_filter


def split_testbenches(task_dir: Path, split: str) -> list[Path]:
    split_root = task_dir / f"test_{split}"
    if not split_root.exists():
        return []
    return sorted(path for path in split_root.rglob("*.scs") if path.is_file())


def collect_lint_cases(
    task_dir: Path,
    *,
    artifact_root_name: str,
    split: str,
) -> tuple[list[LintCase], list[str]]:
    targets = tuple(read_task_artifact_targets(task_dir))
    task_id = read_task_index_id(task_dir) or task_dir.name
    candidate_root = task_dir / artifact_root_name
    notes: list[str] = []
    cases: list[LintCase] = []
    if not candidate_root.exists():
        return [], [f"missing_artifact_root={candidate_root}"]
    if not targets:
        return [], ["missing_task_targets"]

    target_scs = [candidate_root / target for target in targets if target.endswith(".scs")]
    for tb_path in target_scs:
        if not tb_path.exists():
            notes.append(f"missing_target_scs={tb_path}")
            continue
        cases.append(
            LintCase(
                case_id=f"{task_dir.name}:target:{tb_path.name}",
                task_slug=task_dir.name,
                task_id=task_id,
                source_kind="target",
                lint_input=tb_path,
                candidate_root=candidate_root,
                targets=targets,
            )
        )

    requested_splits = ("visible", "hidden") if split == "all" else (split,)
    if not target_scs:
        for split_name in requested_splits:
            for tb_path in split_testbenches(task_dir, split_name):
                cases.append(
                    LintCase(
                        case_id=f"{task_dir.name}:{split_name}:{tb_path.name}",
                        task_slug=task_dir.name,
                        task_id=task_id,
                        source_kind=split_name,
                        lint_input=tb_path,
                        candidate_root=candidate_root,
                        targets=targets,
                    )
                )

    if cases:
        return cases, notes

    for target in targets:
        if not target.endswith((".va", ".vams")):
            continue
        target_path = candidate_root / target
        if not target_path.exists():
            notes.append(f"missing_target_source={target_path}")
            continue
        cases.append(
            LintCase(
                case_id=f"{task_dir.name}:source:{target_path.name}",
                task_slug=task_dir.name,
                task_id=task_id,
                source_kind="source",
                lint_input=target_path,
                candidate_root=candidate_root,
                targets=targets,
            )
        )

    return cases, notes


def stage_lint_case(case: LintCase, run_dir: Path) -> Path:
    if case.lint_input.suffix.lower() in {".va", ".vams"}:
        staged = run_dir / case.lint_input.name
        shutil.copy2(case.lint_input, staged)
        return staged

    for source_dir in (case.lint_input.parent, case.candidate_root):
        if not source_dir.exists():
            continue
        for src in sorted(source_dir.iterdir()):
            if src.is_dir():
                dst = run_dir / src.name
                if not dst.exists():
                    shutil.copytree(src, dst)
                continue
            if src.suffix.lower() not in {".scs", ".va", ".vams"}:
                continue
            dst = run_dir / src.name
            if src.resolve() != dst.resolve():
                shutil.copy2(src, dst)

    for target in case.targets:
        src = case.candidate_root / target
        dst = run_dir / Path(target).name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    return run_dir / case.lint_input.name


def run_evas_lint(input_path: Path, min_transition: float, timeout_s: int) -> tuple[int, list[dict[str, Any]], str]:
    base_cmd, env = evas_command_and_env()
    if base_cmd == ["evas"]:
        sibling_evas = Path(sys.executable).parent / "evas"
        if sibling_evas.exists():
            base_cmd = [str(sibling_evas)]
    cmd = [
        *base_cmd,
        "lint",
        input_path.name,
        "--format",
        "json",
        "--min-transition",
        str(min_transition),
    ]
    proc = subprocess.run(
        cmd,
        cwd=input_path.parent,
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout_s,
        check=False,
    )
    combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    diagnostics: list[dict[str, Any]] = []
    if proc.stdout.strip():
        try:
            parsed = json.loads(proc.stdout)
        except json.JSONDecodeError:
            parsed = []
        if isinstance(parsed, list):
            diagnostics = [item for item in parsed if isinstance(item, dict)]
    return proc.returncode, diagnostics, combined


def lint_status(returncode: int, diagnostics: list[dict[str, Any]]) -> str:
    if returncode not in {0, 1} and not diagnostics:
        return "FAIL_LINTER"
    if any(diagnostic.get("severity") == "compat-error" for diagnostic in diagnostics):
        return "FAIL_COMPAT"
    if diagnostics:
        return "WARN"
    return "PASS"


def normalize_diagnostic_paths(diagnostics: list[dict[str, Any]], stage_root: Path) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for diagnostic in diagnostics:
        item = dict(diagnostic)
        file_value = item.get("file")
        if isinstance(file_value, str):
            try:
                path = Path(file_value)
                item["file"] = path.relative_to(stage_root).as_posix()
            except ValueError:
                item["file"] = Path(file_value).name
        normalized.append(item)
    return normalized


def lint_one_case(
    case: LintCase,
    *,
    min_transition: float,
    timeout_s: int,
    max_diagnostics: int,
    runner: LintRunner = run_evas_lint,
) -> dict[str, Any]:
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="v3_evas_lint_") as td:
        stage_root = Path(td)
        staged_input = stage_lint_case(case, stage_root)
        try:
            returncode, diagnostics, raw_output = runner(staged_input, min_transition, timeout_s)
        except Exception as exc:  # pragma: no cover - process boundary.
            returncode = 2
            diagnostics = []
            raw_output = f"{type(exc).__name__}: {exc}"
        diagnostics = normalize_diagnostic_paths(diagnostics, stage_root)

    status = lint_status(returncode, diagnostics)
    trimmed = diagnostics[:max_diagnostics] if max_diagnostics >= 0 else diagnostics
    row = {
        "case_id": case.case_id,
        "task_slug": case.task_slug,
        "task_id": case.task_id,
        "source_kind": case.source_kind,
        "status": status,
        "returncode": returncode,
        "diagnostic_count": len(diagnostics),
        "compat_error_count": sum(1 for diagnostic in diagnostics if diagnostic.get("severity") == "compat-error"),
        "warning_count": sum(1 for diagnostic in diagnostics if str(diagnostic.get("severity", "")).endswith("warning")),
        "diagnostics": trimmed,
        "wall_s": round(time.perf_counter() - started, 6),
    }
    if len(trimmed) != len(diagnostics):
        row["diagnostics_truncated"] = len(diagnostics) - len(trimmed)
    if status == "FAIL_LINTER":
        row["raw_output_tail"] = raw_output[-2000:]
    return row


def build_payload(rows: list[dict[str, Any]], skipped: list[dict[str, Any]], *, split: str) -> dict[str, Any]:
    summary = {
        "split": split,
        "cases_total": len(rows),
        "tasks_total": len({row["task_slug"] for row in rows}),
        "pass": sum(row["status"] == "PASS" for row in rows),
        "warn": sum(row["status"] == "WARN" for row in rows),
        "fail_compat": sum(row["status"] == "FAIL_COMPAT" for row in rows),
        "fail_linter": sum(row["status"] == "FAIL_LINTER" for row in rows),
        "diagnostic_count": sum(int(row["diagnostic_count"]) for row in rows),
        "compat_error_count": sum(int(row["compat_error_count"]) for row in rows),
        "warning_count": sum(int(row["warning_count"]) for row in rows),
        "skipped": len(skipped),
    }
    return {"summary": summary, "rows": rows, "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="benchmark-vabench-release-v3/tasks")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=999)
    parser.add_argument(
        "--tasks",
        default="",
        help="Optional comma-separated task slugs or three-digit task numbers inside the start/end range.",
    )
    parser.add_argument("--artifact-root", default="solution", choices=["solution", "starter"])
    parser.add_argument("--split", default="hidden", choices=["visible", "hidden", "all"])
    parser.add_argument("--min-transition", type=float, default=1e-12)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-diagnostics-per-row", type=int, default=20)
    parser.add_argument(
        "--out",
        default="",
        help="Optional JSON output path. Prefer scratch/generated paths; generated reports are not repository evidence.",
    )
    parser.add_argument(
        "--allow-compat-errors",
        action="store_true",
        help="Return success even when EVAS lint reports compatibility errors.",
    )
    args = parser.parse_args()

    root = Path(args.root)
    task_filter = parse_task_filter(args.tasks)
    rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for task_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        if not task_in_requested_range(task_dir, task_filter, args.start, args.end):
            continue
        if not task_matches_filter(task_dir, task_filter):
            continue
        cases, notes = collect_lint_cases(task_dir, artifact_root_name=args.artifact_root, split=args.split)
        if not cases:
            skipped.append({"task_slug": task_dir.name, "notes": notes or ["no_lintable_case"]})
            print(task_dir.name, "SKIP", notes or ["no_lintable_case"], flush=True)
            continue
        for case in cases:
            row = lint_one_case(
                case,
                min_transition=args.min_transition,
                timeout_s=args.timeout,
                max_diagnostics=args.max_diagnostics_per_row,
            )
            rows.append(row)
            print(case.case_id, row["status"], f"diagnostics={row['diagnostic_count']}", flush=True)

    payload = build_payload(rows, skipped, split=args.split)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print("REPORT", out)
    else:
        print(text)

    summary = payload["summary"]
    if args.allow_compat_errors:
        return 0
    return 0 if summary["compat_error_count"] == 0 and summary["fail_linter"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
