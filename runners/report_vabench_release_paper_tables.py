#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
TABLES_ROOT = REPORTS_ROOT / "paper_tables"
REPORT_JSON = REPORTS_ROOT / "paper_tables.json"
REPORT_MD = REPORTS_ROOT / "paper_tables.md"
SUPPORT_CATEGORIES = {"Measurement Instrumentation Flows", "Stimulus and Source Generators"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def csv_value(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def claim_lookup(claim_gate: dict[str, object]) -> dict[str, dict[str, object]]:
    claims = claim_gate.get("claims", [])
    if not isinstance(claims, list):
        return {}
    return {
        str(item.get("id")): item
        for item in claims
        if isinstance(item, dict) and item.get("id")
    }


def list_join(values: object) -> str:
    if isinstance(values, list):
        return "; ".join(str(value) for value in values)
    return str(values or "")


def metric_row(
    *,
    table_id: str,
    metric: str,
    value: object,
    scope: str,
    claim_status: str,
    evidence: str,
    safe_caption_note: str,
) -> dict[str, object]:
    return {
        "table_id": table_id,
        "metric": metric,
        "value": value,
        "scope": scope,
        "claim_status": claim_status,
        "evidence": evidence,
        "safe_caption_note": safe_caption_note,
    }


def build_report() -> dict[str, object]:
    paper = read_json(REPORTS_ROOT / "paper_artifacts.json")
    claim_gate = read_json(REPORTS_ROOT / "claim_gate.json")
    certification = read_json(REPORTS_ROOT / "certification_matrix.json")
    external = read_json(REPORTS_ROOT / "external_blockers.json")
    speed = read_json(REPORTS_ROOT / "speed_debug_artifact.json")
    baseline = read_json(REPORTS_ROOT / "baseline_artifact.json")
    score = read_json(REPORTS_ROOT / "score_denominator_manifest.json")

    coverage = paper.get("coverage_summary", {})
    parity = paper.get("parity_summary", {})
    gap = paper.get("certification_gap_summary", {})
    if not isinstance(coverage, dict):
        coverage = {}
    if not isinstance(parity, dict):
        parity = {}
    if not isinstance(gap, dict):
        gap = {}
    score_claim_rule = score.get("claim_rule", {})
    if not isinstance(score_claim_rule, dict):
        score_claim_rule = {}
    matrix_summary = certification.get("summary", {})
    if not isinstance(matrix_summary, dict):
        matrix_summary = {}
    claims = claim_lookup(claim_gate)
    full_dual_certified = (
        as_int(parity.get("dual_pending_release_task_count", 0)) == 0
        and as_int(parity.get("dual_failed_release_task_count", 0)) == 0
    )
    category_counts = coverage.get("category_counts", {})
    if not isinstance(category_counts, dict):
        category_counts = {}
    support_entry_count = sum(as_int(category_counts.get(category)) for category in SUPPORT_CATEGORIES)
    core_entry_count = as_int(coverage.get("planned_entries", 0)) - support_entry_count

    coverage_rows = [
        metric_row(
            table_id="coverage",
            metric="planned_l1_l2_entries",
            value=coverage.get("planned_entries", 0),
            scope="coverage target",
            claim_status=str(claims.get("C1_coverage_target_defined", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "release_status.json"),
            safe_caption_note="Coverage target only; split core circuit coverage from measurement/stimulus support; not a scored denominator.",
        ),
        metric_row(
            table_id="coverage",
            metric="core_circuit_entries",
            value=core_entry_count,
            scope="core coverage target",
            claim_status=str(claims.get("C1_coverage_target_defined", {}).get("status", "missing")),
            evidence=rel(ROOT / "docs" / "VABENCH_LEVEL_COVERAGE_TABLE.md"),
            safe_caption_note="Core analog/mixed-signal circuit-function entries; excludes measurement and stimulus/source support categories.",
        ),
        metric_row(
            table_id="coverage",
            metric="support_measurement_stimulus_entries",
            value=support_entry_count,
            scope="support coverage target",
            claim_status=str(claims.get("C1_coverage_target_defined", {}).get("status", "missing")),
            evidence=rel(ROOT / "docs" / "VABENCH_LEVEL_COVERAGE_TABLE.md"),
            safe_caption_note="Auxiliary measurement, instrumentation, and stimulus/source entries; report separately from core circuit coverage.",
        ),
        metric_row(
            table_id="coverage",
            metric="l1_entries",
            value=coverage.get("level_counts", {}).get("L1", 0) if isinstance(coverage.get("level_counts"), dict) else 0,
            scope="coverage target",
            claim_status=str(claims.get("C1_coverage_target_defined", {}).get("status", "missing")),
            evidence=rel(ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"),
            safe_caption_note="L1 coverage count from the tracker.",
        ),
        metric_row(
            table_id="coverage",
            metric="l2_entries",
            value=coverage.get("level_counts", {}).get("L2", 0) if isinstance(coverage.get("level_counts"), dict) else 0,
            scope="coverage target",
            claim_status=str(claims.get("C1_coverage_target_defined", {}).get("status", "missing")),
            evidence=rel(ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"),
            safe_caption_note="L2 coverage count from the tracker.",
        ),
        metric_row(
            table_id="coverage",
            metric="source_linked_entries",
            value=coverage.get("source_linked_entry_count", 0),
            scope="source package",
            claim_status=str(claims.get("C2_source_assets_static_clean", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "release_status.json"),
            safe_caption_note="Materialization state, not simulator certification.",
        ),
        metric_row(
            table_id="coverage",
            metric="asset_materialized_entries",
            value=coverage.get("asset_materialized_entry_count", 0),
            scope="source package",
            claim_status=str(claims.get("C2_source_assets_static_clean", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "asset_integrity.json"),
            safe_caption_note="Prompt/meta/checks/gold assets are present.",
        ),
        metric_row(
            table_id="coverage",
            metric="static_certified_forms",
            value=coverage.get("static_certified_release_task_count", 0),
            scope="static checks",
            claim_status=str(claims.get("C2_source_assets_static_clean", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "static_certification.json"),
            safe_caption_note="Static certification is separate from EVAS/Spectre parity.",
        ),
        metric_row(
            table_id="coverage",
            metric="scored_entries",
            value=coverage.get("scored_release_entries", 0),
            scope="score denominator",
            claim_status=str(claims.get("C5_score_denominator_enabled", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            safe_caption_note="Score denominator contains certified content-denominator rows; content-excluded duplicates are not counted.",
        ),
    ]

    parity_rows = [
        metric_row(
            table_id="parity",
            metric="dual_certified_release_forms",
            value=parity.get("dual_certified_release_task_count", 0),
            scope="full certified release" if full_dual_certified else "imported certified subset",
            claim_status=str(claims.get("C3_imported_dual_subset_clean", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "dual_certification.json"),
            safe_caption_note=(
                "Full release dual certification evidence; score/speed/baseline claims are still separate."
                if full_dual_certified
                else "Subset evidence only; do not phrase as full release certification."
            ),
        ),
        metric_row(
            table_id="parity",
            metric="fully_certified_entries",
            value=coverage.get("fully_certified_entry_count", 0),
            scope="full certified release" if full_dual_certified else "imported certified subset",
            claim_status=str(claims.get("C3_imported_dual_subset_clean", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "dual_certification.json"),
            safe_caption_note="Entry-level certification from imported evidence.",
        ),
        metric_row(
            table_id="parity",
            metric="evas_pass_spectre_fail_count",
            value=parity.get("evas_pass_spectre_fail_count", 0),
            scope="full certified release" if full_dual_certified else "imported certified subset",
            claim_status=str(claims.get("C3_imported_dual_subset_clean", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "dual_certification.json"),
            safe_caption_note="Zero mismatch applies to the certified release forms.",
        ),
        metric_row(
            table_id="parity",
            metric="dual_pending_release_forms",
            value=parity.get("dual_pending_release_task_count", 0),
            scope="fresh full-release rerun",
            claim_status=str(claims.get("C4_full_release_dual_certified", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "certification_matrix.json"),
            safe_caption_note="Pending forms block full release certification when nonzero.",
        ),
        metric_row(
            table_id="parity",
            metric="fresh_rerun_queue_rows",
            value=gap.get("fresh_dual_rerun_queue_count", 0),
            scope="fresh full-release rerun",
            claim_status=str(claims.get("C4_full_release_dual_certified", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "dual_rerun_queue.json"),
            safe_caption_note="Queue readiness is execution planning, not pass evidence.",
        ),
        metric_row(
            table_id="parity",
            metric="ready_rerun_bundles",
            value=gap.get("fresh_dual_rerun_ready_bundle_count", 0),
            scope="fresh full-release rerun",
            claim_status=str(claims.get("C4_full_release_dual_certified", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "dual_rerun_staging_manifest.json"),
            safe_caption_note="Staged bundles are runnable when the bridge is reachable.",
        ),
        metric_row(
            table_id="parity",
            metric="bridge_status",
            value=parity.get("bridge_diagnostics_status", "missing"),
            scope="external bridge diagnostics",
            claim_status=str(claims.get("C4_full_release_dual_certified", {}).get("status", "missing")),
            evidence=rel(REPORTS_ROOT / "bridge_profile_diagnostics.json"),
            safe_caption_note=(
                "Current bridge reachability is not part of already imported full release certification."
                if full_dual_certified
                else "Bridge status explains why fresh Spectre evidence is pending."
            ),
        ),
        metric_row(
            table_id="parity",
            metric="main120_gold_evas_pass",
            value=f"{parity.get('main120_gold_evas', {}).get('pass_count', 0)}/{parity.get('main120_gold_evas', {}).get('total_tasks', 0)}"
            if isinstance(parity.get("main120_gold_evas"), dict)
            else "0/0",
            scope="historical supporting evidence",
            claim_status="supporting_only",
            evidence=str(parity.get("main120_gold_evas", {}).get("source", "")) if isinstance(parity.get("main120_gold_evas"), dict) else "",
            safe_caption_note="Historical main120 evidence supports development history, not the release denominator.",
        ),
        metric_row(
            table_id="parity",
            metric="main120_gold_spectre_pass",
            value=f"{parity.get('main120_gold_spectre', {}).get('pass_count', 0)}/{parity.get('main120_gold_spectre', {}).get('total_tasks', 0)}"
            if isinstance(parity.get("main120_gold_spectre"), dict)
            else "0/0",
            scope="historical supporting evidence",
            claim_status="supporting_only",
            evidence=str(parity.get("main120_gold_spectre", {}).get("source", "")) if isinstance(parity.get("main120_gold_spectre"), dict) else "",
            safe_caption_note="Historical main120 evidence supports development history, not the release denominator.",
        ),
    ]

    claim_rows = [
        {
            "claim_id": item.get("id", ""),
            "status": item.get("status", "missing"),
            "completion_required": item.get("completion_required", False),
            "safe_wording": item.get("safe_wording", ""),
            "blocked_until": list_join(item.get("required_before_allowed", [])),
            "evidence": list_join(item.get("evidence", [])),
        }
        for item in claim_gate.get("claims", [])
        if isinstance(item, dict)
    ]

    blockers = external.get("blockers", [])
    if not isinstance(blockers, list):
        blockers = []
    blocker_rows = [
        {
            "blocker_id": item.get("id", ""),
            "status": item.get("status", "missing"),
            "scope": item.get("scope", ""),
            "diagnosis": item.get("diagnosis", ""),
            "claim_impact": list_join(item.get("claim_impact", [])),
            "stop_condition": item.get("stop_condition", ""),
            "evidence": list_join(item.get("evidence", [])),
        }
        for item in blockers
        if isinstance(item, dict)
    ]

    speed_baseline_rows = [
        {
            "artifact": "speed_debug",
            "status": speed.get("status", "missing"),
            "claim_allowed": speed.get("claim_allowed", False),
            "claim_status": str(claims.get("C6_speed_debug_claim", {}).get("status", "missing")),
            "current_value": speed.get("reason", ""),
            "required_before_claim": list_join(speed.get("required_to_claim", [])),
            "evidence": rel(REPORTS_ROOT / "speed_debug_artifact.json"),
        },
        {
            "artifact": "baseline",
            "status": baseline.get("status", "missing"),
            "claim_allowed": baseline.get("claim_allowed", False),
            "claim_status": str(claims.get("C7_model_baseline_claim", {}).get("status", "missing")),
            "current_value": f"summaries={baseline.get('baseline_summary_count', 0)}; scored_entries={baseline.get('scored_release_entries', 0)}",
            "required_before_claim": list_join(baseline.get("required_to_claim", [])),
            "evidence": rel(REPORTS_ROOT / "baseline_artifact.json"),
        },
        {
            "artifact": "score_denominator",
            "status": score.get("status", "missing"),
            "claim_allowed": bool(score_claim_rule.get("score_claim_allowed", False)),
            "claim_status": str(claims.get("C5_score_denominator_enabled", {}).get("status", "missing")),
            "current_value": f"scored_forms={score.get('summary', {}).get('scored_form_count', 0) if isinstance(score.get('summary'), dict) else 0}",
            "required_before_claim": "benchmark_score must be explicitly enabled for counted entries/forms",
            "evidence": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
        },
    ]

    tables = [
        {
            "id": "coverage",
            "title": "vaBench release coverage and materialization status",
            "csv": rel(TABLES_ROOT / "coverage.csv"),
            "row_count": len(coverage_rows),
            "caption": "Coverage/materialization status for the 79-entry L1/L2 release target, split into core circuit coverage and measurement/stimulus support; score denominator claims are governed by the score denominator manifest.",
        },
        {
            "id": "parity",
            "title": "EVAS/Spectre parity and rerun status",
            "csv": rel(TABLES_ROOT / "parity.csv"),
            "row_count": len(parity_rows),
            "caption": "EVAS/Spectre parity status for certified release forms; score, speed/debug, and model baselines are separate gates.",
        },
        {
            "id": "claim_gate",
            "title": "Allowed and blocked paper claims",
            "csv": rel(TABLES_ROOT / "claim_gate.csv"),
            "row_count": len(claim_rows),
            "caption": "Use only safe_wording for allowed claims; blocked claims must not be used as conclusions.",
        },
        {
            "id": "external_blockers",
            "title": "External blockers and stop conditions",
            "csv": rel(TABLES_ROOT / "external_blockers.csv"),
            "row_count": len(blocker_rows),
            "caption": "External blockers explain unavailable fresh Spectre evidence; they are not certification evidence.",
        },
        {
            "id": "speed_baseline",
            "title": "Speed/debug, scoring, and baseline gates",
            "csv": rel(TABLES_ROOT / "speed_baseline.csv"),
            "row_count": len(speed_baseline_rows),
            "caption": "Speed/debug and baseline results are pending until the score denominator is enabled and same-slice evidence exists.",
        },
    ]

    write_csv(TABLES_ROOT / "coverage.csv", coverage_rows, list(coverage_rows[0]))
    write_csv(TABLES_ROOT / "parity.csv", parity_rows, list(parity_rows[0]))
    write_csv(TABLES_ROOT / "claim_gate.csv", claim_rows, list(claim_rows[0]) if claim_rows else ["claim_id"])
    write_csv(TABLES_ROOT / "external_blockers.csv", blocker_rows, list(blocker_rows[0]) if blocker_rows else ["blocker_id"])
    write_csv(TABLES_ROOT / "speed_baseline.csv", speed_baseline_rows, list(speed_baseline_rows[0]))

    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "in_progress" if claim_gate.get("status") != "complete" else "ready",
        "table_count": len(tables),
        "tables": tables,
        "source_reports": {
            "paper_artifacts": rel(REPORTS_ROOT / "paper_artifacts.json"),
            "claim_gate": rel(REPORTS_ROOT / "claim_gate.json"),
            "certification_matrix": rel(REPORTS_ROOT / "certification_matrix.json"),
            "external_blockers": rel(REPORTS_ROOT / "external_blockers.json"),
            "speed_debug_artifact": rel(REPORTS_ROOT / "speed_debug_artifact.json"),
            "baseline_artifact": rel(REPORTS_ROOT / "baseline_artifact.json"),
            "score_denominator_manifest": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
        },
        "table_rows": {
            "coverage": coverage_rows,
            "parity": parity_rows,
            "claim_gate": claim_rows,
            "external_blockers": blocker_rows,
            "speed_baseline": speed_baseline_rows,
        },
        "claim_boundary": [
            "These tables are presentation artifacts; they do not create new certification evidence.",
            "Parity rows must be captioned according to whether they cover the full release or only an imported subset.",
            "Rows with blocked claim_status must not be used as paper conclusions.",
        ],
        "matrix_summary_snapshot": {
            "entry_count": matrix_summary.get("entry_count", 0),
            "form_count": matrix_summary.get("form_count", 0),
            "fully_certified_entry_count": matrix_summary.get("fully_certified_entry_count", 0),
            "pending_form_count": matrix_summary.get("pending_form_count", 0),
        },
    }


def md_table(rows: Iterable[dict[str, object]], fields: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(csv_value(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return lines


def write_markdown(report: dict[str, object]) -> None:
    rows = report["table_rows"]
    lines = [
        "# vaBench Release Paper Tables",
        "",
        f"Date: {report['date']}",
        "",
        "These tables are generated from the release reports and claim gate. They",
        "are designed for paper drafting without turning pending evidence into",
        "claims.",
        "",
        "## Table Inventory",
        "",
        "| ID | Rows | CSV | Caption |",
        "| --- | ---: | --- | --- |",
    ]
    for table in report["tables"]:
        lines.append(f"| `{table['id']}` | {table['row_count']} | `{table['csv']}` | {table['caption']} |")
    lines.extend(["", "## Coverage", ""])
    lines.extend(md_table(rows["coverage"], ["metric", "value", "scope", "claim_status"]))
    lines.extend(["", "## Parity", ""])
    lines.extend(md_table(rows["parity"], ["metric", "value", "scope", "claim_status"]))
    lines.extend(["", "## Claims", ""])
    lines.extend(md_table(rows["claim_gate"], ["claim_id", "status", "completion_required", "safe_wording"]))
    lines.extend(["", "## External Blockers", ""])
    lines.extend(md_table(rows["external_blockers"], ["blocker_id", "status", "scope", "stop_condition"]))
    lines.extend(["", "## Speed / Baseline", ""])
    lines.extend(md_table(rows["speed_baseline"], ["artifact", "status", "claim_allowed", "claim_status"]))
    lines.extend(["", "## Claim Boundary", ""])
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote paper tables: status={status}; tables={tables}".format(
            status=report["status"],
            tables=report["table_count"],
        )
    )


if __name__ == "__main__":
    main()
