#!/usr/bin/env python3
"""Consume one tri-form task record and export an isolated runtime package."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RELEASE = PACKAGE_ROOT / "release" / "tri-form-v4-1200-draft"
AGENTIC = {"G2", "G3", "G4", "G5"}
FORM_SKILLS = {
    "dut": "dut_modeling.md",
    "testbench": "testbench_verification.md",
    "bugfix": "bugfix_diagnosis.md",
}
FEEDBACK_GUIDES = {
    "dut": "feedback_dut.md",
    "testbench": "feedback_testbench.md",
    "bugfix": "feedback_bugfix.md",
}
WRAPPERS_BY_PROCESS = {
    "direct_one_shot": "direct_wrapper.md",
    "agentic": "agentic_wrapper.md",
}
COMPONENT_SUBDIR_BY_NAME = {
    **{name: "form_skills" for name in FORM_SKILLS.values()},
    **{name: "feedback_guides" for name in FEEDBACK_GUIDES.values()},
    **{name: "wrappers" for name in WRAPPERS_BY_PROCESS.values()},
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def copy_tree(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)


def prompt_record(release: Path, task_id: str, mode: str) -> dict[str, Any]:
    for line in (release / "prompt_modes" / "PROMPT_RECORDS.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("task_id") == task_id and row.get("mode") == mode:
            return row
    raise SystemExit(f"missing prompt record for {task_id}/{mode}")


def task_record(release: Path, task_id: str) -> tuple[dict[str, Any], Path]:
    index = read_json(release / "TASK_INDEX.json")
    matches = [row for row in index.get("tasks") or [] if row.get("task_id") == task_id]
    if len(matches) != 1:
        raise SystemExit(f"expected one task record for {task_id}, found {len(matches)}")
    task_dir = release / str(matches[0]["task_dir"])
    return read_json(task_dir / "task_record.json"), task_dir


def serialize_public_artifacts(task_dir: Path, form: str) -> str:
    lines: list[str] = []
    public = task_dir / "public"
    roots = []
    if form == "testbench":
        roots.append(public / "supplied_dut")
    elif form == "bugfix":
        roots.append(public / "buggy_bundle")
    for root in roots:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(public).as_posix()
            lines.extend([
                f'<<<VABENCH_INPUT_ARTIFACT path="{relative}">>>',
                path.read_text(encoding="utf-8"),
                "<<<END_VABENCH_INPUT_ARTIFACT>>>",
            ])
    return "\n".join(lines)


def prompt_component_path(release: Path, component_id: str) -> Path:
    subdir = COMPONENT_SUBDIR_BY_NAME.get(component_id)
    if subdir is None:
        raise SystemExit(f"unknown prompt component: {component_id}")
    return release / "prompt_modes" / subdir / component_id


def ordered_prompt_components(mode_record: dict[str, Any]) -> list[str]:
    wrapper = WRAPPERS_BY_PROCESS[str(mode_record["process"])]
    component_hashes = mode_record.get("prompt_component_hashes") or {}
    if wrapper not in component_hashes:
        raise SystemExit(f"prompt record is missing wrapper hash: {wrapper}")
    components = [
        str(component_id)
        for component_id in mode_record.get("component_order") or []
        if component_id in component_hashes
    ]
    if not components or components[-1] != wrapper:
        raise SystemExit(f"prompt record wrapper is not last: {wrapper}")
    return components


def render_prompt(release: Path, task_dir: Path, record: dict[str, Any], mode_record: dict[str, Any], *, inline_artifacts: bool) -> str:
    parts = [(task_dir / "public" / "instruction.md").read_text(encoding="utf-8")]
    artifacts = serialize_public_artifacts(task_dir, str(record["form"])) if inline_artifacts else ""
    if artifacts:
        parts.append(artifacts)
    for component in ordered_prompt_components(mode_record):
        parts.extend([
            f'<<<VABENCH_COMPONENT id="{component}">>>',
            prompt_component_path(release, component).read_text(encoding="utf-8"),
            "<<<END_VABENCH_COMPONENT>>>",
        ])
    return "\n\n".join(parts)


def install_public(task_dir: Path, public_root: Path, form: str, mode: str) -> None:
    task_public = task_dir / "public"
    target = public_root / "task"
    target.mkdir(parents=True)
    shutil.copy2(task_public / "instruction.md", target / "instruction.md")
    if form == "testbench":
        copy_tree(task_public / "supplied_dut", target / "supplied_dut")
    elif form == "bugfix":
        copy_tree(task_public / "buggy_bundle", target / "buggy_bundle")
        if mode in AGENTIC:
            copy_tree(task_public / "buggy_bundle", public_root / "submission")
    if mode in AGENTIC:
        write_json(public_root / "tool_manifest.json", {
            "schema_version": "v4-public-tool-manifest-v1",
            "commands": ["vabench feedback capabilities", "vabench feedback run"],
            "available_channels": ["ahdl", "sim-log", "trace", "metrics", "properties"],
            "private_score_available": False,
        })


def install_evaluator(task_dir: Path, evaluator_root: Path, record: dict[str, Any]) -> None:
    source_task = PACKAGE_ROOT / str(record["canonical_dut_source"])
    source_eval = source_task / "evaluator"
    provenance = task_dir / "provenance"
    form = str(record["form"])
    evaluator_root.mkdir(parents=True)
    for name in ("task_record.json", "family_spec.json", "checker_profile.json", "harness_spec.json", "toolchain_lock.json"):
        shutil.copy2(source_eval / name, evaluator_root / name)
    copy_tree(source_eval / "profiles", evaluator_root / "profiles")
    shutil.copy2(task_dir / "evaluator" / "score_policy.json", evaluator_root / "score_policy.json")
    if form in {"dut", "bugfix"}:
        copy_tree(source_eval / "solution", evaluator_root / "solution")
        shutil.copy2(source_eval / "score_tb.scs", evaluator_root / "trusted_feedback_tb.scs")
    if form == "testbench":
        copy_tree(source_eval / "solution", evaluator_root / "trusted_solution")
        copy_tree(source_eval / "mutation_bundles", evaluator_root / "mutation_bundles")
        shutil.copy2(source_eval / "mutation_catalog.json", evaluator_root / "mutation_catalog.json")
        for name in ("reference_tb.scs", "testbench_security_policy.json"):
            shutil.copy2(task_dir / "evaluator" / name, evaluator_root / name)
        for name in ("derivation_manifest.json", "reference_certificate.json"):
            shutil.copy2(provenance / name, evaluator_root / name)
    elif form == "bugfix":
        shutil.copy2(provenance / "derivation_manifest.json", evaluator_root / "derivation_manifest.json")
        shutil.copy2(provenance / "gold_reference.json", evaluator_root / "gold_reference.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--task", required=True)
    parser.add_argument("--mode", choices=[f"G{x}" for x in range(6)], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--working-token-budget", type=int, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    release = args.release.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if output.exists():
        if not args.force:
            raise SystemExit(f"output exists: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)
    record, task_dir = task_record(release, args.task)
    mode_record = prompt_record(release, args.task, args.mode)
    public_root = output / "public"
    (public_root / "submission").mkdir(parents=True)
    install_public(task_dir, public_root, str(record["form"]), args.mode)
    install_evaluator(task_dir, output / "evaluator", record)
    prompt = render_prompt(
        release,
        task_dir,
        record,
        mode_record,
        inline_artifacts=args.mode not in AGENTIC,
    )
    prompt_name = "agent_prompt.txt" if args.mode in AGENTIC else "direct_prompt.txt"
    (output / prompt_name).write_text(prompt, encoding="utf-8")
    model_mounts = [] if args.mode not in AGENTIC else ["public/task:ro", "public/submission:rw"]
    write_json(output / "MODEL_ACCESS_POLICY.json", {
        "schema_version": "v4-model-access-policy-v1",
        "mode": args.mode,
        "mounts": model_mounts,
        "network": False,
        "evaluator_mounted": False,
    })
    write_json(output / "evidence" / "attempt_record.json", {
        "schema_version": "v4-attempt-record-v1",
        "task_id": args.task,
        "family_id": record["family_id"],
        "form": record["form"],
        "mode": args.mode,
        "state": "prepared",
        "working_token_budget": args.working_token_budget,
        "public_bundle_sha256": tree_sha(public_root / "task"),
        "initial_submission_sha256": tree_sha(public_root / "submission"),
        "submission_seeded_from_buggy_bundle": bool(record["form"] == "bugfix" and args.mode in AGENTIC),
        "evaluator_bundle_sha256": tree_sha(output / "evaluator"),
        "prompt_record_sha256": hashlib.sha256(json.dumps(mode_record, sort_keys=True).encode("utf-8")).hexdigest(),
        "final_candidate_sha256": None,
        "private_score_decisions": 0,
        "telemetry": {
            "working_tokens": None,
            "provider_tokens": None,
            "model_turns": None,
            "feedback_calls": None,
            "simulator_calls": None,
            "wall_time_s": None,
        },
    })
    print(json.dumps({
        "task_id": args.task,
        "form": record["form"],
        "mode": args.mode,
        "output": str(output),
        "model_mounts": model_mounts,
        "evaluator_mounted": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
