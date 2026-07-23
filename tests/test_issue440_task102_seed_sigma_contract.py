from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_102 import CHECKER, PROPERTY_IDS  # noqa: E402


FAMILY = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
    / "102-clocked-sine-source"
)

COMMON_MODE = 0.45
AMPLITUDE = 0.02
FREQUENCY_HZ = 1.0e6
NOISE_A = (0.003, -0.005, 0.007, -0.002, 0.004, -0.006, 0.001)
NOISE_ALT = (-0.004, 0.006, -0.001, 0.005, -0.007, 0.002, -0.003)
EXTRA_OBSERVABLES = (
    "vinp_seed_b",
    "vinn_seed_b",
    "vinp_seed_alt",
    "vinn_seed_alt",
    "vinp_sigma0",
    "vinn_sigma0",
)


def _clocked_source_rows(
    *,
    same_seed_diverges: bool = False,
    alternate_seed_collapses: bool = False,
    sigma_zero_perturbed: bool = False,
) -> list[dict[str, float]]:
    states = {
        "vinp": COMMON_MODE,
        "vinp_seed_b": COMMON_MODE,
        "vinp_seed_alt": COMMON_MODE,
        "vinp_sigma0": COMMON_MODE,
    }
    rows: list[dict[str, float]] = []
    active_edge = 0
    for step in range(4001):
        time_ns = 0.5 * step
        time_s = time_ns * 1.0e-9
        clock_high = 10 <= step % 40 < 28
        reset_high = step >= 80
        if reset_high and step % 40 == 10:
            baseline = COMMON_MODE + AMPLITUDE * math.sin(
                2.0 * math.pi * FREQUENCY_HZ * time_s
            )
            noise_a = NOISE_A[active_edge % len(NOISE_A)]
            noise_b = noise_a + (0.003 if same_seed_diverges else 0.0)
            noise_alt = (
                noise_a
                if alternate_seed_collapses
                else NOISE_ALT[active_edge % len(NOISE_ALT)]
            )
            sigma_zero_noise = (
                0.004 * (1.0 if active_edge % 2 else -1.0)
                if sigma_zero_perturbed
                else 0.0
            )
            states.update(
                {
                    "vinp": baseline + noise_a,
                    "vinp_seed_b": baseline + noise_b,
                    "vinp_seed_alt": baseline + noise_alt,
                    "vinp_sigma0": baseline + sigma_zero_noise,
                }
            )
            active_edge += 1

        vin_diff = states["vinp"] - COMMON_MODE
        rows.append(
            {
                "time": time_s,
                "clk": 0.9 if clock_high else 0.0,
                "rst_n": 0.9 if reset_high else 0.0,
                "vinp": states["vinp"],
                "vinn": COMMON_MODE,
                "vinp_seed_b": states["vinp_seed_b"],
                "vinn_seed_b": COMMON_MODE,
                "vinp_seed_alt": states["vinp_seed_alt"],
                "vinn_seed_alt": COMMON_MODE,
                "vinp_sigma0": states["vinp_sigma0"],
                "vinn_sigma0": COMMON_MODE,
                "vamp_p": COMMON_MODE + 4.32 * vin_diff,
                "vamp_n": COMMON_MODE - 4.32 * vin_diff,
            }
        )
    return rows


def test_102_checker_accepts_repeatable_seed_and_sigma_zero_fixture() -> None:
    passed, detail = CHECKER(_clocked_source_rows())
    assert passed, detail
    for property_id in PROPERTY_IDS:
        assert f"{property_id} mismatch_count=0" in detail


def test_102_checker_rejects_same_seed_instances_that_diverge() -> None:
    passed, detail = CHECKER(_clocked_source_rows(same_seed_diverges=True))
    assert not passed
    assert "P_SEEDED_REPEATABILITY" in detail
    assert "same_seed" in detail


def test_102_checker_rejects_an_implementation_that_ignores_seed() -> None:
    passed, detail = CHECKER(_clocked_source_rows(alternate_seed_collapses=True))
    assert not passed
    assert "P_SEEDED_REPEATABILITY" in detail
    assert "alternate_seed" in detail


def test_102_checker_rejects_sigma_zero_perturbation() -> None:
    passed, detail = CHECKER(_clocked_source_rows(sigma_zero_perturbed=True))
    assert not passed
    assert "P_SEEDED_REPEATABILITY" in detail
    assert "sigma_zero" in detail


def test_102_decks_and_contract_make_seed_and_sigma_semantics_observable() -> None:
    feedback = (FAMILY / "public/task/feedback_tb.scs").read_text(encoding="utf-8")
    score = (FAMILY / "evaluator/score_tb.scs").read_text(encoding="utf-8")
    reference = (FAMILY / "evaluator/reference_tb.scs").read_text(encoding="utf-8")
    instance_lines = (
        "IVIN_SEED_A (clk rst_n vinp vinn) vin_src vdd=vdd vth=0.45 ampl=0.02 freq=fin sigma=VIN_NOISE SEED=17",
        "IVIN_SEED_B (clk rst_n vinp_seed_b vinn_seed_b) vin_src vdd=vdd vth=0.45 ampl=0.02 freq=fin sigma=VIN_NOISE SEED=17",
        "IVIN_SEED_ALT (clk rst_n vinp_seed_alt vinn_seed_alt) vin_src vdd=vdd vth=0.45 ampl=0.02 freq=fin sigma=VIN_NOISE SEED=29",
        "IVIN_SIGMA0 (clk rst_n vinp_sigma0 vinn_sigma0) vin_src vdd=vdd vth=0.45 ampl=0.02 freq=fin sigma=0 SEED=17",
    )
    save_line = "save clk rst_n vinp vinn vamp_p vamp_n " + " ".join(EXTRA_OBSERVABLES)
    for deck in (feedback, score, reference):
        for line in instance_lines:
            assert line in deck
        assert save_line in deck

    public_contract = json.loads(
        (FAMILY / "public/task/public_contract.json").read_text(encoding="utf-8")
    )
    assert public_contract["public_observables"] == [
        "clk",
        "rst_n",
        "vinp",
        "vinn",
        "vamp_p",
        "vamp_n",
        *EXTRA_OBSERVABLES,
    ]

    checker_profile = json.loads(
        (FAMILY / "evaluator/checker_profile.json").read_text(encoding="utf-8")
    )
    assert checker_profile["trace_contract"]["public_observables"] == [
        "clk",
        "rst_n",
        "vinp",
        "vinn",
        "vamp_p",
        "vamp_n",
        *EXTRA_OBSERVABLES,
    ]

    harness_path = FAMILY / "evaluator/harness_spec.json"
    harness = json.loads(harness_path.read_text(encoding="utf-8"))
    assert tuple(harness["property_ids"]) == PROPERTY_IDS
    assert harness["deck"]["save_signals"] == [
        "clk",
        "rst_n",
        "vinp",
        "vinn",
        "vamp_p",
        "vamp_n",
        *EXTRA_OBSERVABLES,
    ]
    for line in instance_lines:
        assert line in harness["deck"]["body_lines"]

    harness_sha = hashlib.sha256(harness_path.read_bytes()).hexdigest()
    for profile_name in ("feedback", "score"):
        profile = json.loads(
            (FAMILY / f"evaluator/profiles/{profile_name}.json").read_text(
                encoding="utf-8"
            )
        )
        assert profile["property_ids"] == list(PROPERTY_IDS)
        assert profile["harness_spec_sha256"] == harness_sha
