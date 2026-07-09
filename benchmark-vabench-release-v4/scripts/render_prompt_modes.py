#!/usr/bin/env python3
"""Render v4 pilot prompts for G0-G5 comparison modes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TASKS_JSON = PACKAGE_ROOT / "TASKS.json"
MODES_JSON = PACKAGE_ROOT / "prompt_modes" / "modes.json"
SKILLS_DIR = PACKAGE_ROOT / "prompt_modes" / "skills"
WRAPPER_VERSION = "v4-pilot-wrapper-v2"
ALL_MODES = ("G0", "G1", "G2", "G3", "G4", "G5")
SKILL_FILES = {
    "veriloga": SKILLS_DIR / "veriloga_writing.md",
    "feedback_debug": SKILLS_DIR / "feedback_debug_loop.md",
}

DIRECT_SYSTEM_PROMPT = """\
You are an expert Verilog-A behavioral modeling engineer.
Write the requested voltage-domain behavioral Verilog-A artifacts.
Follow the public task contract exactly. Do not add explanatory prose, private reasoning, or unrequested files.
"""

AGENTIC_FEEDBACK_WRAPPER = """\
Agentic feedback-loop interface:
- You may inspect only the task's public `instruction.md`, `public_contract.json`, `test_feedback/public_tb.scs`, and `test_feedback/run_feedback.py` files.
- You may run the black-box feedback oracle against a candidate source directory:
  `VABENCH_FEEDBACK_SOURCE_DIR=<candidate-dir> python3 <task>/test_feedback/run_feedback.py`
- The feedback oracle may return AHDL-like preflight diagnostics, EVAS simulation errors, trace-availability errors, and behavior-property diagnostics.
- The public feedback testbench is a debugging example, not final correctness proof. Private score testbenches, checker profiles, and final scoring remain inaccessible.
- Do not hard-code only the public feedback stimulus constants. Generalize to the public task contract; final scoring may use different stimuli under the same contract.
"""

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(PACKAGE_ROOT).as_posix()


def artifact_language(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".va":
        return "verilog-a"
    if suffix == ".scs":
        return "spectre"
    if suffix == ".json":
        return "json"
    return "text"


def build_file_protocol(target_artifacts: list[str]) -> str:
    lines = ["Return exactly the target artifacts below, using this file-marker protocol:", ""]
    for filename in target_artifacts:
        language = artifact_language(filename)
        lines.extend(
            [
                f"[BEGIN file: {filename}]",
                f"```{language}",
                f"<contents of {filename}>",
                "```",
                f"[DONE file: {filename}]",
                "",
            ]
        )
    lines.extend(
        [
            "Do not include prose before, between, or after file blocks.",
            "Do not rename target files. Do not emit additional files.",
        ]
    )
    return "\n".join(lines).strip()


def task_dir(slug: str) -> Path:
    return PACKAGE_ROOT / "tasks" / slug


def load_tasks() -> dict[str, dict[str, Any]]:
    payload = read_json(TASKS_JSON)
    defaults = payload.get("defaults", {})
    tasks: dict[str, dict[str, Any]] = {}
    for slug, entry in payload.get("tasks", {}).items():
        merged = dict(defaults)
        merged.update(entry)
        tasks[slug] = merged
    return tasks


def resolve_task(token: str, tasks: dict[str, dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    token = token.strip()
    for slug, task in tasks.items():
        if token in {slug, str(task.get("id")), slug.split("-", 1)[0]}:
            return slug, task
    matches = [(slug, task) for slug, task in tasks.items() if slug.startswith(token)]
    if len(matches) == 1:
        return matches[0]
    raise SystemExit(f"unknown or ambiguous v4 task: {token}")


def canonical_prompt(slug: str) -> str:
    path = task_dir(slug) / "instruction.md"
    return path.read_text(encoding="utf-8").strip()


def mode_skill_names(mode: str) -> list[str]:
    skills: list[str] = []
    if mode in {"G1", "G3", "G5"}:
        skills.append("veriloga")
    if mode in {"G4", "G5"}:
        skills.append("feedback_debug")
    return skills


def skill_text(skill: str) -> str:
    path = SKILL_FILES[skill]
    if not path.exists():
        raise SystemExit(f"missing skill file: {path}")
    return path.read_text(encoding="utf-8").strip()


def skill_file_metadata(skill: str) -> dict[str, str]:
    text = skill_text(skill)
    return {
        "skill": skill,
        "path": rel(SKILL_FILES[skill]),
        "sha256": sha256_text(text),
    }


def skill_files_for_mode(mode: str) -> list[dict[str, str]]:
    return [skill_file_metadata(skill) for skill in mode_skill_names(mode)]


def build_prompt(slug: str, task: dict[str, Any], mode: str) -> str:
    if mode not in ALL_MODES:
        raise SystemExit(f"unsupported mode {mode}; choose one of {', '.join(ALL_MODES)}")

    targets = list(task.get("target") or [])
    task_prompt = canonical_prompt(slug)
    sections = [
        f"Wrapper version: `{WRAPPER_VERSION}`",
        f"Mode: `{mode}`",
        "System:",
        DIRECT_SYSTEM_PROMPT.strip(),
        "Question:",
        task_prompt,
    ]

    for skill in mode_skill_names(mode):
        if skill == "feedback_debug":
            continue
        sections.append(skill_text(skill))
    if mode in {"G2", "G3", "G4", "G5"}:
        sections.append(AGENTIC_FEEDBACK_WRAPPER.strip())
    if "feedback_debug" in mode_skill_names(mode):
        sections.append(skill_text("feedback_debug"))

    sections.extend(["Answer:", build_file_protocol(targets)])
    return "\n\n".join(sections).strip() + "\n"


def write_rendered_prompt(slug: str, task: dict[str, Any], mode: str, out_dir: Path) -> dict[str, Any]:
    prompt = build_prompt(slug, task, mode)
    mode_dir = out_dir / slug / mode
    mode_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = mode_dir / "prompt.md"
    meta_path = mode_dir / "metadata.json"
    canonical = canonical_prompt(slug)
    prompt_path.write_text(prompt, encoding="utf-8")
    metadata = {
        "benchmark": "benchmark-vabench-release-v4",
        "task_slug": slug,
        "task_id": task.get("id"),
        "source_task_id": task.get("source_task_id"),
        "mode": mode,
        "wrapper_version": WRAPPER_VERSION,
        "target_artifacts": task.get("target", []),
        "skill_files": skill_files_for_mode(mode),
        "canonical_prompt_sha256": sha256_text(canonical),
        "final_prompt_sha256": sha256_text(prompt),
        "prompt_path": rel(prompt_path),
    }
    meta_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", action="append", default=[], help="task slug, id, or numeric prefix")
    parser.add_argument("--mode", choices=(*ALL_MODES, "all"), default="G0")
    parser.add_argument("--out-dir", help="write rendered prompt(s) under this directory")
    parser.add_argument("--print", action="store_true", help="print the rendered prompt when exactly one task/mode is selected")
    args = parser.parse_args()

    tasks = load_tasks()
    selected = [resolve_task(token, tasks) for token in args.task] if args.task else sorted(tasks.items())
    modes = list(ALL_MODES) if args.mode == "all" else [args.mode]

    rendered: list[dict[str, Any]] = []
    if args.out_dir:
        out_dir = Path(args.out_dir)
        if not out_dir.is_absolute():
            out_dir = PACKAGE_ROOT / out_dir
        for slug, task in selected:
            for mode in modes:
                rendered.append(write_rendered_prompt(slug, task, mode, out_dir))
        (out_dir / "index.json").write_text(
            json.dumps({"rendered": rendered}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if args.print:
        if len(selected) != 1 or len(modes) != 1:
            raise SystemExit("--print requires exactly one selected task and one selected mode")
        slug, task = selected[0]
        print(build_prompt(slug, task, modes[0]), end="")

    if args.out_dir:
        print(json.dumps({"rendered": rendered}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
