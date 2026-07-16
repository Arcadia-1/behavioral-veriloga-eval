#!/usr/bin/env python3
"""Load and maintain the family-sharded V4 score denominator registry."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REGISTRY_DIRNAME = "score_denominator_registry"
META_FILENAME = "_meta.json"
FAMILY_SCHEMA = "v4-score-denominator-family-registry-v1"


class RegistryError(ValueError):
    """Raised when the registry is incomplete or internally inconsistent."""


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def registry_dir(source: Path) -> Path:
    return source / REGISTRY_DIRNAME


def family_path(source: Path, family: str) -> Path:
    return registry_dir(source) / f"{int(family):03d}.json"


def expected_family_ids(meta: dict[str, Any]) -> list[str]:
    canonical_range = meta.get("canonical_range") or []
    if len(canonical_range) != 2:
        raise RegistryError("registry metadata must declare a two-value canonical_range")
    start, end = (int(value) for value in canonical_range)
    if start > end:
        raise RegistryError("registry metadata canonical_range is descending")
    return [f"{value:03d}" for value in range(start, end + 1)]


def load_family_row(source: Path, family: str) -> dict[str, Any]:
    family = f"{int(family):03d}"
    path = family_path(source, family)
    if not path.is_file():
        raise RegistryError(f"missing family registry: {path}")
    shard = read_json(path)
    if shard.get("schema_version") != FAMILY_SCHEMA:
        raise RegistryError(f"{path}: unsupported schema_version")
    if str(shard.get("family_id") or "") != family:
        raise RegistryError(f"{path}: family_id does not match filename")
    row = shard.get("task")
    if not isinstance(row, dict):
        raise RegistryError(f"{path}: task must be an object")
    if str(row.get("canonical_dut_id") or "") != family:
        raise RegistryError(f"{path}: task canonical_dut_id does not match shard")
    return row


def write_family_row(source: Path, family: str, row: dict[str, Any]) -> None:
    family = f"{int(family):03d}"
    if str(row.get("canonical_dut_id") or "") != family:
        raise RegistryError(f"family {family}: task canonical_dut_id mismatch")
    write_json(
        family_path(source, family),
        {"schema_version": FAMILY_SCHEMA, "family_id": family, "task": row},
    )


def load_score_denominator_registry(source: Path) -> dict[str, Any]:
    directory = registry_dir(source)
    meta_path = directory / META_FILENAME
    if not meta_path.is_file():
        raise RegistryError(f"missing registry metadata: {meta_path}")
    meta = read_json(meta_path)
    if "tasks" in meta or "content_sha256" in meta:
        raise RegistryError("registry metadata must not contain generated manifest fields")
    expected = expected_family_ids(meta)
    actual = sorted(path.stem for path in directory.glob("[0-9][0-9][0-9].json"))
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise RegistryError(f"registry family coverage mismatch: missing={missing} extra={extra}")
    manifest = dict(meta)
    manifest["tasks"] = [load_family_row(source, family) for family in expected]
    manifest["content_sha256"] = canonical_manifest_sha(manifest)
    if int(manifest.get("counted_task_count") or -1) != len(expected):
        raise RegistryError("registry counted_task_count does not match family coverage")
    return manifest


def canonical_manifest_sha(manifest: dict[str, Any]) -> str:
    value = dict(manifest)
    value.pop("content_sha256", None)
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def rendered_manifest_bytes(source: Path) -> bytes:
    manifest = load_score_denominator_registry(source)
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def score_denominator_manifest_sha256(source: Path) -> str:
    return hashlib.sha256(rendered_manifest_bytes(source)).hexdigest()


def migrate_legacy_manifest(source: Path, legacy_manifest: Path) -> None:
    manifest = read_json(legacy_manifest)
    rows = manifest.pop("tasks", None)
    recorded_content_sha = manifest.pop("content_sha256", None)
    if not isinstance(rows, list) or not rows:
        raise RegistryError("legacy manifest has no task rows")
    directory = registry_dir(source)
    if directory.exists() and any(directory.iterdir()):
        raise RegistryError(f"registry directory is not empty: {directory}")
    write_json(directory / META_FILENAME, manifest)
    for row in rows:
        family = str(row.get("canonical_dut_id") or "")
        write_family_row(source, family, row)
    generated = load_score_denominator_registry(source)
    if recorded_content_sha and generated["content_sha256"] != recorded_content_sha:
        raise RegistryError("sharded registry changed the legacy manifest semantic hash")
    if rendered_manifest_bytes(source) != legacy_manifest.read_bytes():
        raise RegistryError("sharded registry does not reproduce the legacy manifest byte-for-byte")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--migrate-legacy", type=Path)
    parser.add_argument("--render")
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    if args.migrate_legacy:
        migrate_legacy_manifest(source, args.migrate_legacy.expanduser().resolve())
    manifest = load_score_denominator_registry(source)
    if args.render:
        output = Path(args.render).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(rendered_manifest_bytes(source))
    print(json.dumps({
        "status": "PASS",
        "family_count": len(manifest["tasks"]),
        "content_sha256": manifest["content_sha256"],
        "rendered_sha256": score_denominator_manifest_sha256(source),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
