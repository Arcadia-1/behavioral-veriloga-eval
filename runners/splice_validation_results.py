#!/usr/bin/env python3
"""Splice targeted validation results into a prior full result root.

Default workflow:
  old full results - affected old tasks + targeted rerun tasks -> merged root

The merged root is meant for fast development summaries.  It does not replace
checkpoint full runs for paper tables or kernel-level claims.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Any

from score import build_model_results


RESULT_FILES = {
    "evas": "evas_result.json",
    "spectre": "spectre_result.json",
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _normalized_required_axes(required_axes: list[str] | None = None) -> list[str]:
    aliases = {
        "syntax": "dut_compile",
        "routing": "tb_compile",
        "simulation": "sim_correct",
        "behavior": "sim_correct",
    }
    axes = required_axes or ["dut_compile", "tb_compile", "sim_correct"]
    normalized: list[str] = []
    for axis in axes:
        mapped = aliases.get(axis, axis)
        if mapped not in normalized:
            normalized.append(mapped)
    return normalized or ["dut_compile", "tb_compile", "sim_correct"]


def _passes_required_axes(result: dict[str, Any]) -> bool:
    scores = result.get("scores", {})
    required_axes = _normalized_required_axes(result.get("required_axes"))
    return all(float(scores.get(axis, 0.0) or 0.0) >= 1.0 for axis in required_axes)


def _detect_backend(root: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    found = [backend for backend, filename in RESULT_FILES.items() if list(root.glob(f"*/{filename}"))]
    if len(found) != 1:
        raise SystemExit(f"cannot auto-detect backend in {root}; use --backend evas|spectre")
    return found[0]


def _task_result_dirs(root: Path, backend: str) -> dict[str, Path]:
    filename = RESULT_FILES[backend]
    dirs: dict[str, Path] = {}
    for path in sorted(root.glob(f"*/{filename}")):
        data = _read_json(path)
        task_id = data.get("task_id") or path.parent.name
        dirs[task_id] = path.parent
    return dirs


def _load_results(root: Path, backend: str) -> dict[str, dict[str, Any]]:
    filename = RESULT_FILES[backend]
    results: dict[str, dict[str, Any]] = {}
    for path in sorted(root.glob(f"*/{filename}")):
        data = _read_json(path)
        task_id = data.get("task_id") or path.parent.name
        results[task_id] = data
    return results


def _aggregate(results: list[dict[str, Any]], *, backend: str, family: str, model_name: str) -> dict[str, Any]:
    model_like = [
        {
            "task_id": r["task_id"],
            "family": family,
            "required_axes": _normalized_required_axes(r.get("required_axes")),
            "scores": r.get("scores", {}),
            "status": r.get("status", "FAIL_INFRA"),
        }
        for r in results
    ]
    aggregate = build_model_results(model_name, model_like, 0.0, 1.0)
    aggregate["backend"] = backend
    aggregate["pass_tasks"] = [r["task_id"] for r in results if _passes_required_axes(r)]
    aggregate["fail_tasks"] = [
        {"task_id": r["task_id"], "status": r.get("status"), "notes": r.get("notes", [])[-5:]}
        for r in results
        if not _passes_required_axes(r)
    ]
    return aggregate


def _replace_dir(src: Path, dst: Path, *, copy: bool) -> None:
    if dst.exists() or dst.is_symlink():
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
        else:
            shutil.rmtree(dst)
    if copy:
        shutil.copytree(src, dst)
    else:
        os.symlink(src.resolve(), dst, target_is_directory=True)


def _compare_statuses(base: dict[str, dict[str, Any]], other: dict[str, dict[str, Any]]) -> dict[str, Any]:
    tasks = sorted(set(base) | set(other))
    status_mismatches = []
    binary_mismatches = []
    for task_id in tasks:
        left = base.get(task_id, {}).get("status", "MISSING")
        right = other.get(task_id, {}).get("status", "MISSING")
        if left != right:
            status_mismatches.append({"task_id": task_id, "left": left, "right": right})
        if (left == "PASS") != (right == "PASS"):
            binary_mismatches.append({"task_id": task_id, "left": left, "right": right})
    return {
        "left_total": len(base),
        "right_total": len(other),
        "left_pass": sum(1 for item in base.values() if item.get("status") == "PASS"),
        "right_pass": sum(1 for item in other.values() if item.get("status") == "PASS"),
        "binary_pass_fail_mismatches": binary_mismatches,
        "status_label_mismatches": status_mismatches,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-results", required=True, type=Path)
    parser.add_argument("--patch-results", required=True, action="append", type=Path)
    parser.add_argument("--output-results", required=True, type=Path)
    parser.add_argument("--backend", choices=["auto", "evas", "spectre"], default="auto")
    parser.add_argument("--family", default=None)
    parser.add_argument("--model-name", default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--copy", action="store_true", help="Copy task dirs instead of symlinking them.")
    parser.add_argument("--compare-results", action="append", type=Path, default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_root = args.base_results.resolve()
    patch_roots = [path.resolve() for path in args.patch_results]
    output_root = args.output_results.resolve()
    backend = _detect_backend(base_root, args.backend)

    if output_root.exists() or output_root.is_symlink():
        if not args.force:
            raise SystemExit(f"output exists; pass --force to replace: {output_root}")
        if output_root.is_symlink() or output_root.is_file():
            output_root.unlink()
        else:
            shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    base_dirs = _task_result_dirs(base_root, backend)
    patch_dirs: dict[str, tuple[Path, Path]] = {}
    for patch_root in patch_roots:
        patch_backend = _detect_backend(patch_root, backend)
        if patch_backend != backend:
            raise SystemExit(f"backend mismatch: base={backend}, patch={patch_backend} ({patch_root})")
        for task_id, task_dir in _task_result_dirs(patch_root, backend).items():
            patch_dirs[task_id] = (patch_root, task_dir)

    missing_from_base = sorted(set(patch_dirs) - set(base_dirs))
    if missing_from_base:
        raise SystemExit(f"patch contains tasks missing from base: {missing_from_base[:10]}")

    selected_dirs: dict[str, Path] = dict(base_dirs)
    selected_source: dict[str, str] = {task_id: str(base_root) for task_id in base_dirs}
    for task_id, (patch_root, task_dir) in patch_dirs.items():
        selected_dirs[task_id] = task_dir
        selected_source[task_id] = str(patch_root)

    for task_id, task_dir in sorted(selected_dirs.items()):
        _replace_dir(task_dir, output_root / task_id, copy=args.copy)

    results_by_task = _load_results(output_root, backend)
    results = [results_by_task[task_id] for task_id in sorted(results_by_task)]

    base_summary = _read_json(base_root / "summary.json") if (base_root / "summary.json").exists() else {}
    family = args.family
    if family is None:
        family = next(iter((base_summary.get(backend) or {}).get("by_family", {"spliced": 0.0})), "spliced")
    model_name = args.model_name or f"{family}-spliced-{backend}"

    aggregate = _aggregate(results, backend=backend, family=family, model_name=model_name)
    summary = {
        "total_tasks": len(results),
        "backend": backend,
        "source": base_summary.get("source", "spliced"),
        "candidate_root": base_summary.get("candidate_root"),
        "model": base_summary.get("model"),
        backend: aggregate,
        "splice": {
            "base_results": str(base_root),
            "patch_results": [str(path) for path in patch_roots],
            "patched_tasks": sorted(patch_dirs),
            "patched_task_count": len(patch_dirs),
            "copy_mode": "copy" if args.copy else "symlink",
        },
    }

    _write_json(output_root / f"{backend}_model_results.json", aggregate)
    _write_json(output_root / "summary.json", summary)

    manifest = {
        **summary["splice"],
        "backend": backend,
        "output_results": str(output_root),
        "task_sources": selected_source,
    }
    _write_json(output_root / "splice_manifest.json", manifest)

    comparisons: dict[str, Any] = {}
    for compare_root in args.compare_results:
        compare_root = compare_root.resolve()
        compare_backend = _detect_backend(compare_root, "auto")
        comparisons[str(compare_root)] = _compare_statuses(results_by_task, _load_results(compare_root, compare_backend))
        comparisons[str(compare_root)]["right_backend"] = compare_backend
    if comparisons:
        _write_json(output_root / "splice_comparisons.json", comparisons)

    print(json.dumps({
        "output_results": str(output_root),
        "backend": backend,
        "total_tasks": len(results),
        "pass_count": aggregate["pass_count"],
        "patched_task_count": len(patch_dirs),
        "comparisons": {
            key: {
                "binary_pass_fail_mismatches": len(value["binary_pass_fail_mismatches"]),
                "status_label_mismatches": len(value["status_label_mismatches"]),
            }
            for key, value in comparisons.items()
        },
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
