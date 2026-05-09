#!/usr/bin/env python3
"""Export normalized failure taxonomy for a validation result root."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from failure_taxonomy_normalizer import normalize_failure


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
        raise SystemExit(f"cannot auto-detect backend in {root}; use --backend evas|spectre")
    return found[0]


def _load(root: Path, backend: str) -> dict[str, dict[str, Any]]:
    filename = RESULT_FILES[backend]
    results: dict[str, dict[str, Any]] = {}
    for path in sorted(root.glob(f"*/{filename}")):
        data = _read_json(path)
        task_id = data.get("task_id") or path.parent.name
        results[task_id] = data
    if not results:
        raise SystemExit(f"no {filename} files found in {root}")
    return results


def collect(root: Path, backend: str) -> dict[str, Any]:
    results = _load(root, backend)
    rows: list[dict[str, Any]] = []
    for task_id, result in sorted(results.items()):
        norm = normalize_failure(result)
        rows.append(
            {
                "task_id": task_id,
                "backend": backend,
                "raw_status": norm["raw_status"],
                "normalized_status": norm["normalized_status"],
                "failure_stage": norm["failure_stage"],
                "failure_origin": norm["failure_origin"],
                "failure_reason": norm["failure_reason"],
                "confidence": norm["confidence"],
                "blocking": norm["blocking"],
                "evidence": norm["evidence"],
                "notes_tail": result.get("notes", [])[-6:],
            }
        )

    status_counts = Counter(row["normalized_status"] for row in rows)
    raw_status_counts = Counter(row["raw_status"] for row in rows)
    stage_counts = Counter(row["failure_stage"] for row in rows)
    origin_counts = Counter(row["failure_origin"] for row in rows)
    reason_counts = Counter(row["failure_reason"] for row in rows)
    return {
        "result_root": str(root),
        "backend": backend,
        "total_tasks": len(rows),
        "normalized_status_counts": dict(sorted(status_counts.items())),
        "raw_status_counts": dict(sorted(raw_status_counts.items())),
        "failure_stage_counts": dict(sorted(stage_counts.items())),
        "failure_origin_counts": dict(sorted(origin_counts.items())),
        "failure_reason_counts": dict(sorted(reason_counts.items())),
        "rows": rows,
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "task_id",
        "backend",
        "raw_status",
        "normalized_status",
        "failure_stage",
        "failure_origin",
        "failure_reason",
        "confidence",
        "blocking",
        "evidence",
        "notes_tail",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "notes_tail": " | ".join(str(item) for item in row["notes_tail"])})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--backend", choices=["auto", "evas", "spectre"], default="auto")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--csv-output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.results.resolve()
    backend = _detect_backend(root, args.backend)
    payload = collect(root, backend)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.csv_output:
        _write_csv(args.csv_output, payload["rows"])
    print(
        json.dumps(
            {
                "output": str(args.output),
                "backend": backend,
                "total_tasks": payload["total_tasks"],
                "normalized_status_counts": payload["normalized_status_counts"],
                "failure_reason_counts": payload["failure_reason_counts"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
