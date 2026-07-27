from __future__ import annotations

from runners.checkers.v4.registry import load_checker


VDD = 0.9
PERIOD_NS = 8.0


def _check(rows: list[dict[str, float]]) -> tuple[bool, str]:
    checker = load_checker("v4_079_ramp_step_source")
    assert checker is not None
    return checker(rows)


def _spectre_adaptive_rows() -> list[dict[str, float]]:
    """Reduced form of the archived v4-1079 Spectre accepted-step trace."""
    first_sample_ns = (
        0.0,
        0.308596963451411,
        0.41779089035424,
        0.02698481725706,
        0.13617874415986,
    )
    common_samples_ns = (
        0.5,
        1.0,
        1.5,
        1.8,
        2.0,
        2.5,
        3.0,
        3.5,
        4.0,
        4.5,
        5.0,
        5.5,
        6.0,
        6.5,
        7.0,
        7.5,
    )
    rows: list[dict[str, float]] = []
    for cycle, first_ns in enumerate(first_sample_ns):
        for offset_ns in sorted({first_ns, *common_samples_ns}):
            time_ns = cycle * PERIOD_NS + offset_ns
            if time_ns > 34.0:
                continue
            phase = offset_ns / PERIOD_NS
            rows.append(
                {
                    "time": time_ns * 1.0e-9,
                    "VDD": VDD,
                    "VSS": 0.0,
                    "phase_out": VDD * phase,
                    "guard_out": VDD if offset_ns < 1.5 else 0.0,
                }
            )
    return sorted(rows, key=lambda row: row["time"])


def _evas_quantized_rows() -> list[dict[str, float]]:
    """Model the accepted-step quantization in the archived EVAS replay."""
    phase_origin_ns = 0.3125
    rows: list[dict[str, float]] = []
    for sample in range(137):
        time_ns = sample * 0.25
        phase_time_ns = (time_ns - phase_origin_ns) % PERIOD_NS
        rows.append(
            {
                "time": time_ns * 1.0e-9,
                "VDD": VDD,
                "VSS": 0.0,
                "phase_out": VDD * phase_time_ns / PERIOD_NS,
                "guard_out": VDD if phase_time_ns < 1.5 else 0.0,
            }
        )
    return rows


def test_079_adaptive_post_wrap_samples_do_not_shift_the_phase_epoch() -> None:
    ok, note = _check(_spectre_adaptive_rows())
    assert ok, note


def test_079_quantized_evas_wrap_samples_remain_accepted() -> None:
    ok, note = _check(_evas_quantized_rows())
    assert ok, note


def test_079_bad_phase_mutation_remains_rejected() -> None:
    rows = [
        {
            **row,
            "phase_out": 0.0 if row["time"] >= 16.0e-9 else row["phase_out"],
        }
        for row in _spectre_adaptive_rows()
    ]
    ok, _note = _check(rows)
    assert not ok
