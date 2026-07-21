from __future__ import annotations

import json
import hashlib
from pathlib import Path
import sys


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


def _sample(time_ns: float, *, sigma: float, dt_ns: float) -> float:
    index = int((time_ns + 1e-10) / dt_ns) % len(SEQUENCE)
    return sigma * SEQUENCE[index]


def _dual_parameter_rows(*, override_ignores_parameters: bool) -> list[dict[str, float]]:
    rows = []
    for index in range(401):
        time_ns = index * 0.05
        vin = 0.7
        override_sigma = 0.01 if override_ignores_parameters else 0.037
        override_dt_ns = 0.5 if override_ignores_parameters else 0.8
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vin_i": vin,
                "vout_default": vin + _sample(time_ns, sigma=0.01, dt_ns=0.5),
                "vout_override": vin
                + _sample(time_ns, sigma=override_sigma, dt_ns=override_dt_ns),
            }
        )
    return rows


def test_077_checker_requires_default_and_override_parameter_behavior() -> None:
    passed, detail = check_077(_dual_parameter_rows(override_ignores_parameters=False))
    assert passed, detail

    passed, detail = check_077(_dual_parameter_rows(override_ignores_parameters=True))
    assert not passed
    assert "override" in detail


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
