from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
TASK_695 = (
    ROOT
    / "benchmark-vabench-release-v4/release/benchmarkv4-r51/tasks"
    / "695-clock-sample-1600n-sequencer-testbench"
)
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_077 import CHECKER as check_077  # noqa: E402
from checkers.v4.task_195 import CHECKER as check_195  # noqa: E402


SEQUENCE_077 = (-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5)


def _transitioned_sequence_value(time_s: float, *, sigma: float, dt: float) -> float:
    interval = math.floor(time_s / dt + 1e-9)
    phase = (time_s - interval * dt) / dt
    current = sigma * SEQUENCE_077[interval % len(SEQUENCE_077)]
    if interval == 0 or phase > 1e-9:
        if phase >= 0.10:
            return current
        previous = sigma * SEQUENCE_077[(interval - 1) % len(SEQUENCE_077)]
        return previous + (current - previous) * phase / 0.10
    return sigma * SEQUENCE_077[(interval - 1) % len(SEQUENCE_077)]


def _sparse_077_rows(*, mutation: str | None = None) -> list[dict[str, float]]:
    default_dt = 0.5e-9
    override_dt = 0.8e-9
    stop = 20e-9
    sample_times = {0.0, stop}
    for dt in (default_dt, override_dt):
        interval_count = round(stop / dt)
        for interval in range(interval_count + 1):
            start = interval * dt
            for phase in (0.0, 0.10, 0.60):
                time_s = start + phase * dt
                if time_s <= stop:
                    sample_times.add(time_s)

    vin = 0.62
    rows = [
        {
            "time": time_s,
            "vin_i": vin,
            "vout_default": vin
            + _transitioned_sequence_value(time_s, sigma=0.01, dt=default_dt),
            "vout_override": vin
            + _transitioned_sequence_value(time_s, sigma=0.037, dt=override_dt),
        }
        for time_s in sorted(sample_times)
    ]
    for row in rows:
        if mutation == "zero":
            row["vout_default"] = 0.0
            row["vout_override"] = 0.0
        elif mutation == "passthrough":
            row["vout_default"] = row["vin_i"]
            row["vout_override"] = row["vin_i"]
        elif mutation == "too_large_noise":
            row["vout_default"] = row["vin_i"] + 2.0 * (
                row["vout_default"] - row["vin_i"]
            )
            row["vout_override"] = row["vin_i"] + 2.0 * (
                row["vout_override"] - row["vin_i"]
            )
        elif mutation == "biased_noise":
            row["vout_default"] += 0.12
            row["vout_override"] += 0.12
        elif mutation == "metric_scale_low":
            row["vout_default"] *= 0.42
            row["vout_override"] *= 0.42
    return rows


def test_077_accepts_correct_behavior_on_sparse_adaptive_time_grid() -> None:
    rows = _sparse_077_rows()
    first_stable_rows = [row for row in rows if 0.06e-9 <= row["time"] < 0.5e-9]
    assert len(first_stable_rows) == 3

    passed, detail = check_077(rows)

    assert passed, detail


@pytest.mark.parametrize(
    "mutation",
    ["zero", "passthrough", "too_large_noise", "biased_noise", "metric_scale_low"],
)
def test_077_still_rejects_semantic_mutations_on_sparse_grid(mutation: str) -> None:
    passed, _ = check_077(_sparse_077_rows(mutation=mutation))

    assert not passed


WINDOWS_195 = {
    "rst": ((0.0, 0.2),),
    "s": ((1.0, 1.8), (9.0, 9.8)),
    "nc": ((2.0, 2.25), (10.0, 10.25)),
    "res": ((3.0, 3.25), (4.5, 4.75), (6.0, 6.25), (7.5, 7.75)),
    "conv": ((3.0, 7.0), (11.0, 15.0)),
}


def _sequencer_195_rows(
    *,
    stop_ns: float = 16.5,
    mutation: str | None = None,
) -> list[dict[str, float]]:
    step_ns = 0.06
    sample_times_ns = [
        index * step_ns for index in range(math.floor(stop_ns / step_ns) + 1)
    ]
    if sample_times_ns[-1] < stop_ns:
        sample_times_ns.append(stop_ns)

    rows: list[dict[str, float]] = []
    for time_ns in sample_times_ns:
        frame_ns = time_ns % 16.0
        row = {"time": time_ns * 1e-9}
        for signal, windows in WINDOWS_195.items():
            row[signal] = (
                1.1
                if any(start_ns <= frame_ns < end_ns for start_ns, end_ns in windows)
                else 0.0
            )
        if mutation == "zero":
            for signal in WINDOWS_195:
                row[signal] = 0.0
        elif mutation == "half_conv_level":
            row["conv"] *= 0.5
        elif mutation == "swap_nc_res":
            row["nc"], row["res"] = row["res"], row["nc"]
        elif mutation == "missing_second_sample" and 9.0 <= frame_ns < 9.8:
            row["s"] = 0.0
        elif mutation == "metric_scale_low":
            row["nc"] *= 0.42
            row["conv"] *= 0.42
        rows.append(row)
    return rows


def test_195_checks_complete_narrow_windows_on_coarse_adaptive_time_grid() -> None:
    passed, detail = check_195(_sequencer_195_rows())

    assert passed, detail
    assert "checked_windows=12" in detail


def test_195_keeps_legacy_12ns_sibling_decks_compatible() -> None:
    passed, detail = check_195(_sequencer_195_rows(stop_ns=12.0))

    assert passed, detail
    assert "checked_windows=10" in detail


@pytest.mark.parametrize(
    "mutation",
    [
        "zero",
        "half_conv_level",
        "swap_nc_res",
        "missing_second_sample",
        "metric_scale_low",
    ],
)
def test_195_still_rejects_semantic_mutations_on_coarse_grid(mutation: str) -> None:
    passed, _ = check_195(_sequencer_195_rows(mutation=mutation))

    assert not passed


def test_695_canonical_decks_keep_the_source_12ns_contract() -> None:
    harness = json.loads(
        (TASK_695 / "evaluator/harness_spec.json").read_text(encoding="utf-8")
    )
    assert harness["deck"]["analyses"] == ["tran tran stop=12n maxstep=20p"]

    for deck_name in ("reference_tb.scs", "score_tb.scs"):
        deck = (TASK_695 / "evaluator" / deck_name).read_text(encoding="utf-8")
        assert "tran tran stop=12n maxstep=20p" in deck

    evaluator = TASK_695 / "evaluator"
    harness_sha = hashlib.sha256(
        (evaluator / "harness_spec.json").read_bytes()
    ).hexdigest()
    for profile_name in ("feedback", "score"):
        profile = json.loads(
            (evaluator / f"profiles/{profile_name}.json").read_text(encoding="utf-8")
        )
        assert profile["harness_spec_sha256"] == harness_sha

    policy = json.loads(
        (evaluator / "score_policy.json").read_text(encoding="utf-8")
    )
    reference_sha = hashlib.sha256(
        (evaluator / "reference_tb.scs").read_bytes()
    ).hexdigest()
    assert policy["reference_tb_sha256"] == reference_sha
