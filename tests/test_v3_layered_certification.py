from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
REPORT = V3 / "reports" / "layered_certification.json"
TASKS = V3 / "TASKS.json"
SOP_AUDIT = V3 / "reports" / "extension_sop_audit.json"
CHECKS = V3 / "CHECKS.yaml"
VERIFY_REPORT = V3 / "reports" / "verify_301_494_layered.json"


def test_v3_layered_certification_counts_match_task_manifest() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]
    sop_audit = json.loads(SOP_AUDIT.read_text(encoding="utf-8"))
    sop_ready_count = sop_audit["summary"]["sop_ready_count"]
    summary = report["summary"]

    assert summary["task_count"] == len(tasks) == 494
    assert summary["original_full_300_count"] == 300
    assert summary["extension_candidate_count"] == 194
    assert summary["behavior_certified_count"] == 300 + sop_ready_count
    assert summary["behavior_certified_extension_count"] == sop_ready_count
    assert summary["compile_supported_candidate_count"] == 194 - sop_ready_count
    assert summary["unsupported_candidate_count"] == 0

    tier_counts = Counter((task.get("tier") or "<none>") for task in tasks.values())
    assert summary["tier_counts"] == dict(sorted(tier_counts.items()))


def test_v3_extension_sop_audit_tracks_visible_hidden_diversity() -> None:
    sop_audit = json.loads(SOP_AUDIT.read_text(encoding="utf-8"))
    rows = sop_audit["tasks"]
    summary = sop_audit["summary"]

    distinct_rows = [row for row in rows if row["visible_hidden_distinct"]]
    identical_rows = [row for row in rows if not row["visible_hidden_distinct"]]

    assert summary["visible_hidden_distinct_count"] == len(distinct_rows) == 194
    assert summary["visible_hidden_identical_count"] == len(identical_rows) == 0
    assert summary["behavior_contract_complete_count"] == 194
    assert summary["negative_cases_aligned_count"] == 194
    assert summary["negative_descriptions_task_specific_count"] == 194
    assert summary["sop_ready_visible_hidden_identical_count"] == 0
    assert summary["staged_visible_hidden_identical_count"] == 0
    assert summary["warning_counts"].get("visible_hidden_identical", 0) == 0
    assert all("visible_hidden_identical" in row["warnings"] for row in identical_rows)
    assert all(row["behavior_contract_complete"] for row in rows)
    assert all(row["negative_cases_aligned"] for row in rows)
    assert all(row["negative_descriptions_task_specific"] for row in rows)


def test_v3_extension_rows_do_not_overclaim_behavior_certification() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    sop_audit = json.loads(SOP_AUDIT.read_text(encoding="utf-8"))
    sop_ready_tasks = {
        row["task"]
        for row in sop_audit["tasks"]
        if row["sop_ready"]
    }
    rows = report["task_rows"]

    extension_rows = [row for row in rows if row["extension_candidate"]]
    assert len(extension_rows) == 194
    for row in extension_rows:
        if row["task_key"] in sop_ready_tasks:
            assert row["behavior_certified"]
            assert row["score_claim"] == "extension_behavior_certified_outside_original_300"
        else:
            assert not row["behavior_certified"]
            assert row["score_claim"] == "excluded_until_behavior_promotion"
            assert row["blocking_issue_urls"].startswith("https://github.com/Arcadia-1/EVAS/issues/")

    continuous_rows = [
        row for row in rows
        if row["semantic_layer"] == "behavioral_continuous_time_extension"
    ]
    kcl_rows = [
        row for row in rows
        if row["semantic_layer"] == "conservative_kcl_syntax_extension"
    ]
    assert len(continuous_rows) == 14
    assert {
        row["task_key"][:3]
        for row in continuous_rows
    } == {
        "435",
        "436",
        "437",
        "438",
        "439",
        "440",
        "441",
        "442",
        "443",
        "444",
        "471",
        "472",
        "493",
        "494",
    }
    assert len(kcl_rows) == 6
    continuous_by_key = {row["task_key"]: row for row in continuous_rows}
    behavior_certified_continuous = {
        "435-ddt-voltage-derivative-source",
        "436-idt-voltage-integrator-source",
        "437-laplace-nd-lowpass-filter",
        "438-laplace-np-pole-filter",
        "439-laplace-zd-zero-den-filter",
        "440-laplace-zp-zero-pole-filter",
        "441-zi-nd-discrete-filter",
        "442-zi-np-discrete-filter",
        "443-zi-zd-discrete-filter",
        "444-zi-zp-discrete-filter",
    }
    for key in behavior_certified_continuous:
        assert continuous_by_key[key]["certification_level"] == "behavior_certified_extension"
    assert all(
        row["certification_level"] == "compile_supported_continuous_time_candidate"
        for key, row in continuous_by_key.items()
        if key not in behavior_certified_continuous
    )
    kcl_by_key = {row["task_key"]: row for row in kcl_rows}
    for key in (
        "469-current-contribution-conductance",
        "491-kcl-capacitor-ddt-current",
    ):
        assert kcl_by_key[key]["certification_level"] == "compile_supported_kcl_candidate"
    for key in (
        "470-branch-current-probe-contribution",
        "481-analog-primitive-resistor-instance",
        "482-analog-primitive-isource-instance",
        "492-kcl-inductor-idt-voltage",
    ):
        assert kcl_by_key[key]["certification_level"] == "behavior_certified_extension"


def test_v3_layered_certification_claim_boundary_is_explicit() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    boundary = "\n".join(report["claim_boundary"])

    assert "Only tasks 001-300" in boundary
    assert "Tasks 301-494 are extension candidates" in boundary
    assert "do not certify continuous-time numeric accuracy" in boundary
    assert "do not certify MNA/KCL solving behavior" in boundary


def _checks_block(checks_text: str, task_key: str) -> str:
    lines = checks_text.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line == f"{task_key}: |":
            start = index + 1
            break
    assert start is not None, f"missing CHECKS block for {task_key}"
    end = len(lines)
    for index in range(start, len(lines)):
        if re.match(r"^\d{3}-", lines[index]):
            end = index
            break
    return "\n".join(lines[start:end])


def test_staged_extension_rows_have_traceable_evas_issues() -> None:
    sop_audit = json.loads(SOP_AUDIT.read_text(encoding="utf-8"))
    checks_text = CHECKS.read_text(encoding="utf-8")
    issue_url = "https://github.com/Arcadia-1/EVAS/issues/"

    staged_tasks = [
        row["task"]
        for row in sop_audit["tasks"]
        if "checker_syntax_only_no_behavior_score" in row.get("issues", [])
    ]
    assert len(staged_tasks) == sop_audit["summary"]["task_count"] - sop_audit["summary"]["sop_ready_count"]

    missing_checks_url: list[str] = []
    missing_audit_url: list[str] = []
    for task_key in staged_tasks:
        if issue_url not in _checks_block(checks_text, task_key):
            missing_checks_url.append(task_key)
        audit_path = V3 / "tasks" / task_key / "AUDIT.md"
        assert audit_path.exists(), f"missing AUDIT.md for {task_key}"
        if issue_url not in audit_path.read_text(encoding="utf-8"):
            missing_audit_url.append(task_key)

    assert missing_checks_url == []
    assert missing_audit_url == []


def test_blocking_issue_matrix_covers_all_staged_rows() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    staged_rows = [
        row for row in report["task_rows"]
        if row["score_claim"] == "excluded_until_behavior_promotion"
    ]
    blocking_issues = report["blocking_issues"]
    issue_task_keys = {
        task["task_key"]
        for issue in blocking_issues
        for task in issue["tasks"]
    }
    staged_count = report["summary"]["compile_supported_candidate_count"]

    assert len(staged_rows) == staged_count
    assert sum(issue["task_count"] for issue in blocking_issues) == staged_count
    assert issue_task_keys == {row["task_key"] for row in staged_rows}
    assert report["summary"]["blocking_issue_counts"] == {
        issue["issue_url"]: issue["task_count"]
        for issue in blocking_issues
    }


def test_blocking_issue_matrix_has_promotion_checklists() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    for issue in report["blocking_issues"]:
        task_count = issue["task_count"]
        negative_count = task_count * 5
        command = issue["promotion_command"]
        acceptance = issue["promotion_acceptance"]
        task_numbers = [task["task_key"][:3] for task in issue["tasks"]]

        assert "--include-staged" in command
        assert "--tasks " in command
        assert "run_v3_gold_negative_verification.py" in command
        assert f"--tasks {','.join(task_numbers)}" in command
        assert f"{task_count}/{task_count} gold PASS" in acceptance
        assert f"{negative_count}/{negative_count} negative variants rejected" in acceptance
        assert "zero expectation_fail" in acceptance


def test_staged_gold_probe_documents_current_promotion_boundary() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    evidence = report["evidence_sources"]
    probe_path = ROOT / evidence["staged_gold_probe"]
    probe_summary_path = ROOT / evidence["staged_gold_probe_summary"]

    assert probe_path.exists()
    assert probe_summary_path.exists()
    probe = json.loads(probe_path.read_text(encoding="utf-8"))
    summary = probe["summary"]
    staged_rows = [
        row for row in report["task_rows"]
        if row["score_claim"] == "excluded_until_behavior_promotion"
    ]

    assert summary["gold_total"] == len(staged_rows)
    assert summary["gold_pass"] == 0
    assert summary["expectation_fail"] == len(staged_rows)
    assert len(probe["rows"]) == len(staged_rows)
    assert {row["task_slug"] for row in probe["rows"]} == {
        row["task_key"] for row in staged_rows
    }
    assert all(row.get("failure_summary") for row in probe["rows"])
    assert not any(
        str(row.get("failure_summary")).startswith(("returncode=", "evas_engine=", "dut_not_compiled", "tb_not_executed"))
        for row in probe["rows"]
    )


def test_staged_blocker_matrix_tracks_each_unpromoted_task() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    evidence = report["evidence_sources"]
    matrix_path = ROOT / evidence["staged_blocker_matrix"]
    matrix_summary_path = ROOT / evidence["staged_blocker_matrix_summary"]

    assert matrix_path.exists()
    assert matrix_summary_path.exists()
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    staged_rows = {
        row["task_key"]: row
        for row in report["task_rows"]
        if row["score_claim"] == "excluded_until_behavior_promotion"
    }
    matrix_rows = {row["task_key"]: row for row in matrix["tasks"]}

    assert matrix["summary"]["staged_task_count"] == len(staged_rows)
    assert matrix["summary"]["missing_issue_count"] == 0
    assert matrix["summary"]["missing_failure_summary_count"] == 0
    assert set(matrix_rows) == set(staged_rows)
    assert all(row["issue_urls"] for row in matrix_rows.values())
    assert all(row["failure_summary"] for row in matrix_rows.values())
    for row in matrix_rows.values():
        task_number = int(row["task_key"].split("-", 1)[0])
        assert row["task_promotion_command"]
        assert f"--start {task_number}" in row["task_promotion_command"]
        assert f"--end {task_number}" in row["task_promotion_command"]
        assert f"--tasks {task_number:03d}" in row["task_promotion_command"]
        assert f"verify_task_{task_number:03d}.json" in row["task_promotion_command"]
        assert "1/1 gold PASS" in row["task_promotion_acceptance"]
        assert "5/5 negative variants rejected" in row["task_promotion_acceptance"]


def test_staged_task_audits_include_current_promotion_gate() -> None:
    matrix = json.loads((V3 / "reports" / "staged_blocker_matrix.json").read_text(encoding="utf-8"))

    for row in matrix["tasks"]:
        audit_path = V3 / "tasks" / row["task_key"] / "AUDIT.md"
        assert audit_path.exists(), f"{row['task_key']} missing AUDIT.md"
        audit = audit_path.read_text(encoding="utf-8")

        assert "## Staged Promotion Gate" in audit
        assert f"- Current probe status: `{row['probe_status']}`." in audit
        assert f"- Current failure summary: {row['failure_summary']}" in audit
        assert "- Promotion requirements: repository `sim_correct` checker evidence" in audit
        assert "gold PASS" in audit
        assert "five useful negative variants rejected" in audit
        assert "zero expectation_fail" in audit
        assert f"- Per-task promotion command: `{row['task_promotion_command']}`" in audit
        assert f"- Per-task acceptance: {row['task_promotion_acceptance']}" in audit
        for issue_url in row["issue_urls"]:
            assert issue_url in audit


def test_generate_genvar_task_is_ams_mixed_signal_layer() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    rows = {row["task_key"]: row for row in report["task_rows"]}

    row = rows["449-generate-genvar-replicated-stage"]
    assert row["tier"] == "ams-mixed-signal-candidate"
    assert row["semantic_layer"] == "ams_mixed_signal_extension"
    assert row["certification_level"] == "behavior_certified_extension"
    assert row["behavior_certified"] is True

    specify = rows["453-specify-specparam-delay"]
    assert specify["tier"] == "ams-mixed-signal-candidate"
    assert specify["semantic_layer"] == "ams_mixed_signal_extension"
    assert specify["certification_level"] == "behavior_certified_extension"
    assert specify["behavior_certified"] is True

    resistor = rows["481-analog-primitive-resistor-instance"]
    assert resistor["semantic_layer"] == "conservative_kcl_syntax_extension"
    assert resistor["certification_level"] == "behavior_certified_extension"
    assert resistor["behavior_certified"] is True

    isource = rows["482-analog-primitive-isource-instance"]
    assert isource["semantic_layer"] == "conservative_kcl_syntax_extension"
    assert isource["certification_level"] == "behavior_certified_extension"
    assert isource["behavior_certified"] is True


def test_staged_gold_probe_uses_specific_checkers_when_available() -> None:
    probe = json.loads((V3 / "reports" / "staged_promotion_gold_probe.json").read_text(encoding="utf-8"))
    rows = {row["task_slug"]: row for row in probe["rows"]}
    checker_backed_staged_tasks = {
        "469-current-contribution-conductance": "staged_kcl_boundary",
        "471-indirect-branch-null-balance": "operator=indirect_branch_equation",
        "472-indirect-branch-ddt-balance": "operator=indirect_branch_ddt_equation",
        "491-kcl-capacitor-ddt-current": "staged_kcl_boundary",
        "493-continuous-laplace-nd-filter": "operator=continuous_laplace_nd",
        "494-continuous-zi-nd-filter": "operator=continuous_zi_nd",
    }

    for row in probe["rows"]:
        notes = " ".join(str(note) for note in row["notes"])
        assert "no behavior check implemented" not in notes

    for task_key, marker in checker_backed_staged_tasks.items():
        notes = " ".join(str(note) for note in rows[task_key]["notes"])
        assert marker in notes


def test_completion_audit_preserves_full_goal_boundary() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    audit = report["completion_audit"]
    requirements = audit["requirements"]
    by_requirement = {item["requirement"]: item for item in requirements}

    assert audit["status"] == "partial_external_blocked"
    assert audit["is_complete"] is False
    staged_count = report["summary"]["compile_supported_candidate_count"]
    behavior_count = report["summary"]["behavior_certified_extension_count"]
    assert f"{staged_count} extension tasks" in audit["reason"]
    assert len(requirements) == 7
    assert by_requirement[
        "Each extension task has repository behavior checker evidence and can be scored fairly."
    ]["status"] == "partial"
    assert f"{behavior_count} extension tasks are behavior-certified" in by_requirement[
        "Each extension task has repository behavior checker evidence and can be scored fairly."
    ]["evidence"]
    assert f"{staged_count} remain excluded_until_behavior_promotion" in by_requirement[
        "Each extension task has repository behavior checker evidence and can be scored fairly."
    ]["evidence"]
    assert by_requirement[
        "Behavior-certified extension tasks pass gold verification and reject all negative variants."
    ]["status"] == "satisfied"


def test_behavior_certified_extension_negatives_fail_behavior_checkers_only() -> None:
    verification = json.loads(VERIFY_REPORT.read_text(encoding="utf-8"))
    summary = verification["summary"]
    negative_rows = [row for row in verification["rows"] if row["kind"] == "negative"]
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    behavior_count = report["summary"]["behavior_certified_extension_count"]
    expected_negative_count = behavior_count * 5

    assert summary["gold_pass"] == behavior_count
    assert summary["gold_fail"] == 0
    assert summary["negative_rejected"] == len(negative_rows) == expected_negative_count
    assert summary["negative_accepted"] == 0
    assert summary["expectation_fail"] == 0
    assert {row["status"] for row in negative_rows} == {"FAIL_SIM_CORRECTNESS"}
    assert all(row["meets_expectation"] for row in negative_rows)


def test_behavior_certified_extension_task_evidence_matches_case_report() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    evidence_path = ROOT / report["evidence_sources"]["behavior_certified_extension_task_evidence"]
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    verification = json.loads(VERIFY_REPORT.read_text(encoding="utf-8"))
    verification_rows = verification["rows"]

    gold_by_task = {
        row["task_slug"]: row
        for row in verification_rows
        if row["kind"] == "gold"
    }
    negative_statuses_by_task: dict[str, dict[str, str]] = {}
    for row in verification_rows:
        if row["kind"] != "negative":
            continue
        negative_statuses_by_task.setdefault(row["task_slug"], {})[row["variant"]] = row["status"]

    summary = evidence["summary"]
    task_rows = evidence["tasks"]
    behavior_count = report["summary"]["behavior_certified_extension_count"]
    expected_negative_count = behavior_count * 5
    assert summary["task_count"] == len(task_rows) == behavior_count
    assert summary["gold_pass_count"] == behavior_count
    assert summary["negative_total"] == expected_negative_count
    assert summary["negative_behavior_rejected_total"] == expected_negative_count
    assert summary["all_tasks_have_five_behavior_rejected_negatives"] is True

    for task_row in task_rows:
        task = task_row["task"]
        assert task_row["gold_status"] == gold_by_task[task]["status"] == "PASS"
        assert task_row["gold_meets_expectation"] is True
        assert task_row["negative_count"] == 5
        assert task_row["negative_statuses"] == negative_statuses_by_task[task]
        assert task_row["negative_behavior_rejected_count"] == 5
        assert task_row["all_negatives_behavior_rejected"] is True
