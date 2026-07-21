import hashlib
import json
import math
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_077 import CHECKER as check_077  # noqa: E402


FAMILY = (
    ROOT
    / "benchmark-vabench-release-v4/provenance/dut-base-v3-exact-five-hash-bound-v2"
    / "077-dither-noise-like-deterministic-source"
)
SEQUENCE = (-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5)


def _sample(
    time_ns: float,
    *,
    sigma: float,
    dt_ns: float,
    delay_fraction: float = 0.0,
    transition: bool = False,
) -> float:
    sample_time_ns = max(0.0, time_ns - delay_fraction * dt_ns)
    interval = int((sample_time_ns + 1e-10) / dt_ns)
    current = sigma * SEQUENCE[interval % len(SEQUENCE)]
    if not transition or delay_fraction:
        return current
    phase = max(0.0, (time_ns - interval * dt_ns) / dt_ns)
    if phase >= 0.10:
        return current
    previous = sigma * SEQUENCE[(interval - 1) % len(SEQUENCE)]
    return previous + (current - previous) * phase / 0.10


def _dual_parameter_rows(
    *,
    override_ignores_parameters: bool = False,
    delay_fraction: float = 0.0,
    transition: bool = False,
) -> list[dict[str, float]]:
    rows = []
    for index in range(801):
        time_ns = index * 0.025
        vin = 0.7
        override_sigma = 0.01 if override_ignores_parameters else 0.037
        override_dt_ns = 0.5 if override_ignores_parameters else 0.8
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vin_i": vin,
                "vout_default": vin
                + _sample(
                    time_ns,
                    sigma=0.01,
                    dt_ns=0.5,
                    delay_fraction=delay_fraction,
                    transition=transition,
                ),
                "vout_override": vin
                + _sample(
                    time_ns,
                    sigma=override_sigma,
                    dt_ns=override_dt_ns,
                    delay_fraction=delay_fraction,
                    transition=transition,
                ),
            }
        )
    return rows


def test_077_checker_requires_default_and_override_parameter_behavior() -> None:
    passed, detail = check_077(_dual_parameter_rows())
    assert passed, detail

    passed, detail = check_077(_dual_parameter_rows(override_ignores_parameters=True))
    assert not passed
    assert "override" in detail


def test_077_checker_scans_stable_rows_between_nominal_probe_phases() -> None:
    rows = _dual_parameter_rows()
    glitch_time_ns = 6.25
    row = min(rows, key=lambda item: abs(item["time"] * 1e9 - glitch_time_ns))
    row["vout_default"] += 0.23 * 0.01
    passed, detail = check_077(rows)
    assert not passed
    assert "hold" in detail or "level" in detail


def test_077_checker_rejects_global_update_delay_beyond_transition_guard() -> None:
    passed, detail = check_077(_dual_parameter_rows(delay_fraction=0.20))
    assert not passed
    assert "default" in detail


def test_077_checker_allows_the_declared_transition_edge() -> None:
    passed, detail = check_077(_dual_parameter_rows(transition=True))
    assert passed, detail


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
@pytest.mark.parametrize(
    "signal", ["time", "vin_i", "vout_default", "vout_override"]
)
def test_077_checker_rejects_nonfinite_trace_values(signal: str, value: float) -> None:
    rows = _dual_parameter_rows()
    rows[173][signal] = value
    passed, detail = check_077(rows)
    assert not passed
    assert "nonfinite" in detail


def test_077_checker_rejects_nonfinite_derived_noise() -> None:
    rows = _dual_parameter_rows()
    rows[173]["vin_i"] = -1e308
    rows[173]["vout_default"] = 1e308
    passed, detail = check_077(rows)
    assert not passed
    assert "nonfinite" in detail


def test_077_public_and_score_decks_exercise_the_same_two_parameter_sets() -> None:
    feedback = (FAMILY / "public/task/feedback_tb.scs").read_text(encoding="utf-8")
    score = (FAMILY / "evaluator/score_tb.scs").read_text(encoding="utf-8")
    reference = (FAMILY / "evaluator/reference_tb.scs").read_text(encoding="utf-8")
    shared_lines = [
        "IDUT_DEFAULT (vin_i vout_default) noise_gen",
        "IDUT_OVERRIDE (vin_i vout_override) noise_gen sigma=0.037 dt=0.8n",
        "save vin_i vout_default vout_override",
    ]
    for line in shared_lines:
        assert line in feedback
        assert line in score
        assert line in reference

    contract = json.loads(
        (FAMILY / "public/task/public_contract.json").read_text(encoding="utf-8")
    )
    assert contract["public_observables"] == [
        "time",
        "vin_i",
        "vout_default",
        "vout_override",
    ]

    harness = json.loads(
        (FAMILY / "evaluator/harness_spec.json").read_text(encoding="utf-8")
    )
    assert shared_lines[0] in harness["deck"]["body_lines"]
    assert shared_lines[1] in harness["deck"]["body_lines"]
    assert harness["deck"]["save_signals"] == [
        "vin_i",
        "vout_default",
        "vout_override",
    ]
    source_contract = harness["source_contract"]
    assert source_contract["checker_profile_sha256"] == hashlib.sha256(
        (FAMILY / "evaluator/checker_profile.json").read_bytes()
    ).hexdigest()
    assert source_contract["family_spec_sha256"] == hashlib.sha256(
        (FAMILY / "evaluator/family_spec.json").read_bytes()
    ).hexdigest()
    harness_sha = hashlib.sha256(
        (FAMILY / "evaluator/harness_spec.json").read_bytes()
    ).hexdigest()
    for profile_name in ("feedback", "score"):
        profile = json.loads(
            (FAMILY / f"evaluator/profiles/{profile_name}.json").read_text(
                encoding="utf-8"
            )
        )
        assert profile["harness_spec_sha256"] == harness_sha
