from __future__ import annotations

from pathlib import Path

import pytest


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
EVAS_MANIFEST = WORKSPACE_ROOT / "EVAS" / "evas-capabilities.manifest"
SKILL_CACHE = WORKSPACE_ROOT / "veriloga-skills" / "veriloga" / "references" / "evas-capabilities.manifest"


def _sections(path: Path) -> dict[str, list[str]]:
    current: str | None = None
    sections: dict[str, list[str]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1]
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def test_veriloga_skill_capability_manifest_is_cache_not_source_of_truth() -> None:
    if not EVAS_MANIFEST.exists() or not SKILL_CACHE.exists():
        pytest.skip("workspace sibling EVAS/veriloga-skills repos are not available")

    cache_text = SKILL_CACHE.read_text(encoding="utf-8")

    assert "LOCAL CACHE" in cache_text
    assert "source of truth is in the EVAS repo" in cache_text
    assert "Do not edit EVAS capability support decisions in this cache first" in cache_text


def test_veriloga_skill_capability_cache_matches_evas_manifest_sections() -> None:
    if not EVAS_MANIFEST.exists() or not SKILL_CACHE.exists():
        pytest.skip("workspace sibling EVAS/veriloga-skills repos are not available")

    evas = _sections(EVAS_MANIFEST)
    cache = _sections(SKILL_CACHE)

    assert cache == evas
