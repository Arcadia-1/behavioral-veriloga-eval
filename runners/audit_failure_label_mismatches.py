#!/usr/bin/env python3
"""Audit failure-label mismatches between two validation result roots."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from failure_taxonomy_normalizer import normalize_failure, normalize_pair


RESULT_FILES = {
    "evas": "evas_result.json",
    "spectre": "spectre_result.json",
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _detect_backend(root: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    found = [backend for backend, filename in RESULT_FILES.items() if list(root.glob(f"*/{filename}"))]
    if len(found) != 1:
        raise SystemExit(f"cannot auto-detect backend in {root}; use explicit backend")
    return found[0]


def _load(root: Path, backend: str) -> dict[str, dict[str, Any]]:
    filename = RESULT_FILES[backend]
    out = {}
    for path in sorted(root.glob(f"*/{filename}")):
        data = _read_json(path)
        task_id = data.get("task_id") or path.parent.name
        out[task_id] = data
    return out


def _pass_binary(status: str) -> bool:
    return status == "PASS"


def audit(left_root: Path, right_root: Path, left_backend: str, right_backend: str) -> dict[str, Any]:
    left = _load(left_root, left_backend)
    right = _load(right_root, right_backend)
    rows = []
    for task_id in sorted(set(left) | set(right)):
        l = left.get(task_id, {"status": "MISSING", "notes": []})
        r = right.get(task_id, {"status": "MISSING", "notes": []})
        left_status = l.get("status", "MISSING")
        right_status = r.get("status", "MISSING")
        if left_status == right_status:
            continue
        left_norm = normalize_failure(l)
        right_norm = normalize_failure(r)
        pair_norm = normalize_pair(l, r)
        row = {
            "task_id": task_id,
            "left_status": left_status,
            "right_status": right_status,
            "binary_mismatch": _pass_binary(left_status) != _pass_binary(right_status),
            "reason_family": pair_norm["failure_reason"],
            "pair_failure_stage": pair_norm["failure_stage"],
            "pair_failure_origin": pair_norm["failure_origin"],
            "left_normalized_status": left_norm["normalized_status"],
            "right_normalized_status": right_norm["normalized_status"],
            "left_failure_stage": left_norm["failure_stage"],
            "right_failure_stage": right_norm["failure_stage"],
            "left_failure_origin": left_norm["failure_origin"],
            "right_failure_origin": right_norm["failure_origin"],
            "left_failure_reason": left_norm["failure_reason"],
            "right_failure_reason": right_norm["failure_reason"],
            "normalized_reason_mismatch": left_norm["failure_reason"] != right_norm["failure_reason"],
            "normalized_stage_mismatch": left_norm["failure_stage"] != right_norm["failure_stage"],
            "left_notes": l.get("notes", [])[-6:],
            "right_notes": r.get("notes", [])[-6:],
        }
        rows.append(row)
    reason_counts = Counter(row["reason_family"] for row in rows)
    left_reason_counts = Counter(row["left_failure_reason"] for row in rows)
    right_reason_counts = Counter(row["right_failure_reason"] for row in rows)
    return {
        "left_root": str(left_root),
        "right_root": str(right_root),
        "left_backend": left_backend,
        "right_backend": right_backend,
        "left_total": len(left),
        "right_total": len(right),
        "left_pass": sum(1 for item in left.values() if item.get("status") == "PASS"),
        "right_pass": sum(1 for item in right.values() if item.get("status") == "PASS"),
        "status_mismatch_count": len(rows),
        "binary_mismatch_count": sum(1 for row in rows if row["binary_mismatch"]),
        "normalized_reason_mismatch_count": sum(1 for row in rows if row["normalized_reason_mismatch"]),
        "normalized_stage_mismatch_count": sum(1 for row in rows if row["normalized_stage_mismatch"]),
        "reason_counts": dict(sorted(reason_counts.items())),
        "left_reason_counts": dict(sorted(left_reason_counts.items())),
        "right_reason_counts": dict(sorted(right_reason_counts.items())),
        "mismatches": rows,
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "task_id",
        "left_status",
        "right_status",
        "binary_mismatch",
        "reason_family",
        "pair_failure_stage",
        "pair_failure_origin",
        "left_normalized_status",
        "right_normalized_status",
        "left_failure_reason",
        "right_failure_reason",
        "normalized_reason_mismatch",
        "left_failure_stage",
        "right_failure_stage",
        "normalized_stage_mismatch",
        "left_failure_origin",
        "right_failure_origin",
        "left_notes",
        "right_notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "left_notes": " | ".join(row["left_notes"]), "right_notes": " | ".join(row["right_notes"])})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left-results", required=True, type=Path)
    parser.add_argument("--right-results", required=True, type=Path)
    parser.add_argument("--left-backend", choices=["auto", "evas", "spectre"], default="auto")
    parser.add_argument("--right-backend", choices=["auto", "evas", "spectre"], default="auto")
    parser.add_argument("--output", type=Path, default=Path("analysis") / "failure_label_mismatch_audit.json")
    parser.add_argument("--csv-output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    left_root = args.left_results.resolve()
    right_root = args.right_results.resolve()
    left_backend = _detect_backend(left_root, args.left_backend)
    right_backend = _detect_backend(right_root, args.right_backend)
    result = audit(left_root, right_root, left_backend, right_backend)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.csv_output:
        _write_csv(args.csv_output, result["mismatches"])
    print(json.dumps({
        "output": str(args.output),
        "status_mismatch_count": result["status_mismatch_count"],
        "binary_mismatch_count": result["binary_mismatch_count"],
        "normalized_reason_mismatch_count": result["normalized_reason_mismatch_count"],
        "normalized_stage_mismatch_count": result["normalized_stage_mismatch_count"],
        "reason_counts": result["reason_counts"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
