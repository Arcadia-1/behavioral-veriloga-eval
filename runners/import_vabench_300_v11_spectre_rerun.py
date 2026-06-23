#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "benchmark-vabench-release-v1" / "vabench-300-expansion"
MANIFEST = EXPANSION / "VABENCH_300_MANIFEST.json"
REPORT_JSON = ROOT / "benchmark-vabench-release-v1" / "reports" / "vabench_300_v11_fresh_spectre_rerun.json"
REPORT_MD = ROOT / "benchmark-vabench-release-v1" / "reports" / "vabench_300_v11_fresh_spectre_rerun.md"
README = EXPANSION / "README.md"
TASK_SPECIFIC_EVIDENCE = "benchmark-vabench-release-v1/vabench-300-expansion/v11_task_specific_quality_evidence.json"
PROVISIONAL_STATUS = "provisional_v1.1_management"
CERTIFIED_STATUS = "certified_v1.1_promoted"
FRESH_CERTIFICATION = "fresh_evas_spectre_certified"
PAPER_SCORE_PENDING = "disabled_until_score_denominator_admission"
EXPECTED_V11_ROWS = 29


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def as_float(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) else None


def compact_result_row(row: dict[str, Any]) -> dict[str, Any]:
    raw = row.get("raw_result")
    if not isinstance(raw, dict):
        raw = {}
    evas = raw.get("evas")
    if not isinstance(evas, dict):
        evas = {}
    spectre = raw.get("spectre")
    if not isinstance(spectre, dict):
        spectre = {}
    parity = raw.get("parity")
    if not isinstance(parity, dict):
        parity = {}
    timing = raw.get("timing")
    if not isinstance(timing, dict):
        timing = {}
    vabench300 = row.get("vabench_300")
    if not isinstance(vabench300, dict):
        vabench300 = {}
    warnings = spectre.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []
    behavior_notes = spectre.get("behavior_notes", [])
    if not isinstance(behavior_notes, list):
        behavior_notes = []
    return {
        "task_id": str(vabench300.get("task_id") or raw.get("task_id") or ""),
        "topic_id": str(vabench300.get("topic_id") or "").split(":")[0],
        "legacy_entry_id": str(row.get("entry_id", "")),
        "form": str(row.get("form", "")),
        "variant": str(row.get("variant", "")),
        "expected_result": row.get("expected_result"),
        "expected_result_met": row.get("expected_result_met"),
        "expansion_status_at_run": vabench300.get("expansion_status"),
        "certification_at_run": vabench300.get("certification"),
        "raw_status": raw.get("status"),
        "evas_status": evas.get("status"),
        "evas_engine_used": evas.get("evas_engine_used"),
        "spectre_ok": spectre.get("ok"),
        "spectre_status": spectre.get("status"),
        "spectre_behavior_score": as_float(spectre.get("behavior_score")),
        "spectre_mode": spectre.get("spectre_mode"),
        "spectre_rows": spectre.get("rows"),
        "spectre_warning_count": len(warnings),
        "spectre_behavior_notes": [str(note) for note in behavior_notes[-3:]],
        "parity_status": parity.get("status"),
        "parity_policy": (parity.get("policy") or {}).get("policy")
        if isinstance(parity.get("policy"), dict)
        else parity.get("policy"),
        "signals_compared": parity.get("signals_compared"),
        "samples": parity.get("samples"),
        "common_window_s": parity.get("common_window_s"),
        "max_rmse_v": parity.get("max_rmse_v"),
        "max_abs_v": parity.get("max_abs_v"),
        "mean_relative_rms_error": parity.get("mean_relative_rms_error"),
        "max_relative_rms_error": parity.get("max_relative_rms_error"),
        "raw_max_rmse_v": parity.get("raw_max_rmse_v"),
        "raw_max_abs_v": parity.get("raw_max_abs_v"),
        "raw_mean_relative_rms_error": parity.get("raw_mean_relative_rms_error"),
        "raw_max_relative_rms_error": parity.get("raw_max_relative_rms_error"),
        "evas_wall_time_s": timing.get("evas_wall_time_s"),
        "spectre_wall_time_s": timing.get("spectre_wall_time_s"),
        "combined_wall_time_s": timing.get("combined_wall_time_s"),
        "row_wall_time_s": row.get("wall_time_s"),
        "staged_task_dir": row.get("staged_task_dir"),
        "result_root": row.get("result_root"),
    }


def result_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in summary.get("results", [])
        if isinstance(row, dict)
        and row.get("variant") == "gold"
        and row.get("expected_result") == "pass"
    ]
    rows.sort(key=lambda item: (str(item.get("entry_id")), str(item.get("form"))))
    return rows


def validate_summary(summary: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    if len(rows) != EXPECTED_V11_ROWS:
        failures.append({"scope": "summary", "reason": f"expected {EXPECTED_V11_ROWS} rows, got {len(rows)}"})
    if summary.get("status") != "complete":
        failures.append({"scope": "summary", "reason": f"summary status is {summary.get('status')}"})
    for row in rows:
        raw = row.get("raw_result") if isinstance(row.get("raw_result"), dict) else {}
        evas = raw.get("evas") if isinstance(raw.get("evas"), dict) else {}
        spectre = raw.get("spectre") if isinstance(raw.get("spectre"), dict) else {}
        parity = raw.get("parity") if isinstance(raw.get("parity"), dict) else {}
        row_failures: list[str] = []
        if row.get("expected_result_met") is not True:
            row_failures.append("expected_result_met is not true")
        if raw.get("status") != "PASS":
            row_failures.append(f"raw status is {raw.get('status')}")
        if evas.get("status") != "PASS":
            row_failures.append(f"EVAS status is {evas.get('status')}")
        if spectre.get("ok") is not True:
            row_failures.append("Spectre ok is not true")
        if as_float(spectre.get("behavior_score")) != 1.0:
            row_failures.append(f"Spectre behavior_score is {spectre.get('behavior_score')}")
        if parity.get("status") != "passed":
            row_failures.append(f"parity status is {parity.get('status')}")
        if row_failures:
            failures.append(
                {
                    "task": f"{row.get('entry_id')}:{row.get('form')}",
                    "reasons": row_failures,
                }
            )
    return failures


def update_release_task(task_manifest: Path, report_rel: str) -> None:
    payload = read_json(task_manifest)
    certification = payload.setdefault("certification", {})
    if not isinstance(certification, dict):
        certification = {}
        payload["certification"] = certification
    certification.update(
        {
            "static": "pass",
            "evas": "pass",
            "spectre": "pass",
            "evidence": report_rel,
            "fresh_spectre_evidence": report_rel,
            "task_specific_quality_evidence": TASK_SPECIFIC_EVIDENCE,
            "paper_score_status": PAPER_SCORE_PENDING,
        }
    )
    counts = payload.setdefault("counts", {})
    if isinstance(counts, dict):
        counts["benchmark_score"] = False
    notes = payload.setdefault("notes", [])
    if isinstance(notes, list):
        note = "Fresh EVAS/Spectre rerun passed; row remains outside paper score until score-denominator admission."
        if note not in notes:
            notes.append(note)
    write_json(task_manifest, payload)


def update_release_entries(manifest_rows: list[dict[str, Any]], report_rel: str) -> None:
    by_entry: dict[Path, list[dict[str, Any]]] = defaultdict(list)
    for row in manifest_rows:
        task_manifest = ROOT / str(row["release_task_manifest"])
        by_entry[task_manifest.parent.parent.parent / "release_entry.json"].append(row)

    for entry_path, rows in sorted(by_entry.items(), key=lambda item: str(item[0])):
        entry = read_json(entry_path)
        entry["package_status"] = "v1.1_fresh_spectre_certified_score_pending"
        certification = entry.setdefault("certification", {})
        if not isinstance(certification, dict):
            certification = {}
            entry["certification"] = certification
        certification.update(
            {
                "static": "pass",
                "evas": "pass",
                "spectre": "pass",
                "evidence": report_rel,
                "fresh_spectre_evidence": report_rel,
                "task_specific_quality_evidence": TASK_SPECIFIC_EVIDENCE,
                "paper_score_status": PAPER_SCORE_PENDING,
            }
        )
        counts = entry.setdefault("counts", {})
        if isinstance(counts, dict):
            counts["benchmark_score"] = False
        entry["release_blockers"] = ["score_denominator_admission_pending_after_certification"]
        forms = {str(row["form"]) for row in rows}
        release_tasks = entry.get("release_tasks", [])
        if isinstance(release_tasks, list):
            for release_task in release_tasks:
                if not isinstance(release_task, dict) or str(release_task.get("form")) not in forms:
                    continue
                release_task["evas_status"] = "pass"
                release_task["spectre_status"] = "pass"
                release_task["fresh_spectre_evidence"] = report_rel
        write_json(entry_path, entry)


def write_expansion_readme(report_rel: str) -> None:
    lines = [
        "# vaBench 300 Expansion Manifest",
        "",
        "- tasks: 300",
        "- existing certified v1 tasks: 271",
        "- task-specific v1.1 tasks: 29",
        "- paper-score-ready tasks: 271",
        "- simulator-certified benchmark tasks: 300",
        "- fresh Spectre-certified v1.1 tasks: 29",
        "- score-denominator-pending v1.1 tasks: 29",
        "- negatives per task: 5",
        "- total partial-pass negatives: 1500",
        "- static shallow-shape verified negatives after audit: 1500",
        "- simulator shallow-lane verified negatives: recorded by `v11_task_specific_quality_evidence.json`",
        "- full-checker fail verified negatives: recorded by `v11_task_specific_quality_evidence.json`",
        "",
        "Certification boundary: the 29 v1.1 rows now have task-specific prompts, gold implementations, checker IDs, near-miss negatives, local EVAS quality evidence, and fresh EVAS/Spectre PASS evidence. They remain outside the paper score denominator until score-denominator admission is explicitly enabled.",
        "",
        "## Purpose",
        "",
        "This directory is the primary vaBench 300 management surface. It indexes 271 inherited certified v1 form-level rows plus 29 task-specific v1.1 rows. Use 300 as the asset-management and simulator-certification surface; use 271 as the current paper-score-ready surface until v1.1 denominator admission is complete.",
        "",
        f"`{report_rel}` records the compact fresh Spectre rerun import for the 29 v1.1 rows. Raw simulator outputs are intentionally not versioned.",
        "",
        "Every task has a partial-pass negative manifest with five near-miss candidates. For v1.1 rows, the negatives are generated from task-specific variants intended to compile and run while failing the registered full checker.",
        "",
        "## Files",
        "",
        "- `VABENCH_300_MANIFEST.json`: the 300-task index.",
        "- `v11_task_specific_quality_evidence.json`: EVAS gold/negative quality evidence for v1.1 rows.",
        f"- `{report_rel}`: compact fresh Spectre rerun evidence for v1.1 rows.",
        "- `negative_audit.json`: asset/hash/count audit for all negative manifests.",
        "- `existing-negatives/`: five negative candidates for each existing certified v1 task.",
        "- `proposed-tasks/`: the 29 v1.1 task assets, including prompt, checks, gold, release task manifests, and negatives.",
        "",
        "## Schemas",
        "",
        "- `../../schemas/vabench-300-expansion-manifest.schema.json`",
        "- `../../schemas/vabench-partial-pass-negatives.schema.json`",
        "",
        "## Commands",
        "",
        "Regenerate the pre-import expansion package:",
        "",
        "```bash",
        "python3 runners/build_vabench_300_expansion.py",
        "```",
        "",
        "Reattach fresh v1.1 Spectre evidence after a rerun:",
        "",
        "```bash",
        "python3 runners/import_vabench_300_v11_spectre_rerun.py --summary /path/to/summary.json",
        "```",
        "",
        "Audit negative manifests:",
        "",
        "```bash",
        "python3 runners/audit_vabench_300_expansion.py",
        "```",
        "",
        "Run the focused tests:",
        "",
        "```bash",
        "PYTHONPATH=runners python3 -m pytest tests/test_vabench_300_expansion.py -q",
        "```",
        "",
    ]
    README.write_text("\n".join(lines), encoding="utf-8")


def update_manifest(report: dict[str, Any], compact_rows: list[dict[str, Any]]) -> None:
    manifest = read_json(MANIFEST)
    report_rel = rel(REPORT_JSON)
    by_task = {str(row["task_id"]): row for row in compact_rows}
    updated_rows: list[dict[str, Any]] = []
    for row in manifest.get("tasks", []):
        if not isinstance(row, dict):
            continue
        is_v11 = row.get("expansion_status") in {PROVISIONAL_STATUS, CERTIFIED_STATUS} or str(
            row.get("legacy_entry_id", "")
        ).startswith("vbr11")
        if not is_v11:
            continue
        compact = by_task.get(str(row.get("task_id")))
        if compact is None:
            continue
        row.update(
            {
                "static": "pass",
                "evas": "pass",
                "spectre": "pass",
                "certification": FRESH_CERTIFICATION,
                "expansion_status": CERTIFIED_STATUS,
                "gold_status": "promoted_certified",
                "counted_in_score": False,
                "fresh_spectre_evidence": report_rel,
                "fresh_spectre_parity_status": compact.get("parity_status"),
                "fresh_spectre_max_rmse_v": compact.get("max_rmse_v"),
                "fresh_spectre_max_abs_v": compact.get("max_abs_v"),
                "fresh_spectre_mean_relative_rms_error": compact.get("mean_relative_rms_error"),
                "fresh_spectre_max_relative_rms_error": compact.get("max_relative_rms_error"),
                "paper_score_status": PAPER_SCORE_PENDING,
            }
        )
        update_release_task(ROOT / str(row["release_task_manifest"]), report_rel)
        updated_rows.append(row)

    if len(updated_rows) != EXPECTED_V11_ROWS:
        raise AssertionError(f"expected to update {EXPECTED_V11_ROWS} v1.1 rows, updated {len(updated_rows)}")

    summary = manifest.setdefault("summary", {})
    if not isinstance(summary, dict):
        summary = {}
        manifest["summary"] = summary
    existing_count = int(summary.get("existing_certified_v1_task_count", 271))
    v11_count = len(updated_rows)
    summary.update(
        {
            "certified_task_count": existing_count + v11_count,
            "pending_certification_task_count": 0,
            "promoted_v11_task_count": v11_count,
            "provisional_v11_task_count": 0,
            "fresh_spectre_v11_pass_count": v11_count,
            "fresh_spectre_v11_nonpass_count": 0,
            "fresh_spectre_v11_parity_pass_count": v11_count,
            "score_denominator_pending_v11_task_count": v11_count,
            "paper_score_ready_task_count": existing_count,
            "paper_score_disabled_v11_task_count": v11_count,
        }
    )
    manifest["status"] = "management_surface_with_v11_fresh_spectre_certified_score_pending"
    manifest["v11_fresh_spectre_rerun_evidence"] = report_rel
    manifest["claim_boundary"] = [
        "This expansion manifest materializes the 300-task and 1500-negative asset plan.",
        "The 271 inherited v1 rows remain the only current paper-score-ready rows in this 300-task management surface.",
        "The 29 v1.1 rows have task-specific prompts, gold implementations, checkers, near-miss negatives, and fresh EVAS/Spectre PASS evidence.",
        "The 29 v1.1 rows remain outside the paper score denominator until score-denominator admission is explicitly enabled.",
        f"Fresh v1.1 Spectre evidence: {report_rel}.",
        f"Task-specific EVAS quality evidence: {TASK_SPECIFIC_EVIDENCE}.",
    ]
    update_release_entries(updated_rows, report_rel)
    write_json(MANIFEST, manifest)
    write_expansion_readme(report_rel)


def write_markdown(report: dict[str, Any]) -> None:
    rows = report["rows"]
    counts = report["summary"]
    lines = [
        "# vaBench 300 v1.1 Fresh Spectre Rerun",
        "",
        f"- date: `{report['date']}`",
        f"- status: `{report['status']}`",
        f"- source summary sha256: `{report['source_summary_sha256']}`",
        f"- rows: {counts['task_count']}",
        f"- PASS: {counts['pass_count']}",
        f"- non-PASS: {counts['nonpass_count']}",
        f"- parity passed: {counts['parity_pass_count']}",
        f"- EVAS PASS / Spectre FAIL: {counts['evas_pass_spectre_fail_count']}",
        f"- total wall time: {counts['total_wall_time_s']} s",
        "",
        "This report imports compact evidence from the fresh v1.1 EVAS/Spectre rerun.",
        "Raw simulator directories remain outside the repository; this file is the versioned certification summary.",
        "Score-denominator admission is tracked separately in `benchmark-vabench-release-v1/reports/vabench_300_v11_score_admission.json`.",
        "",
        "## Rows",
        "",
        "| Task | Raw | EVAS | Spectre | Parity | max RMSE V | max abs V | Evidence timing |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['task_id']}`",
                    f"`{row['raw_status']}`",
                    f"`{row['evas_status']}`",
                    "`PASS`" if row["spectre_ok"] else "`FAIL`",
                    f"`{row['parity_status']}`",
                    str(row.get("max_rmse_v")),
                    str(row.get("max_abs_v")),
                    str(row.get("combined_wall_time_s")),
                ]
            )
            + " |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_report(summary_path: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    compact_rows = [compact_result_row(row) for row in rows]
    raw_counts = Counter(str(row.get("raw_status")) for row in compact_rows)
    form_counts = Counter(str(row.get("form")) for row in compact_rows)
    parity_pass = sum(1 for row in compact_rows if row.get("parity_status") == "passed")
    evas_pass_spectre_fail = sum(
        1
        for row in compact_rows
        if row.get("evas_status") == "PASS" and row.get("spectre_ok") is not True
    )
    failures = validate_summary(summary, rows)
    return {
        "date": str(date.today()),
        "status": "pass" if not failures else "fail",
        "source_summary_path": str(summary_path),
        "source_summary_sha256": sha256(summary_path),
        "source_summary_started_at": summary.get("started_at"),
        "source_summary_finished_at": summary.get("finished_at"),
        "bridge_preflight": summary.get("bridge_preflight"),
        "spectre_backend": summary.get("spectre_backend"),
        "spectre_mode": summary.get("spectre_mode"),
        "workers": summary.get("workers"),
        "vabench_300_manifest_status_at_run": summary.get("vabench_300_manifest_status"),
        "summary": {
            "task_count": len(compact_rows),
            "pass_count": int(summary.get("pass_count", 0)),
            "nonpass_count": int(summary.get("nonpass_count", 0)),
            "expected_met_count": int(summary.get("expected_met_count", 0)),
            "expected_miss_count": int(summary.get("expected_miss_count", 0)),
            "parity_pass_count": parity_pass,
            "evas_pass_spectre_fail_count": evas_pass_spectre_fail,
            "raw_status_counts": dict(sorted(raw_counts.items())),
            "form_counts": dict(sorted(form_counts.items())),
            "selected_expansion_status_counts": summary.get("selected_expansion_status_counts", {}),
            "selected_form_counts": summary.get("selected_form_counts", {}),
            "total_wall_time_s": summary.get("total_wall_time_s"),
        },
        "validation_failures": failures,
        "rows": compact_rows,
        "claim_boundary": [
            "This report certifies fresh EVAS/Spectre behavior for the 29 task-specific v1.1 rows only.",
            "It does not admit v1.1 rows into the paper score denominator.",
            "Spectre remains the final judge; every imported row has Spectre ok=true, behavior_score=1.0, and parity status=passed.",
            "Raw simulator outputs are intentionally not committed; the source summary hash anchors the imported evidence.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Import fresh Spectre rerun evidence for vaBench 300 v1.1 rows.")
    parser.add_argument("--summary", required=True, help="Path to run_vabench_300_dual_rerun.py summary.json")
    args = parser.parse_args()

    summary_path = Path(args.summary).expanduser().resolve()
    summary = read_json(summary_path)
    rows = result_rows(summary)
    report = build_report(summary_path, summary, rows)
    if report["status"] != "pass":
        write_json(REPORT_JSON, report)
        write_markdown(report)
        print(json.dumps({"status": "fail", "validation_failures": report["validation_failures"]}, indent=2))
        return 1

    write_json(REPORT_JSON, report)
    write_markdown(report)
    update_manifest(report, report["rows"])
    print(
        json.dumps(
            {
                "status": report["status"],
                "report": rel(REPORT_JSON),
                "task_count": report["summary"]["task_count"],
                "pass_count": report["summary"]["pass_count"],
                "parity_pass_count": report["summary"]["parity_pass_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
