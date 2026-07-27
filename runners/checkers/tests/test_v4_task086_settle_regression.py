from __future__ import annotations

from runners.checkers.v4.task_086 import edge_settled_values


def test_task086_samples_the_post_transition_plateau_on_coarse_traces() -> None:
    edge_row = {"time": 1.0e-9, "clk": 0.9, "rst": 0.0, "trim_mon": 0.45}
    rows = [
        {"time": 0.9e-9, "clk": 0.0, "rst": 0.0, "trim_mon": 0.45},
        edge_row,
        {"time": 1.2e-9, "clk": 0.9, "rst": 0.0, "trim_mon": 0.45},
        {"time": 1.4e-9, "clk": 0.9, "rst": 0.0, "trim_mon": 0.32},
    ]

    assert edge_settled_values(rows, "trim_mon") == [(edge_row, 0.32)]
