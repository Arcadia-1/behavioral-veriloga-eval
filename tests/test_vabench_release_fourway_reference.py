from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

import report_vabench_release_fourway_reference as fourway


def write_csv(path: Path, values: list[float]) -> None:
    path.write_text(
        "time,vout\n" + "\n".join(f"{idx * 1e-9},{value}" for idx, value in enumerate(values)) + "\n",
        encoding="utf-8",
    )


def result_row(
    *,
    backend: str,
    mode: str,
    csv_path: Path,
    wall: float,
    subprocess: float,
    checker: float,
    behavior_ok: bool = True,
    perf_counters: dict[str, float] | None = None,
) -> dict[str, object]:
    split: dict[str, float]
    if backend == "evas":
        split = {
            "run_case_behavior_checker_s": checker,
            "run_case_evas_runner_csv_write_s": 0.01,
            "run_case_evas_subprocess_wall_s": subprocess,
            "fixture_materialize_s": 0.02,
        }
    else:
        split = {
            "behavior_checker_s": checker,
            "psf_parse_s": 0.03,
            "spectre_subprocess_wall_s": subprocess,
            "fixture_materialize_s": 0.02,
        }
    return {
        "entry_id": "demo",
        "form": "tb",
        "variant": "gold",
        "task_id": "demo_tb",
        "backend": backend,
        "mode": mode,
        "status": "PASS",
        "ok": behavior_ok,
        "simulation_ok": True,
        "behavior_ok": behavior_ok,
        "csv_path": str(csv_path),
        "wall_time_s": wall,
        "simulator_subprocess_wall_s": subprocess,
        "timing": {"tran_elapsed_s": subprocess / 10.0},
        "timing_split": split,
        "checker_policy": {"implementation": "row_based"},
        "perf_counters": perf_counters or {},
    }


def test_fourway_reference_merges_modes_and_compares_to_spectre_strict(tmp_path: Path) -> None:
    csv = tmp_path / "same.csv"
    write_csv(csv, [0.0, 0.5, 1.0])
    source = tmp_path / "raw.json"
    source.write_text(
        json.dumps(
            {
                "artifact_kind": "candidate_same_server_evas_spectre_timing",
                "schema_version": "same-server-speed.v1",
                "created_at": "2026-06-06T00:00:00",
                "selected_rows": 1,
                "evas_modes": ["strict_current", "profile_fast_evas2"],
                "spectre_modes": ["ax_speed", "reference_strict_primary"],
                "results": [
                    result_row(backend="evas", mode="strict_current", csv_path=csv, wall=4.0, subprocess=3.0, checker=0.4),
                    result_row(
                        backend="evas",
                        mode="profile_fast_evas2",
                        csv_path=csv,
                        wall=2.0,
                        subprocess=0.5,
                        checker=0.4,
                        perf_counters={
                            "rust_full_model_fastpath_enabled": 1,
                            "rust_sim_program_enabled": 1,
                            "rust_sim_program_event_count": 2,
                        },
                    ),
                    result_row(backend="spectre", mode="ax_speed", csv_path=csv, wall=8.0, subprocess=6.0, checker=0.2),
                    result_row(
                        backend="spectre",
                        mode="reference_strict_primary",
                        csv_path=csv,
                        wall=10.0,
                        subprocess=7.0,
                        checker=0.3,
                    ),
                ],
            }
        ),
        encoding="utf-8",
    )

    report = fourway.build_report([source], coverage_json=None, top_limit=5)

    assert report["scope"]["common_row_count"] == 1
    assert report["scope"]["behavior_refresh_policy"] == "refresh stale non-pass source rows from existing CSV checkers only"
    assert report["experiment_lock"]["status"] == "frozen"
    assert report["experiment_lock"]["experiment_id"] == "vabench-release-fourway-rust-evas2-spectreax-strict-20260606"
    assert report["experiment_lock"]["row_set_size"] == 1
    assert len(report["experiment_lock"]["row_set_sha256"]) == 64
    assert report["experiment_lock"]["source_artifacts"][0]["sha256"]
    assert report["speed"]["modes"]["rust_evas2"]["component_totals_s"]["subprocess_wall_s"] == 0.5
    rust_vs_ax = next(row for row in report["speed"]["comparisons"] if row["alias"] == "rust_evas2")
    assert rust_vs_ax["speedup_vs_spectre_ax_e2e"] == 4.0
    precision = {row["candidate"]: row for row in report["precision"]["summary"]}
    assert precision["rust_evas2"]["equivalent_rows"] == 1
    assert precision["spectre_ax"]["equivalent_rows"] == 1
    assert report["claim_status"]["speed_aggregate_vs_spectre_ax"]["allowed"] is True
    assert report["claim_status"]["precision_equivalence_vs_spectre_strict"]["allowed"] is True
    assert report["claim_status"]["precision_better_than_spectre_ax"]["allowed"] is False
    assert any(
        "more accurate than Spectre AX" in item
        for item in report["claim_status"]["forbidden_wording"]
    )
    assert report["rust_coverage"]["rust_full_model_enabled_rows"] == 1
    assert report["rust_coverage"]["rust_sim_program_enabled_rows"] == 1


def test_spectre_strict_behavior_nonpass_blocks_precision_reference(tmp_path: Path) -> None:
    csv = tmp_path / "same.csv"
    write_csv(csv, [0.0, 0.5, 1.0])
    source = tmp_path / "raw.json"
    source.write_text(
        json.dumps(
            {
                "results": [
                    result_row(
                        backend="evas",
                        mode="profile_fast_evas2",
                        csv_path=csv,
                        wall=2.0,
                        subprocess=0.5,
                        checker=0.4,
                    ),
                    result_row(
                        backend="spectre",
                        mode="reference_strict_primary",
                        csv_path=csv,
                        wall=10.0,
                        subprocess=7.0,
                        checker=0.3,
                        behavior_ok=False,
                    ),
                ]
            }
        ),
        encoding="utf-8",
    )

    report = fourway.build_report([source], coverage_json=None, top_limit=5)

    rust_precision = next(row for row in report["precision"]["summary"] if row["candidate"] == "rust_evas2")
    assert rust_precision["reference_usable_rows"] == 0
    assert rust_precision["blocked_rows"] == 1
    blocked = next(
        row
        for row in report["precision"]["needs_review_or_blocked_rows"]
        if row["candidate"] == "rust_evas2"
    )
    assert blocked["reason"] == "reference behavior non-pass"


def test_fourway_reference_refreshes_behavior_from_existing_csv(tmp_path: Path, monkeypatch) -> None:
    csv = tmp_path / "same.csv"
    write_csv(csv, [0.0, 0.5, 1.0])
    row = result_row(
        backend="spectre",
        mode="reference_strict_primary",
        csv_path=csv,
        wall=10.0,
        subprocess=7.0,
        checker=0.3,
        behavior_ok=False,
    )
    row["checker_id"] = "demo_checker"
    refreshed_calls: list[tuple[str, Path]] = []

    def fake_evaluate(checker_id: str, csv_path: Path, *, timeout_s: int):
        refreshed_calls.append((checker_id, csv_path))
        return 1.0, ["fresh pass"]

    monkeypatch.setattr(fourway, "has_behavior_check", lambda checker_id: checker_id == "demo_checker")
    monkeypatch.setattr(fourway, "evaluate_behavior_with_timeout", fake_evaluate)
    monkeypatch.setattr(
        fourway,
        "behavior_checker_policy",
        lambda checker_id, notes: {"implementation": "refreshed", "checker_id": checker_id, "notes": notes},
    )

    refreshed = fourway.refresh_behavior_from_csv(row)

    assert refreshed_calls == [("demo_checker", csv)]
    assert refreshed["raw_behavior_ok"] is False
    assert refreshed["behavior_ok"] is True
    assert refreshed["ok"] is True
    assert refreshed["notes"] == ["fresh pass"]
    assert refreshed["checker_policy"]["implementation"] == "refreshed"


def test_fourway_reference_missing_raw_sources_are_actionable(tmp_path: Path) -> None:
    missing = tmp_path / "missing-source.json"

    try:
        fourway.build_report([missing], coverage_json=None, top_limit=5)
    except FileNotFoundError as exc:
        message = str(exc)
    else:  # pragma: no cover - the assertion above is the behavior under test.
        raise AssertionError("missing source JSON should raise")

    assert "missing four-way source JSON artifact" in message
    assert "--source-json" in message
    assert "archived raw source JSONs" in message
