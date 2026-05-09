#!/usr/bin/env python3
"""Select affected benchmark tasks from feature tags.

This is the front door for targeted regression.  Feed it the JSON produced by
`tag_benchmark_features.py`, then choose one or more change types or explicit
features.  The output task list can be passed to validation runners with
repeated `--task` arguments.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEATURES = ROOT / "analysis" / "vabench_main_feature_tags.json"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_task_file(path: Path | None) -> set[str]:
    if path is None:
        return set()
    tasks: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if item and not item.startswith("#"):
            tasks.add(item)
    return tasks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features-json", type=Path, default=DEFAULT_FEATURES)
    parser.add_argument("--change-type", action="append", default=[], help="Named change family, e.g. cross, timer, pulse, preflight.")
    parser.add_argument("--feature", action="append", default=[], help="Explicit feature name, e.g. uses_cross.")
    parser.add_argument("--task", action="append", default=[], help="Force-include task id.")
    parser.add_argument("--task-file", type=Path, help="Force-include task ids from a newline-delimited file.")
    parser.add_argument("--form", action="append", default=[], help="Restrict to task form(s).")
    parser.add_argument("--pack", action="append", default=[], help="Restrict to pack id(s).")
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--format", choices=["json", "plain", "args"], default="json")
    parser.add_argument("--allow-empty", action="store_true", help="Return success even when no tasks are selected.")
    parser.add_argument("--include-uncertain", action="store_true",
                        help="Also include tasks with tagger uncertainty markers after form/pack filters.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = _read_json(args.features_json)
    change_map = data.get("change_feature_map", {})
    selected_features: set[str] = set(args.feature)
    unknown_change_types: list[str] = []
    for change_type in args.change_type:
        features = change_map.get(change_type)
        if not features:
            unknown_change_types.append(change_type)
            continue
        selected_features.update(features)

    forced_tasks = set(args.task) | _load_optional_task_file(args.task_file)
    forms = set(args.form)
    packs = set(args.pack)
    selected: list[dict[str, Any]] = []
    for task_id, task in sorted(data.get("tasks", {}).items()):
        if forms and task.get("task_form") not in forms:
            continue
        if packs and task.get("pack_id") not in packs:
            continue
        features = set(task.get("features", []))
        uncertainty = list(task.get("uncertainty", []))
        matched = sorted(features & selected_features)
        uncertain = bool(args.include_uncertain and uncertainty)
        forced = task_id in forced_tasks
        if not matched and not forced and not uncertain:
            continue
        selected.append({
            "task_id": task_id,
            "task_form": task.get("task_form", ""),
            "pack_id": task.get("pack_id", ""),
            "matched_features": matched,
            "uncertainty": uncertainty,
            "forced": forced,
            "included_by_uncertainty": uncertain and not matched and not forced,
        })

    selected.sort(key=lambda item: (not item["forced"], item["task_id"]))

    if args.max_tasks > 0:
        selected = selected[: args.max_tasks]

    result = {
        "features_json": str(args.features_json),
        "change_types": args.change_type,
        "selected_features": sorted(selected_features),
        "include_uncertain": args.include_uncertain,
        "unknown_change_types": unknown_change_types,
        "selected_count": len(selected),
        "tasks": selected,
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif args.format == "plain":
        for item in selected:
            print(item["task_id"])
    else:
        print(" ".join(f"--task {item['task_id']}" for item in selected))
    if unknown_change_types:
        return 1
    if not selected and not args.allow_empty:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
