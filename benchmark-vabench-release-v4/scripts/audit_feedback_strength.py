#!/usr/bin/env python3
"""Classify v4 pilot feedback oracles by behavioral feedback strength."""
from __future__ import annotations

import argparse
import ast
import inspect
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = SCRIPT_DIR.parents[0]
REPO_ROOT = PACKAGE_ROOT.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
RUNNERS_DIR = REPO_ROOT / "runners"
if str(RUNNERS_DIR) not in sys.path:
    sys.path.insert(0, str(RUNNERS_DIR))

from render_prompt_modes import load_tasks, task_dir  # noqa: E402

try:
    import simulate_evas  # noqa: E402
except Exception as exc:  # pragma: no cover - reported in audit output
    simulate_evas = None  # type: ignore[assignment]
    SIMULATE_EVAS_IMPORT_ERROR = f"{type(exc).__name__}: {exc}"
else:
    SIMULATE_EVAS_IMPORT_ERROR = None

SCHEMA_VERSION = "v4-pilot-feedback-strength-v1"
LIGHT_BEHAVIOR_MARKERS = (
    "tran.csv",
    "csv",
    "sample",
    "edge",
    "threshold",
    "assert",
    "expected",
)


def rel(path: Path) -> str:
    return path.relative_to(PACKAGE_ROOT).as_posix()


def rel_repo(path: str | Path | None) -> str | None:
    if path is None:
        return None
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(resolved)


def extract_checker_id(text: str) -> str | None:
    match = re.search(r"checker_task_id\s*=\s*[\"']([^\"']+)[\"']", text)
    return match.group(1) if match else None


def load_checker_profile(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data


def extract_extra_trace_signals(text: str) -> list[str]:
    match = re.search(r"extra_trace_signals\s*=\s*(\{[^)]*?\})", text, flags=re.DOTALL)
    if match is None:
        return []
    try:
        parsed = ast.literal_eval(match.group(1))
    except (SyntaxError, ValueError):
        return []
    if not isinstance(parsed, (set, list, tuple)):
        return []
    signals = []
    for item in parsed:
        signal = str(item).strip()
        if signal:
            signals.append(signal)
    return sorted(set(signals))


def checker_static_features(source: str) -> dict[str, Any]:
    return {
        "return_false_count": source.count("return False"),
        "sample_signal_calls": source.count("sample_signal(") + source.count("sample_signal_at("),
        "mean_window_calls": source.count("mean_in_window("),
        "edge_or_crossing_calls": source.count("rising_edges(") + source.count("_crossing_times(") + source.count("crossing"),
        "uses_expected_sequences": "expected" in source or "sample_plan" in source,
    }


def checker_details(
    checker_id: str | None,
    runner_text: str = "",
    configured_extra_trace_signals: list[str] | None = None,
) -> dict[str, Any]:
    runner_extra_trace_signals = extract_extra_trace_signals(runner_text)
    profile_extra_trace_signals = sorted(set(configured_extra_trace_signals or []))
    details: dict[str, Any] = {
        "checker_task_id": checker_id,
        "checker_function": None,
        "checker_source": None,
        "checker_source_line": None,
        "required_trace_signal_count": 0,
        "required_trace_signals": [],
        "checker_profile_extra_trace_signals": profile_extra_trace_signals,
        "runner_extra_trace_signals": runner_extra_trace_signals,
        "effective_trace_signal_count": len(set(runner_extra_trace_signals) | set(profile_extra_trace_signals)),
        "effective_trace_signals": sorted(set(runner_extra_trace_signals) | set(profile_extra_trace_signals)),
        "checker_level": "no_public_behavior_checker",
        "static_features": {},
        "notes": [],
    }
    if not checker_id:
        details["notes"].append("no checker_task_id in checker profile")
        return details
    if simulate_evas is None:
        details["checker_level"] = "checker_unresolved"
        details["notes"].append(f"could not import simulate_evas: {SIMULATE_EVAS_IMPORT_ERROR}")
        return details

    checker = getattr(simulate_evas, "CHECKS", {}).get(checker_id)
    if checker is None:
        details["checker_level"] = "checker_unresolved"
        details["notes"].append("checker_task_id is not registered in simulate_evas.CHECKS")
        return details

    details["checker_function"] = getattr(checker, "__name__", None)
    details["checker_source"] = rel_repo(inspect.getsourcefile(checker))
    try:
        source_lines, source_line = inspect.getsourcelines(checker)
    except (OSError, TypeError):
        source_lines, source_line = [], None
    details["checker_source_line"] = source_line
    source = "".join(source_lines)
    details["static_features"] = checker_static_features(source)

    try:
        trace_signals = sorted(getattr(simulate_evas, "required_trace_signals_for_checker")(checker_id))
    except Exception as exc:  # pragma: no cover - reported in audit output
        trace_signals = []
        details["notes"].append(f"required_trace_signals_for_checker failed: {type(exc).__name__}: {exc}")
    details["required_trace_signals"] = trace_signals
    details["required_trace_signal_count"] = len(trace_signals)
    effective_trace_signals = sorted(set(trace_signals) | set(runner_extra_trace_signals) | set(profile_extra_trace_signals))
    details["effective_trace_signals"] = effective_trace_signals
    details["effective_trace_signal_count"] = len(effective_trace_signals)
    features = details["static_features"]
    if effective_trace_signals:
        if int(features.get("return_false_count", 0)) >= 2 and len(effective_trace_signals) >= 3:
            details["checker_level"] = "multi_signal_behavior_checker"
        else:
            details["checker_level"] = "basic_behavior_checker"
        if not trace_signals and profile_extra_trace_signals:
            details["notes"].append("trace contract is supplied by checker_profile.json")
        elif not trace_signals and runner_extra_trace_signals:
            details["notes"].append("trace contract is supplied by runner extra_trace_signals")
    else:
        details["checker_level"] = "behavior_checker_without_explicit_trace_contract"
        details["notes"].append("checker exists, but no explicit required trace-signal contract was reported")
    return details


def classify_feedback(slug: str, task: dict[str, Any]) -> dict[str, Any]:
    tdir = task_dir(slug)
    runner = tdir / "test_feedback" / "run_feedback.py"
    checker_profile = tdir / "evaluator" / "checker_profile.json"
    expected_checker_id = str(task.get("feedback_checker_task_id") or task.get("public_visible_checker_task_id") or "")
    row: dict[str, Any] = {
        "task_slug": slug,
        "task_id": task.get("id"),
        "source_task_id": task.get("source_task_id"),
        "runner": rel(runner) if runner.exists() else None,
        "checker_profile": rel(checker_profile) if checker_profile.exists() else None,
        "expected_checker_task_id": expected_checker_id or None,
        "observed_checker_task_id": None,
        "classification": "missing_or_unknown",
        "checker_details": checker_details(None),
        "rationale": [],
    }

    if not runner.exists():
        row["rationale"].append("missing feedback oracle runner")
        return row
    if not checker_profile.exists():
        row["rationale"].append("missing checker profile")
        return row

    text = runner.read_text(encoding="utf-8")
    runner_checker_id = extract_checker_id(text)
    checker_payload = load_checker_profile(checker_profile)
    profile_checker_id = checker_payload.get("checker_task_id")
    trace_contract = checker_payload.get("trace_contract") or {}
    profile_extra_trace_signals = [str(signal) for signal in trace_contract.get("extra_trace_signals") or []]
    checker_id = profile_checker_id or runner_checker_id
    row["observed_checker_task_id"] = checker_id
    row["checker_details"] = checker_details(checker_id, text, profile_extra_trace_signals)
    if "run_feedback" in text and checker_id:
        row["classification"] = "behavior_checked"
        row["rationale"].append("runner invokes shared feedback_oracle; task-specific checker id is bound in private checker profile")
        if expected_checker_id and checker_id == expected_checker_id:
            row["rationale"].append("checker id matches TASKS.json feedback_checker_task_id")
        elif expected_checker_id:
            row["rationale"].append("checker id does not match TASKS.json feedback_checker_task_id")
        if runner_checker_id:
            row["rationale"].append("warning: runner still exposes checker id directly")
        return row

    if any(marker in text.lower() for marker in LIGHT_BEHAVIOR_MARKERS):
        row["classification"] = "light_behavior"
        row["rationale"].append("runner appears to inspect traces or expected values but no shared checker id was found")
        return row

    if "Compiled Verilog-A module:" in text and "Transient Analysis" in text:
        row["classification"] = "compile_only_smoke"
        row["rationale"].append("runner checks compile/transient markers only")
        return row

    row["rationale"].append("runner shape is not recognized by the static classifier")
    return row


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# v4 Pilot Feedback Strength Audit",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Task count: `{report['task_count']}`",
        f"- Status: `{report['status']}`",
        f"- Warnings: `{report['warning_count']}`",
        "",
        "## Classification Types",
        "",
        "- `compile_only_smoke`: feedback runner checks compile/transient markers only.",
        "- `light_behavior`: public runner appears to inspect traces or expected values, but no shared task checker id was found.",
        "- `behavior_checked`: public runner invokes EVAS and a task-specific behavior checker.",
        "- `missing_or_unknown`: missing runner/profile or unrecognized runner shape.",
        "",
        "Checker levels are a second layer over `behavior_checked`:",
        "",
        "- `multi_signal_behavior_checker`: checker is registered, has explicit trace-signal requirements, and has multiple failure conditions.",
        "- `basic_behavior_checker`: checker is registered and has an explicit trace-signal requirement, but the static checker shape is smaller.",
        "- `behavior_checker_without_explicit_trace_contract`: checker is registered, but the sparse-trace contract is not explicit.",
        "- `checker_unresolved` / `no_public_behavior_checker`: no registered public behavior checker could be found.",
        "",
        "## Results",
        "",
        "| Task | Runner classification | Checker level | Checker | Effective trace signals | Rationale |",
        "|---|---|---|---|---:|---|",
    ]
    for row in report["tasks"]:
        rationale = "; ".join(row["rationale"])
        checker = row.get("checker_details") or {}
        lines.append(
            "| {task} | `{classification}` | `{checker_level}` | `{checker}` | {signals} | {rationale} |".format(
                task=row["task_slug"],
                classification=row["classification"],
                checker_level=checker.get("checker_level") or "-",
                checker=row.get("observed_checker_task_id") or "-",
                signals=checker.get("effective_trace_signal_count", 0),
                rationale=rationale or "-",
            )
        )
    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_report() -> dict[str, Any]:
    tasks = load_tasks()
    rows = [classify_feedback(slug, task) for slug, task in sorted(tasks.items())]
    counts: dict[str, int] = {}
    checker_level_counts: dict[str, int] = {}
    for row in rows:
        key = row["classification"]
        counts[key] = counts.get(key, 0) + 1
        checker = row.get("checker_details") or {}
        checker_level = str(checker.get("checker_level") or "unknown")
        checker_level_counts[checker_level] = checker_level_counts.get(checker_level, 0) + 1
    problems = [
        f"{row['task_slug']}: feedback strength is {row['classification']}"
        for row in rows
        if row["classification"] != "behavior_checked"
    ]
    for row in rows:
        checker = row.get("checker_details") or {}
        if checker.get("checker_level") in {"checker_unresolved", "no_public_behavior_checker"}:
            problems.append(f"{row['task_slug']}: public behavior checker is unresolved")
    warnings = [
        f"{row['task_slug']}: checker exists but has no effective trace-signal contract"
        for row in rows
        if (row.get("checker_details") or {}).get("checker_level") == "behavior_checker_without_explicit_trace_contract"
    ]
    return {
        "benchmark": "benchmark-vabench-release-v4",
        "schema_version": SCHEMA_VERSION,
        "task_count": len(rows),
        "classification_counts": counts,
        "checker_level_counts": checker_level_counts,
        "status": "PASS" if not problems else "FAIL",
        "problem_count": len(problems),
        "problems": problems,
        "warning_count": len(warnings),
        "warnings": warnings,
        "tasks": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        default="reports/feedback_strength",
        help="output directory relative to the v4 package",
    )
    args = parser.parse_args()

    report = build_report()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PACKAGE_ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "feedback_strength.json"
    md_path = out_dir / "feedback_strength.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
