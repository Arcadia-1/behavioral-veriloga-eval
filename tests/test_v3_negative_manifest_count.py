from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
TASKS = V3 / "TASKS.json"
TASK_ROOT = V3 / "tasks"
NEGATIVE_LIST_KEYS = ("cases", "negative_cases", "negative_variants", "variants", "negatives")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_manifest(task_dir: Path) -> Path:
    root_manifest = task_dir / "negative_variants" / "manifest.json"
    if root_manifest.exists():
        return root_manifest
    nested = sorted((task_dir / "negative_variants").glob("*/manifest.json"))
    assert len(nested) == 1, f"{task_dir.name} must have one canonical negative manifest"
    return nested[0]


def manifest_cases(manifest_path: Path) -> list[dict[str, Any]]:
    manifest = read_json(manifest_path)
    assert isinstance(manifest, dict), f"{manifest_path} must contain an object"
    for key in NEGATIVE_LIST_KEYS:
        cases = manifest.get(key)
        if isinstance(cases, list):
            return [case for case in cases if isinstance(case, dict)]
    raise AssertionError(f"{manifest_path} does not declare negative cases")


def case_file_candidates(task_dir: Path, case: dict[str, Any], target: str) -> list[Path]:
    variant_id = str(case.get("id") or "")
    raw_paths: list[str] = []
    for key in ("files", "source", "path", "artifact", "target"):
        value = case.get(key)
        if isinstance(value, str):
            raw_paths.append(value)
        elif isinstance(value, list):
            raw_paths.extend(str(item) for item in value if isinstance(item, str))
    candidates: list[Path] = []
    for raw_path in raw_paths:
        path = Path(raw_path)
        if path.is_absolute():
            candidates.append(path)
        else:
            candidates.extend([
                task_dir / path,
                task_dir / "negative_variants" / path,
                task_dir / "negative_variants" / variant_id / path,
            ])
    if variant_id:
        candidates.append(task_dir / "negative_variants" / variant_id / target)
    return candidates


def test_every_v3_task_declares_exactly_five_negative_variants() -> None:
    tasks = read_json(TASKS)["tasks"]
    task_dirs = {path.name for path in TASK_ROOT.iterdir() if path.is_dir()}
    assert set(tasks) == task_dirs

    for slug, task in tasks.items():
        task_dir = TASK_ROOT / slug
        target = str((task.get("target") or [""])[0])
        manifest_path = canonical_manifest(task_dir)
        cases = manifest_cases(manifest_path)
        ids = [str(case.get("id") or "") for case in cases]

        assert len(cases) == 5, f"{slug} must declare exactly five negative variants"
        assert all(ids), f"{slug} has a negative variant with no id"
        assert len(set(ids)) == 5, f"{slug} negative variant ids must be unique"
        for case in cases:
            existing = [path for path in case_file_candidates(task_dir, case, target) if path.exists()]
            assert existing, f"{slug} {case.get('id')} does not reference a materialized negative file"
