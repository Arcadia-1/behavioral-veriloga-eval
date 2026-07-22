from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.registry import load_checker  # noqa: E402
from checkers.v4.task_379 import CHECKER as check_379  # noqa: E402
from checkers.v4.task_379 import _rising_times, _sample_after, _v4_close, _v4_missing_columns  # noqa: E402


def _old_disabled_metric_skip_checker(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "rst", "sample_en", "vhold", "aperture_metric", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    hold = 0.0
    valid = False
    errors = 0
    checked = 0
    disabled_hold_checks = 0
    metric_nonzero = False
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        old_hold = hold
        if edge_row["rst"] > 0.45:
            hold = 0.0
            metric = 0.0
            valid = False
        elif edge_row["sample_en"] > 0.45:
            metric = min(0.9, 0.5 * abs(edge_row["vin"] - old_hold))
            hold = edge_row["vin"]
            valid = True
            metric_nonzero = metric_nonzero or metric > 0.03
        else:
            metric = None
            disabled_hold_checks += 1
        sample = _sample_after(rows, edge_t, 0.8e-9)
        if not _v4_close(sample["vhold"], hold, 0.06):
            errors += 1
        if metric is not None and not _v4_close(sample["aperture_metric"], metric, 0.06):
            errors += 1
        if (sample["valid"] > 0.45) != valid:
            errors += 1
        checked += 1
    ok = errors == 0 and checked >= 8 and disabled_hold_checks >= 1 and metric_nonzero
    return ok, f"old checked={checked} disabled_hold_checks={disabled_hold_checks} errors={errors}"


def _task379_rows(*, disabled_metric_drops: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    hold = 0.0
    metric = 0.0
    valid = 0.0
    events = (
        (0.35, True, True),
        (0.80, True, False),
        (0.15, False, False),
        (0.15, True, False),
        (0.65, True, False),
        (0.10, True, True),
        (0.70, False, False),
        (0.55, True, False),
        (0.30, False, False),
        (0.05, True, False),
    )
    for index, (vin, enabled, rst) in enumerate(events):
        edge = (2.0 + 6.0 * index) * 1e-9
        pre = {
            "time": edge - 0.2e-9,
            "vin": vin,
            "clk": 0.0,
            "rst": 0.9 if rst else 0.0,
            "sample_en": 0.9 if enabled else 0.0,
            "vhold": hold,
            "aperture_metric": metric,
            "valid": valid,
        }
        rows.append(pre)

        if rst:
            hold = 0.0
            metric = 0.0
            valid = 0.0
        elif enabled:
            metric = min(0.9, 0.5 * abs(vin - hold))
            hold = vin
            valid = 0.9

        rows.append({**pre, "time": edge, "clk": 0.9})
        observed_metric = 0.0 if disabled_metric_drops and not enabled and not rst else metric
        rows.append(
            {
                **pre,
                "time": edge + 1.0e-9,
                "clk": 0.9,
                "vhold": hold,
                "aperture_metric": observed_metric,
                "valid": valid,
            }
        )
    return rows


def _shift_and_scale(rows: list[dict[str, float]], *, offset: float = 2.0e-9, scale: float = 1.31):
    shifted = copy.deepcopy(rows)
    for row in shifted:
        row["time"] = row["time"] * scale + offset
    return shifted


def test_379_disabled_edges_hold_last_aperture_metric_old_pass_new_fail() -> None:
    bad_rows = _task379_rows(disabled_metric_drops=True)

    assert _old_disabled_metric_skip_checker(bad_rows)[0]
    passed, detail = check_379(bad_rows)

    assert not passed
    assert "errors=" in detail


def test_379_gold_reset_recovery_and_registry_timing_invariance() -> None:
    rows = _task379_rows()
    registry_checker = load_checker("v4_379_periodic_sampler_aperture_metric")

    assert check_379(rows)[0]
    assert registry_checker is not None
    assert registry_checker(rows)[0]
    assert registry_checker(_shift_and_scale(rows))[0]


def test_379_active_state_mutations_are_rejected() -> None:
    bad_hold = _task379_rows()
    bad_hold[11]["vhold"] = 0.55

    bad_reset = _task379_rows()
    bad_reset[17]["aperture_metric"] = 0.25

    assert not check_379(bad_hold)[0]
    assert not check_379(bad_reset)[0]
