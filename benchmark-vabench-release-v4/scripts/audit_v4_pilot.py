#!/usr/bin/env python3
"""Audit v4 pilot prompt-surface and feedback-oracle boundaries."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = SCRIPT_DIR.parents[0]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_prompt_modes import ALL_MODES, build_prompt, canonical_prompt, load_tasks, task_dir


REQUIRED_HEADINGS = [
    "# ",
    "## Task Contract",
    "## Public Verilog-A Interface",
    "## Public Parameter Contract",
    "## Required Behavior",
    "## Modeling Constraints",
    "## Output Contract",
]

CANONICAL_FORBIDDEN = [
    r"\bEVAS\b",
    r"\bSpectre\b",
    r"\bVela\b",
    r"\bhidden\b",
    r"\bchecker\b",
    r"\btest_visible\b",
    r"\bvisible testbench\b",
    r"\bpublic visible\b",
    r"\bfeedback oracle\b",
    r"\bvalidation harness\b",
    r"\bvalidation sample\b",
    r"\bsample window\b",
    r"\btransient stop time\b",
    r"\btestbench\b",
    r"\bsimulator\b",
    r"^- Form:\s*`",
    r"^- Level:\s*`",
    r"^- Category:\s*`",
]

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


def matches(patterns: list[str], text: str) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            hits.append(pattern)
    return hits


def audit_headings(slug: str, text: str) -> list[str]:
    problems: list[str] = []
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        problems.append(f"{slug}: first line must be an H1 task title")
    for heading in REQUIRED_HEADINGS[1:]:
        if heading not in text:
            problems.append(f"{slug}: missing heading {heading}")
    return problems


def audit_canonical(slug: str) -> list[str]:
    text = canonical_prompt(slug)
    problems = audit_headings(slug, text)
    for hit in matches(CANONICAL_FORBIDDEN, text):
        problems.append(f"{slug}: canonical prompt contains forbidden surface {hit}")
    return problems


def audit_modes(slug: str, task: dict[str, object]) -> list[str]:
    problems: list[str] = []
    for mode in ALL_MODES:
        prompt = build_prompt(slug, task, mode)
        if mode in {"G0", "G1"}:
            for hit in matches(DIRECT_FORBIDDEN, prompt):
                problems.append(f"{slug}/{mode}: direct clean prompt contains forbidden surface {hit}")
        if mode in {"G2", "G3", "G4", "G5"}:
            if "black-box feedback oracle" not in prompt:
                problems.append(f"{slug}/{mode}: missing feedback-oracle agentic wrapper")
            if "EVAS" not in prompt:
                problems.append(f"{slug}/{mode}: missing EVAS feedback channel text")
        if mode in {"G3", "G5"} and "Verilog-A writing checklist" not in prompt:
            problems.append(f"{slug}/{mode}: missing Verilog-A writing checklist")
        if mode in {"G0", "G2", "G4"} and "Verilog-A writing checklist" in prompt:
            problems.append(f"{slug}/{mode}: unexpected Verilog-A writing checklist")
        if mode in {"G4", "G5"} and "Feedback/debug skill:" not in prompt:
            problems.append(f"{slug}/{mode}: missing feedback/debug skill")
        if mode in {"G0", "G1", "G2", "G3"} and "Feedback/debug skill:" in prompt:
            problems.append(f"{slug}/{mode}: unexpected feedback/debug skill")
        if "Public feedback-interface contents for the G5 ablation" in prompt:
            problems.append(f"{slug}/{mode}: prompt still embeds deprecated public feedback-interface context")
    return problems


def audit_feedback_surface(slug: str, task: dict[str, object]) -> list[str]:
    problems: list[str] = []
    tdir = task_dir(slug)
    script = tdir / "test_feedback" / "run_feedback.py"
    public_tb = tdir / "test_feedback" / "public_tb.scs"
    contract = tdir / "public_contract.json"
    checker_profile = tdir / "evaluator" / "checker_profile.json"
    score_tb = tdir / "evaluator" / "score_tb.scs"
    if not script.exists():
        problems.append(f"{slug}: missing feedback oracle runner")
        return problems
    if not public_tb.exists():
        problems.append(f"{slug}: missing public feedback testbench")
    if not contract.exists():
        problems.append(f"{slug}: missing public_contract.json")
    if not checker_profile.exists():
        problems.append(f"{slug}: missing evaluator checker_profile.json")
    if not score_tb.exists():
        problems.append(f"{slug}: missing evaluator score_tb.scs")
    if public_tb.exists() and score_tb.exists() and public_tb.read_text(encoding="utf-8") == score_tb.read_text(encoding="utf-8"):
        problems.append(f"{slug}: public feedback TB and private score TB are byte-identical")
    for obsolete in ["starter", "test_visible", "test_hidden", "evaluator/profiles"]:
        if (tdir / obsolete).exists():
            problems.append(f"{slug}: obsolete public/raw-test surface still exists: {obsolete}/")
    text = script.read_text(encoding="utf-8")
    checker_id = str(task.get("feedback_checker_task_id") or task.get("public_visible_checker_task_id") or "")
    if "run_feedback" not in text:
        problems.append(f"{slug}: feedback runner does not use shared feedback_oracle helper")
    if checker_id and checker_id in text:
        problems.append(f"{slug}: feedback runner leaks checker id {checker_id}")
    if checker_profile.exists():
        profile = json.loads(checker_profile.read_text(encoding="utf-8"))
        observed_checker_id = str(profile.get("checker_task_id") or "")
        if checker_id and observed_checker_id != checker_id:
            problems.append(f"{slug}: checker profile id {observed_checker_id!r} does not match {checker_id!r}")
        if "testbench" in profile:
            problems.append(f"{slug}: checker_profile.json must not contain testbench content")
    if contract.exists():
        public_contract = json.loads(contract.read_text(encoding="utf-8"))
        feedback_oracle = public_contract.get("feedback_oracle") or {}
        score_oracle = public_contract.get("score_oracle") or {}
        if isinstance(feedback_oracle, dict) and "checker_task_id" in feedback_oracle:
            problems.append(f"{slug}: public_contract leaks feedback checker_task_id")
        if isinstance(score_oracle, dict) and "profile_path" in score_oracle:
            problems.append(f"{slug}: public_contract leaks score profile_path")
        visible_files = public_contract.get("agent_visible_files") or []
        if "test_feedback/public_tb.scs" not in visible_files:
            problems.append(f"{slug}: public_contract does not expose public feedback TB")
        for item in visible_files:
            item_text = str(item)
            if item_text.startswith(("evaluator/", "solution/", "test_harness/", "negative_variants/")):
                problems.append(f"{slug}: public_contract marks private file as agent-visible: {item_text}")
        if isinstance(feedback_oracle, dict) and feedback_oracle.get("public_tb") != "test_feedback/public_tb.scs":
            problems.append(f"{slug}: public_contract feedback_oracle.public_tb is missing or wrong")
        if isinstance(score_oracle, dict) and score_oracle.get("private_score_tb_exposed") is not False:
            problems.append(f"{slug}: public_contract must keep private score TB hidden")
        if isinstance(score_oracle, dict) and score_oracle.get("checker_profile_exposed") is not False:
            problems.append(f"{slug}: public_contract must keep checker profile hidden")
    return problems


def main() -> int:
    tasks = load_tasks()
    problems: list[str] = []
    for slug, task in sorted(tasks.items()):
        problems.extend(audit_canonical(slug))
        problems.extend(audit_modes(slug, task))
        problems.extend(audit_feedback_surface(slug, task))

    summary = {
        "benchmark": "benchmark-vabench-release-v4",
        "task_count": len(tasks),
        "modes": list(ALL_MODES),
        "status": "PASS" if not problems else "FAIL",
        "problem_count": len(problems),
        "problems": problems,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
