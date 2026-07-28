from __future__ import annotations

from runners.checkers.v4.task_154 import check_v3_flash_adc_threshold_taps
from runners.checkers.v4.task_203 import check_v3_cdac_8b_monodown
from runners.checkers.v4.task_209 import check_v3_dac_restore_6bit_1p8
from runners.checkers.v4.task_234 import check_v3_programmable_divider_by_n


def _flash_expected(vin: float) -> list[float]:
    tap_indices = [1, 5, 10, 15, 20, 25, 30]
    thresholds = [-0.125 + tap * (0.25 / 31.0) for tap in tap_indices]
    return [0.9 if vin > threshold else 0.0 for threshold in thresholds]


def _task154_rows(*, wrong_stable: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    previous = [0.0] * 7
    for edge_index, edge_ns in enumerate([5.0, 2005.0, 4005.0, 6005.0]):
        vin = [-0.20, -0.05, 0.05, 0.20][edge_index]
        expected = _flash_expected(vin)
        stable = [0.0] * 7 if wrong_stable and edge_index == 3 else expected
        rows.append({"time": (edge_ns - 1.0) * 1e-9, "vin": vin, "clk": 0.0, **{f"dout{i}": previous[i] for i in range(7)}})
        rows.append({"time": edge_ns * 1e-9, "vin": vin, "clk": 0.9, **{f"dout{i}": previous[i] for i in range(7)}})
        rows.append({"time": (edge_ns + 3.125) * 1e-9, "vin": vin, "clk": 0.0, **{f"dout{i}": stable[i] for i in range(7)}})
        previous = expected
    return rows


def test_task154_samples_next_grid_point_after_clocked_transition() -> None:
    rows = _task154_rows()
    ok, note = check_v3_flash_adc_threshold_taps(rows)
    assert ok, note


def _task203_rows(*, wrong_stable: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    controls = {f"dctrl{i}": 0.0 for i in range(8)}
    residue = 1.0

    def add_row(time_ns: float, *, clks: float, vres: float) -> None:
        rows.append({"time": time_ns * 1e-9, "vin": 1.0, "clks": clks, "vres": vres, **controls})

    add_row(0.0, clks=0.9, vres=residue)
    add_row(0.9, clks=0.9, vres=residue)
    add_row(1.1, clks=0.0, vres=0.0)
    add_row(1.4, clks=0.0, vres=residue)
    for bit, event_ns in [(7, 2.0), (6, 3.0), (5, 4.0), (4, 5.0)]:
        before = residue
        after = residue - 1.0 / (2 ** (8 - bit))
        add_row(event_ns - 0.1, clks=0.0, vres=before)
        controls[f"dctrl{bit}"] = 0.9
        add_row(event_ns + 0.1, clks=0.0, vres=before)
        stable = after + 0.12 if wrong_stable and bit == 4 else after
        add_row(event_ns + 0.4, clks=0.0, vres=stable)
        residue = after
    return rows


def test_task203_samples_next_grid_point_after_cdac_event() -> None:
    rows = _task203_rows()
    ok, note = check_v3_cdac_8b_monodown(rows)
    assert ok, note


def _restore_rows_for_code(
    edge_ns: float,
    code: int,
    previous_vout: float,
    *,
    wrong_stable: bool = False,
) -> list[dict[str, float]]:
    bits = {
        "d1": 1.8 if code & 32 else 0.0,
        "d2": 1.8 if code & 16 else 0.0,
        "d3": 1.8 if code & 8 else 0.0,
        "d4": 1.8 if code & 4 else 0.0,
        "d5": 1.8 if code & 2 else 0.0,
        "d6": 1.8 if code & 1 else 0.0,
    }
    expected = (code + 0.5) * 3.6 / 64.0 - 1.8
    stable = expected + 0.12 if wrong_stable else expected
    return [
        {"time": (edge_ns - 0.1) * 1e-9, "clk": 0.0, "vout": previous_vout, **bits},
        {"time": (edge_ns + 0.1) * 1e-9, "clk": 1.8, "vout": previous_vout, **bits},
        {"time": (edge_ns + 0.3) * 1e-9, "clk": 0.0, "vout": stable, **bits},
    ]


def _task209_rows(*, wrong_stable: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    previous_vout = 0.0
    for index, (edge_ns, code) in enumerate([(10.0, 0), (20.0, 63), (30.0, 1), (40.0, 2)]):
        rows.extend(_restore_rows_for_code(edge_ns, code, previous_vout, wrong_stable=wrong_stable and index == 3))
        previous_vout = (code + 0.5) * 3.6 / 64.0 - 1.8
    return rows


def test_task209_samples_next_grid_point_after_restore_clock() -> None:
    rows = _task209_rows()
    ok, note = check_v3_dac_restore_6bit_1p8(rows)
    assert ok, note


def _task234_rows(*, wrong_stable: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    previous_out = 0.0
    for edge_index, edge_ns in enumerate([10.0, 20.0, 30.0, 40.0], start=1):
        want = 0.9 if edge_index % 2 == 0 else 0.0
        stable = 0.0 if wrong_stable and edge_index == 4 else want
        rows.append({"time": (edge_ns - 0.1) * 1e-9, "clk": 0.0, "divctrl": 2.0, "out": previous_out})
        rows.append({"time": (edge_ns + 0.1) * 1e-9, "clk": 0.9, "divctrl": 2.0, "out": previous_out})
        rows.append({"time": (edge_ns + 0.3) * 1e-9, "clk": 0.0, "divctrl": 2.0, "out": stable})
        previous_out = want
    return rows


def test_task234_samples_next_grid_point_after_divider_edge() -> None:
    rows = _task234_rows()
    ok, note = check_v3_programmable_divider_by_n(rows)
    assert ok, note


def test_event_probe_grid_alignment_rejects_wrong_stable_values() -> None:
    cases = [
        (check_v3_flash_adc_threshold_taps, _task154_rows(wrong_stable=True)),
        (check_v3_cdac_8b_monodown, _task203_rows(wrong_stable=True)),
        (check_v3_dac_restore_6bit_1p8, _task209_rows(wrong_stable=True)),
        (check_v3_programmable_divider_by_n, _task234_rows(wrong_stable=True)),
    ]
    for checker, rows in cases:
        ok, note = checker(rows)
        assert not ok, note
