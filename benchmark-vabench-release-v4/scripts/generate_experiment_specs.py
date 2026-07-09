#!/usr/bin/env python3
"""Generate structured G0-G5 experiment records for the v4 pilot."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = SCRIPT_DIR.parents[0]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_prompt_modes import (  # noqa: E402
    ALL_MODES,
    MODES_JSON,
    WRAPPER_VERSION,
    build_prompt,
    load_tasks,
    sha256_text,
    skill_files_for_mode,
    task_dir,
)

SCHEMA_VERSION = "v4-pilot-experiment-spec-v1"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(PACKAGE_ROOT).as_posix()


def public_feedback_files(slug: str) -> list[str]:
    base = task_dir(slug)
    candidates = [
        base / "public_contract.json",
        base / "test_feedback" / "public_tb.scs",
        base / "test_feedback" / "run_feedback.py",
    ]
    return [rel(path) for path in candidates if path.exists()]


def feedback_runner(slug: str) -> str | None:
    path = task_dir(slug) / "test_feedback" / "run_feedback.py"
    return rel(path) if path.exists() else None


def prompt_path(slug: str, mode: str) -> Path:
    return PACKAGE_ROOT / "reports" / "rendered_prompts" / slug / mode / "prompt.md"


def mode_skills(mode_policy: dict[str, Any]) -> list[str]:
    skills: list[str] = []
    if mode_policy.get("veriloga_skill"):
        skills.append("veriloga")
    if mode_policy.get("feedback_debug_skill"):
        skills.append("feedback_debug")
    return skills


def build_record(slug: str, task: dict[str, Any], mode: str, mode_policy: dict[str, Any]) -> dict[str, Any]:
    is_agentic = mode in {"G2", "G3", "G4", "G5"}
    is_clean_direct = mode == "G0"
    prompt = build_prompt(slug, task, mode)
    public_files = public_feedback_files(slug)
    runner = feedback_runner(slug)
    evas_feedback_channels = [
        "ahdl_like_preflight",
        "evas_simulation",
        "behavior_property_diagnostics",
    ] if is_agentic else []
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "benchmark": "benchmark-vabench-release-v4",
        "wrapper_version": WRAPPER_VERSION,
        "task_slug": slug,
        "task_id": task.get("id"),
        "source_task_id": task.get("source_task_id"),
        "mode": mode,
        "mode_label": mode_policy.get("label"),
        "runner_family": "agents" if is_agentic else "llms",
        "process_type": "agentic" if is_agentic else "direct_llm",
        "clean_direct_baseline": is_clean_direct,
        "prompt_path": rel(prompt_path(slug, mode)),
        "prompt_sha256": sha256_text(prompt),
        "canonical_prompt_path": rel(task_dir(slug) / "instruction.md"),
        "target_artifacts": task.get("target", []),
        "source_release_entry_id": task.get("source_release_entry_id"),
        "access_policy": {
            "shell": is_agentic,
            "file_browsing": "feedback_surface_only" if is_agentic else "none",
            "tool_access": bool(mode_policy.get("tool_access")),
            "public_feedback_access": mode_policy.get("public_feedback_access"),
            "hidden_access": False,
            "private_score_access": False,
            "feedback_runner": runner if is_agentic else None,
            "feedback_files": public_files if is_agentic else [],
            "embedded_feedback_files": [],
            "evas_feedback_channels": evas_feedback_channels,
            "allowed_commands": [
                f"VABENCH_FEEDBACK_SOURCE_DIR=<candidate-dir> python3 {runner}"
            ]
            if is_agentic and runner
            else [],
        },
        "skills": mode_skills(mode_policy),
        "skill_files": skill_files_for_mode(mode),
        "notes": [],
    }
    if mode == "G0":
        record["notes"].append("Direct baseline: canonical task prompt only.")
    if mode == "G1":
        record["notes"].append("Direct one-shot with generic Verilog-A writing skill.")
    if mode == "G2":
        record["notes"].append("Agent with visible feedback oracle and no additional Verilog-A or feedback/debug skill wrapper.")
    if mode == "G3":
        record["notes"].append("Agent with visible feedback oracle plus generic Verilog-A writing skill.")
    if mode == "G4":
        record["notes"].append("Agent with visible feedback oracle plus feedback/debug skill.")
    if mode == "G5":
        record["notes"].append("Agent with visible feedback oracle plus both Verilog-A writing skill and feedback/debug skill.")
    return record


def generate_records() -> list[dict[str, Any]]:
    tasks = load_tasks()
    modes = read_json(MODES_JSON)["modes"]
    records: list[dict[str, Any]] = []
    for slug, task in sorted(tasks.items()):
        for mode in ALL_MODES:
            records.append(build_record(slug, task, mode, modes[mode]))
    return records


def write_outputs(records: list[dict[str, Any]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    records_json = out_dir / "records.json"
    records_jsonl = out_dir / "records.jsonl"
    manifest = out_dir / "manifest.json"
    records_json.write_text(json.dumps({"records": records}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    records_jsonl.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    mode_counts: dict[str, int] = {}
    runner_counts: dict[str, int] = {}
    for record in records:
        mode_counts[record["mode"]] = mode_counts.get(record["mode"], 0) + 1
        runner_counts[record["runner_family"]] = runner_counts.get(record["runner_family"], 0) + 1
    manifest.write_text(
        json.dumps(
            {
                "benchmark": "benchmark-vabench-release-v4",
                "schema_version": SCHEMA_VERSION,
                "wrapper_version": WRAPPER_VERSION,
                "record_count": len(records),
                "mode_counts": mode_counts,
                "runner_family_counts": runner_counts,
                "records_json": rel(records_json),
                "records_jsonl": rel(records_jsonl),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        default="reports/experiment_specs",
        help="output directory relative to the v4 package",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PACKAGE_ROOT / out_dir
    records = generate_records()
    write_outputs(records, out_dir)
    print(
        json.dumps(
            {
                "benchmark": "benchmark-vabench-release-v4",
                "schema_version": SCHEMA_VERSION,
                "status": "WROTE",
                "record_count": len(records),
                "out_dir": rel(out_dir),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
