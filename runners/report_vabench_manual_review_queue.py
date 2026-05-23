#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
MANIFEST_JSON = PACKAGE_ROOT / "MANIFEST.json"
QUEUE_CSV = ROOT / "docs" / "VABENCH_MANUAL_REVIEW_QUEUE.csv"
QUEUE_MD = ROOT / "docs" / "VABENCH_MANUAL_REVIEW_QUEUE.md"

FORM_PRIORITY = ("dut", "e2e", "tb", "bugfix")
CATEGORY_BATCH = {
    "Data Converters": "A Data converters",
    "PLL / Clock / Event Timing": "B Clocking and PLL",
    "Comparators and Decision Circuits": "C Comparators",
    "Calibration, DEM, and Control": "D Calibration and DEM",
    "Measurement and Testbench Instrumentation": "E Measurement and TB",
    "Stimulus and Sources": "F Stimulus and sources",
    "Analog Behavioral Signal Conditioning": "G Signal conditioning",
    "Sample, Hold, and Analog Memory": "H Sample/hold memory",
}

FIELDS = [
    "batch",
    "risk",
    "entry_id",
    "level",
    "category",
    "base_function",
    "forms",
    "certification",
    "representative_form",
    "prompt_preview",
    "gold_modules",
    "checker_focus",
    "risk_reason",
    "human_review_question",
    "next_action_preference",
]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def clean_cell(value: object) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return re.sub(r"\s+", " ", text).strip()


def representative_form(forms: list[str]) -> str:
    for form in FORM_PRIORITY:
        if form in forms:
            return form
    return forms[0] if forms else ""


def prompt_preview(path: Path) -> str:
    if not path.exists():
        return "missing prompt"
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
        if len(" ".join(lines)) > 220:
            break
    text = " ".join(lines)
    return clean_cell(text[:260] + ("..." if len(text) > 260 else ""))


def gold_modules(paths: list[Path]) -> str:
    modules: list[str] = []
    for path in paths:
        if path.suffix != ".va" or not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        modules.extend(re.findall(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_$]*)\s*\(", text))
    return ", ".join(dict.fromkeys(modules)) or "no Verilog-A module found"


def checker_focus(path: Path) -> str:
    if not path.exists():
        return "missing checks.yaml"
    text = path.read_text(encoding="utf-8")
    focus: list[str] = []
    for pattern in ("sim_correct", "behavior", "metric", "waveform", "compile", "spectre"):
        if pattern in text:
            focus.append(pattern)
    return ", ".join(focus) or "generic/static guard only"


def findings_by_entry() -> dict[str, list[str]]:
    audit = read_json(REPORTS_ROOT / "content_contract_audit.json")
    grouped: dict[str, list[str]] = defaultdict(list)
    for item in audit.get("findings", []):
        if not isinstance(item, dict):
            continue
        entry_id = item.get("entry_id") or item.get("keep_candidate")
        if not entry_id:
            continue
        form = item.get("form") or "entry"
        kind = item.get("kind", "finding")
        message = item.get("message", "")
        grouped[str(entry_id)].append(f"{kind}/{form}: {message}")
    remaining = read_json(REPORTS_ROOT / "remaining_work.json")
    for item in remaining.get("source_equivalence_blocked_forms", []):
        if not isinstance(item, dict):
            continue
        entry_id = str(item.get("entry_id", ""))
        if entry_id:
            grouped[entry_id].append(
                "source_equivalence_blocker/{form}: {blockers}".format(
                    form=item.get("form", "form"),
                    blockers="; ".join(str(blocker) for blocker in item.get("pending_blockers", [])),
                )
            )
    return grouped


def risk_for(entry: dict[str, Any], reasons: list[str]) -> tuple[str, str, str]:
    joined = " ".join(reasons)
    entry_id = str(entry["release_entry_id"])
    base = str(entry["base_function"])
    level = str(entry["level"])
    category = str(entry["category"])

    if "source_equivalence_blocker" in joined:
        return (
            "P0",
            joined,
            "Decide whether the release gold/evidence link is trustworthy or needs fresh dual certification before this form can be claimed.",
        )
    if "historical_name_in_public_prompt" in joined:
        return (
            "P0",
            joined,
            "Rename public wording/module contract or explicitly approve the legacy module name as private provenance only.",
        )
    if "shallow_generic_checker" in joined:
        return (
            "P1",
            joined,
            "Add a real function-level checker or mark this form as auxiliary until the checker proves the named behavior.",
        )
    if reasons:
        return (
            "P1",
            joined,
            "Review prompt, checker, and gold together and tighten the public observable if the checker is weaker than the task statement.",
        )
    if level == "L2":
        return (
            "P1",
            "L2 composition task requires manual verification that multiple functions really interact.",
            "Confirm this is a composed circuit flow, not a renamed L1 kernel or single-module smoke.",
        )
    if category in {"Measurement and Testbench Instrumentation", "Stimulus and Sources"}:
        return (
            "P2",
            "Auxiliary benchmark category; valid only when it has reusable measurement/source semantics.",
            "Confirm this is a reusable testbench/source function rather than checker syntax or simulator conformance.",
        )
    if entry.get("certification") != "certified":
        return (
            "P2",
            "Not fully EVAS/Spectre certified in the current manifest.",
            "Review semantic contract now, then leave certification blocked until fresh dual evidence imports.",
        )
    return (
        "P3",
        "No current automated high-risk finding, but every release task still needs human semantic sign-off.",
        "Confirm naming, prompt, checker, and gold describe the same circuit function.",
    )


def build_rows() -> list[dict[str, str]]:
    manifest = read_json(MANIFEST_JSON)
    forms_by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for form in manifest.get("forms", []):
        if isinstance(form, dict):
            forms_by_entry[str(form.get("release_entry_id", ""))].append(form)

    findings = findings_by_entry()
    rows: list[dict[str, str]] = []
    for entry in sorted(manifest.get("entries", []), key=lambda item: (item["category"], item["level"], item["base_function"])):
        entry_id = str(entry["release_entry_id"])
        forms = list(entry.get("forms", []))
        rep = representative_form(forms)
        form_rows = forms_by_entry.get(entry_id, [])
        rep_form = next((item for item in form_rows if item.get("form") == rep), form_rows[0] if form_rows else {})
        prompt_path = ROOT / str(rep_form.get("prompt", ""))
        checks_path = ROOT / str(rep_form.get("checks", ""))
        task_manifest = read_json(ROOT / str(rep_form.get("release_task_manifest", "")))
        artifacts = task_manifest.get("artifacts", {}) if isinstance(task_manifest.get("artifacts"), dict) else {}
        gold_paths = [ROOT / str(path) for path in artifacts.get("gold", []) if isinstance(path, str)]
        risk, reason, question = risk_for(entry, findings.get(entry_id, []))
        action = {
            "P0": "review first; fix wording/checker/evidence before paper claims",
            "P1": "review in first two batches; strengthen checker or downgrade claim",
            "P2": "review after P0/P1; keep conservative certification wording",
            "P3": "spot-check and sign off after higher-risk batches",
        }[risk]
        rows.append(
            {
                "batch": CATEGORY_BATCH.get(str(entry["category"]), "Z Other"),
                "risk": risk,
                "entry_id": entry_id,
                "level": str(entry["level"]),
                "category": str(entry["category"]),
                "base_function": str(entry["base_function"]),
                "forms": ",".join(forms),
                "certification": str(entry.get("certification", "")),
                "representative_form": rep,
                "prompt_preview": prompt_preview(prompt_path),
                "gold_modules": gold_modules(gold_paths),
                "checker_focus": checker_focus(checks_path),
                "risk_reason": clean_cell(reason),
                "human_review_question": clean_cell(question),
                "next_action_preference": action,
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    with QUEUE_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    risk_counts = defaultdict(int)
    batch_counts = defaultdict(int)
    for row in rows:
        risk_counts[row["risk"]] += 1
        batch_counts[row["batch"]] += 1

    lines = [
        "# vaBench Manual Review Queue",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This is the human-review queue for task 2 and task 3 after locking the",
        "clean 72-entry function table. Every entry requires manual semantic",
        "sign-off; risk level only decides review order.",
        "",
        "## Review Contract",
        "",
        "| Task | Human check | Pass condition |",
        "| --- | --- | --- |",
        "| Task 2: semantic alignment | Compare function name, prompt, checker, gold code, and saved observables. | They describe the same circuit behavior without relying on historical names or hidden implementation details. |",
        "| Task 3: risk triage/fix | Decide whether each risk needs wording fix, stronger checker, fresh EVAS/Spectre evidence, or downgrade. | No task enters a paper-facing claim with ambiguous semantics, shallow checker, or stale evidence. |",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| total review entries | {len(rows)} |",
    ]
    for risk in ("P0", "P1", "P2", "P3"):
        lines.append(f"| {risk} entries | {risk_counts[risk]} |")
    lines.extend(["", "## Batch Order", "", "| Batch | Entries |", "| --- | ---: |"])
    for batch in sorted(batch_counts):
        lines.append(f"| {batch} | {batch_counts[batch]} |")
    lines.extend(
        [
            "",
            "Recommended manual order: finish all P0 entries first, then P1 checker/composition entries, then P2 auxiliary or pending-certification entries, then P3 sign-off.",
            "",
        ]
    )

    for batch in sorted(batch_counts):
        lines.extend([f"## {batch}", "", "| Risk | Entry | Level | Function | Forms | Rep prompt | Gold modules | Review question |", "| --- | --- | --- | --- | --- | --- | --- | --- |"])
        for row in [item for item in rows if item["batch"] == batch]:
            lines.append(
                "| {risk} | `{entry_id}` | {level} | {base_function} | `{forms}` | {prompt_preview} | `{gold_modules}` | {human_review_question} |".format(
                    **{key: clean_cell(value) for key, value in row.items()}
                )
            )
        lines.append("")

    lines.extend(
        [
            "## Machine-Readable Queue",
            "",
            f"CSV: `{rel(QUEUE_CSV)}`",
            "",
            "The CSV contains `checker_focus`, `risk_reason`, and `next_action_preference` for every entry.",
        ]
    )
    QUEUE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_csv(rows)
    write_markdown(rows)
    print(f"wrote manual review queue: entries={len(rows)} csv={rel(QUEUE_CSV)}")


if __name__ == "__main__":
    main()
