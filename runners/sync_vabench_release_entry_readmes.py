#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "benchmark-vabench-release-v1" / "tasks"
FORM_ORDER = {"bugfix": 0, "dut": 1, "e2e": 2, "tb": 3}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "none"


def release_forms(entry: dict[str, Any]) -> list[str]:
    forms = [str(task.get("form", "")) for task in entry.get("release_tasks", []) if task.get("form")]
    return sorted(forms, key=lambda item: (FORM_ORDER.get(item, 99), item))


def render_entry_readme(entry: dict[str, Any]) -> str:
    title = str(entry.get("base_function") or entry.get("release_entry_id") or "Release Entry")
    entry_id = str(entry.get("release_entry_id") or entry.get("id") or "")
    level = str(entry.get("level") or "")
    category = str(entry.get("category") or "")
    package_status = str(entry.get("package_status") or "")
    score_surface = str(entry.get("score_surface") or "")
    forms = release_forms(entry)
    missing_forms = [str(item) for item in entry.get("missing_forms", [])]
    counts = entry.get("counts", {}) if isinstance(entry.get("counts"), dict) else {}
    certification = entry.get("certification", {}) if isinstance(entry.get("certification"), dict) else {}
    benchmark_score = "enabled" if bool(counts.get("benchmark_score")) else "disabled"
    evidence = str(certification.get("evidence") or "")

    lines = [
        f"# {title}",
        "",
        f"- Entry: `{entry_id}`",
        f"- Level: `{level}`",
        f"- Category: `{category}`",
        f"- Package status: `{package_status}`",
        f"- Score surface: `{score_surface}`",
        f"- Benchmark score: `{benchmark_score}`",
        f"- Materialized forms: `{format_list(forms)}`",
        f"- Missing forms: `{format_list(missing_forms)}`",
        (
            "- Certification: "
            f"static `{certification.get('static', 'unknown')}`; "
            f"EVAS `{certification.get('evas', 'unknown')}`; "
            f"Spectre `{certification.get('spectre', 'unknown')}`"
        ),
    ]
    if evidence:
        lines.append(f"- Evidence: `{evidence}`")
    lines.extend(
        [
            "",
            "This release entry is materialized in the paper-facing vaBench release package.",
            "`release_entry.json` is the structured source of truth for forms, scoring, and certification status.",
        ]
    )
    return "\n".join(lines) + "\n"


def sync_readmes(*, level: str | None, dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    for entry_path in sorted(TASKS_ROOT.glob("CT*/vbr1_*/release_entry.json")):
        entry = read_json(entry_path)
        if level is not None and str(entry.get("level")) != level:
            continue
        readme_path = entry_path.parent / "README.md"
        rendered = render_entry_readme(entry)
        current = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
        if current == rendered:
            continue
        changed.append(readme_path)
        if not dry_run:
            readme_path.write_text(rendered, encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=("L0", "L1", "L2"), help="Only sync release entries at this level.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    changed = sync_readmes(level=args.level, dry_run=args.dry_run)
    print(f"[release-readme-sync] changed={len(changed)} dry_run={args.dry_run}")
    for path in changed:
        print(f"  - {path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
