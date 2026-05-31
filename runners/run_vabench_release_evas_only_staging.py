#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from run_gold_suite import run_gold_case


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
DEFAULT_MANIFEST = PACKAGE_ROOT / "reports" / "dual_rerun_staging_manifest.json"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / "vabench-release-v1-evas-only-staging"
PRIMARY_VARIANTS = {"gold", "fixed"}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def rel_or_abs(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def normalize_path(text: str, *, default_root: Path = ROOT) -> Path:
    path = Path(text)
    return path if path.is_absolute() else default_root / path


def select_bundles(
    manifest: dict[str, object],
    *,
    include_buggy: bool,
    entry: set[str] | None,
    form: set[str] | None,
    variant: set[str] | None,
    limit: int | None,
) -> list[dict[str, object]]:
    bundles: list[dict[str, object]] = []
    for record in manifest.get("bundles", []):
        if not isinstance(record, dict) or record.get("status") != "ready":
            continue
        record_variant = str(record["variant"])
        if not include_buggy and record_variant not in PRIMARY_VARIANTS:
            continue
        if entry and str(record["entry_id"]) not in entry:
            continue
        if form and str(record["form"]) not in form:
            continue
        if variant and record_variant not in variant:
            continue
        bundles.append(record)
    bundles.sort(key=lambda row: (str(row["entry_id"]), str(row["form"]), str(row["variant"])))
    return bundles[:limit] if limit is not None else bundles


def expected_result_met(raw_result: dict[str, object], expected_result: str) -> bool:
    status = str(raw_result.get("status", "UNKNOWN"))
    if expected_result == "pass":
        return status == "PASS"
    if expected_result == "fail":
        # Buggy counterparts should compile and then fail the behavioral check.
        return status == "FAIL_SIM_CORRECTNESS"
    return False


def run_one(
    *,
    index: int,
    record: dict[str, object],
    output_root: Path,
    timeout_s: int,
) -> tuple[int, dict[str, object]]:
    task_dir = normalize_path(str(record["staged_task_dir"]))
    result_root = output_root / str(record["entry_id"]) / str(record["form"]) / str(record["variant"])
    started_at = datetime.now().isoformat(timespec="seconds")
    t0 = time.perf_counter()
    try:
        raw_result = run_gold_case(task_dir, result_root, timeout_s)
    except Exception as exc:
        raw_result = {
            "task_id": record.get("source_task_id") or record.get("entry_id"),
            "checker_task_id": record.get("checker_task_id"),
            "status": "FAIL_INFRA",
            "notes": [f"evas_only_exception={type(exc).__name__}: {str(exc)[:500]}"],
        }
    wall_time_s = time.perf_counter() - t0
    expected = str(record.get("expected_result", "pass"))
    result = {
        "entry_id": record["entry_id"],
        "form": record["form"],
        "variant": record["variant"],
        "expected_result": expected,
        "expected_result_met": expected_result_met(raw_result, expected),
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "wall_time_s": round(wall_time_s, 6),
        "staged_task_dir": record["staged_task_dir"],
        "result_root": rel_or_abs(result_root),
        "raw_result": raw_result,
    }
    return index, result


def summarize_results(
    *,
    manifest_path: Path,
    output_root: Path,
    bundles: list[dict[str, object]],
    results: list[dict[str, object]],
    started_at: str,
    workers: int,
    timeout_s: int,
    status: str,
) -> dict[str, object]:
    raw_status_counts = Counter(str(row["raw_result"].get("status", "UNKNOWN")) for row in results)
    form_counts = Counter(str(row["form"]) for row in results)
    variant_counts = Counter(str(row["variant"]) for row in results)
    expected_counts = Counter(
        "met" if row["expected_result_met"] else "miss"
        for row in results
    )
    miss_rows = [
        {
            "entry_id": row["entry_id"],
            "form": row["form"],
            "variant": row["variant"],
            "expected_result": row["expected_result"],
            "status": row["raw_result"].get("status"),
            "notes": row["raw_result"].get("notes", []),
            "checker_task_id": row["raw_result"].get("checker_task_id"),
        }
        for row in results
        if not row["expected_result_met"]
    ]
    return {
        "status": status,
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "manifest": rel_or_abs(manifest_path),
        "output_root": rel_or_abs(output_root),
        "workers": workers,
        "timeout_s": timeout_s,
        "selected_bundle_count": len(bundles),
        "completed_bundle_count": len(results),
        "pass_count": raw_status_counts.get("PASS", 0),
        "nonpass_count": len(results) - raw_status_counts.get("PASS", 0),
        "expected_met_count": expected_counts.get("met", 0),
        "expected_miss_count": expected_counts.get("miss", 0),
        "raw_status_counts": dict(sorted(raw_status_counts.items())),
        "form_counts": dict(sorted(form_counts.items())),
        "variant_counts": dict(sorted(variant_counts.items())),
        "expected_miss_rows": miss_rows,
        "results": results,
    }


def write_markdown(summary: dict[str, object], path: Path) -> None:
    lines = [
        "# vaBench Release EVAS-Only Staging Audit",
        "",
        f"Status: `{summary['status']}`",
        f"Manifest: `{summary['manifest']}`",
        f"Output root: `{summary['output_root']}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| selected bundles | {summary['selected_bundle_count']} |",
        f"| completed bundles | {summary['completed_bundle_count']} |",
        f"| PASS | {summary['pass_count']} |",
        f"| non-PASS | {summary['nonpass_count']} |",
        f"| expected met | {summary['expected_met_count']} |",
        f"| expected miss | {summary['expected_miss_count']} |",
        "",
        "## Raw Status Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status, count in dict(summary["raw_status_counts"]).items():
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## Expected Miss Rows", ""])
    miss_rows = list(summary["expected_miss_rows"])
    if not miss_rows:
        lines.append("None.")
    else:
        lines.extend(["| Entry | Form | Variant | Expected | Actual | Notes |", "| --- | --- | --- | --- | --- | --- |"])
        for row in miss_rows:
            notes = "; ".join(str(note) for note in row.get("notes", []))[:240]
            lines.append(
                f"| `{row['entry_id']}` | `{row['form']}` | `{row['variant']}` | "
                f"`{row['expected_result']}` | `{row['status']}` | {notes} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run EVAS-only checks over a staged vaBench release manifest.")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout-s", type=int, default=180)
    ap.add_argument("--include-buggy", action="store_true")
    ap.add_argument("--entry", action="append")
    ap.add_argument("--form", action="append")
    ap.add_argument("--variant", action="append")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--summary-json", default="")
    ap.add_argument("--summary-md", default="")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = normalize_path(args.manifest)
    output_root = normalize_path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    manifest = read_json(manifest_path)
    bundles = select_bundles(
        manifest,
        include_buggy=args.include_buggy,
        entry=set(args.entry) if args.entry else None,
        form=set(args.form) if args.form else None,
        variant=set(args.variant) if args.variant else None,
        limit=args.limit,
    )
    started_at = datetime.now().isoformat(timespec="seconds")
    results_by_index: dict[int, dict[str, object]] = {}
    summary_json = normalize_path(args.summary_json) if args.summary_json else output_root / "summary.json"
    summary_md = normalize_path(args.summary_md) if args.summary_md else output_root / "summary.md"
    partial_json = output_root / "summary.partial.json"
    workers = max(1, min(args.workers, len(bundles) or 1))

    def write_partial() -> None:
        results = [results_by_index[idx] for idx in sorted(results_by_index)]
        partial = summarize_results(
            manifest_path=manifest_path,
            output_root=output_root,
            bundles=bundles,
            results=results,
            started_at=started_at,
            workers=workers,
            timeout_s=args.timeout_s,
            status="running",
        )
        write_json(partial_json, partial)

    if workers == 1:
        for idx, record in enumerate(bundles, start=1):
            completed_idx, result = run_one(index=idx, record=record, output_root=output_root, timeout_s=args.timeout_s)
            results_by_index[completed_idx] = result
            write_partial()
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(run_one, index=idx, record=record, output_root=output_root, timeout_s=args.timeout_s)
                for idx, record in enumerate(bundles, start=1)
            ]
            for future in as_completed(futures):
                completed_idx, result = future.result()
                results_by_index[completed_idx] = result
                write_partial()

    results = [results_by_index[idx] for idx in sorted(results_by_index)]
    summary = summarize_results(
        manifest_path=manifest_path,
        output_root=output_root,
        bundles=bundles,
        results=results,
        started_at=started_at,
        workers=workers,
        timeout_s=args.timeout_s,
        status="complete",
    )
    write_json(summary_json, summary)
    write_markdown(summary, summary_md)
    print(
        "EVAS-only staging audit: {met}/{total} expected outcomes met; status_counts={counts}".format(
            met=summary["expected_met_count"],
            total=summary["selected_bundle_count"],
            counts=summary["raw_status_counts"],
        )
    )
    return 0 if summary["expected_miss_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
