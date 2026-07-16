from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


PREP = Path(__file__).resolve().parents[2] / "operations" / "tri_form_derivation_prep"
SOURCE = Path(__file__).resolve().parents[2] / "provenance" / "dut-base-v3-exact-five-hash-bound-v2"
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from score_denominator_registry import (  # noqa: E402
    RegistryError,
    load_score_denominator_registry,
    migrate_legacy_manifest,
    rendered_manifest_bytes,
    write_family_row,
)


def test_canonical_source_has_only_family_shards() -> None:
    assert not (SOURCE / "score_denominator_manifest.json").exists()
    manifest = load_score_denominator_registry(SOURCE)
    assert len(manifest["tasks"]) == 400


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def row(family: str) -> dict[str, object]:
    return {
        "canonical_dut_id": family,
        "release_dir": f"{family}-sample",
        "active_mutation_count": 5,
        "active_mutations": [],
        "hashes": {},
    }


def test_legacy_migration_is_byte_exact(tmp_path: Path) -> None:
    source = tmp_path / "source"
    legacy = tmp_path / "score_denominator_manifest.json"
    manifest = {
        "schema_version": "sample-v1",
        "canonical_range": ["001", "002"],
        "counted_task_count": 2,
        "tasks": [row("001"), row("002")],
    }
    from score_denominator_registry import canonical_manifest_sha  # noqa: PLC0415

    manifest["content_sha256"] = canonical_manifest_sha(manifest)
    write_json(legacy, manifest)

    migrate_legacy_manifest(source, legacy)

    assert rendered_manifest_bytes(source) == legacy.read_bytes()
    assert [item["canonical_dut_id"] for item in load_score_denominator_registry(source)["tasks"]] == [
        "001",
        "002",
    ]


def test_registry_rejects_missing_family_shard(tmp_path: Path) -> None:
    source = tmp_path / "source"
    write_json(
        source / "score_denominator_registry" / "_meta.json",
        {"canonical_range": ["001", "002"], "counted_task_count": 2},
    )
    write_family_row(source, "001", row("001"))

    with pytest.raises(RegistryError, match="coverage mismatch"):
        load_score_denominator_registry(source)


def test_updating_one_family_does_not_touch_other_shards(tmp_path: Path) -> None:
    source = tmp_path / "source"
    write_json(
        source / "score_denominator_registry" / "_meta.json",
        {"canonical_range": ["001", "002"], "counted_task_count": 2},
    )
    write_family_row(source, "001", row("001"))
    write_family_row(source, "002", row("002"))
    untouched = (source / "score_denominator_registry" / "002.json").read_bytes()

    changed = row("001")
    changed["bugfix_seed"] = "neg_001"
    write_family_row(source, "001", changed)

    assert (source / "score_denominator_registry" / "002.json").read_bytes() == untouched
    assert load_score_denominator_registry(source)["tasks"][0]["bugfix_seed"] == "neg_001"
