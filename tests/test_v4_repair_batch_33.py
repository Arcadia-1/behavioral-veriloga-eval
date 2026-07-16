from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmark-vabench-release-v4" / "provenance" / "dut-base-v3-exact-five-hash-bound-v2"
RENDERER = ROOT / "benchmark-vabench-release-v4" / "scripts" / "render_v4_harness.py"
PARITY = ROOT / "benchmark-vabench-release-v4" / "scripts" / "validate_v4_profile_parity.py"
FAMILIES = tuple(f"{value:03d}" for value in range(321, 331))
PREP = ROOT / "benchmark-vabench-release-v4" / "operations" / "tri_form_derivation_prep"
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from score_denominator_registry import load_score_denominator_registry  # noqa: E402


def _family(family: str) -> Path:
    matches = sorted(SOURCE.glob(f"{family}-*"))
    assert len(matches) == 1
    return matches[0]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_batch_33_profiles_have_zero_semantic_drift() -> None:
    result = subprocess.run(
        [sys.executable, str(PARITY), "--family-range", "321-330"],
        cwd=ROOT,
        capture_output=True,
        env={
            **os.environ,
            "EVAS_ENGINE": "evas2",
            "VAEVAS_DEFAULT_EVAS_ENGINE": "evas2",
        },
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert report["checked_families"] == list(FAMILIES)


def test_batch_33_source_profiles_are_deterministically_regenerated(tmp_path: Path) -> None:
    for family in FAMILIES:
        task = _family(family)
        evaluator = task / "evaluator"
        spec = evaluator / "harness_spec.json"
        for profile_name in ("feedback", "score"):
            profile_out = tmp_path / family / f"{profile_name}.json"
            deck_out = tmp_path / family / f"{profile_name}.scs"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--spec",
                    str(spec),
                    "--profile",
                    profile_name,
                    "--profile-output",
                    str(profile_out),
                    "--deck-output",
                    str(deck_out),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0, result.stdout + result.stderr
            expected_profile = evaluator / "profiles" / f"{profile_name}.json"
            expected_deck = task / "public" / "task" / "feedback_tb.scs" if profile_name == "feedback" else evaluator / "score_tb.scs"
            assert _sha(profile_out) == _sha(expected_profile)
            assert _sha(deck_out) == _sha(expected_deck)


def test_batch_33_checkers_do_not_use_absolute_start_or_stop_windows() -> None:
    absolute = re.compile(r"\bt\s*(?:<|>|<=|>=)\s*[0-9]+(?:\.[0-9]+)?e-9")
    forbidden_edge_window = re.compile(r"_v4_edges\([^\n]*\b(?:start|stop)\s*=")
    for value in range(321, 331):
        path = ROOT / "runners" / "checkers" / "v4" / f"task_{value:03d}.py"
        text = path.read_text(encoding="utf-8")
        assert absolute.search(text) is None, path
        assert forbidden_edge_window.search(text) is None, path


def test_batch_33_checkers_emit_every_canonical_property_id() -> None:
    for family in FAMILIES:
        task = _family(family)
        properties = json.loads(
            (task / "evaluator" / "harness_spec.json").read_text(encoding="utf-8")
        )["property_ids"]
        checker_text = (
            ROOT / "runners" / "checkers" / "v4" / f"task_{int(family):03d}.py"
        ).read_text(encoding="utf-8")
        assert all(property_id in checker_text for property_id in properties), family


def test_batch_33_source_rows_bind_all_ten_five_mutation_families() -> None:
    manifest = load_score_denominator_registry(SOURCE)
    rows = {str(row["canonical_dut_id"]): row for row in manifest["tasks"]}
    assert set(FAMILIES) <= rows.keys()
    for family in FAMILIES:
        task = _family(family)
        catalog = json.loads((task / "evaluator" / "mutation_catalog.json").read_text(encoding="utf-8"))
        record = json.loads((task / "evaluator" / "task_record.json").read_text(encoding="utf-8"))
        assert len(catalog["mutations"]) >= 5
        assert rows[family]["active_mutation_count"] == 5
        assert len(rows[family]["active_mutations"]) == 5
        assert record["evaluator_hashes"]["harness_spec.json"] == _sha(task / "evaluator" / "harness_spec.json")
        assert record["evaluator_hashes"]["profiles/feedback.json"] == _sha(task / "evaluator" / "profiles" / "feedback.json")
        assert record["evaluator_hashes"]["profiles/score.json"] == _sha(task / "evaluator" / "profiles" / "score.json")
        assert record["evaluator_hashes"]["score_tb.scs"] == _sha(task / "evaluator" / "score_tb.scs")
        assert record["public_hashes"]["feedback_tb.scs"] == _sha(task / "public" / "task" / "feedback_tb.scs")
        assert rows[family]["hashes"]["score_deck_sha256"] == _sha(task / "evaluator" / "score_tb.scs")
