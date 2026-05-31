#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "counterpart_asset_repair.json"
REPORT_MD = REPORTS_ROOT / "counterpart_asset_repair.md"


@dataclass(frozen=True)
class RepairAction:
    entry_id: str
    form: str
    copied: list[str]
    reason: str


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def form_gold_dir(task: dict) -> Path:
    return ROOT / str(task["release_path"]) / "gold"


def current_gold_files(task: dict) -> list[Path]:
    gold_dir = form_gold_dir(task)
    if not gold_dir.exists():
        return []
    return sorted(path for path in gold_dir.iterdir() if path.is_file() and path.suffix in {".va", ".scs"})


def update_gold_list(task: dict) -> None:
    task["gold"] = [rel(path) for path in current_gold_files(task)]


def normalize_private_reference_artifacts(task: dict) -> None:
    form = str(task.get("form", ""))
    if "private_reference_artifacts" not in task:
        return
    refs = list(task.get("private_reference_artifacts", []))
    if form == "bugfix":
        task["private_reference_artifacts"] = [ref for ref in refs if Path(str(ref)).name == "dut_fixed.va"]
    elif form in {"dut", "tb"}:
        task["private_reference_artifacts"] = []


def copy_missing(src_paths: list[Path], dst_dir: Path, suffix: str) -> list[Path]:
    copied: list[Path] = []
    dst_dir.mkdir(parents=True, exist_ok=True)
    for src in src_paths:
        if src.suffix != suffix:
            continue
        dst = dst_dir / src.name
        if not dst.exists():
            shutil.copy2(src, dst)
            copied.append(dst)
    return copied


def repair_entry(entry_path: Path) -> tuple[dict, list[RepairAction], list[str]]:
    entry = read_json(entry_path)
    tasks = [task for task in entry.get("release_tasks", []) if isinstance(task, dict)]
    by_form = {str(task.get("form")): task for task in tasks}
    e2e = by_form.get("e2e")
    actions: list[RepairAction] = []
    blockers: list[str] = []
    if not e2e:
        return entry, actions, blockers

    e2e_gold = current_gold_files(e2e)
    e2e_vas = [path for path in e2e_gold if path.suffix == ".va"]
    e2e_tbs = [path for path in e2e_gold if path.suffix == ".scs"]
    entry_id = str(entry.get("release_entry_id", entry_path.parent.name))

    for form in ("dut", "tb", "bugfix"):
        task = by_form.get(form)
        if not task:
            continue
        gold_files = current_gold_files(task)
        has_va = any(path.suffix == ".va" for path in gold_files)
        has_tb = any(path.suffix == ".scs" for path in gold_files)
        copied: list[Path] = []
        reason = ""

        if form in {"dut", "bugfix"} and not has_tb:
            if not e2e_tbs:
                blockers.append(f"{entry_id}:{form}: no e2e testbench counterpart")
            else:
                copied = copy_missing(e2e_tbs, form_gold_dir(task), ".scs")
                reason = "added reference testbench counterpart from e2e/gold"
        elif form == "tb" and not has_va:
            if not e2e_vas:
                blockers.append(f"{entry_id}:tb: no e2e DUT counterpart")
            else:
                copied = copy_missing(e2e_vas, form_gold_dir(task), ".va")
                reason = "added reference DUT counterpart from e2e/gold"

        if copied:
            update_gold_list(task)
            actions.append(
                RepairAction(
                    entry_id=entry_id,
                    form=form,
                    copied=[rel(path) for path in copied],
                    reason=reason,
                )
            )
        else:
            update_gold_list(task)
        normalize_private_reference_artifacts(task)

    return entry, actions, blockers


def score_runnable_issues() -> list[str]:
    issues: list[str] = []
    for task_path in sorted(TASKS_ROOT.glob("*/vbr1_*/forms/*/release_task.json")):
        task = read_json(task_path)
        form = str(task.get("form", task_path.parent.name))
        gold_dir = task_path.parent / "gold"
        gold_files = sorted(
            path for path in gold_dir.iterdir() if path.is_file() and path.suffix in {".va", ".scs"}
        ) if gold_dir.exists() else []
        has_va = any(path.suffix == ".va" for path in gold_files)
        has_scs = any(path.suffix == ".scs" for path in gold_files)
        task_id = str(task.get("task_id", task_path.parent.parent.parent.name))
        if form in {"dut", "bugfix"} and not has_scs:
            issues.append(f"{task_id}: missing reference Spectre testbench counterpart")
        elif form == "tb" and not has_va:
            issues.append(f"{task_id}: missing reference Verilog-A DUT counterpart")
        elif form == "e2e" and (not has_va or not has_scs):
            issues.append(f"{task_id}: missing e2e Verilog-A/testbench pair")
    return issues


def build_report(actions: list[RepairAction], blockers: list[str]) -> dict:
    issues = score_runnable_issues()
    return {
        "status": "pass" if not blockers and not issues else "blocked",
        "action_scope": "current script invocation; reruns are idempotent after assets are repaired",
        "repaired_form_count": len(actions),
        "copied_asset_count": sum(len(action.copied) for action in actions),
        "checked_release_form_count": len(list(TASKS_ROOT.glob("*/vbr1_*/forms/*/release_task.json"))),
        "score_runnable_counterpart_issue_count": len(issues),
        "score_runnable_counterpart_issues": issues,
        "blockers": blockers,
        "actions": [
            {
                "release_entry_id": action.entry_id,
                "form": action.form,
                "reason": action.reason,
                "copied": action.copied,
            }
            for action in actions
        ],
    }


def write_markdown(report: dict) -> None:
    lines = [
        "# vaBench Counterpart Asset Repair",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| action scope | {report['action_scope']} |",
        f"| repaired forms | {report['repaired_form_count']} |",
        f"| copied assets | {report['copied_asset_count']} |",
        f"| checked release forms | {report['checked_release_form_count']} |",
        f"| score-runnable counterpart issues | {report['score_runnable_counterpart_issue_count']} |",
        "",
    ]
    if report["blockers"]:
        lines.extend(["## Blockers", ""])
        lines.extend(f"- `{item}`" for item in report["blockers"])
        lines.append("")
    if report["score_runnable_counterpart_issues"]:
        lines.extend(["## Score-Runnable Counterpart Issues", ""])
        lines.extend(f"- `{item}`" for item in report["score_runnable_counterpart_issues"])
        lines.append("")
    lines.extend(["## Actions", ""])
    for action in report["actions"]:
        copied = ", ".join(f"`{path}`" for path in action["copied"])
        lines.append(f"- `{action['release_entry_id']}:{action['form']}`: {action['reason']} -> {copied}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    all_actions: list[RepairAction] = []
    all_blockers: list[str] = []
    for entry_path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        before = read_json(entry_path)
        entry, actions, blockers = repair_entry(entry_path)
        if actions or entry != before:
            write_json(entry_path, entry)
        all_actions.extend(actions)
        all_blockers.extend(blockers)

    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report(all_actions, all_blockers)
    write_json(REPORT_JSON, report)
    write_markdown(report)
    print(
        f"status={report['status']} repaired_forms={report['repaired_form_count']} "
        f"copied_assets={report['copied_asset_count']} blockers={len(report['blockers'])}"
    )
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
