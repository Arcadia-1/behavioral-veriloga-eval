#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from vabench_release_prompt_wrapper import RELEASE_RUNNER_WRAPPER_VERSION


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "prompt_contract_manifest.json"
REPORT_MD = REPORTS_ROOT / "prompt_contract_manifest.md"
PACKAGE_MANIFEST = PACKAGE_ROOT / "MANIFEST.json"

PROMPT_VERSION_ID = "public-contract-v3"
SYNC_SCRIPT = ROOT / "runners" / "sync_vabench_release_prompt_contracts.py"
REQUIRED_SECTIONS = [
    "## Release Task Contract",
    "## Form-Specific Requirements",
    "## Output Contract",
    "## Task-Specific Public Description",
]
FORBIDDEN_TEXT = [
    "Bug to fix:",
    "injected Strict EVAS Validation Contract",
    "Question:",
    "Answer:",
    "System:",
    "few-shot",
    "ICL",
    "Known defect:",
    "[BEGIN file]",
    "[DONE file]",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_prompt_count(default: int) -> int:
    if not PACKAGE_MANIFEST.exists():
        return default
    manifest = read_json(PACKAGE_MANIFEST)
    summary = manifest.get("summary", {})
    if not isinstance(summary, dict):
        return default
    try:
        return int(summary.get("form_count", default))
    except (TypeError, ValueError):
        return default


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def release_form_dirs() -> list[Path]:
    if PACKAGE_MANIFEST.exists():
        manifest = read_json(PACKAGE_MANIFEST)
        rows = manifest.get("forms", [])
        form_dirs: list[Path] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            value = row.get("release_task_manifest")
            if not isinstance(value, str) or not value:
                continue
            path = ROOT / value
            if path.exists():
                form_dirs.append(path.parent)
        if form_dirs:
            return sorted(form_dirs)
    return sorted(path.parent for path in TASKS_ROOT.glob("*/vbr1_*/forms/*/release_task.json"))


def target_artifacts(form: str, gold_names: list[str], explicit: list[str] | None = None) -> list[str]:
    if explicit:
        return [str(item) for item in explicit]
    if form == "dut":
        return [name for name in gold_names if name.endswith(".va") and not name.startswith("tb_")]
    if form == "tb":
        return [name for name in gold_names if name.endswith(".scs")]
    if form == "bugfix":
        fixed = [name for name in gold_names if name == "dut_fixed.va"]
        return fixed or [name for name in gold_names if name.endswith(".va") and "buggy" not in name]
    if form == "e2e":
        return [name for name in gold_names if name.endswith((".va", ".scs"))]
    return [name for name in gold_names if name.endswith((".va", ".scs"))]


def build_row(form_dir: Path) -> dict[str, Any]:
    release_task_path = form_dir / "release_task.json"
    release_task = read_json(release_task_path)
    prompt_path = form_dir / "prompt.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    form = form_dir.name
    artifacts = release_task.get("artifacts", {})
    gold_names = [Path(path).name for path in artifacts.get("gold", [])]
    explicit = artifacts.get("submission_artifacts")
    targets = target_artifacts(form, gold_names, explicit if isinstance(explicit, list) else None)
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in prompt]
    forbidden = [item for item in FORBIDDEN_TEXT if item in prompt]
    missing_targets = [name for name in targets if f"`{name}`" not in prompt]
    status = "pass" if not missing_sections and not forbidden and not missing_targets else "fail"
    return {
        "status": status,
        "prompt_version_id": PROMPT_VERSION_ID,
        "release_entry_id": release_task.get("release_entry_id", ""),
        "task_id": release_task.get("id", ""),
        "form": form,
        "level": release_task.get("level", ""),
        "category": release_task.get("category", ""),
        "base_function": release_task.get("base_function", ""),
        "prompt": rel(prompt_path),
        "release_task_manifest": rel(release_task_path),
        "target_artifacts": targets,
        "prompt_sha256": sha256_text(prompt),
        "required_sections_present": [section for section in REQUIRED_SECTIONS if section in prompt],
        "missing_sections": missing_sections,
        "forbidden_text_present": forbidden,
        "missing_target_artifacts": missing_targets,
        "baseline_compatibility": "requires_rerun",
        "change_type": "public_contract_scaffold_normalization",
    }


def build_report() -> dict[str, Any]:
    rows = [build_row(form_dir) for form_dir in release_form_dirs()]
    expected_count = expected_prompt_count(len(rows))
    status_counts = Counter(str(row["status"]) for row in rows)
    form_counts = Counter(str(row["form"]) for row in rows)
    failed_rows = [row for row in rows if row["status"] != "pass"]
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "pass" if not failed_rows and len(rows) == expected_count else "fail",
        "prompt_version_id": PROMPT_VERSION_ID,
        "previous_prompt_version": "public-contract-v2",
        "runner_wrapper_version": RELEASE_RUNNER_WRAPPER_VERSION,
        "prompt_count": len(rows),
        "expected_prompt_count": expected_count,
        "status_counts": dict(sorted(status_counts.items())),
        "form_counts": dict(sorted(form_counts.items())),
        "sync_script": rel(SYNC_SCRIPT),
        "change_summary": [
            "Normalized all release prompts to explicit public benchmark contracts.",
            "Added explicit Spectre .scs scaffold guidance for TB/E2E prompts, including ahdl_include and instance syntax.",
            "Moved runner-only wrapper, ICL, and repair-feedback protocol out of public prompts.",
            "Removed explicit bug-root-cause hints from bugfix prompts; bugfix tasks now expose only public behavior and observable mismatch framing.",
            f"Recorded runner-side baseline wrapper `{RELEASE_RUNNER_WRAPPER_VERSION}` for Question/Answer markers and shared EVAS/Spectre rules.",
            "Recorded target artifact names from release_task/gold assets for prompt-version traceability.",
            "Old model-baseline results should be treated as historical and rerun before comparison.",
        ],
        "claim_policy": {
            "public_prompt_scope": "task contract only: form, target artifacts, interfaces, public observables, public behavior checks, and output contract",
            "runner_wrapper_scope": "model invocation protocol, output extraction markers, optional repair feedback, and optional ICL variants",
            "evas_rules_scope": "shared voltage-domain and EVAS/Spectre compatibility guidance injected by runners, not benchmark prompt content",
            "baseline_comparison": "public-contract-v2, public-contract-v3, and different runner wrapper versions are not directly comparable without rerun",
        },
        "rows": rows,
    }


def write_markdown(report: dict[str, Any]) -> None:
    lines = [
        "# vaBench Release Prompt Contract Manifest",
        "",
        f"Date: {report['date']}",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| prompt version | `{report['prompt_version_id']}` |",
        f"| runner wrapper | `{report['runner_wrapper_version']}` |",
        f"| prompts | {report['prompt_count']} |",
        "",
        "## Form Counts",
        "",
        "| Form | Prompts |",
        "| --- | ---: |",
    ]
    for form, count in report["form_counts"].items():
        lines.append(f"| `{form}` | {count} |")
    lines.extend(
        [
            "",
            "## Change Summary",
            "",
        ]
    )
    for item in report["change_summary"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Claim Policy",
            "",
            f"- Public prompts are benchmark contracts: {report['claim_policy']['public_prompt_scope']}.",
            f"- Runner wrappers remain outside the prompt body: {report['claim_policy']['runner_wrapper_scope']}.",
            f"- EVAS rules remain shared runner guidance: {report['claim_policy']['evas_rules_scope']}.",
            f"- Baseline comparability: {report['claim_policy']['baseline_comparison']}.",
            "",
            "## Sample Rows",
            "",
            "| Task | Form | Target Artifacts | Prompt SHA256 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in report["rows"][:20]:
        targets = ", ".join(f"`{name}`" for name in row["target_artifacts"]) or "-"
        lines.append(f"| `{row['task_id']}` | `{row['form']}` | {targets} | `{row['prompt_sha256'][:12]}` |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote prompt contract manifest: status={status}; version={version}; prompts={count}".format(
            status=report["status"],
            version=report["prompt_version_id"],
            count=report["prompt_count"],
        )
    )
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
