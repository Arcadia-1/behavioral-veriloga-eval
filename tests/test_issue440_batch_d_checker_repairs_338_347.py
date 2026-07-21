from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_338 import CHECKER as CHECKER_338
from checkers.v4.task_340 import CHECKER as CHECKER_340
from checkers.v4.task_341 import CHECKER as CHECKER_341
from checkers.v4.task_347 import CHECKER as CHECKER_347


VDD = 0.9
VSS = 0.0


def _lna_expected(vin: float, blocker: float) -> tuple[float, float, float]:
    excess = max(0.0, blocker - 0.6)
    gain = 6.0 / (1.0 + excess / 0.25)
    vout = max(0.0, min(0.9, 0.45 + gain * (vin - 0.45)))
    metric = 0.9 * (6.0 - gain) / 6.0
    compressed = VDD if metric > 0.1 else VSS
    return vout, metric, compressed


def _lna_rows(*, corrupt_between_sampled_rows: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    time_step = 0.1e-9
    row_index = 0

    def append(vin: float, blocker: float, enable: float, rst: float, *, corrupt: bool = False) -> None:
        nonlocal row_index
        vout, metric, compressed = _lna_expected(vin, blocker)
        if corrupt:
            vout, metric, compressed = 0.0, 0.9, VDD if compressed == VSS else VSS
        rows.append(
            {
                "time": row_index * time_step,
                "vin": vin,
                "blocker": blocker,
                "enable": enable,
                "rst": rst,
                "vout": vout if not rst and enable > 0.45 else 0.45,
                "compression_metric": metric if not rst and enable > 0.45 else 0.0,
                "compressed": compressed if not rst and enable > 0.45 else 0.0,
            }
        )
        row_index += 1

    for _ in range(6):
        append(0.45, 0.2, VSS, VDD)
    cases = [(0.47, 0.2)] * 12 + [(0.47, 0.9)] * 18
    for vin, blocker in cases:
        for phase in range(6):
            append(
                vin,
                blocker,
                VDD,
                VSS,
                corrupt=corrupt_between_sampled_rows and phase != 0,
            )
    for _ in range(14):
        append(0.47, 0.9, VSS, VSS)
    return rows


def _thermal_rows(*, one_bad_thermal_ok: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    time_ns = 0.0
    state = {
        "power_cmd": 0.55,
        "temp_sense": 0.50,
        "clk": 0.0,
        "rst": VDD,
        "enable": VSS,
        "limited_cmd": 0.0,
        "foldback_metric": 0.0,
        "thermal_ok": VSS,
    }

    def emit(dt_ns: float = 0.0) -> None:
        nonlocal time_ns
        time_ns += dt_ns
        rows.append({"time": time_ns * 1e-9, **state})

    emit()
    state.update({"rst": VSS, "enable": VDD, "thermal_ok": VDD})
    emit(0.3)
    active_edges = [
        (0.50, 0.55, 0.55, 0.0, VDD),
        (0.52, 0.60, 0.60, 0.0, VDD),
        (0.70, 0.60, 0.42, 0.18, VSS),
        (0.76, 0.65, 0.38, 0.27, VSS),
        (0.48, 0.50, 0.50, 0.0, VDD),
        (0.78, 0.70, 0.38, 0.32, VSS),
        (0.52, 0.56, 0.56, 0.0, VDD),
        (0.73, 0.62, 0.40, 0.22, VSS),
        (0.49, 0.58, 0.58, 0.0, VDD),
        (0.80, 0.68, 0.35, 0.33, VSS),
    ]
    for edge_index, (temp, cmd, limited, metric, ok) in enumerate(active_edges):
        state.update({"clk": 0.0, "temp_sense": temp, "power_cmd": cmd})
        emit(0.2)
        state.update(
            {
                "clk": VDD,
                "limited_cmd": limited,
                "foldback_metric": metric,
                "thermal_ok": VDD if one_bad_thermal_ok and edge_index == 3 else ok,
            }
        )
        emit(0.2)
        emit(0.75)
    state.update({"clk": 0.0, "enable": VSS, "limited_cmd": 0.0, "foldback_metric": 0.0, "thermal_ok": VSS})
    for _ in range(8):
        emit(0.2)
    return rows


def _soft_start_rows(*, excessive_single_step: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    time_ns = 0.0
    state = {
        "clk": 0.0,
        "rst": VDD,
        "enable": VSS,
        "target_ref": 0.32,
        "soft_ref": 0.0,
        "ramp_metric": 0.0,
        "done": VSS,
    }

    def emit(dt_ns: float = 0.0) -> None:
        nonlocal time_ns
        time_ns += dt_ns
        rows.append({"time": time_ns * 1e-9, **state})

    emit()
    state.update({"rst": VSS, "enable": VDD})
    emit(0.2)
    soft = 0.0
    targets = [0.32] * 10 + [0.18] * 3 + [0.30] * 5
    for edge_index, target in enumerate(targets):
        state.update({"clk": 0.0, "target_ref": target})
        emit(0.15)
        if soft > target:
            soft = target
        else:
            soft = min(target, soft + 0.04)
        observed = soft + (0.035 if excessive_single_step and edge_index == 3 else 0.0)
        metric = max(0.0, target - soft)
        state.update({"clk": VDD})
        emit(0.10)
        state.update(
            {
                "soft_ref": observed,
                "ramp_metric": metric,
                "done": VDD if metric <= 0.005 else VSS,
            }
        )
        emit(0.75)
    state.update({"clk": 0.0, "enable": VSS, "soft_ref": 0.0, "ramp_metric": 0.0, "done": VSS})
    for _ in range(8):
        emit(0.2)
    return rows


def _sequencer_rows(*, delayed_async_clear: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    time_ns = 0.0
    state = {
        "vdd_sense": 0.9,
        "clk": 0.0,
        "rst_n_ext": VDD,
        "enable_req": VDD,
        "por_n": VSS,
        "rst_n_core": VSS,
        "en_ana": VSS,
        "en_dig": VSS,
        "ready": VSS,
    }

    def emit(dt_ns: float = 0.0) -> None:
        nonlocal time_ns
        time_ns += dt_ns
        rows.append({"time": time_ns * 1e-9, **state})

    emit()
    expected = [
        (VSS, VSS, VSS, VSS, VSS),
        (VDD, VSS, VSS, VSS, VSS),
        (VDD, VDD, VSS, VSS, VSS),
        (VDD, VDD, VDD, VSS, VSS),
        (VDD, VDD, VDD, VDD, VSS),
        (VDD, VDD, VDD, VDD, VDD),
    ]
    for por, core, ana, dig, ready in expected + [(VDD, VDD, VDD, VDD, VDD)] * 6:
        state["clk"] = VSS
        emit(0.25)
        state["clk"] = VDD
        emit(0.10)
        state.update({"por_n": por, "rst_n_core": core, "en_ana": ana, "en_dig": dig, "ready": ready})
        emit(0.75)
    state.update({"clk": VSS, "vdd_sense": 0.45})
    if delayed_async_clear:
        for _ in range(4):
            emit(0.25)
        state.update({"por_n": VSS, "rst_n_core": VSS, "en_ana": VSS, "en_dig": VSS, "ready": VSS})
        emit(0.25)
    else:
        state.update({"por_n": VSS, "rst_n_core": VSS, "en_ana": VSS, "en_dig": VSS, "ready": VSS})
        emit(0.25)
    for _ in range(6):
        emit(0.25)
    return rows


def test_338_rejects_unsampled_lna_errors_between_profile_rows() -> None:
    assert CHECKER_338(_lna_rows(corrupt_between_sampled_rows=False))[0]
    passed, detail = CHECKER_338(_lna_rows(corrupt_between_sampled_rows=True))
    assert not passed, detail
    assert "vout_errors=" in detail


def test_340_rejects_single_foldback_thermal_ok_violation() -> None:
    assert CHECKER_340(_thermal_rows(one_bad_thermal_ok=False))[0]
    passed, detail = CHECKER_340(_thermal_rows(one_bad_thermal_ok=True))
    assert not passed, detail
    assert "thermal_errors=" in detail


def test_341_rejects_single_soft_start_step_overshoot() -> None:
    assert CHECKER_341(_soft_start_rows(excessive_single_step=False))[0]
    passed, detail = CHECKER_341(_soft_start_rows(excessive_single_step=True))
    assert not passed, detail
    assert "step_errors=" in detail


def test_347_rejects_eventual_only_async_brownout_clear() -> None:
    assert CHECKER_347(_sequencer_rows(delayed_async_clear=False))[0]
    passed, detail = CHECKER_347(_sequencer_rows(delayed_async_clear=True))
    assert not passed, detail
    assert "P_PWR_ASYNC_CLEAR" in detail
