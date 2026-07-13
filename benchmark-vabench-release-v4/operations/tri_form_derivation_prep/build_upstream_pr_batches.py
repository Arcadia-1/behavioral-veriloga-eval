#!/usr/bin/env python3
"""Build canonical-family PR batches for the v4 DUT release."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NUMBERING = ROOT / "reports/v4_task_family_numbering/numbering_plan.json"
DEFAULT_ACTIVE = Path(__file__).resolve().parent / "ACTIVE_MUTATION_SUITE_INDEX.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "UPSTREAM_PR_BATCHES.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--numbering-plan", type=Path, default=DEFAULT_NUMBERING)
    parser.add_argument("--active-suite", type=Path, default=DEFAULT_ACTIVE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--batch-size", type=int, default=50)
    args = parser.parse_args()

    if args.batch_size <= 0:
        raise SystemExit("batch size must be positive")

    rows = read_json(args.numbering_plan.resolve()).get("rows") or []
    active_payload = read_json(args.active_suite.resolve())
    active = {
        str(item["family_id"]).zfill(3): item
        for item in active_payload.get("families") or []
    }
    if len(rows) != 400 or len(active) != 400:
        raise SystemExit(f"expected 400 numbering rows and suites, got {len(rows)} and {len(active)}")

    families: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda item: int(item["canonical_dut_id"])):
        canonical_id = str(row["canonical_dut_id"]).zfill(3)
        suite = active.get(canonical_id)
        if suite is None:
            raise SystemExit(f"missing exact-five suite for family {canonical_id}")
        mutations = [str(item) for item in suite.get("testbench_suite") or []]
        if len(mutations) != 5 or len(set(mutations)) != 5:
            raise SystemExit(f"family {canonical_id} does not have five distinct active mutations")
        bugfix_seed = str(suite.get("bugfix_seed") or "")
        if bugfix_seed not in mutations:
            raise SystemExit(f"family {canonical_id} bugfix seed is outside its active suite")
        old_slug = str(row["old_dut_slug"])
        families.append(
            {
                "canonical_id": canonical_id,
                "canonical_dut_slug": str(row["canonical_dut_slug"]),
                "source_task_dir": f"tasks/{old_slug}",
                "category": str(row["category"]),
                "level": str(row["level"]),
                "active_mutations": mutations,
                "bugfix_seed": bugfix_seed,
                "suite_review_status": str(suite.get("review_status") or ""),
            }
        )

    batches: list[dict[str, Any]] = []
    for start in range(0, len(families), args.batch_size):
        items = families[start : start + args.batch_size]
        batch_number = len(batches) + 1
        batches.append(
            {
                "batch_id": f"dut-{items[0]['canonical_id']}-{items[-1]['canonical_id']}",
                "sequence": batch_number,
                "canonical_start": items[0]["canonical_id"],
                "canonical_end": items[-1]["canonical_id"],
                "family_count": len(items),
                "commit_groups": [
                    {
                        "canonical_start": group[0]["canonical_id"],
                        "canonical_end": group[-1]["canonical_id"],
                        "family_count": len(group),
                    }
                    for offset in range(0, len(items), 10)
                    for group in [items[offset : offset + 10]]
                ],
                "families": items,
            }
        )

    payload = {
        "schema_version": "v4-upstream-pr-batches-v1",
        "status": "preparation_only",
        "policy": {
            "family_batch_size": args.batch_size,
            "commit_family_count": 10,
            "membership_key": "canonical_dut_id",
            "active_mutations_per_family": 5,
        },
        "summary": {
            "batch_count": len(batches),
            "family_count": len(families),
            "active_mutation_count": sum(len(item["active_mutations"]) for item in families),
        },
        "batches": batches,
    }
    args.output.resolve().write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "UPSTREAM_PR_BATCHES "
        f"batches={len(batches)} families={len(families)} "
        f"active_mutations={payload['summary']['active_mutation_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
