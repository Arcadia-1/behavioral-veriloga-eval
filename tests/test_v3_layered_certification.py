from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
REPORT = V3 / "reports" / "layered_certification.json"
TASKS = V3 / "TASKS.json"


def test_v3_layered_certification_counts_match_task_manifest() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]
    summary = report["summary"]

    assert summary["task_count"] == len(tasks) == 494
    assert summary["original_full_300_count"] == 300
    assert summary["extension_candidate_count"] == 194
    assert summary["behavior_certified_count"] == 300
    assert summary["behavior_certified_extension_count"] == 0
    assert summary["compile_supported_candidate_count"] == 194
    assert summary["unsupported_candidate_count"] == 0

    tier_counts = Counter((task.get("tier") or "<none>") for task in tasks.values())
    assert summary["tier_counts"] == dict(sorted(tier_counts.items()))


def test_v3_extension_rows_do_not_overclaim_behavior_certification() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    rows = report["task_rows"]

    extension_rows = [row for row in rows if row["extension_candidate"]]
    assert len(extension_rows) == 194
    assert all(not row["behavior_certified"] for row in extension_rows)
    assert all(row["score_claim"] == "excluded_until_behavior_promotion" for row in extension_rows)

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
