#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
VABENCH300_MANIFEST = PACKAGE_ROOT / "vabench-300-expansion" / "VABENCH_300_MANIFEST.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_entry(payload: dict[str, Any]) -> dict[str, Any]:
    if "release_entry_id" not in payload and payload.get("legacy_entry_id"):
        payload["release_entry_id"] = payload["legacy_entry_id"]
    return payload


def infer_level(entry_id: str) -> str:
    if "_l1_" in entry_id:
        return "L1"
    if "_l2_" in entry_id:
        return "L2"
    return ""


def certification_status(task_manifest: dict[str, Any], row: dict[str, Any], key: str) -> str:
    cert = task_manifest.get("certification", {})
    if not isinstance(cert, dict):
        cert = {}
    return str(cert.get(key, row.get(key, row.get(f"{key}_status", "pending"))))


def release_task_from_manifest(row: dict[str, Any]) -> dict[str, Any]:
    task_manifest_path = ROOT / str(row.get("release_task_manifest", ""))
    task_manifest = read_json(task_manifest_path)
    artifacts = task_manifest.get("artifacts", {})
    if not isinstance(artifacts, dict):
        artifacts = {}
    source = task_manifest.get("source", {})
    if not isinstance(source, dict):
        source = {}
    return {
        "asset_materialized": True,
        "checks": artifacts.get("checks", row.get("checks", "")),
        "evas_status": certification_status(task_manifest, row, "evas"),
        "form": str(row.get("form", "")),
        "gold": artifacts.get("gold", []),
        "meta": artifacts.get("meta", row.get("meta", "")),
        "negatives": artifacts.get("negatives", row.get("negative_manifest", "")),
        "prompt": artifacts.get("prompt", row.get("prompt", "")),
        "release_path": source.get("release_path", task_manifest_path.parent.relative_to(ROOT).as_posix()),
        "spectre_status": certification_status(task_manifest, row, "spectre"),
        "static_status": certification_status(task_manifest, row, "static"),
    }


def merged_entry(entry_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    entry_paths = sorted(
        {
            entry_manifest_from_task_manifest(ROOT / str(row["release_task_manifest"]))
            for row in rows
            if row.get("release_task_manifest")
        }
    )
    payloads = [normalize_entry(read_json(path)) for path in entry_paths]
    primary = next((payload for payload in payloads if payload), {})
    first_row = rows[0]
    release_tasks = [release_task_from_manifest(row) for row in rows]
    release_tasks.sort(key=lambda item: {"dut": 0, "tb": 1, "e2e": 2, "bugfix": 3}.get(str(item.get("form")), 99))

    score_enabled_flags = []
    model_capability_flags = []
    l0_flags = []
    for row in rows:
        task_manifest = read_json(ROOT / str(row.get("release_task_manifest", "")))
        counts = task_manifest.get("counts", {}) if isinstance(task_manifest.get("counts"), dict) else {}
        score_enabled_flags.append(bool(counts.get("benchmark_score", False)))
        model_capability_flags.append(bool(counts.get("model_capability", False)))
        l0_flags.append(bool(counts.get("l0_conformance", False)))

    statuses = {
        key: [str(task.get(f"{key}_status", "pending")) for task in release_tasks]
        for key in ("static", "evas", "spectre")
    }
    certification = {
        key: "pass"
        if values and all(value == "pass" for value in values)
        else "fail"
        if any(value == "fail" for value in values)
        else "pending"
        for key, values in statuses.items()
    }
    existing_certification = primary.get("certification", {})
    if isinstance(existing_certification, dict):
        certification.update({key: value for key, value in existing_certification.items() if key not in certification})

    entry = dict(primary)
    entry.update(
        {
            "release_entry_id": entry_id,
            "legacy_entry_id": entry.get("legacy_entry_id", entry_id),
            "id": entry.get("id", first_row.get("topic_id", entry_id)),
            "level": entry.get("level") or first_row.get("level") or infer_level(entry_id),
            "track": entry.get("track") or first_row.get("track", "core"),
            "difficulty": entry.get("difficulty") or first_row.get("difficulty", "D2"),
            "category": entry.get("category") or first_row.get("category", ""),
            "base_function": entry.get("base_function") or first_row.get("base_function", ""),
            "score_surface": entry.get("score_surface") or first_row.get("score_surface", "model-capability"),
            "release_tasks": release_tasks,
            "missing_forms": [],
            "release_blockers": [
                blocker
                for blocker in entry.get("release_blockers", [])
                if blocker != "score_denominator_admission_pending_after_certification" or not all(score_enabled_flags)
            ],
            "certification": certification,
            "counts": {
                "benchmark_score": bool(score_enabled_flags) and all(score_enabled_flags),
                "l0_conformance": any(l0_flags),
                "model_capability": bool(model_capability_flags) and all(model_capability_flags),
            },
            "_manifest_path": rel(entry_paths[0]) if entry_paths else rel(VABENCH300_MANIFEST),
        }
    )
    return entry


def entry_manifest_from_task_manifest(task_manifest: Path) -> Path:
    return task_manifest.parent.parent.parent / "release_entry.json"


def task_manifest_path(task: dict[str, Any]) -> Path:
    return ROOT / str(task.get("release_path", "")) / "release_task.json"


def read_vabench300_entries() -> list[dict[str, Any]]:
    manifest = read_json(VABENCH300_MANIFEST)
    rows_by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in manifest.get("tasks", []):
        if not isinstance(row, dict):
            continue
        entry_id = str(row.get("legacy_entry_id") or row.get("release_entry_id") or "")
        if not entry_id or not row.get("release_task_manifest"):
            continue
        rows_by_entry[entry_id].append(row)

    return [merged_entry(entry_id, rows) for entry_id, rows in sorted(rows_by_entry.items())]


def read_release_entries() -> list[dict[str, Any]]:
    if VABENCH300_MANIFEST.exists():
        entries = read_vabench300_entries()
        if entries:
            return entries

    entries: list[dict[str, Any]] = []
    for path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        payload = normalize_entry(read_json(path))
        if payload:
            payload["_manifest_path"] = rel(path)
            entries.append(payload)
    return entries
