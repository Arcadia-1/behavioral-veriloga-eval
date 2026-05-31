#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

from materialize_vabench_release_designed_sources import DIFFICULTY_OVERRIDES, difficulty_for_row


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "vabench_difficulty_recalibration_20260529.json"
REPORT_MD = REPORTS_ROOT / "vabench_difficulty_recalibration_20260529.md"


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def calibrated_difficulty(entry: dict[str, object]) -> str:
    return difficulty_for_row(
        {
            "entry_id": str(entry["release_entry_id"]),
            "level": str(entry.get("level", "L1")),
        }
    )


def update_difficulty(path: Path, expected: str) -> tuple[str, bool]:
    payload = read_json(path)
    old = str(payload.get("difficulty", "D2"))
    if old != expected:
        payload["difficulty"] = expected
        write_json(path, payload)
        return old, True
    return old, False


def build_report() -> dict[str, object]:
    before_entries: Counter[str] = Counter()
    after_entries: Counter[str] = Counter()
    before_forms: Counter[str] = Counter()
    after_forms: Counter[str] = Counter()
    changed_entries: list[dict[str, object]] = []
    calibrated_override_entries: list[dict[str, object]] = []
    changed_files: list[str] = []

    for entry_path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        entry = read_json(entry_path)
        entry_id = str(entry["release_entry_id"])
        old_entry_difficulty = str(entry.get("difficulty", "D2"))
        new_difficulty = calibrated_difficulty(entry)
        before_entries[old_entry_difficulty] += 1
        after_entries[new_difficulty] += 1

        entry_changed = False
        if old_entry_difficulty != new_difficulty:
            entry["difficulty"] = new_difficulty
            write_json(entry_path, entry)
            entry_changed = True
            changed_files.append(rel(entry_path))
        if entry_id in DIFFICULTY_OVERRIDES:
            calibrated_override_entries.append(
                {
                    "release_entry_id": entry_id,
                    "difficulty": new_difficulty,
                    "rationale": rationale_for_entry(entry_id, new_difficulty),
                }
            )

        form_file_changes: list[str] = []
        for form_dir in sorted((entry_path.parent / "forms").glob("*")):
            if not form_dir.is_dir():
                continue
            form_old_difficulty = None
            for source_name in ("meta.json", "release_task.json"):
                source_path = form_dir / source_name
                if source_path.exists():
                    form_old_difficulty = str(read_json(source_path).get("difficulty", "D2"))
                    break
            before_forms[form_old_difficulty or old_entry_difficulty] += 1
            after_forms[new_difficulty] += 1
            for filename in ("meta.json", "release_task.json"):
                path = form_dir / filename
                if not path.exists():
                    continue
                _, file_changed = update_difficulty(path, new_difficulty)
                if file_changed:
                    form_file_changes.append(rel(path))
                    changed_files.append(rel(path))

        if entry_changed or form_file_changes:
            changed_entries.append(
                {
                    "release_entry_id": entry_id,
                    "level": entry.get("level", ""),
                    "old_difficulty": old_entry_difficulty,
                    "new_difficulty": new_difficulty,
                    "changed_files": [rel(entry_path)] if entry_changed else [],
                    "changed_form_files": form_file_changes,
                    "rationale": rationale_for_entry(entry_id, new_difficulty),
                }
            )

    return {
        "date": date.today().isoformat(),
        "status": "pass",
        "policy": {
            "basis": "Difficulty is calibrated from benchmark-facing circuit/form complexity, not from one model's pass rate.",
            "D1": "single-block threshold, first-order, or simple bounded voltage behavior",
            "D2": "standard L1 analog/mixed-signal macromodel with state, hysteresis, settling, or moderate nonlinearity",
            "D3": "L2 composition/flow rows or advanced nonlinear approximation rows that require multiple public behavior constraints",
        },
        "difficulty_overrides": dict(sorted(DIFFICULTY_OVERRIDES.items())),
        "entry_counts_before": dict(sorted(before_entries.items())),
        "entry_counts_after": dict(sorted(after_entries.items())),
        "form_counts_before": dict(sorted(before_forms.items())),
        "form_counts_after": dict(sorted(after_forms.items())),
        "changed_entry_count": len(changed_entries),
        "changed_file_count": len(changed_files),
        "changed_entries": changed_entries,
        "calibrated_override_entries": calibrated_override_entries,
    }


def rationale_for_entry(entry_id: str, difficulty: str) -> str:
    if entry_id in {
        "vbr1_l1_binary_weighted_voltage_dac",
        "vbr1_l1_thermometer_code_decoder",
        "vbr1_l1_unit_element_thermometer_dac",
        "vbr1_l1_sine_periodic_voltage_source",
    }:
        return "Preserved as D1 from prior release calibration: a single reusable primitive with a direct public input/output relation."
    if entry_id == "vbr1_l1_pipeline_adc_stage":
        return "Preserved as D3 from prior release calibration because the L1 row still requires residue/decision/stage behavior rather than one direct scalar transform."
    if entry_id in {
        "vbr1_l1_bias_voltage_generator_with_enable_trim",
        "vbr1_l1_uvlo_brownout_detector",
        "vbr1_l1_limiting_amplifier_frontend",
    }:
        return "Reclassified as D1 because the public task is a single-block bounded voltage behavior with one dominant decision or limiting relation."
    if entry_id in {
        "vbr1_l1_log_rssi_power_detector",
        "vbr1_l1_pa_compression_macro",
    }:
        return "Reclassified as D3 because the task requires a nonlinear compressed approximation and multiple public behavior constraints under the supported Verilog-A subset."
    if difficulty == "D3":
        return "L2 rows remain D3 because they compose multiple behaviors or flow-level checks."
    return "Default calibrated difficulty from release level and entry override policy."


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Difficulty Recalibration",
        "",
        f"Date: {report['date']}",
        "",
        "## Policy",
        "",
        f"- Basis: {report['policy']['basis']}",
        f"- D1: {report['policy']['D1']}",
        f"- D2: {report['policy']['D2']}",
        f"- D3: {report['policy']['D3']}",
        "",
        "## Counts",
        "",
        "| Metric | Before | After |",
        "| --- | --- | --- |",
        f"| entry difficulty counts | `{report['entry_counts_before']}` | `{report['entry_counts_after']}` |",
        f"| form difficulty counts | `{report['form_counts_before']}` | `{report['form_counts_after']}` |",
        "",
        "## Changed Entries",
        "",
        "| Entry | Old | New | Rationale |",
        "| --- | --- | --- | --- |",
    ]
    for row in report["changed_entries"]:
        lines.append(
            "| `{entry}` | `{old}` | `{new}` | {rationale} |".format(
                entry=row["release_entry_id"],
                old=row["old_difficulty"],
                new=row["new_difficulty"],
                rationale=row["rationale"],
            )
        )
    lines.extend(
        [
            "",
            "## Calibrated Override Entries",
            "",
            "| Entry | Difficulty | Rationale |",
            "| --- | --- | --- |",
        ]
    )
    for row in report["calibrated_override_entries"]:
        lines.append(
            "| `{entry}` | `{difficulty}` | {rationale} |".format(
                entry=row["release_entry_id"],
                difficulty=row["difficulty"],
                rationale=row["rationale"],
            )
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    write_json(REPORT_JSON, report)
    write_markdown(report)
    print(
        "wrote difficulty recalibration: changed_entries={entries}; entry_counts={counts}".format(
            entries=report["changed_entry_count"],
            counts=report["entry_counts_after"],
        )
    )


if __name__ == "__main__":
    main()
