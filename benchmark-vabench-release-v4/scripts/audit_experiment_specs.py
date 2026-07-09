#!/usr/bin/env python3
"""Audit v4 pilot G0-G5 experiment records against the mode policy."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = SCRIPT_DIR.parents[0]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_prompt_modes import ALL_MODES, MODES_JSON, build_prompt, load_tasks, sha256_text, skill_files_for_mode  # noqa: E402

DIRECT_FORBIDDEN = [
    r"\bEVAS\b",
    r"\bSpectre\b",
    r"\bVela\b",
    r"\bhidden\b",
    r"\bchecker\b",
    r"\btest_visible\b",
    r"\bvisible\b",
    r"\bfeedback\b",
    r"\boracle\b",
    r"\bvalidation\b",
    r"\btestbench\b",
    r"\bsimulator\b",
]
AGENTIC_EVAS_FEEDBACK_CHANNELS = [
    "ahdl_like_preflight",
    "evas_simulation",
    "behavior_property_diagnostics",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def matches(patterns: list[str], text: str) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            hits.append(pattern)
    return hits


def rel_path(record_path: str) -> Path:
    return PACKAGE_ROOT / record_path


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_no}: invalid JSONL record: {exc}") from exc
    return records


def require(condition: bool, problems: list[str], message: str) -> None:
    if not condition:
        problems.append(message)


def audit_direct(record: dict[str, Any], prompt: str, problems: list[str]) -> None:
    slug = record["task_slug"]
    mode = record["mode"]
    access = record.get("access_policy") or {}
    require(record.get("runner_family") == "llms", problems, f"{slug}/{mode}: direct record must use llms")
    require(record.get("process_type") == "direct_llm", problems, f"{slug}/{mode}: direct record must use direct_llm")
    require(record.get("clean_direct_baseline") is (mode == "G0"), problems, f"{slug}/{mode}: clean_direct_baseline mismatch")
    require(access.get("tool_access") is False, problems, f"{slug}/{mode}: direct record must not expose tools")
    require(access.get("shell") is False, problems, f"{slug}/{mode}: direct record must not expose shell")
    require(access.get("file_browsing") == "none", problems, f"{slug}/{mode}: direct record must not expose file browsing")
    require(access.get("public_feedback_access") == "none", problems, f"{slug}/{mode}: direct record must not expose feedback oracle")
    require(access.get("feedback_runner") is None, problems, f"{slug}/{mode}: direct record must not expose a feedback runner")
    require(not access.get("feedback_files"), problems, f"{slug}/{mode}: direct record must not expose feedback files")
    require(not access.get("embedded_feedback_files"), problems, f"{slug}/{mode}: direct record must not embed feedback files")
    require(not access.get("allowed_commands"), problems, f"{slug}/{mode}: direct record must not expose commands")
    require(not access.get("evas_feedback_channels"), problems, f"{slug}/{mode}: direct record must not expose EVAS feedback channels")
    for hit in matches(DIRECT_FORBIDDEN, prompt):
        problems.append(f"{slug}/{mode}: direct prompt contains forbidden surface {hit}")


def audit_agentic(record: dict[str, Any], prompt: str, problems: list[str]) -> None:
    slug = record["task_slug"]
    mode = record["mode"]
    access = record.get("access_policy") or {}
    require(record.get("runner_family") == "agents", problems, f"{slug}/{mode}: agentic record must use agents")
    require(record.get("process_type") == "agentic", problems, f"{slug}/{mode}: agentic record must use agentic process_type")
    require(access.get("tool_access") is True, problems, f"{slug}/{mode}: agentic record must expose tools")
    require(access.get("shell") is True, problems, f"{slug}/{mode}: agentic record must expose shell")
    require(access.get("file_browsing") == "feedback_surface_only", problems, f"{slug}/{mode}: agentic file browsing must be feedback_surface_only")
    require(access.get("public_feedback_access") == "runnable_oracle", problems, f"{slug}/{mode}: agentic feedback access must be runnable_oracle")
    require(bool(access.get("feedback_runner")), problems, f"{slug}/{mode}: agentic record must expose feedback runner")
    require(bool(access.get("feedback_files")), problems, f"{slug}/{mode}: agentic record must expose feedback files")
    require(
        f"tasks/{slug}/test_feedback/public_tb.scs" in set(access.get("feedback_files") or []),
        problems,
        f"{slug}/{mode}: agentic record must expose public feedback TB",
    )
    require(bool(access.get("allowed_commands")), problems, f"{slug}/{mode}: agentic record must expose feedback command")
    require(access.get("private_score_access") is False, problems, f"{slug}/{mode}: agentic record must block private score access")
    require(
        access.get("evas_feedback_channels") == AGENTIC_EVAS_FEEDBACK_CHANNELS,
        problems,
        f"{slug}/{mode}: agentic record must expose structured EVAS feedback channels",
    )
    require("black-box feedback oracle" in prompt, problems, f"{slug}/{mode}: prompt missing feedback-oracle wrapper")
    require("EVAS" in prompt, problems, f"{slug}/{mode}: prompt missing EVAS feedback channel text")
    require(not access.get("embedded_feedback_files"), problems, f"{slug}/{mode}: agentic record must not embed feedback files in prompt")


def audit_record(record: dict[str, Any], tasks: dict[str, dict[str, Any]], problems: list[str]) -> None:
    slug = str(record.get("task_slug") or "")
    mode = str(record.get("mode") or "")
    if slug not in tasks:
        problems.append(f"{slug or '<missing>'}/{mode or '<missing>'}: unknown task slug")
        return
    if mode not in ALL_MODES:
        problems.append(f"{slug}/{mode or '<missing>'}: unknown mode")
        return

    expected_prompt = build_prompt(slug, tasks[slug], mode)
    prompt_path = rel_path(str(record.get("prompt_path") or ""))
    require(prompt_path.exists(), problems, f"{slug}/{mode}: prompt_path does not exist")
    if prompt_path.exists():
        prompt = prompt_path.read_text(encoding="utf-8")
        require(prompt == expected_prompt, problems, f"{slug}/{mode}: prompt_path content differs from renderer")
    else:
        prompt = expected_prompt
    require(record.get("prompt_sha256") == sha256_text(expected_prompt), problems, f"{slug}/{mode}: prompt_sha256 mismatch")
    require((record.get("access_policy") or {}).get("hidden_access") is False, problems, f"{slug}/{mode}: hidden_access must be false")
    require((record.get("access_policy") or {}).get("private_score_access") is False, problems, f"{slug}/{mode}: private_score_access must be false")

    if mode in {"G0", "G1"}:
        audit_direct(record, prompt, problems)
    elif mode in {"G2", "G3", "G4", "G5"}:
        audit_agentic(record, prompt, problems)

    skills = set(record.get("skills") or [])
    require(record.get("skill_files") == skill_files_for_mode(mode), problems, f"{slug}/{mode}: skill_files mismatch")
    if mode in {"G1", "G3", "G5"}:
        require("veriloga" in skills, problems, f"{slug}/{mode}: expected veriloga skill marker")
        require("Verilog-A writing checklist" in prompt, problems, f"{slug}/{mode}: prompt missing Verilog-A checklist")
    else:
        require("veriloga" not in skills, problems, f"{slug}/{mode}: unexpected veriloga skill marker")
        require("Verilog-A writing checklist" not in prompt, problems, f"{slug}/{mode}: unexpected Verilog-A checklist")
    if mode in {"G4", "G5"}:
        require("feedback_debug" in skills, problems, f"{slug}/{mode}: expected feedback_debug skill marker")
        require("Feedback/debug skill:" in prompt, problems, f"{slug}/{mode}: prompt missing feedback/debug skill")
    else:
        require("feedback_debug" not in skills, problems, f"{slug}/{mode}: unexpected feedback_debug skill marker")
        require("Feedback/debug skill:" not in prompt, problems, f"{slug}/{mode}: unexpected feedback/debug skill")
    if mode in {"G0", "G2"}:
        require(not skills, problems, f"{slug}/{mode}: unexpected skill marker(s) {sorted(skills)}")


def build_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    mode_counts: dict[str, int] = {}
    runner_counts: dict[str, int] = {}
    for record in records:
        mode = str(record.get("mode"))
        runner = str(record.get("runner_family"))
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
        runner_counts[runner] = runner_counts.get(runner, 0) + 1
    return {"mode_counts": mode_counts, "runner_family_counts": runner_counts}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--records-jsonl",
        default="reports/experiment_specs/records.jsonl",
        help="records JSONL path relative to the v4 package",
    )
    args = parser.parse_args()

    records_path = Path(args.records_jsonl)
    if not records_path.is_absolute():
        records_path = PACKAGE_ROOT / records_path
    records = load_jsonl(records_path)
    tasks = load_tasks()
    modes = read_json(MODES_JSON)["modes"]
    problems: list[str] = []

    expected_count = len(tasks) * len(ALL_MODES)
    require(len(records) == expected_count, problems, f"record count must be {expected_count}, got {len(records)}")
    seen: set[tuple[str, str]] = set()
    for record in records:
        key = (str(record.get("task_slug") or ""), str(record.get("mode") or ""))
        if key in seen:
            problems.append(f"{key[0]}/{key[1]}: duplicate record")
        seen.add(key)
        expected_label = modes.get(key[1], {}).get("label")
        if expected_label:
            require(record.get("mode_label") == expected_label, problems, f"{key[0]}/{key[1]}: mode_label mismatch")
        audit_record(record, tasks, problems)

    for slug in tasks:
        for mode in ALL_MODES:
            if (slug, mode) not in seen:
                problems.append(f"{slug}/{mode}: missing record")

    summary = {
        "benchmark": "benchmark-vabench-release-v4",
        "records_path": records_path.relative_to(PACKAGE_ROOT).as_posix(),
        "record_count": len(records),
        "expected_record_count": expected_count,
        "status": "PASS" if not problems else "FAIL",
        "problem_count": len(problems),
        "problems": problems,
        **build_summary(records),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
