#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "claim_gate.json"
REPORT_MD = REPORTS_ROOT / "claim_gate.md"


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


def claim(
    *,
    claim_id: str,
    allowed: bool,
    claim_text: str,
    safe_wording: str,
    unsafe_wording: list[str],
    evidence: list[str],
    required_before_allowed: list[str],
    numbers: dict[str, object] | None = None,
    completion_required: bool = False,
    notes: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": claim_id,
        "status": "allowed" if allowed else "blocked",
        "allowed": allowed,
        "completion_required": completion_required,
        "claim_text": claim_text,
        "safe_wording": safe_wording,
        "unsafe_wording": unsafe_wording,
        "evidence": evidence,
        "required_before_allowed": required_before_allowed,
        "numbers": numbers or {},
        "notes": notes or [],
    }


def build_report() -> dict[str, object]:
    release_status = read_json(REPORTS_ROOT / "release_status.json")
    asset = read_json(REPORTS_ROOT / "asset_integrity.json")
    static = read_json(REPORTS_ROOT / "static_certification.json")
    dual = read_json(REPORTS_ROOT / "dual_certification.json")
    certification_matrix = read_json(REPORTS_ROOT / "certification_matrix.json")
    conformance = read_json(REPORTS_ROOT / "conformance_manifest.json")
    remaining = read_json(REPORTS_ROOT / "remaining_work.json")
    bridge = read_json(REPORTS_ROOT / "bridge_profile_diagnostics.json")
    external_blockers = read_json(REPORTS_ROOT / "external_blockers.json")
    paper = read_json(REPORTS_ROOT / "paper_artifacts.json")
    score = read_json(REPORTS_ROOT / "score_denominator_manifest.json")
    speed = read_json(REPORTS_ROOT / "speed_debug_artifact.json")
    baseline = read_json(REPORTS_ROOT / "baseline_artifact.json")

    score_summary = score.get("summary", {})
    if not isinstance(score_summary, dict):
        score_summary = {}
    score_claim_rule = score.get("claim_rule", {})
    if not isinstance(score_claim_rule, dict):
        score_claim_rule = {}
    paper_gates = paper.get("claim_gates", {})
    if not isinstance(paper_gates, dict):
        paper_gates = {}

    planned_entries = as_int(release_status.get("planned_entries"))
    source_linked_entries = as_int(release_status.get("source_linked_entry_count"))
    materialized_entries = as_int(release_status.get("asset_materialized_entry_count"))
    static_forms = as_int(static.get("static_certified_release_task_count"))
    dual_certified_forms = as_int(dual.get("dual_certified_release_task_count"))
    dual_pending_forms = as_int(dual.get("dual_pending_release_task_count"))
    dual_failed_forms = as_int(dual.get("dual_failed_release_task_count"))
    mismatch_forms = as_int(dual.get("evas_pass_spectre_fail_count"))
    scored_entries = as_int(release_status.get("scored_release_entries"))
    scored_forms = as_int(score_summary.get("scored_form_count"))
    source_pending = as_int(remaining.get("source_design_pending_entry_count"))
    missing_required = as_int(remaining.get("missing_required_form_entry_count"))
    rerun_pending = as_int(remaining.get("selected_rerun_pending_form_count"))
    source_equivalence_blocked = as_int(remaining.get("source_equivalence_blocked_form_count"))
    fresh_dual_rerun_queue_forms = as_int(remaining.get("fresh_dual_rerun_queue_form_count"))

    assets_static_clean = (
        planned_entries == 75
        and source_linked_entries == 75
        and materialized_entries == 75
        and asset.get("status") == "pass"
        and static.get("status") == "pass"
    )
    imported_dual_clean = dual_certified_forms > 0 and dual_failed_forms == 0 and mismatch_forms == 0
    full_dual_certified = (
        dual.get("status") == "pass"
        and dual_pending_forms == 0
        and dual_failed_forms == 0
        and mismatch_forms == 0
    )
    package_complete = (
        assets_static_clean
        and full_dual_certified
        and source_pending == 0
        and missing_required == 0
    )
    score_enabled = bool(score_claim_rule.get("score_claim_allowed", False)) and scored_entries > 0
    baseline_requirements = [
        *(["score denominator must be enabled"] if not score_enabled else []),
        *(
            ["baseline runs must report against counted release entries/forms only"]
            if not baseline.get("claim_allowed")
            else []
        ),
    ]

    claims = [
        claim(
            claim_id="C1_coverage_target_defined",
            allowed=planned_entries == 75,
            completion_required=True,
            claim_text="The release target defines a 75-entry L1/L2 vaBench coverage plan.",
            safe_wording="The current release package defines 75 planned L1/L2 entries; this is a coverage target, not a final scored benchmark result.",
            unsafe_wording=[
                "vaBench is fully certified because it has 75 rows.",
                "The 75-entry table alone proves benchmark correctness.",
            ],
            evidence=[rel(REPORTS_ROOT / "release_status.json"), rel(ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv")],
            required_before_allowed=[] if planned_entries == 75 else ["release_status.planned_entries must equal 75"],
            numbers={"planned_entries": planned_entries},
        ),
        claim(
            claim_id="C2_source_assets_static_clean",
            allowed=assets_static_clean,
            completion_required=True,
            claim_text="All release entries have materialized source-task assets and pass static checks.",
            safe_wording=f"The release has {materialized_entries}/75 materialized entries and {static_forms} static-certified forms with zero asset issues.",
            unsafe_wording=[
                "Static certification proves EVAS/Spectre behavioral parity.",
                "Asset materialization means the task is scored.",
            ],
            evidence=[
                rel(REPORTS_ROOT / "asset_integrity.json"),
                rel(REPORTS_ROOT / "static_certification.json"),
                rel(REPORTS_ROOT / "release_status.json"),
            ],
            required_before_allowed=[] if assets_static_clean else ["asset_integrity and static_certification must pass for all release forms"],
            numbers={
                "source_linked_entries": source_linked_entries,
                "materialized_entries": materialized_entries,
                "static_certified_forms": static_forms,
            },
        ),
        claim(
            claim_id="C3_imported_dual_subset_clean",
            allowed=imported_dual_clean,
            claim_text="The imported EVAS/Spectre evidence subset has no EVAS PASS / Spectre FAIL mismatch.",
            safe_wording=(
                f"On the full imported release evidence ({dual_certified_forms} forms), EVAS PASS / Spectre FAIL count is {mismatch_forms}."
                if full_dual_certified
                else f"On the imported certified subset ({dual_certified_forms} forms), EVAS PASS / Spectre FAIL count is {mismatch_forms}."
            ),
            unsafe_wording=[
                "Imported parity evidence enables benchmark scores by itself.",
                "Zero EVAS PASS / Spectre FAIL proves speedup or model baseline claims.",
            ],
            evidence=[
                rel(REPORTS_ROOT / "dual_certification.json"),
                rel(REPORTS_ROOT / "certification_matrix.json"),
            ],
            required_before_allowed=[] if imported_dual_clean else ["dual_certification must contain at least one clean imported form"],
            numbers={
                "dual_certified_forms": dual_certified_forms,
                "dual_pending_forms": dual_pending_forms,
                "dual_failed_forms": dual_failed_forms,
                "evas_pass_spectre_fail_count": mismatch_forms,
            },
            notes=[] if full_dual_certified else ["This is an imported-evidence subset claim only."],
        ),
        claim(
            claim_id="C4_full_release_dual_certified",
            allowed=full_dual_certified,
            completion_required=True,
            claim_text="The full release package is EVAS/Spectre certified.",
            safe_wording=(
                f"The full release package has EVAS/Spectre certification for {dual_certified_forms} forms with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches."
                if full_dual_certified
                else "This claim is blocked until every release form has current EVAS/Spectre evidence with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches."
            ),
            unsafe_wording=[
                "vaBench release is fully EVAS/Spectre certified.",
                "All release tasks pass Spectre and EVAS.",
            ],
            evidence=[
                rel(REPORTS_ROOT / "dual_certification.json"),
                rel(REPORTS_ROOT / "dual_rerun_queue.json"),
                rel(REPORTS_ROOT / "dual_rerun_import.json"),
                rel(REPORTS_ROOT / "bridge_profile_diagnostics.json"),
                rel(REPORTS_ROOT / "external_blockers.json"),
            ],
            required_before_allowed=[
                f"resolve {dual_pending_forms} dual-pending forms",
                (
                    f"complete fresh rerun for {fresh_dual_rerun_queue_forms} queued forms "
                    f"(includes {source_equivalence_blocked} historical source-equivalence blockers)"
                ),
                "bridge diagnostics must report a ready profile",
                "fresh dual rerun summary must import successfully",
            ]
            if not full_dual_certified
            else [],
            numbers={
                "dual_pending_forms": dual_pending_forms,
                "selected_rerun_pending_forms": rerun_pending,
                "source_equivalence_blocked_forms": source_equivalence_blocked,
                "fresh_dual_rerun_queue_forms": fresh_dual_rerun_queue_forms,
                "bridge_status": bridge.get("status", "missing"),
                "bridge_required_for_current_claim": not full_dual_certified,
                "external_blockers_status": external_blockers.get("status", "missing"),
            },
        ),
        claim(
            claim_id="C5_score_denominator_enabled",
            allowed=score_enabled,
            completion_required=True,
            claim_text="The release benchmark has an enabled score denominator.",
            safe_wording=(
                f"The release benchmark score denominator is enabled for {scored_entries} certified content-denominator entries and {scored_forms} forms."
                if score_enabled
                else "Benchmark scoring is disabled until full certification decides which entries/forms count."
            ),
            unsafe_wording=[
                "Current baseline percentages are release benchmark scores.",
                "The 75 planned entries are already the scored denominator.",
            ],
            evidence=[
                rel(REPORTS_ROOT / "score_denominator_manifest.json"),
                rel(REPORTS_ROOT / "release_status.json"),
            ],
            required_before_allowed=[
                "score_denominator_manifest must mark counted_in_score entries/forms",
            ]
            if not score_enabled
            else [],
            numbers={
                "score_denominator_status": score.get("status", "missing"),
                "scored_entries": scored_entries,
                "scored_forms": scored_forms,
            },
        ),
        claim(
            claim_id="C6_speed_debug_claim",
            allowed=bool(speed.get("claim_allowed")),
            completion_required=True,
            claim_text="EVAS has measured same-slice speed/debug advantages over Spectre on the release package.",
            safe_wording=(
                "Speed/debug has subset timing evidence, but release-wide speedup remains blocked until "
                "the dedicated artifact marks the speed claim allowed."
            ),
            unsafe_wording=[
                "EVAS is faster on vaBench-release-v1.",
                "EVAS debug advantage is proven by the current release artifacts.",
            ],
            evidence=[rel(REPORTS_ROOT / "speed_debug_artifact.json")],
            required_before_allowed=(
                list(speed.get("required_to_claim", []))
                if isinstance(speed.get("required_to_claim", []), list)
                and speed.get("required_to_claim", [])
                else ["speed_debug_artifact must mark claim_allowed=true"]
            ),
            numbers={
                "speed_status": speed.get("status", "missing"),
                "claim_allowed": speed.get("claim_allowed", False),
                "timed_rows": speed.get("measurement_scope", {}).get("timed_rows", "missing")
                if isinstance(speed.get("measurement_scope", {}), dict)
                else "missing",
                "timed_scored_forms": speed.get("measurement_scope", {}).get(
                    "timed_scored_form_count", "missing"
                )
                if isinstance(speed.get("measurement_scope", {}), dict)
                else "missing",
                "scored_forms": speed.get("measurement_scope", {}).get("scored_form_count", "missing")
                if isinstance(speed.get("measurement_scope", {}), dict)
                else "missing",
            },
        ),
        claim(
            claim_id="C7_model_baseline_claim",
            allowed=bool(baseline.get("claim_allowed")),
            completion_required=True,
            claim_text="Model baselines are scored on the clean vaBench release package.",
            safe_wording=(
                "Model baseline reporting is pending until baseline runs report against the enabled score denominator."
                if score_enabled
                else "Model baseline reporting is pending until a certified score denominator is enabled."
            ),
            unsafe_wording=[
                "The current unscored release rows support model baseline results.",
                "Historical candidate runs are release benchmark baselines.",
            ],
            evidence=[rel(REPORTS_ROOT / "baseline_artifact.json"), rel(REPORTS_ROOT / "score_denominator_manifest.json")],
            required_before_allowed=baseline_requirements,
            numbers={
                "baseline_status": baseline.get("status", "missing"),
                "baseline_claim_allowed": baseline.get("claim_allowed", False),
                "baseline_summary_count": baseline.get("baseline_summary_count", 0),
            },
        ),
        claim(
            claim_id="C8_l0_conformance_separate",
            allowed=conformance.get("benchmark_coverage_count") == 0,
            completion_required=True,
            claim_text="L0 EVAS/Spectre conformance cases are kept outside the L1/L2 benchmark denominator.",
            safe_wording=f"L0 conformance has {conformance.get('conformance_case_count', 0)} cases and contributes {conformance.get('benchmark_coverage_count', 'missing')} entries to benchmark coverage.",
            unsafe_wording=[
                "L0 conformance cases increase the 75-entry benchmark size.",
                "Conformance regressions are scored release tasks.",
            ],
            evidence=[rel(REPORTS_ROOT / "conformance_manifest.json")],
            required_before_allowed=[] if conformance.get("benchmark_coverage_count") == 0 else ["benchmark_coverage_count must be zero"],
            numbers={
                "conformance_case_count": conformance.get("conformance_case_count", 0),
                "benchmark_coverage_count": conformance.get("benchmark_coverage_count", "missing"),
            },
        ),
        claim(
            claim_id="C9_release_package_complete",
            allowed=package_complete,
            completion_required=True,
            claim_text="The clean vaBench release package is complete.",
            safe_wording=(
                "The clean vaBench release package structure, source assets, EVAS/Spectre certification, and score denominator are complete; speed/debug and model baselines remain separate gated claims."
                if package_complete
                else "The package structure and source assets are ready, but full completion remains blocked by fresh dual rerun, scoring, speed, and baseline gates."
            ),
            unsafe_wording=[
                "The release package is complete.",
                "The active goal is done.",
            ],
            evidence=[
                rel(REPORTS_ROOT / "completion_audit.json"),
                rel(REPORTS_ROOT / "paper_artifacts.json"),
                rel(REPORTS_ROOT / "external_blockers.json"),
            ],
            required_before_allowed=(
                []
                if package_complete
                else list(paper_gates.get("blocking_conditions", []))
                if isinstance(paper_gates.get("blocking_conditions", []), list)
                else ["all paper claim gates must clear"]
            ),
            numbers={
                "package_complete": package_complete,
                "source_design_pending_entries": source_pending,
                "missing_required_form_entries": missing_required,
                "dual_pending_forms": dual_pending_forms,
                "scored_entries": scored_entries,
            },
        ),
    ]

    blocked_claims = [item for item in claims if not item["allowed"]]
    required_claims = [item for item in claims if item["completion_required"]]
    blocked_required_claims = [item for item in required_claims if not item["allowed"]]
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "complete" if not blocked_required_claims else "in_progress",
        "claim_count": len(claims),
        "allowed_claim_count": sum(1 for item in claims if item["allowed"]),
        "blocked_claim_count": len(blocked_claims),
        "completion_required_claim_count": len(required_claims),
        "blocked_completion_required_claim_count": len(blocked_required_claims),
        "claims": claims,
        "blocked_claim_ids": [item["id"] for item in blocked_claims],
        "blocked_completion_required_claim_ids": [item["id"] for item in blocked_required_claims],
        "claim_policy": [
            "Allowed claims may be used only with their safe_wording scope.",
            "Blocked claims must not appear as paper conclusions, abstract claims, figure captions, or benchmark result text.",
            "Partial imported evidence must not be phrased as full-release certification.",
            "Score, speed, and baseline claims require an enabled denominator and fresh release evidence.",
        ],
        "source_reports": {
            "release_status": rel(REPORTS_ROOT / "release_status.json"),
            "asset_integrity": rel(REPORTS_ROOT / "asset_integrity.json"),
            "static_certification": rel(REPORTS_ROOT / "static_certification.json"),
            "dual_certification": rel(REPORTS_ROOT / "dual_certification.json"),
            "certification_matrix": rel(REPORTS_ROOT / "certification_matrix.json"),
            "remaining_work": rel(REPORTS_ROOT / "remaining_work.json"),
            "bridge_profile_diagnostics": rel(REPORTS_ROOT / "bridge_profile_diagnostics.json"),
            "external_blockers": rel(REPORTS_ROOT / "external_blockers.json"),
            "paper_artifacts": rel(REPORTS_ROOT / "paper_artifacts.json"),
            "score_denominator_manifest": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            "speed_debug_artifact": rel(REPORTS_ROOT / "speed_debug_artifact.json"),
            "baseline_artifact": rel(REPORTS_ROOT / "baseline_artifact.json"),
        },
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Claim Gate",
        "",
        f"Date: {report['date']}",
        "",
        "This report is the paper-facing claim ledger. It separates what may be",
        "claimed from the current release artifacts from what is still blocked.",
        "It is not simulator certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| claims | {report['claim_count']} |",
        f"| allowed claims | {report['allowed_claim_count']} |",
        f"| blocked claims | {report['blocked_claim_count']} |",
        f"| blocked completion-required claims | {report['blocked_completion_required_claim_count']} |",
        "",
        "## Claims",
        "",
        "| ID | Status | Safe wording |",
        "| --- | --- | --- |",
    ]
    for item in report["claims"]:
        lines.append(f"| `{item['id']}` | `{item['status']}` | {item['safe_wording']} |")
    lines.extend(["", "## Blocked Claim Details", ""])
    blocked = [item for item in report["claims"] if not item["allowed"]]
    if not blocked:
        lines.append("- none")
    for item in blocked:
        lines.append(f"### {item['id']}")
        for requirement in item["required_before_allowed"]:
            lines.append(f"- {requirement}")
    lines.extend(["", "## Policy", ""])
    for rule in report["claim_policy"]:
        lines.append(f"- {rule}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote claim gate: status={status}; allowed={allowed}; blocked={blocked}".format(
            status=report["status"],
            allowed=report["allowed_claim_count"],
            blocked=report["blocked_claim_count"],
        )
    )


if __name__ == "__main__":
    main()
