from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
REPORT = V3 / "reports" / "score_support_manifest.json"
TASKS = V3 / "TASKS.json"

SUPPORT_CATEGORIES = {
    "measurement",
    "measurement_instrumentation_flows",
    "stimulus",
    "stimulus_source_generators",
    "testbench_utility_modules",
}


def task_manifest() -> dict[str, dict]:
    return json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]


def task_number(task_key: str) -> int | None:
    match = re.match(r"^(\d{3})-", task_key)
    return int(match.group(1)) if match else None


def score_manifest() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_v3_score_support_manifest_matches_current_task_tree() -> None:
    report = score_manifest()
    tasks = task_manifest()
    rows = report["task_rows"]
    summary = report["summary"]

    assert summary["total_tasks"] == len(tasks) == len(rows)
    assert summary["numbered_tasks"] == sum(task_number(key) is not None for key in tasks)
    assert summary["unnumbered_candidates"] == sum(task_number(key) is None for key in tasks)
    assert summary["original_001_300_tasks"] == 300
    assert summary["extension_301_plus_tasks"] == 151
    assert summary["score_role_counts"] == {
        "candidate_provenance": 9,
        "language_extension": 147,
        "scored_benchmark": 258,
        "support": 42,
    }


def test_v3_score_support_manifest_separates_core_support_and_extensions() -> None:
    rows = score_manifest()["task_rows"]
    rows_by_key = {row["task_key"]: row for row in rows}
    tasks = task_manifest()

    for task_key, task in tasks.items():
        row = rows_by_key[task_key]
        number = task_number(task_key)
        category = task.get("category")
        if number is not None and number <= 300 and category not in SUPPORT_CATEGORIES:
            assert row["score_role"] == "scored_benchmark"
            assert row["counted_in_core_score"] is True
            assert row["support_suite"] is False
            assert row["exclusion_reason"] == ""
        elif number is not None and number <= 300:
            assert row["score_role"] == "support"
            assert row["counted_in_core_score"] is False
            assert row["support_suite"] is True
            assert row["exclusion_reason"] == "v3_support_category_excluded_from_core_score"
        elif number is not None:
            assert row["counted_in_core_score"] is False
            assert row["support_suite"] is False
            assert row["score_role"] in {"language_extension", "candidate_provenance"}
        else:
            assert row["score_role"] == "candidate_provenance"
            assert row["counted_in_core_score"] is False
            assert row["support_suite"] is False


def test_v3_score_support_manifest_does_not_use_historical_denominators() -> None:
    report = score_manifest()
    policy = report["policy"]
    summary = report["summary"]

    assert "provenance only" in policy["historical_denominators"]
    assert summary["scored_benchmark_tasks"] == 258
    assert summary["support_tasks"] == 42
    assert "66" not in json.dumps(summary, sort_keys=True)
    assert "73" not in json.dumps(summary, sort_keys=True)
    assert "236" not in json.dumps(summary, sort_keys=True)
    assert "265" not in json.dumps(summary, sort_keys=True)
