from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "provenance" / "dut-base-v3-exact-five-hash-bound-v2"
RELEASE_ROOT = ROOT / "release" / "benchmarkv4"
RENDERER = ROOT / "scripts" / "render_v4_harness.py"


def _semantic_projection(spec: dict, profile_name: str) -> dict:
    defaults = copy.deepcopy(spec["profile_defaults"][profile_name])
    overrides = defaults.get("deck_overrides", {})
    return {
        "body_lines": list(spec["deck"].get("body_lines", []))
        + list(overrides.get("body_lines", [])),
        "analyses": list(overrides.get("analyses", spec["deck"].get("analyses", []))),
        "save_signals": list(overrides.get("save_signals", spec["deck"].get("save_signals", []))),
        "parameters": defaults.get("parameters", {}),
        "corners": defaults.get("corners", []),
        "property_ids": list(spec["property_ids"]),
    }


def _family_source(family_id: int) -> Path:
    return next(SOURCE_ROOT.glob(f"{family_id:03d}-*"))


def _release_testbench_task(family_id: int) -> Path:
    return next(RELEASE_ROOT.joinpath("tasks").glob(f"{family_id + 500:03d}-*"))


def _without_backend_options(deck: str) -> str:
    return "\n".join(
        line
        for line in deck.splitlines()
        if line.strip() and not line.startswith("simulatorOptions options ")
    )


def test_batch35_canonical_specs_have_feedback_score_semantic_parity() -> None:
    for family_id in range(341, 351):
        spec = json.loads((_family_source(family_id) / "evaluator" / "harness_spec.json").read_text())
        feedback = _semantic_projection(spec, "feedback")
        score = _semantic_projection(spec, "score")
        assert feedback == score, f"family {family_id:03d} profile semantic drift"


def test_batch35_rendered_profiles_match_and_keep_backend_only_difference(tmp_path: Path) -> None:
    for family_id in range(341, 351):
        source = _family_source(family_id) / "evaluator"
        spec_path = source / "harness_spec.json"
        output = tmp_path / f"{family_id:03d}"
        output.mkdir()
        generated = {}
        generated_decks = {}
        for profile_name in ("feedback", "score"):
            profile_path = output / f"{profile_name}.json"
            deck_path = output / f"{profile_name}.scs"
            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--spec",
                    str(spec_path),
                    "--profile",
                    profile_name,
                    "--profile-output",
                    str(profile_path),
                    "--deck-output",
                    str(deck_path),
                ],
                check=True,
                cwd=ROOT,
            )
            generated[profile_name] = json.loads(profile_path.read_text())
            generated_decks[profile_name] = deck_path.read_text()

        assert generated["feedback"]["property_ids"] == generated["score"]["property_ids"]
        assert generated["feedback"]["parameters"] == generated["score"]["parameters"]
        assert generated["feedback"]["corners"] == generated["score"]["corners"]
        assert generated["feedback"]["deck_overrides"] == generated["score"]["deck_overrides"]
        assert generated["feedback"]["simulatorOptions"] == {"evas_profile": "balanced"}
        assert generated["score"]["simulatorOptions"] == {}
        assert generated["feedback"]["public_visible"] is True
        assert generated["score"]["public_visible"] is False
        assert _without_backend_options(generated_decks["feedback"]) == _without_backend_options(
            generated_decks["score"]
        )
        assert generated_decks["feedback"] == (
            source.parent / "public" / "task" / "feedback_tb.scs"
        ).read_text()
        assert generated_decks["score"] == (source / "score_tb.scs").read_text()


def test_batch35_checker_trace_and_mutation_contracts_are_structurally_complete() -> None:
    for family_id in range(341, 351):
        family = _family_source(family_id)
        evaluator = family / "evaluator"
        public_contract = json.loads(
            (family / "public" / "task" / "public_contract.json").read_text()
        )
        checker = json.loads((evaluator / "checker_profile.json").read_text())
        mutations = json.loads(
            (evaluator / "mutation_bundles" / "manifest.json").read_text()
        )
        score_policy = json.loads(
            (_release_testbench_task(family_id) / "evaluator" / "score_policy.json").read_text()
        )

        assert checker["schema_version"] == "v4-checker-profile-v1"
        assert checker["score_and_feedback_share_checker"] is True
        assert checker["trace_contract"]["public_observables"] == public_contract[
            "public_observables"
        ]
        assert public_contract["oracle_policy"]["single_public_contract"] is True
        assert public_contract["oracle_policy"]["testbench_and_checker_split_required"] is True
        catalog = {item["id"]: item for item in mutations["mutations"]}
        active_ids = score_policy["negative_suite_mutation_ids"]
        assert len(active_ids) == 5
        assert len(set(active_ids)) == 5
        active = [catalog[mutation_id] for mutation_id in active_ids]
        assert all(
            item["certification"]["compile_status"] == "pass"
            and item["certification"]["simulation_status"] == "pass"
            and item["certification"]["status"] == "pass"
            and item["violated_property_ids"]
            for item in active
        )
