from __future__ import annotations

from runners.checkers.common.issue109_split import (
    _is_settled,
    _stimulus_change_times,
)


def test_transition_breakpoint_is_not_treated_as_a_steady_state_sample() -> None:
    rows = [
        {"time": 5.80e-9, "en": 0.9, "ctrl0": 0.9},
        {"time": 5.85e-9, "en": 0.0, "ctrl0": 0.9},
        {"time": 5.90e-9, "en": 0.0, "ctrl0": 0.9},
        {"time": 5.95e-9, "en": 0.0, "ctrl0": 0.9},
    ]

    changes = _stimulus_change_times(rows, ("en", "ctrl0"))

    assert changes == [5.85e-9]
    assert not _is_settled(changes, 5.85e-9, 100e-12)
    assert not _is_settled(changes, 5.90e-9, 100e-12)
    assert _is_settled(changes, 5.95e-9, 100e-12)
