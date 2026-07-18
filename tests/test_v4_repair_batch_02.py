from __future__ import annotations

import hashlib
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmark-vabench-release-v4" / "provenance" / "dut-base-v3-exact-five-hash-bound-v2"
RENDERER = ROOT / "benchmark-vabench-release-v4" / "scripts" / "render_v4_harness.py"
PARITY = ROOT / "benchmark-vabench-release-v4" / "scripts" / "validate_v4_profile_parity.py"
FAMILIES = tuple(f"{value:03d}" for value in range(11, 21))
PREP = ROOT / "benchmark-vabench-release-v4" / "operations" / "tri_form_derivation_prep"
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from score_denominator_registry import load_family_rows  # noqa: E402


def _family(family: str) -> Path:
    matches = sorted(SOURCE.glob(f"{family}-*"))
    assert len(matches) == 1
    return matches[0]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_batch_02_profiles_have_zero_semantic_drift() -> None:
    result = subprocess.run(
        [sys.executable, str(PARITY), "--family-range", "011-020"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert report["checked_families"] == list(FAMILIES)


def test_batch_02_source_profiles_are_deterministically_regenerated(tmp_path: Path) -> None:
    for family in FAMILIES:
        task = _family(family)
        evaluator = task / "evaluator"
        for profile_name in ("feedback", "score"):
            profile_out = tmp_path / family / f"{profile_name}.json"
            deck_out = tmp_path / family / f"{profile_name}.scs"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--spec",
                    str(evaluator / "harness_spec.json"),
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


def test_batch_02_checkers_are_stimulus_relative_and_emit_all_properties() -> None:
    absolute_window = re.compile(r"\b(?:time|t)\s*(?:<|>|<=|>=)\s*[0-9]+(?:\.[0-9]+)?e-9")
    for family in FAMILIES:
        checker = ROOT / "runners" / "checkers" / "v4" / f"task_{family}.py"
        text = checker.read_text(encoding="utf-8")
        assert absolute_window.search(text) is None, checker
        properties = json.loads((_family(family) / "evaluator" / "harness_spec.json").read_text())["property_ids"]
        assert all(property_id in text for property_id in properties), family


def test_batch_02_underexcited_traces_are_explicitly_rejected() -> None:
    for family in FAMILIES:
        profile = json.loads((_family(family) / "evaluator" / "checker_profile.json").read_text())
        signals = ["time", *profile["trace_contract"]["public_observables"]]
        rows = [{signal: (index * 1e-9 if signal == "time" else 0.0) for signal in signals} for index in range(6)]
        checker = importlib.import_module(f"runners.checkers.v4.task_{family}").CHECKER
        passed, note = checker(rows)
        assert not passed, family
        assert "insufficient_excitation" in note, (family, note)


def test_batch_02_trace_contracts_match_public_observables() -> None:
    for family in FAMILIES:
        task = _family(family)
        public = json.loads((task / "public" / "task" / "public_contract.json").read_text())
        checker = json.loads((task / "evaluator" / "checker_profile.json").read_text())
        assert {name.lower() for name in public["public_observables"]} == {
            name.lower() for name in checker["trace_contract"]["public_observables"]
        }


def test_batch_02_source_rows_bind_exact_five_and_current_hashes() -> None:
    rows = {str(row["canonical_dut_id"]): row for row in load_family_rows(SOURCE)}
    for family in FAMILIES:
        task = _family(family)
        record = json.loads((task / "evaluator" / "task_record.json").read_text())
        assert rows[family]["active_mutation_count"] == 5
        assert len(rows[family]["active_mutations"]) == 5
        for relative in (
            "checker_profile.json",
            "harness_spec.json",
            "profiles/feedback.json",
            "profiles/score.json",
            "score_tb.scs",
        ):
            assert record["evaluator_hashes"][relative] == _sha(task / "evaluator" / relative)
        assert record["public_hashes"]["feedback_tb.scs"] == _sha(task / "public" / "task" / "feedback_tb.scs")


def test_batch_02_combinational_checkers_ignore_affine_time_relabeling() -> None:
    cases = {
        "014": (["b0", "b1", "t0", "t1", "t2"], [0, 1, 2, 7, 15]),
        "015": (["code_0", "code_1", "code_2", "code_3"], list(range(16))),
        "018": ([f"seg{index}" for index in range(15)], [0, 1, 1, 2, 7, 14, 15]),
    }
    for family, (signals, codes) in cases.items():
        rows: list[dict[str, float]] = []
        for plateau, code in enumerate(codes):
            for point in range(5):
                row = {"time": (5 * plateau + point) * 1e-9, "vref": 0.9, "vss": 0.0}
                if family == "014":
                    vector = [code & 1, (code >> 1) & 1, int(code >= 4), int(code >= 8), int(code >= 12)]
                    expected_code = vector[0] + 2 * vector[1] + 4 * sum(vector[2:])
                elif family == "015":
                    vector = [(code >> index) & 1 for index in range(4)]
                    expected_code = code
                else:
                    offset = 0 if plateau != 2 else 1
                    vector = [int((index - offset) % 15 < code) for index in range(15)]
                    expected_code = code
                row.update({signal: 0.9 * bit for signal, bit in zip(signals, vector)})
                row["aout"] = 0.9 * expected_code / 15.0
                rows.append(row)
        checker = importlib.import_module(f"runners.checkers.v4.task_{family}").CHECKER
        original = checker(rows)
        transformed = checker([{**row, "time": 1.37 * row["time"] + 2e-9} for row in rows])
        assert original[0], (family, original)
        assert transformed[0], (family, transformed)
