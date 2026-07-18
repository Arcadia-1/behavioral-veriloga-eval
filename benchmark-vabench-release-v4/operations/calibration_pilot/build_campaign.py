#!/usr/bin/env python3
"""Build the preregistered v4 calibration campaign without running models."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
DEFAULT_RELEASE = PACKAGE / "release" / "benchmarkv4-r46"
MODES = tuple(f"G{i}" for i in range(6))
FORM_ORDER = {"dut": 0, "testbench": 1, "bugfix": 2}
MODE_RESPONSE_PROTOCOL = {
    "direct_one_shot": "v4-exact-artifact-blocks-v1",
    "agentic": "v4-strict-workspace-finalizer-v1",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_records(release: Path) -> dict[tuple[str, str], dict[str, Any]]:
    records_path = release / "prompt_modes" / "PROMPT_RECORDS.jsonl"
    if not records_path.is_file():
        return {}
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for line in records_path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        rows[(str(row["task_id"]), str(row["mode"]))] = row
    return rows


def mode_prompt_record(release: Path, task_id: str, mode: str) -> dict[str, Any]:
    modes = read_json(release / "prompt_modes" / "modes.json")["modes"]
    spec = modes[mode]
    process = str(spec["process"])
    return {
        "task_id": task_id,
        "mode": mode,
        "process": process,
        "evas_cli_available": process == "agentic",
        "response_protocol": MODE_RESPONSE_PROTOCOL[process],
        "prompt_mode_spec": spec,
    }


def complete_family_ids(task_index: list[dict[str, Any]]) -> list[str]:
    forms_by_family: dict[str, set[str]] = {}
    for row in task_index:
        forms_by_family.setdefault(str(row["family_id"]), set()).add(str(row["form"]))
    required = {"dut", "testbench", "bugfix"}
    return sorted(
        (family_id for family_id, forms in forms_by_family.items() if forms == required),
        key=lambda value: int(value),
    )


def selected_family_ids(
    task_index: list[dict[str, Any]],
    *,
    selection_path: Path | None,
    sample_families: int | None,
    family_ids: list[str] | None = None,
    seed: int,
) -> tuple[list[str], dict[str, Any]]:
    selector_count = sum(
        item is not None for item in (selection_path, sample_families, family_ids)
    )
    if selector_count > 1:
        raise ValueError("use only one of --selection, --sample-families, or explicit family_ids")
    if family_ids is not None:
        selected = sorted({str(item) for item in family_ids}, key=lambda value: int(value))
        if not selected:
            raise ValueError("explicit family_ids must not be empty")
        return selected, {
            "selection_manifest": None,
            "selection": {
                "schema_version": "v4-calibration-explicit-family-selection-v1",
                "method": "explicit_family_ids",
                "family_ids": selected,
            },
        }
    if selection_path is not None:
        selection = read_json(selection_path)
        family_ids = sorted(
            {str(row["family_id"]) for row in selection["families"]},
            key=lambda value: int(value),
        )
        return family_ids, {
            "selection_manifest": str(selection_path),
            "selection_manifest_sha256": sha256(selection_path),
        }
    if sample_families is None:
        raise ValueError("provide --selection or --sample-families")
    candidates = complete_family_ids(task_index)
    if sample_families <= 0 or sample_families > len(candidates):
        raise ValueError(
            f"--sample-families must be in 1..{len(candidates)}, got {sample_families}"
        )
    rng = random.Random(seed)
    family_ids = sorted(rng.sample(candidates, sample_families), key=lambda value: int(value))
    return family_ids, {
        "selection_manifest": None,
        "selection": {
            "schema_version": "v4-calibration-random-family-selection-v1",
            "method": "complete_family_sample_without_replacement",
            "seed": seed,
            "sample_families": sample_families,
            "family_ids": family_ids,
        },
    }


def build_campaign(
    release: Path,
    *,
    selection_path: Path | None = None,
    sample_families: int | None = None,
    family_ids: list[str] | None = None,
    seed: int = 0,
    model_provider: str,
    model: str,
    max_working_tokens: int,
    repetitions: int,
) -> dict[str, Any]:
    task_index = read_json(release / "TASK_INDEX.json")["tasks"]
    family_ids, selection_record = selected_family_ids(
        task_index,
        selection_path=selection_path,
        sample_families=sample_families,
        family_ids=family_ids,
        seed=seed,
    )
    family_set = set(family_ids)
    tasks = [row for row in task_index if str(row["family_id"]) in family_set]
    tasks.sort(key=lambda row: (str(row["family_id"]), FORM_ORDER[str(row["form"])]))
    if len(tasks) != len(family_set) * 3:
        raise ValueError(f"expected {len(family_set) * 3} pilot tasks, found {len(tasks)}")
    prompts = prompt_records(release)
    cells = []
    for repetition in range(repetitions):
        for task in tasks:
            for mode in MODES:
                task_id = str(task["task_id"])
                prompt = prompts.get((task_id, mode)) or mode_prompt_record(release, task_id, mode)
                cells.append({
                    "cell_id": f"{task_id}-{mode}-r{repetition:02d}",
                    "family_id": str(task["family_id"]),
                    "task_id": task_id,
                    "form": str(task["form"]),
                    "mode": mode,
                    "process": str(prompt["process"]),
                    "repetition": repetition,
                    "seed": repetition,
                    "max_output_tokens": max_working_tokens,
                    "max_working_tokens": max_working_tokens,
                    "prompt_record_sha256": hashlib.sha256(
                        json.dumps(prompt, sort_keys=True, separators=(",", ":")).encode("utf-8")
                    ).hexdigest(),
                    "evas_cli_available": bool(prompt["evas_cli_available"]),
                    "response_protocol": str(prompt["response_protocol"]),
                })
    return {
        "schema_version": "v4-calibration-campaign-v2",
        "status": "planned",
        "release": str(release),
        "release_manifest_sha256": sha256(release / "MANIFEST.json"),
        **selection_record,
        "model_provider": model_provider,
        "model": model,
        "budget_metric": "provider_completion_tokens_including_reasoning",
        "max_output_tokens": max_working_tokens,
        "max_working_tokens": max_working_tokens,
        "repetitions": repetitions,
        "family_count": len(family_set),
        "task_count": len(tasks),
        "mode_count": len(MODES),
        "cell_count": len(cells),
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--sample-families", type=int)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-provider", default="openai-compatible")
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--max-output-tokens", "--max-working-tokens",
        dest="max_working_tokens", type=int, required=True,
    )
    parser.add_argument("--repetitions", type=int, default=1)
    args = parser.parse_args()
    if args.max_working_tokens <= 0 or args.repetitions <= 0:
        parser.error("token budget and repetitions must be positive")
    campaign = build_campaign(
        args.release.resolve(),
        selection_path=args.selection.resolve() if args.selection else None,
        sample_families=args.sample_families,
        seed=args.seed,
        model_provider=args.model_provider,
        model=args.model,
        max_working_tokens=args.max_working_tokens,
        repetitions=args.repetitions,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(campaign, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: campaign[key] for key in ("family_count", "task_count", "mode_count", "cell_count")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
