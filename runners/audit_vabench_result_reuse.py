#!/usr/bin/env python3
"""Audit whether prior simulator results can be reused for current benchmark gold.

The intended use is incremental benchmark expansion: if a previous EVAS/Spectre
run already validated unchanged tasks, this script checks that the current
`gold/` files for those tasks still match the staged files saved by that prior
run. It does not prove prompt/checker stability; use the semantic and integrity
audits for that layer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _json_read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _backend_payload(summary: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    backend = summary.get("backend")
    if backend in ("evas", "spectre") and isinstance(summary.get(backend), dict):
        return backend, summary[backend]
    for key in ("evas", "spectre"):
        if isinstance(summary.get(key), dict):
            return key, summary[key]
    raise ValueError("summary.json does not contain an EVAS or Spectre payload")


def _file_names(root: Path) -> list[str]:
    if not root.exists():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_file())


def audit(bench_dir: Path, result_dir: Path, tasks: list[str] | None = None) -> dict[str, Any]:
    summary = _json_read(result_dir / "summary.json")
    backend, payload = _backend_payload(summary)
    selected = tasks or list(payload.get("pass_tasks", []))
    result: dict[str, Any] = {
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bench_dir": str(bench_dir.resolve()),
        "result_dir": str(result_dir.resolve()),
        "backend": backend,
        "tasks_checked": len(selected),
        "issues": [],
        "task_results": {},
    }

    issues: list[dict[str, Any]] = []
    task_results: dict[str, Any] = {}
    for task_id in sorted(selected):
        staged = result_dir / task_id / "staged"
        gold = bench_dir / "tasks" / task_id / "gold"
        staged_names = _file_names(staged)
        gold_names = _file_names(gold)
        task_info: dict[str, Any] = {
            "staged_files": staged_names,
            "gold_files": gold_names,
            "matches": [],
            "issues": [],
        }
        if not staged.exists():
            task_info["issues"].append("missing_staged_dir")
        if not gold.exists():
            task_info["issues"].append("missing_current_gold_dir")
        if staged_names != gold_names:
            task_info["issues"].append("file_list_mismatch")
        for name in sorted(set(staged_names) & set(gold_names)):
            staged_hash = _sha256(staged / name)
            gold_hash = _sha256(gold / name)
            match = staged_hash == gold_hash
            task_info["matches"].append(
                {
                    "file": name,
                    "match": match,
                    "staged_sha256": staged_hash,
                    "gold_sha256": gold_hash,
                }
            )
            if not match:
                task_info["issues"].append(f"hash_mismatch:{name}")
        if task_info["issues"]:
            issues.append({"task_id": task_id, "issues": task_info["issues"]})
        task_results[task_id] = task_info

    result["issues"] = issues
    result["task_results"] = task_results
    if issues:
        result["status"] = "FAIL"
    return result


def _write_report(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md = path.with_suffix(".md")
    lines = [
        "# vaBench Result Reuse Audit",
        "",
        f"- Status: `{data['status']}`",
        f"- Backend: `{data['backend']}`",
        f"- Tasks checked: `{data['tasks_checked']}`",
        f"- Result dir: `{data['result_dir']}`",
        f"- Benchmark dir: `{data['bench_dir']}`",
        "",
    ]
    if data["issues"]:
        lines.append("## Issues")
        for issue in data["issues"]:
            lines.append(f"- `{issue['task_id']}`: {', '.join(issue['issues'])}")
    else:
        lines.append("No staged/current gold mismatches found.")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bench-dir", type=Path, required=True)
    parser.add_argument("--result-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = audit(args.bench_dir, args.result_dir, args.task or None)
    _write_report(args.output, data)
    print(json.dumps({"status": data["status"], "tasks_checked": data["tasks_checked"]}, indent=2))
    return 0 if data["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
