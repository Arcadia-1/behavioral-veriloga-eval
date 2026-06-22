from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "benchmark-vabench-release-v1" / "reports"
REPORT = REPORTS / "benchmark_overview.json"
REPORT_MD = REPORTS / "benchmark_overview.md"
ENTRY_CSV = REPORTS / "benchmark_overview_entries.csv"
FORM_CSV = REPORTS / "benchmark_overview_forms.csv"
CATEGORY_CSV = REPORTS / "benchmark_overview_categories.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_benchmark_overview_exports_complete_lists() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "ready"
    assert report["summary"]["entry_count"] == 86
    assert report["summary"]["form_count"] == 300
    assert report["summary"]["certified_form_count"] == 300
    assert report["summary"]["pending_form_count"] == 0
    assert report["summary"]["scored_form_count"] == 265
    assert report["summary"]["existing_certified_v1_task_count"] == 271
    assert report["summary"]["promoted_v11_task_count"] == 29

    assert len(read_csv(ENTRY_CSV)) == 86
    assert len(read_csv(FORM_CSV)) == 300
    assert len(read_csv(CATEGORY_CSV)) > 0


def test_benchmark_overview_answers_dual_certification_questions() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    metrics = report["aggregate_parity_metrics"]

    assert report["summary"]["dual_certification_status"] == "pass"
    assert report["summary"]["dual_certified_release_task_count"] == 271
    assert report["summary"]["dual_failed_release_task_count"] == 0
    assert report["summary"]["dual_pending_release_task_count"] == 0
    assert report["summary"]["evas_pass_spectre_fail_count"] == 0

    assert metrics["parity_passed_form_count"] == 300
    assert metrics["parity_form_count"] == 300
    assert metrics["waveform_metric_form_count"] == 263
    assert metrics["gain_metric_form_count"] == 4
    assert metrics["pll_task_aware_form_count"] == 4
    assert metrics["max_worst_signal_relative_rms_error"] <= 0.22
    assert metrics["max_relative_gain_delta"] <= 0.25


def test_benchmark_overview_reports_four_backend_pass() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    coverage = report["backend_coverage"]
    by_backend = {row["backend"]: row for row in coverage["rows"]}
    md = REPORT_MD.read_text(encoding="utf-8")

    assert report["status"] == "ready"
    assert report["summary"]["four_backend_status"] == "pass"
    assert coverage["completed_backend_count"] == 4
    assert coverage["certified_backend_count"] == 4
    assert coverage["required_backend_count"] == 4

    assert by_backend["spectre_reference"]["full_300_status"] == "pass"
    assert by_backend["spectre_reference"]["rows"] == 300
    assert by_backend["spectre_reference"]["nonpass_rows"] == 0
    assert by_backend["spectre_reference"]["spectre_ok_rows"] == 300
    assert by_backend["spectre_reference"]["no_checker_rows"] == 0
    assert by_backend["spectre_ax"]["full_300_status"] == "pass"
    assert by_backend["spectre_ax"]["rows"] == 300
    assert by_backend["spectre_ax"]["nonpass_rows"] == 0
    assert by_backend["spectre_ax"]["spectre_ok_rows"] == 300
    assert by_backend["spectre_ax"]["no_checker_rows"] == 0
    assert by_backend["evas_rust"]["full_300_status"] == "pass"
    assert by_backend["evas_rust"]["rows"] == 300
    assert by_backend["evas_rust"]["behavior_checker_pass_rows"] == 300
    assert by_backend["evas_rust"]["behavior_checker_missing_rows"] == 0
    assert by_backend["evas_python"]["full_300_status"] == "pass"
    assert by_backend["evas_python"]["rows"] == 300
    assert by_backend["evas_python"]["behavior_checker_pass_rows"] == 300
    assert by_backend["evas_python"]["behavior_checker_missing_rows"] == 0

    assert "Four-backend certification status: `pass`" in md
    assert "Full-300 runs completed for 4 / 4" in md
    assert "behavior-certified PASS evidence exists for 4 / 4" in md
    assert "Claim 300/300 four-backend behavior certification only when" in " ".join(report["claim_boundary"])


def test_benchmark_overview_keeps_exactness_claim_precise() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    contract = report["equivalence_contract"]
    md = REPORT_MD.read_text(encoding="utf-8")

    assert contract["bit_exact_claim"] == "not_asserted"
    assert "max_rmse_v<=0.05" in contract["small_absolute_gate"]
    assert "worst_signal_relative_rms_error<=0.22" in contract["relative_rms_gate"]
    assert "Bit-exact equality claim: `not_asserted`" in md
    assert any("VABENCH_300_MANIFEST.json is the benchmark management manifest" in item for item in report["claim_boundary"])


def test_benchmark_overview_uses_300_as_single_management_surface() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    expansion = report["vabench300_expansion"]
    staging = report["staging_bundle_counts"]
    md = REPORT_MD.read_text(encoding="utf-8")
    forms = read_csv(FORM_CSV)

    assert report["summary"]["form_count"] == 300
    assert expansion["status"] == "present"
    assert expansion["task_count"] == 300
    assert expansion["certified_task_count"] == 300
    assert expansion["pending_certification_task_count"] == 0
    assert expansion["promoted_v11_task_count"] == 29
    assert staging["current_dual_staging_bundles"] == 65
    assert staging["speed_remaining_staging_bundles"] == 225
    assert staging["total_staging_bundles"] == 290
    assert staging["total_primary_queue_rows"] == 238
    assert staging["buggy_companion_bundles"] == 52
    assert sum(1 for row in forms if row["expansion_status"] == "certified_v1.1_promoted") == 29
    assert "Use 300 as the benchmark task count" in md
    assert "single management denominator" in md
    assert "execution inputs only; not a benchmark count" in md


def test_benchmark_overview_entry_rows_have_traceable_evidence() -> None:
    entries = {row["release_entry_id"]: row for row in read_csv(ENTRY_CSV)}
    binary_dac = entries["vbr1_l1_binary_weighted_voltage_dac"]

    assert binary_dac["level"] == "L1"
    assert binary_dac["track"] == "core"
    assert binary_dac["form_count"] == "4"
    assert binary_dac["counted_in_score"] == "True"
    assert binary_dac["evas"] == "pass"
    assert binary_dac["spectre"] == "pass"
    assert binary_dac["evidence_count"] == "4"
    assert "benchmark-vabench-release-v1/evidence/dual/" in binary_dac["evidence_paths"]
