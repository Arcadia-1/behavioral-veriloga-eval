from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))


def _logic(value: int | bool) -> float:
    return 0.9 if value else 0.0


def _stable_intervals(
    states: list[dict[str, float]],
    *,
    start_s: float = 137.0e-9,
    interval_s: float = 7.25e-9,
    gap_s: float = 0.35e-9,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    time_s = start_s
    for state in states:
        left = {"time": time_s, **state}
        right = {"time": time_s + interval_s, **state}
        rows.extend([left, right])
        time_s += interval_s + gap_s
    return rows


def _row_048(code: int, *, enabled: bool) -> dict[str, float]:
    row: dict[str, float] = {"en": _logic(enabled)}
    for bit in range(8):
        row[f"b{bit}"] = _logic((code >> bit) & 1)
    expected_count = code if enabled else 0
    for index in range(256):
        row[f"th{index}"] = _logic(index < expected_count)
    return row


def _trace_048() -> list[dict[str, float]]:
    return _stable_intervals(
        [
            _row_048(5, enabled=False),
            _row_048(0, enabled=True),
            _row_048(1, enabled=True),
            _row_048(37, enabled=True),
            _row_048(255, enabled=True),
        ]
    )


def _row_049(count: int, *, invalid: bool = False) -> dict[str, float]:
    row: dict[str, float] = {}
    high = {0, 2} if invalid else set(range(count))
    for index in range(256):
        row[f"th{index}"] = _logic(index in high)
    expected_code = 0 if invalid else count
    for bit in range(8):
        row[f"b{bit}"] = _logic((expected_code >> bit) & 1)
    row["valid"] = _logic(not invalid)
    return row


def _trace_049() -> list[dict[str, float]]:
    return _stable_intervals(
        [
            _row_049(0),
            _row_049(1),
            _row_049(37),
            _row_049(255),
            _row_049(0, invalid=True),
        ]
    )


def _adc_row(time_s: float, vin: float) -> dict[str, float]:
    code = max(0, min(7, int(8.0 * min(1.0, max(0.0, vin)))))
    return {
        "time": time_s,
        "vin": vin,
        "d2": _logic(code & 4),
        "d1": _logic(code & 2),
        "d0": _logic(code & 1),
    }


def _trace_050() -> list[dict[str, float]]:
    vins = (-0.05, 0.14, 0.26, 0.43, 0.58, 0.76, 0.91, 1.20)
    return [_adc_row((101.0 + index * 3.7) * 1e-9, vin) for index, vin in enumerate(vins)]


def _trace_041() -> list[dict[str, float]]:
    return _stable_intervals(
        [
            {"rst": 0.9, "clk": 0.0, "vin": 0.45, "out": 0.45, "metric": 0.0},
            {"rst": 0.0, "clk": 0.9, "vin": 0.70, "out": 0.72, "metric": 0.72},
            {"rst": 0.0, "clk": 0.0, "vin": 0.70, "out": 0.22, "metric": 0.72},
            {"rst": 0.0, "clk": 0.9, "vin": 0.20, "out": 0.22, "metric": 0.72},
            {"rst": 0.0, "clk": 0.0, "vin": 0.20, "out": 0.68, "metric": 0.72},
        ]
    )


def _trace_042() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []

    def add(time_ns: float, sample: float, rst: float, vin: float, vout: float) -> None:
        rows.append({"time": time_ns * 1e-9, "sample": sample, "rst": rst, "vin": vin, "vout": vout})

    add(100.0, 0.0, 0.0, 0.22, 0.20)
    add(119.99, 0.0, 0.0, 0.22, 0.20)
    add(120.01, 0.9, 0.0, 0.22, 0.20)
    add(121.20, 0.9, 0.0, 0.22, 0.22)
    add(125.0, 0.0, 0.0, 0.22, 0.22)
    add(159.99, 0.0, 0.0, 0.82, 0.22)
    add(160.01, 0.9, 0.0, 0.82, 0.22)
    add(161.20, 0.9, 0.0, 0.82, 0.82)
    for index in range(12):
        time_ns = 162.0 + index * (42.0 / 11.0)
        vout = 0.80 - index * (0.12 / 11.0)
        add(time_ns, 0.0, 0.0, 0.82, vout)
    add(205.99, 0.0, 0.0, 0.82, 0.68)
    add(206.01, 0.0, 0.9, 0.82, 0.68)
    add(214.0, 0.0, 0.9, 0.34, 0.02)
    add(219.99, 0.0, 0.9, 0.34, 0.02)
    add(220.01, 0.0, 0.0, 0.34, 0.02)
    add(229.99, 0.0, 0.0, 0.34, 0.02)
    add(230.01, 0.9, 0.0, 0.34, 0.02)
    add(231.20, 0.9, 0.0, 0.34, 0.34)
    add(235.0, 0.0, 0.0, 0.34, 0.34)
    return rows


def _trace_043() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state_out = state_metric = 0.45
    scenarios = [
        (0.9, 0.45, 0.45, 0.45),
        (0.0, 0.82, 0.82, 0.61),
        (0.0, 0.45, 0.53, 0.61),
        (0.0, 0.18, 0.10, 0.29),
        (0.0, 0.45, 0.37, 0.29),
    ]
    for index, (rst, vin, next_out, next_metric) in enumerate(scenarios):
        edge = (101.0 + 2.0 * index) * 1e-9
        rows.append({"time": edge - 0.4e-9, "clk": 0.0, "rst": rst, "vin": vin,
                     "out": state_out, "metric": state_metric})
        rows.append({"time": edge, "clk": 0.9, "rst": rst, "vin": vin,
                     "out": state_out, "metric": state_metric})
        rows.append({"time": edge + 0.4e-9, "clk": 0.9, "rst": rst, "vin": vin,
                     "out": next_out, "metric": next_metric})
        rows.append({"time": edge + 0.8e-9, "clk": 0.0, "rst": rst, "vin": vin,
                     "out": next_out, "metric": next_metric})
        state_out, state_metric = next_out, next_metric
    return rows


def _trace_044() -> list[dict[str, float]]:
    rows = [
        {"time": 100.0e-9, "clk": 0.0, "rst": 0.9, "vin": 0.45, "out": 0.45, "metric": 0.0},
        {"time": 100.3e-9, "clk": 0.0, "rst": 0.9, "vin": 0.45, "out": 0.45, "metric": 0.0},
        {"time": 100.5e-9, "clk": 0.0, "rst": 0.0, "vin": 0.60, "out": 0.45, "metric": 0.0},
    ]
    state = 0.45
    step = 0.18
    for index, vin in enumerate((0.60, 0.30, 0.70, 0.20, 0.80), start=1):
        edge = (100.5 + 2.0 * index) * 1e-9
        rows.append({"time": edge - 0.2e-9, "clk": 0.0, "rst": 0.0, "vin": vin, "out": state, "metric": 0.9 if index > 4 else 0.0})
        rows.append({"time": edge, "clk": 0.9, "rst": 0.0, "vin": vin, "out": state, "metric": 0.9 if index > 4 else 0.0})
        if index <= 4:
            state += step if vin > 0.45 else -step
            state = min(0.85, max(0.05, state))
            step *= 0.5
        rows.append({"time": edge + 0.3e-9, "clk": 0.9, "rst": 0.0, "vin": vin, "out": state, "metric": 0.9 if index >= 4 else 0.0})
    return rows


def _trace_045() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(31):
        if index <= 10:
            diff = -0.10 + 0.02 * index
        elif index <= 20:
            diff = 0.10 - 0.02 * (index - 10)
        else:
            diff = -0.10
        rows.append(
            {
                "time": (100.0 + index) * 1e-9,
                "vinp": 0.50 + 0.5 * diff,
                "vinn": 0.50 - 0.5 * diff,
                "out_p": 0.85 if diff > 0.0 else 0.05,
            }
        )
    return rows


def _trace_046() -> list[dict[str, float]]:
    return _stable_intervals(
        [
            {"clk": 0.0, "rst": 0.9, "vin": 0.50, "out": 0.0, "metric": 0.0},
            {"clk": 0.0, "rst": 0.0, "vin": 0.50, "out": 0.06, "metric": 0.0},
            {"clk": 0.9, "rst": 0.0, "vin": 0.70, "out": 0.82, "metric": 0.9},
            {"clk": 0.0, "rst": 0.0, "vin": 0.58, "out": 0.80, "metric": 0.9},
            {"clk": 0.9, "rst": 0.0, "vin": 0.52, "out": 0.05, "metric": 0.0},
            {"clk": 0.0, "rst": 0.0, "vin": 0.62, "out": 0.06, "metric": 0.0},
            {"clk": 0.9, "rst": 0.0, "vin": 0.70, "out": 0.82, "metric": 0.9},
        ]
    )


def _trace_047() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(101):
        phase = index / 100.0
        vin = 1.6 * phase if phase <= 0.5 else 1.6 * (1.0 - phase)
        rows.append(
            {
                "time": (120.0 + index * 0.7) * 1e-9,
                "vin": vin,
                "out": 0.82 if 0.34 <= vin <= 0.56 else 0.05,
            }
        )
    return rows


def test_v4_repair_batch_05_checkers_accept_shifted_observable_traces() -> None:
    from checkers.v4.registry import load_checker

    traces = {
        "v4_041_rf_mixer_downconverter_macro": _trace_041(),
        "v4_042_sample_and_hold_with_droop_leakage": _trace_042(),
        "v4_043_soft_hysteretic_limiter": _trace_043(),
        "v4_044_successive_approximation_calibration_search_fsm": _trace_044(),
        "v4_045_threshold_comparator": _trace_045(),
        "v4_046_uvlo_brownout_detector": _trace_046(),
        "v4_047_window_comparator_detector": _trace_047(),
        "v4_048_bin_to_thermometer_decoder_8b": _trace_048(),
        "v4_049_thermometer_to_binary_encoder_8b": _trace_049(),
        "v4_050_dc_aware_adc3bit": _trace_050(),
    }
    for checker_id, rows in traces.items():
        checker = load_checker(checker_id)
        assert checker is not None, checker_id
        passed, detail = checker(rows)
        assert passed, (checker_id, detail)
        assert "mismatch_count=0" in detail


def test_v4_repair_batch_05_checker_diagnostics_are_structured_and_redacted() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_048_bin_to_thermometer_decoder_8b")
    assert checker is not None
    rows = _trace_048()
    for row in rows:
        row["th0"] = 0.9
    passed, detail = checker(rows)
    assert not passed
    for field in ("property_id=", "category=", "expected=", "observed=", "event="):
        assert field in detail
    assert "secret" not in detail.lower()
    assert "10ns" not in detail.lower()
