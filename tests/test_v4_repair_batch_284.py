from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))


BATCH_284_CHECKERS = (
    "v4_061_event_counter_windowed_16b",
    "v4_062_latency_counter_ready_valid_12b",
    "v4_063_settling_window_detector",
    "v4_064_edge_delay_line_with_deglitch",
    "v4_065_enable_gated_clock_pulse",
    "v4_066_configurable_polarity_edge_detector",
    "v4_067_adc_static_linearity_monitor",
    "v4_068_multiphase_clock_generator_4ph",
    "v4_069_configurable_pulse_train_generator",
    "v4_070_jittered_clock_source_deterministic",
)


def test_batch_284_checkers_return_structured_redacted_missing_trace_diagnostics() -> None:
    from checkers.v4.registry import load_checker

    for checker_id in BATCH_284_CHECKERS:
        checker = load_checker(checker_id)
        assert checker is not None, checker_id
        passed, detail = checker([])
        assert not passed, checker_id
        assert "property_id=" in detail, (checker_id, detail)
        assert "category=invalid_trace" in detail, (checker_id, detail)
        assert "event=full_trace" in detail, (checker_id, detail)


def _step(time_s: float, initial: float, transitions: tuple[tuple[float, float], ...]) -> float:
    value = initial
    for edge_s, next_value in transitions:
        if time_s >= edge_s:
            value = next_value
    return value


def _batch_064_shifted_trace(start_s: float = 300e-9) -> list[dict[str, float]]:
    vin_edges = (
        (start_s + 5.0e-9, 0.9),
        (start_s + 15.0e-9, 0.0),
        (start_s + 25.0e-9, 0.9),
        (start_s + 25.4e-9, 0.0),
        (start_s + 35.0e-9, 0.9),
        (start_s + 45.0e-9, 0.0),
    )
    vout_edges = (
        (start_s + 7.2e-9, 0.9),
        (start_s + 17.2e-9, 0.0),
        (start_s + 37.2e-9, 0.9),
        (start_s + 47.2e-9, 0.0),
    )
    rst_edges = ((start_s + 1.0e-9, 0.0),)
    enable_edges = ((start_s + 2.0e-9, 0.9), (start_s + 50.0e-9, 0.0), (start_s + 54.0e-9, 0.9))
    valid_windows = tuple((edge_s, 0.9) for edge_s, _ in vout_edges) + tuple(
        (edge_s + 0.5e-9, 0.0) for edge_s, _ in vout_edges
    )
    rejected_edges = ((start_s + 25.45e-9, 0.9), (start_s + 26.0e-9, 0.0))
    sample_times = {
        start_s,
        start_s + 0.5e-9,
        start_s + 1.5e-9,
        start_s + 3.0e-9,
        start_s + 52.0e-9,
        start_s + 56.0e-9,
    }
    for edge_s, _ in vin_edges + vout_edges + rst_edges + enable_edges + valid_windows + rejected_edges:
        sample_times.update({edge_s - 0.05e-9, edge_s, edge_s + 0.05e-9, edge_s + 0.8e-9})
    rows: list[dict[str, float]] = []
    for time_s in sorted(sample_times):
        rows.append(
            {
                "time": time_s,
                "vin": _step(time_s, 0.0, vin_edges),
                "rst": _step(time_s, 0.9, rst_edges),
                "enable": _step(time_s, 0.0, enable_edges),
                "vout": _step(time_s, 0.0, vout_edges),
                "edge_valid": _step(time_s, 0.0, tuple(sorted(valid_windows))),
                "rejected": _step(time_s, 0.0, rejected_edges),
            }
        )
    return rows


def test_batch_064_checker_uses_observed_disable_event_not_absolute_window() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_064_edge_delay_line_with_deglitch")
    assert checker is not None
    passed, detail = checker(_batch_064_shifted_trace())
    assert passed, detail


def test_batch_063_checker_rejects_settled_high_outside_tolerance_window() -> None:
    from checkers.v4.registry import load_checker

    rows: list[dict[str, float]] = []
    for time_ns in range(101):
        in_valid_window = 40 <= time_ns < 75
        in_wide_only_window = time_ns < 30
        settled = 0.9 if (20 <= time_ns < 30 or 60 <= time_ns < 75) else 0.0
        entry_code = 40 if in_valid_window else 0
        row = {
            "time": time_ns * 1e-9,
            "vin": 0.51 if in_valid_window else (0.58 if in_wide_only_window else 0.7),
            "target": 0.5,
            "tol": 0.05,
            "settled": settled,
        }
        row.update(
            {f"t_code{bit}": 0.9 if entry_code & (1 << bit) else 0.0 for bit in range(8)}
        )
        rows.append(row)

    checker = load_checker("v4_063_settling_window_detector")
    assert checker is not None
    passed, detail = checker(rows)
    assert not passed
    assert "property_id=P_WINDOW_DEFINITION" in detail
    assert "settled=low_outside_tolerance_window" in detail
