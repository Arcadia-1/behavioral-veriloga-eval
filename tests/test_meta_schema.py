from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "task.schema.json"
CONFORMANCE_SCHEMA_PATH = ROOT / "schemas" / "conformance.schema.json"
TASKS_DIR = ROOT / "tasks"


def test_all_meta_json_files_follow_task_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []

    for meta_path in sorted(TASKS_DIR.rglob("meta.json")):
        payload = json.loads(meta_path.read_text(encoding="utf-8"))
        try:
            jsonschema.validate(payload, schema)
        except jsonschema.ValidationError as exc:
            failures.append(f"{meta_path.relative_to(ROOT)}: {exc.message}")

    assert not failures, "meta.json schema violations:\n" + "\n".join(failures)


def _minimal_task_meta(**updates: object) -> dict:
    payload = {
        "id": "demo_task",
        "family": "spec-to-va",
        "category": "demo",
        "domain": "voltage",
        "difficulty": "easy",
        "expected_backend": "evas",
        "scoring": ["dut_compile", "tb_compile", "sim_correct"],
    }
    payload.update(updates)
    return payload


def test_task_schema_rejects_conformance_style_release_form() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    payload = _minimal_task_meta(release_form="conformance-style")

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_task_schema_excludes_evidence_only_from_count_flags() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    valid = _minimal_task_meta(
        release_form="evidence-only",
        counts={"model_capability": False, "benchmark_coverage": False, "bugfix_claim": False},
    )
    invalid = _minimal_task_meta(
        release_form="evidence-only",
        counts={"model_capability": True, "benchmark_coverage": False, "bugfix_claim": False},
    )

    jsonschema.validate(valid, schema)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid, schema)


def test_conformance_schema_requires_false_counts_and_reject_signature() -> None:
    schema = json.loads(CONFORMANCE_SCHEMA_PATH.read_text(encoding="utf-8"))
    valid = {
        "asset_type": "evas_spectre_conformance",
        "suite": "evas-spectre",
        "conformance_axis": "event-ordering",
        "expected_relation": "both_reject",
        "diagnostic_signature": "empty control branch",
        "minimality_note": "one syntax legality issue only",
        "counts": {
            "model_capability": False,
            "benchmark_coverage": False,
            "bugfix_claim": False,
            "broad_parity_denominator": False,
        },
    }
    invalid = dict(valid)
    invalid.pop("diagnostic_signature")

    jsonschema.validate(valid, schema)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid, schema)
