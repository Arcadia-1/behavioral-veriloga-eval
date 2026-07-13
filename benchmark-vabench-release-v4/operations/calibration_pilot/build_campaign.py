#!/usr/bin/env python3
"""Build the preregistered v4 calibration campaign without running models."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
DEFAULT_RELEASE = PACKAGE / "release" / "tri-form-v4-1200-final"
DEFAULT_SELECTION = PACKAGE / "operations" / "api_pilot_selection_10_20260714.json"
MODES = tuple(f"G{i}" for i in range(6))
FORM_ORDER = {"dut": 0, "testbench": 1, "bugfix": 2}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_records(release: Path) -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for line in (release / "prompt_modes" / "PROMPT_RECORDS.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        rows[(str(row["task_id"]), str(row["mode"]))] = row
    return rows


def build_campaign(
    release: Path,
    selection_path: Path,
    *,
    model_provider: str,
    model: str,
    max_working_tokens: int,
    repetitions: int,
) -> dict[str, Any]:
    selection = read_json(selection_path)
    family_ids = {str(row["family_id"]) for row in selection["families"]}
    task_index = read_json(release / "TASK_INDEX.json")["tasks"]
    tasks = [row for row in task_index if str(row["family_id"]) in family_ids]
    tasks.sort(key=lambda row: (str(row["family_id"]), FORM_ORDER[str(row["form"])]))
    if len(tasks) != len(family_ids) * 3:
        raise ValueError(f"expected {len(family_ids) * 3} pilot tasks, found {len(tasks)}")
    prompts = prompt_records(release)
    cells = []
    for repetition in range(repetitions):
        for task in tasks:
            for mode in MODES:
                task_id = str(task["task_id"])
                prompt = prompts[(task_id, mode)]
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
                    "feedback_cli_available": bool(prompt["feedback_cli_available"]),
                    "response_protocol": str(prompt["response_protocol"]),
                })
    return {
        "schema_version": "v4-calibration-campaign-v2",
        "status": "planned",
        "release": str(release),
        "release_manifest_sha256": sha256(release / "MANIFEST.json"),
        "selection_manifest": str(selection_path),
        "selection_manifest_sha256": sha256(selection_path),
        "model_provider": model_provider,
        "model": model,
        "budget_metric": "provider_completion_tokens_including_reasoning",
        "max_output_tokens": max_working_tokens,
        "max_working_tokens": max_working_tokens,
        "repetitions": repetitions,
        "family_count": len(family_ids),
        "task_count": len(tasks),
        "mode_count": len(MODES),
        "cell_count": len(cells),
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
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
        args.selection.resolve(),
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
