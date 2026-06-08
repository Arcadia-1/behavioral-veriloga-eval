from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from run_vabench_release_evas_speed_experiment import (  # noqa: E402
    MODES,
    inject_simulator_options,
    stage_mode_task,
)


def test_profile_fast_rust_55_keeps_only_production_whole_segment_path() -> None:
    mode = MODES["profile_fast_rust_55"]

    assert mode.phase == "P11"
    assert mode.default_off_fast_path is True
    assert set(mode.simulator_options) == {
        "evas_profile=fast",
        "evas_skip_source_error_control=yes",
        "evas_rust_full_model_fastpath=true",
        "evas_rust_required=true",
    }


def test_profile_fast_rust_55_options_are_injected_once() -> None:
    mode = MODES["profile_fast_rust_55"]
    tb_text = "\n".join(
        [
            "simulator lang=spectre",
            "simulatorOptions options reltol=1e-4 evas_profile=fast",
            "tran tran stop=1u",
        ]
    )

    injected = inject_simulator_options(tb_text, mode.simulator_options)

    assert injected.count("evas_profile=fast") == 1
    for option in mode.simulator_options:
        assert option in injected


def test_profile_fast_evas2_requests_strict_rust_engine() -> None:
    mode = MODES["profile_fast_evas2"]

    assert mode.phase == "EVAS2"
    assert mode.default_off_fast_path is True
    assert set(mode.simulator_options) == {
        "evas_profile=fast",
        "evas_skip_source_error_control=yes",
        "evas_engine=evas2",
    }


def test_stage_mode_task_resolves_entry_local_sibling_include(tmp_path: Path) -> None:
    task_dir = (
        ROOT
        / "benchmark-vabench-release-v1/tasks"
        / "CT05_pll_clock_and_timing_systems"
        / "vbr1_l1_bang_bang_phase_detector"
        / "forms/bugfix"
    )

    _stage_task, primary_dut, tb_path = stage_mode_task(
        task_dir,
        MODES["profile_fast_evas2"],
        tmp_path,
    )

    assert tb_path.name == "tb_bbpd_ref.scs"
    assert primary_dut.name == "bbpd_ref.va"
    assert primary_dut.exists()
