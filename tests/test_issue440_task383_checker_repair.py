from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_383 import CHECKER, CHECKER_ID  # noqa: E402
from checkers.v4.canonical_320_400 import CHECKERS  # noqa: E402


VDD = 0.9
PERIOD = 20e-9
HALF_PERIOD = PERIOD / 2.0
WINDOWS = (
    (5.2e-9, 54.0e-9),
    (64.2e-9, 112.0e-9),
    (118.2e-9, 150.0e-9),
    (160.2e-9, 195.0e-9),
)
STOP = 195e-9


def _enabled_at(t: float) -> bool:
    return any(start <= t <= end for start, end in WINDOWS)


def _rst_at(t: float) -> bool:
    return t <= 3.2e-9 or 112.2e-9 <= t <= 118.0e-9


def _segment_start(t: float) -> float | None:
    for start, end in WINDOWS:
        if start <= t <= end:
            return start
    return None


def _logic(condition: bool) -> float:
    return VDD if condition else 0.0


def _gold_rows(
    dt: float = 0.5e-9,
    shift: float = 0.0,
    *,
    high_first: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    count = int(STOP / dt) + 1
    for index in range(count + 1):
        local_t = index * dt
        t = local_t + shift
        enabled = _enabled_at(local_t) and not _rst_at(local_t)
        start = _segment_start(local_t)
        osc_high = False
        valid_high = False
        metric = 0.0
        if enabled and start is not None:
            elapsed = local_t - start
            half_cycles = int(elapsed // HALF_PERIOD)
            osc_high = (half_cycles % 2 == 0) if high_first else (half_cycles % 2 == 1)
            valid_high = elapsed >= PERIOD
            metric = 0.45 if valid_high else 0.0
        rows.append(
            {
                "time": t,
                "enable": _logic(_enabled_at(local_t)),
                "rst": _logic(_rst_at(local_t)),
                "osc_out": _logic(osc_high),
                "period_metric": metric,
                "valid": _logic(valid_high),
            }
        )
    return rows


def _old_checker(rows: list[dict[str, float]]) -> tuple[bool, str]:
    checked = metric_errors = clear_errors = 0
    reset_clear = disabled_clear = osc_activity = valid_seen = reenable_seen = False
    osc_vals: list[float] = []
    prev_osc = float(rows[0].get("osc_out", 0.0))
    first_reenable_rise: float | None = None
    for row in rows[::6]:
        t = float(row["time"])
        rst = row["rst"] > 0.45
        enabled = row["enable"] > 0.45 and not rst
        if not enabled:
            clear = row["osc_out"] < 0.12 and row["period_metric"] < 0.08 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (54e-9 < t < 64e-9 and clear)
            if ((rst and t < 5e-9) or (54e-9 < t < 64e-9)) and not clear:
                clear_errors += 1
            continue
        reenable_seen = reenable_seen or t > 64e-9
        osc_vals.append(float(row["osc_out"]))
        if t > 64e-9 and first_reenable_rise is None and prev_osc < 0.30 and float(row["osc_out"]) > 0.65:
            first_reenable_rise = t
        valid_seen = valid_seen or row["valid"] > 0.45
        checked += 1
        if abs(float(row["period_metric"]) - 0.45) > 0.10 and t > 12e-9:
            metric_errors += 1
        prev_osc = float(row["osc_out"])
    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    restart_timing_ok = first_reenable_rise is not None and 72e-9 <= first_reenable_rise <= 77e-9
    ok = checked >= 12 and reset_clear and disabled_clear and reenable_seen and restart_timing_ok and osc_activity and valid_seen and metric_errors <= 4 and clear_errors <= 4
    return ok, f"old restart_timing_ok={restart_timing_ok}"


def _one_shot_rows() -> list[dict[str, float]]:
    rows = _gold_rows()
    for row in rows:
        start = _segment_start(row["time"])
        enabled = start is not None and row["enable"] > 0.45 and row["rst"] <= 0.45
        if enabled:
            elapsed = row["time"] - start
            row["osc_out"] = _logic(HALF_PERIOD <= elapsed < PERIOD)
            row["period_metric"] = 0.45
            row["valid"] = _logic(elapsed >= PERIOD)
    return rows


def _mutate(rows: list[dict[str, float]], name: str) -> list[dict[str, float]]:
    mutated = [dict(row) for row in rows]
    for row in mutated:
        if name == "zero":
            row["osc_out"] = row["period_metric"] = row["valid"] = 0.0
        elif name == "half_scale":
            row["osc_out"] *= 0.5
            row["valid"] *= 0.5
        elif name == "inverted_transfer":
            row["osc_out"] = VDD - row["osc_out"]
        elif name == "early_valid":
            if _segment_start(row["time"]) is not None and row["enable"] > 0.45 and row["rst"] <= 0.45:
                row["valid"] = VDD
                row["period_metric"] = 0.45
        elif name == "no_disable_clear":
            if row["enable"] <= 0.45 and row["rst"] <= 0.45:
                row["osc_out"] = row["valid"] = row["period_metric"] = VDD
        elif name == "late_restart":
            start = _segment_start(row["time"])
            if start is not None and start >= 64e-9 and row["enable"] > 0.45 and row["rst"] <= 0.45:
                elapsed = max(0.0, row["time"] - start - 4e-9)
                half_cycles = int(elapsed // HALF_PERIOD)
                row["osc_out"] = _logic(half_cycles % 2 == 1)
                row["valid"] = _logic(elapsed >= PERIOD)
                row["period_metric"] = 0.45 if elapsed >= PERIOD else 0.0
        else:
            raise AssertionError(name)
    return mutated


def test_task383_gold_trace_passes_and_uses_registry_id() -> None:
    assert CHECKER_ID == "v4_383_fixed_frequency_oscillator_source"
    ok, note = CHECKER(_gold_rows())
    assert ok, note
    registry_ok, registry_note = CHECKERS[CHECKER_ID](_gold_rows())
    assert registry_ok, registry_note


def test_task383_checker_rejects_old_pass_one_shot() -> None:
    rows = _one_shot_rows()
    old_ok, old_note = _old_checker(rows)
    assert old_ok, old_note
    ok, note = CHECKER(rows)
    assert not ok
    assert "P_PERIODIC_OSCILLATION mismatch_count=" in note
    registry_ok, registry_note = CHECKERS[CHECKER_ID](rows)
    assert not registry_ok, registry_note


def test_task383_checker_rejects_active_mutations() -> None:
    rows = _gold_rows()
    for mutation in ("zero", "half_scale", "inverted_transfer", "early_valid", "no_disable_clear", "late_restart"):
        ok, note = CHECKER(_mutate(rows, mutation))
        assert not ok, (mutation, note)


def test_task383_checker_is_stable_under_time_prefix_shift_and_sparse_rows() -> None:
    shifted = _gold_rows(shift=0.7e-9)
    sparse = shifted[::2]
    ok, note = CHECKER(sparse)
    assert ok, note


def test_task383_checker_accepts_deterministic_high_first_restart_phase() -> None:
    ok, note = CHECKER(_gold_rows(high_first=True))
    assert ok, note


def test_task383_harness_metadata_matches_extended_score_deck() -> None:
    task = (
        ROOT
        / "benchmark-vabench-release-v4/release/benchmarkv4/tasks"
        / "383-fixed-frequency-oscillator-source/evaluator"
    )
    harness_path = task / "harness_spec.json"
    harness = json.loads(harness_path.read_text())
    score_deck = task / "score_tb.scs"
    assert harness["deck"]["analyses"] == ["tran tran stop=195n maxstep=200p"]
    assert harness["deck"]["body_lines"][:2] == score_deck.read_text().splitlines()[5:7]
    assert harness["migration"]["legacy_score_deck_sha256"] == hashlib.sha256(
        score_deck.read_bytes()
    ).hexdigest()
    harness_hash = hashlib.sha256(harness_path.read_bytes()).hexdigest()
    for profile_name in ("feedback", "score"):
        profile = json.loads((task / "profiles" / f"{profile_name}.json").read_text())
        assert harness["profile_defaults"][profile_name]["parameters"]["stop_time"] == "200n"
        assert profile["parameters"]["stop_time"] == "200n"
        assert profile["harness_spec_sha256"] == harness_hash
