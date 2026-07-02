#!/usr/bin/env python3
"""Run v3 gold and negative-variant EVAS verification for a task range."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import time
from pathlib import Path
from typing import Any

from simulate_evas import read_task_artifact_targets, read_task_index_id, run_case


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_sim_correct_task_slugs(checks_path: Path) -> set[str]:
    if not checks_path.exists():
        return set()
    text = checks_path.read_text(encoding="utf-8", errors="ignore")
    slugs: set[str] = set()
    current_slug: str | None = None
    current_body: list[str] = []
    for line in text.splitlines():
        if line and not line.startswith((" ", "\t")) and line.endswith(": |"):
            if current_slug and any("sim_correct:" in body_line for body_line in current_body):
                slugs.add(current_slug)
            current_slug = line.split(":", 1)[0]
            current_body = []
            continue
        if current_slug is not None:
            current_body.append(line)
    if current_slug and any("sim_correct:" in body_line for body_line in current_body):
        slugs.add(current_slug)
    return slugs


def negative_variant_ids(task_dir: Path) -> list[str]:
    manifest_path = task_dir / "negative_variants" / "manifest.json"
    if not manifest_path.exists():
        return []
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        return []
    for key in ("cases", "variants", "negative_variants"):
        variants = manifest.get(key)
        if not isinstance(variants, list):
            continue
        ids = [str(item.get("id", "")).strip() for item in variants if isinstance(item, dict)]
        return [variant_id for variant_id in ids if variant_id]
    return []


def choose_dut(task_dir: Path, target: str, variant: str | None) -> tuple[Path | None, list[str]]:
    notes: list[str] = []
    dut_root = task_dir / "negative_variants" / variant if variant else task_dir / "solution"
    dut = dut_root / target
    if dut.exists():
        return dut, notes
    va_candidates = sorted([*dut_root.glob("*.va"), *dut_root.glob("*.vams")])
    if len(va_candidates) == 1:
        notes.append(f"used_single_artifact_fallback={va_candidates[0].name}")
        return va_candidates[0], notes
    notes.append(f"missing_candidate_artifact={dut}")
    return None, notes


def choose_hidden_tb(task_dir: Path) -> Path | None:
    tb = task_dir / "test_hidden" / "hidden.scs"
    if tb.exists():
        return tb
    candidates = sorted((task_dir / "test_hidden" / "tests").glob("*.scs"))
    return candidates[0] if len(candidates) == 1 else None


def simulator_failure_summary(text: str) -> str | None:
    """Extract a concise simulator failure reason from EVAS output."""
    if not text.strip():
        return None
    patterns = (
        r"ERROR:\s*(?P<msg>[^\n]+)",
        r"CompilationError:\s*(?P<msg>[^\n]+)",
        r"SyntaxError:\s*(?P<msg>[^\n]+)",
        r"NameError:\s*(?P<msg>[^\n]+)",
        r"ValueError:\s*(?P<msg>[^\n]+)",
    )
    for pattern in patterns:
        matches = list(re.finditer(pattern, text))
        if matches:
            message = matches[-1].group("msg").strip()
            message = re.sub(r"\s+", " ", message)
            return f"simulator_error={message[:240]}"
    if "evas completes with 1 errors" in text:
        return "simulator_error=evas completed with 1 error but did not expose a detailed diagnostic in captured output"
    return None


def run_one(task_dir: Path, variant: str | None, timeout_s: int) -> dict[str, Any]:
    started = time.perf_counter()
    targets = read_task_artifact_targets(task_dir)
    task_index_id = read_task_index_id(task_dir) or task_dir.name
    kind = "negative" if variant else "gold"
    case_id = f"{task_dir.name}:{variant}" if variant else f"{task_dir.name}:gold"
    row: dict[str, Any] = {
        "case_id": case_id,
        "task_slug": task_dir.name,
        "task_id": task_index_id,
        "kind": kind,
        "variant": variant,
    }
    if not targets:
        row.update({
            "status": "FAIL_NO_TARGET",
            "expected_ok": False,
            "meets_expectation": kind == "negative",
            "notes": ["missing target in TASKS.json/task.toml"],
            "wall_s": round(time.perf_counter() - started, 6),
        })
        return row
    tb = choose_hidden_tb(task_dir)
    if tb is None:
        row.update({
            "status": "FAIL_NO_TB",
            "expected_ok": False,
            "meets_expectation": kind == "negative",
            "notes": ["missing hidden.scs or unique test_hidden/tests/*.scs"],
            "wall_s": round(time.perf_counter() - started, 6),
        })
        return row
    dut, selection_notes = choose_dut(task_dir, targets[0], variant)
    if dut is None:
        row.update({
            "status": "FAIL_NO_DUT",
            "expected_ok": False,
            "meets_expectation": kind == "negative",
            "notes": selection_notes,
            "wall_s": round(time.perf_counter() - started, 6),
        })
        return row

    try:
        result = run_case(
            task_dir,
            dut,
            tb,
            timeout_s=timeout_s,
            keep_run_dir=False,
            task_id_override=task_index_id,
        )
    except Exception as exc:  # pragma: no cover - report boundary.
        result = {
            "status": "FAIL_EXCEPTION",
            "scores": {},
            "notes": [f"{type(exc).__name__}: {exc}"],
            "stdout_tail": "",
        }

    status = str(result.get("status", "FAIL_UNKNOWN"))
    expected_ok = kind == "gold"
    meets_expectation = status == "PASS" if expected_ok else status != "PASS"
    stdout_tail = str(result.get("stdout_tail", ""))
    notes = [*selection_notes, *[str(note) for note in result.get("notes", [])]]
    if status != "PASS" and not any(note.startswith("simulator_error=") for note in notes):
        failure_summary = simulator_failure_summary(stdout_tail)
        if failure_summary and failure_summary not in notes:
            notes.append(failure_summary)
    row.update({
        "status": status,
        "expected_ok": expected_ok,
        "meets_expectation": meets_expectation,
        "checker_task_id": result.get("checker_task_id"),
        "scores": result.get("scores", {}),
        "notes": notes,
        "stdout_tail": stdout_tail[-4000:],
        "wall_s": round(time.perf_counter() - started, 6),
    })
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="benchmark-vabench-release-v3/tasks")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument(
        "--tasks",
        default="",
        help="Optional comma-separated task slugs or three-digit task numbers to run inside the start/end range.",
    )
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--out", required=True)
    parser.add_argument("--gold-only", action="store_true")
    parser.add_argument("--negatives-only", action="store_true")
    parser.add_argument(
        "--checks",
        default="benchmark-vabench-release-v3/CHECKS.yaml",
        help="CHECKS.yaml path used to identify behavior-certified sim_correct tasks.",
    )
    parser.add_argument(
        "--include-staged",
        action="store_true",
        help="Also run staged syntax/continuous/KCL candidates without sim_correct blocks.",
    )
    args = parser.parse_args()

    if args.gold_only and args.negatives_only:
        raise SystemExit("--gold-only and --negatives-only are mutually exclusive")

    os.environ.setdefault("VAEVAS_EVAS_PERSISTENT_WORKER", "0")
    root = Path(args.root)
    sim_correct_slugs = read_sim_correct_task_slugs(Path(args.checks))
    task_filter = parse_task_filter(args.tasks)
    cases: list[tuple[Path, str | None, int]] = []
    skipped_tasks: list[str] = []
    for task_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        number = task_number(task_dir)
        if number is None or not (args.start <= number <= args.end):
            continue
        if not task_matches_filter(task_dir, task_filter):
            continue
        if not args.include_staged and task_dir.name not in sim_correct_slugs:
            skipped_tasks.append(task_dir.name)
            print(task_dir.name, "SKIP_STAGED", flush=True)
            continue
        if not args.negatives_only:
            cases.append((task_dir, None, args.timeout))
        if not args.gold_only:
            for variant_id in negative_variant_ids(task_dir):
                cases.append((task_dir, variant_id, args.timeout))

    rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    jobs = max(1, args.jobs)
    if jobs == 1:
        for case in cases:
            row = run_one(*case)
            rows.append(row)
            print(row["case_id"], row["status"], "expect_ok=", row["expected_ok"], "ok=", row["meets_expectation"], flush=True)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
            futures = [executor.submit(run_one, *case) for case in cases]
            for future in concurrent.futures.as_completed(futures):
                row = future.result()
                rows.append(row)
                print(row["case_id"], row["status"], "expect_ok=", row["expected_ok"], "ok=", row["meets_expectation"], flush=True)

    rows.sort(key=lambda row: (row["task_slug"], row["kind"], str(row["variant"] or "")))
    gold_rows = [row for row in rows if row["kind"] == "gold"]
    negative_rows = [row for row in rows if row["kind"] == "negative"]
    summary = {
        "scope": f"{args.start}-{args.end}",
        "cases_total": len(rows),
        "gold_total": len(gold_rows),
        "gold_pass": sum(row["status"] == "PASS" for row in gold_rows),
        "gold_fail": sum(row["status"] != "PASS" for row in gold_rows),
        "negative_total": len(negative_rows),
        "negative_rejected": sum(row["status"] != "PASS" for row in negative_rows),
        "negative_accepted": sum(row["status"] == "PASS" for row in negative_rows),
        "expectation_pass": sum(row["meets_expectation"] for row in rows),
        "expectation_fail": sum(not row["meets_expectation"] for row in rows),
        "skipped_staged_tasks": len(skipped_tasks),
        "wall_s": round(time.perf_counter() - started, 6),
    }
    payload = {"summary": summary, "rows": rows, "skipped_tasks": skipped_tasks}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("REPORT", out)
    return 0 if summary["expectation_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
