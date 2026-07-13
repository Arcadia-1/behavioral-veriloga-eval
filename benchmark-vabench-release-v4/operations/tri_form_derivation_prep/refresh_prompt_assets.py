#!/usr/bin/env python3
"""Refresh prompt components and records without rebuilding task assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from materialize_tri_form_release import (
    DEFAULT_OUTPUT,
    install_prompt_assets,
    materialized_artifact_hashes,
    read_json,
    refresh_public_task_views,
    write_json,
    write_prompt_records,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    release = args.release.expanduser().resolve()
    task_rows = read_json(release / "TASK_INDEX.json").get("tasks") or []
    if len(task_rows) != 1200:
        raise SystemExit(f"release must contain exactly 1200 task rows: {release}")

    refreshed_forms = refresh_public_task_views(release, task_rows)
    skills = install_prompt_assets(release)
    write_prompt_records(release, task_rows, skills)
    manifest = read_json(release / "MANIFEST.json")
    manifest["prompt_record_count"] = len(task_rows) * 6
    manifest["prompt_composition_revision"] = "public_private_contract_v2_wrapper_last_v3"
    manifest["materialized_artifact_sha256"] = materialized_artifact_hashes(release)
    write_json(release / "MANIFEST.json", manifest)

    result = {
        "schema_version": "v4-prompt-refresh-result-v1",
        "release": str(release),
        "task_count": len(task_rows),
        "prompt_record_count": manifest["prompt_record_count"],
        "refreshed_public_task_forms": refreshed_forms,
        "composition_order": read_json(release / "prompt_modes" / "modes.json")["composition_order"],
        "materialized_artifact_sha256": manifest["materialized_artifact_sha256"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
