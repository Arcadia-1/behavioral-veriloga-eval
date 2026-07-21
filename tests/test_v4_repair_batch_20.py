from __future__ import annotations

from pathlib import Path

from runners.checkers.v4.task_193 import CHECKER as check_193
from runners.checkers.v4.task_195 import CHECKER as check_195
from runners.checkers.v4.task_196 import CHECKER as check_196
from runners.checkers.v4.task_197 import CHECKER as check_197
from runners.checkers.v4.task_200 import CHECKER as check_200


ROOT = Path(__file__).resolve().parents[1]
CHECKER_FILES = [
    ROOT / "runners/checkers/v4/task_193.py",
    ROOT / "runners/checkers/v4/task_195.py",
    ROOT / "runners/checkers/v4/task_196.py",
    ROOT / "runners/checkers/v4/task_197.py",
    ROOT / "runners/checkers/v4/task_200.py",
]


def _scaled_shifted(rows: list[dict[str, float]], *, scale: float = 1.7, shift: float = 4e-9):
    return [{**row, "time": shift + scale * row["time"]} for row in rows]


def test_batch_20_repaired_checkers_do_not_use_fixed_sample_maps() -> None:
    for path in CHECKER_FILES:
        text = path.read_text()
        assert "_sample_many" not in text
        assert "_sample_many_within_trace" not in text
        assert "sample_at=" not in text


def test_batch_20_repaired_checkers_reject_underexcited_traces() -> None:
    traces = [
        (
            check_193,
            {
                "time": 0.0,
                "in1": 0.0,
                "in2": 0.0,
                "up": 0.0,
                "dn": 0.0,
                "vdd": 1.0,
                "gnd": 0.0,
            },
        ),
        (
            check_195,
            {"time": 0.0, "rst": 0.0, "s": 0.0, "nc": 0.0, "res": 0.0, "conv": 0.0},
        ),
        (
            check_196,
            {"time": 0.0, "vlocal_osc": 0.0, "vin_rf": 0.1, "vif": 0.0},
        ),
        (
            check_197,
            {
                "time": 0.0,
                "din0": 0.0,
                "din1": 0.0,
                "din2": 0.0,
                "din3": 0.0,
                "din4": 0.0,
                "din5": 0.0,
                "din6": 0.0,
                "dout": 0.0,
            },
        ),
        (
            check_200,
            {
                "time": 0.0,
                "rdy": 0.0,
                "din1": 0.0,
                "din2": 0.0,
                "din3": 0.0,
                "din4": 0.0,
                "aout": 0.0,
            },
        ),
    ]
    for checker, row in traces:
        ok, note = checker([row, {**row, "time": 1e-9}])
        assert not ok
        assert "insufficient_excitation" in note


def test_batch_20_checkers_accept_observable_relative_time_changes() -> None:
    assert check_193(_make_pfd_rows(scale=1.6, shift=2e-9))[0]
    assert check_195(_scaled_shifted(_make_sequence_rows(), scale=1.0))[0]
    assert check_196(_scaled_shifted(_make_chopper_rows()))[0]
    assert check_197(_scaled_shifted(_make_weighted_adc_rows()))[0]
    assert check_200(_scaled_shifted(_make_cdac_rows()))[0]


def _make_pfd_rows(*, scale: float = 1.0, shift: float = 0.0) -> list[dict[str, float]]:
    edge_events = [
        (shift + scale * 0.92e-9, "in1"),
        (shift + scale * 1.47e-9, "in2"),
        (shift + scale * 2.57e-9, "in2"),
        (shift + scale * 3.02e-9, "in1"),
    ]

    def state_at(time_s: float) -> tuple[float, float]:
        state = 0
        hide_until = -1.0
        for event_time, signal in edge_events:
            if time_s < event_time:
                break
            if hide_until > 0.0 and time_s >= hide_until:
                state = 0
                hide_until = -1.0
            if signal == "in1":
                if state == -1:
                    hide_until = event_time + scale * 120e-12
                else:
                    state = 1
            else:
                if state == 1:
                    hide_until = event_time + scale * 120e-12
                else:
                    state = -1
        if hide_until > 0.0 and time_s < hide_until:
            return 1.0, 1.0
        if hide_until > 0.0 and time_s >= hide_until:
            state = 0
        if state == 1:
            return 1.0, 0.0
        if state == -1:
            return 0.0, 1.0
        return 0.0, 0.0

    rows: list[dict[str, float]] = []
    stop = shift + scale * 4.5e-9
    step = (stop - shift) / 900
    for index in range(901):
        time_s = shift + index * step
        source_time = (time_s - shift) / scale
        up, dn = state_at(time_s)
        rows.append(
            {
                "time": time_s,
                "in1": 1.0 if 0.92e-9 <= source_time < 1.22e-9 or 3.02e-9 <= source_time < 3.32e-9 else 0.0,
                "in2": 1.0 if 1.47e-9 <= source_time < 1.77e-9 or 2.57e-9 <= source_time < 2.87e-9 else 0.0,
                "up": up,
                "dn": dn,
                "vdd": 1.0,
                "gnd": 0.0,
            }
        )
    return rows


def _make_sequence_rows() -> list[dict[str, float]]:
    windows = {
        "rst": [(0.0, 0.2)],
        "s": [(1.0, 1.8), (9.0, 9.8)],
        "nc": [(2.0, 2.25), (10.0, 10.25)],
        "res": [(3.0, 3.25), (4.5, 4.75), (6.0, 6.25), (7.5, 7.75)],
        "conv": [(3.0, 7.0), (11.0, 15.0)],
    }
    rows: list[dict[str, float]] = []
    for index in range(901):
        time_s = index * 20e-12
        frame_ns = (time_s % 16e-9) * 1e9
        row = {"time": time_s}
        for signal, signal_windows in windows.items():
            row[signal] = 1.1 if any(start <= frame_ns < end for start, end in signal_windows) else 0.0
        rows.append(row)
    return rows


def _make_chopper_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(401):
        time_s = index * 10e-12
        lo = -0.5 if time_s < 1e-9 or 2e-9 <= time_s < 3e-9 else 0.5
        rf = 0.10 if time_s < 1e-9 else 0.20 if time_s < 2e-9 else -0.16 if time_s < 3e-9 else -0.24
        rows.append(
            {
                "time": time_s,
                "vlocal_osc": lo,
                "vin_rf": rf,
                "vif": 1.25 * (rf if lo > 0 else -rf),
            }
        )
    return rows


def _make_weighted_adc_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    vectors = [
        (0, 0, 0, 0, 0, 0, 0),
        (1, 0, 1, 0, 1, 0, 1),
        (0, 1, 0, 1, 0, 1, 0),
        (1, 1, 1, 1, 1, 1, 1),
    ]
    weights = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0)
    for plateau_index, vector in enumerate(vectors):
        for sample in range(20):
            row = {
                "time": (plateau_index * 20 + sample) * 50e-12,
                "dout": sum(weight for bit, weight in zip(vector, weights) if bit) / 32.0,
            }
            row.update({f"din{bit}": 0.9 * vector[bit] for bit in range(7)})
            rows.append(row)
    return rows


def _make_cdac_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    ready_edges = [0.2e-9, 1.2e-9, 2.2e-9, 3.2e-9]
    aout = 0.0

    def vector_at(time_s: float) -> tuple[int, int, int, int]:
        if time_s < 2.05e-9:
            return (0, 0, 0, 0)
        if time_s < 3.05e-9:
            return (0, 1, 0, 1)
        return (1, 1, 1, 1)

    for index in range(400):
        time_s = index * 10e-12
        if any(abs(time_s - (edge + 20e-12)) < 5e-12 for edge in ready_edges[1:]):
            vector = vector_at(time_s)
            switched = sum(
                weight for bit, weight in zip(vector, (0.5, 1.0, 2.0, 4.0)) if bit
            )
            aout = switched / 8.5 * 2.0 * 1.1 - 1.1
        vector = vector_at(time_s)
        row = {
            "time": time_s,
            "rdy": 1.1 if any(edge <= time_s < edge + 0.4e-9 for edge in ready_edges) else 0.0,
            "aout": aout,
        }
        row.update({f"din{bit + 1}": 1.1 * vector[bit] for bit in range(4)})
        rows.append(row)
    return rows
