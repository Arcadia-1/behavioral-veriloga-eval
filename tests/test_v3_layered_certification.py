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

    assert summary["visible_hidden_distinct_count"] == len(distinct_rows) == 74
    assert summary["visible_hidden_identical_count"] == len(identical_rows) == 120
    assert summary["warning_counts"]["visible_hidden_identical"] == 120
    assert all("visible_hidden_identical" in row["warnings"] for row in identical_rows)


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
    assert len(continuous_rows) == 4
    assert len(kcl_rows) == 6
    assert all(row["certification_level"] == "compile_supported_continuous_time_candidate" for row in continuous_rows)
    assert all(row["certification_level"] == "compile_supported_kcl_candidate" for row in kcl_rows)


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
    assert len(staged_tasks) == 41

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

    assert len(staged_rows) == 41
    assert sum(issue["task_count"] for issue in blocking_issues) == 41
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


def test_completion_audit_preserves_full_goal_boundary() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    audit = report["completion_audit"]
    requirements = audit["requirements"]
    by_requirement = {item["requirement"]: item for item in requirements}

    assert audit["status"] == "partial_external_blocked"
    assert audit["is_complete"] is False
    assert "41 extension tasks" in audit["reason"]
    assert len(requirements) == 7
    assert by_requirement[
        "Each extension task has repository behavior checker evidence and can be scored fairly."
    ]["status"] == "partial"
    assert "153 extension tasks are behavior-certified" in by_requirement[
        "Each extension task has repository behavior checker evidence and can be scored fairly."
    ]["evidence"]
    assert "41 remain excluded_until_behavior_promotion" in by_requirement[
        "Each extension task has repository behavior checker evidence and can be scored fairly."
    ]["evidence"]
    assert by_requirement[
        "Behavior-certified extension tasks pass gold verification and reject all negative variants."
    ]["status"] == "satisfied"
