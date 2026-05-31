#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
DUAL_RERUN_SUMMARY_JSON = ROOT / "results" / "vabench-release-v1-dual-rerun" / "summary.json"
STAGING_MANIFEST_JSON = REPORTS_ROOT / "dual_rerun_staging_manifest.json"
QUEUE_JSON = REPORTS_ROOT / "dual_rerun_queue.json"
BRIDGE_JSON = REPORTS_ROOT / "bridge_profile_diagnostics.json"
IMPORT_JSON = REPORTS_ROOT / "dual_rerun_import.json"
SCORE_DENOMINATOR_JSON = REPORTS_ROOT / "score_denominator_manifest.json"
REPORT_JSON = REPORTS_ROOT / "speed_debug_artifact.json"
REPORT_MD = REPORTS_ROOT / "speed_debug_artifact.md"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def imported_summary_path(import_report: dict[str, object]) -> Path:
    summary = str(import_report.get("summary", "") or "")
    if not summary:
        return DUAL_RERUN_SUMMARY_JSON
    path = Path(summary)
    return path if path.is_absolute() else ROOT / path


def is_release_speed_summary(path: Path, imported_path: Path) -> bool:
    if path == imported_path:
        return True
    name = path.parent.name
    return "full-after-fixes" in name or "speed-remaining" in name


def float_or_none(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def ratio_or_none(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


DURATION_FACTORS = {
    "fs": 1e-15,
    "ps": 1e-12,
    "ns": 1e-9,
    "us": 1e-6,
    "µs": 1e-6,
    "ms": 1e-3,
    "s": 1.0,
    "sec": 1.0,
    "secs": 1.0,
    "second": 1.0,
    "seconds": 1.0,
    "m": 60.0,
    "min": 60.0,
    "mins": 60.0,
    "minute": 60.0,
    "minutes": 60.0,
    "h": 3600.0,
    "hr": 3600.0,
    "hrs": 3600.0,
    "hour": 3600.0,
    "hours": 3600.0,
}
DURATION_RE = r"((?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?)\s*(fs|ps|ns|us|µs|ms|s|secs?|seconds?|m|mins?|minutes?|h|hrs?|hours?)"


def duration_to_seconds(match: re.Match[str] | None) -> float | None:
    if not match:
        return None
    matches = re.findall(DURATION_RE, match.group(0))
    if not matches:
        return None
    value, unit = matches[-1]
    return float(value) * DURATION_FACTORS[unit]


def parse_spectre_timing(spectre_out: Path | None) -> dict[str, float | str | None]:
    if spectre_out is None or not spectre_out.exists():
        return {
            "source": "",
            "tran_elapsed_s": None,
            "total_elapsed_s": None,
            "wall_clock_elapsed_s": None,
        }
    text = spectre_out.read_text(encoding="utf-8", errors="replace")
    tran = duration_to_seconds(
        re.search(rf"Total time required for tran analysis.*?elapsed\s*=\s*{DURATION_RE}", text)
    )
    total = duration_to_seconds(re.search(rf"Time used:\s*CPU\s*=.*?elapsed\s*=\s*{DURATION_RE}", text))
    wall = duration_to_seconds(re.search(rf"elapsed time \(wall clock\):\s*{DURATION_RE}", text))
    return {
        "source": rel(spectre_out),
        "tran_elapsed_s": tran,
        "total_elapsed_s": total,
        "wall_clock_elapsed_s": wall,
    }


def spectre_out_path(raw: dict[str, object], item: dict[str, object]) -> Path | None:
    spectre = raw.get("spectre", {})
    if not isinstance(spectre, dict):
        spectre = {}
    csv_path = str(spectre.get("csv_path", "") or "")
    if csv_path:
        path = Path(csv_path)
        if not path.is_absolute():
            path = ROOT / path
        candidate = path.parent / "spectre.out"
        if candidate.exists():
            return candidate
    result_root = str(item.get("result_root", "") or "")
    task_id = str(raw.get("task_id", "") or "")
    if result_root and task_id:
        path = Path(result_root)
        if not path.is_absolute():
            path = ROOT / path
        candidate = path / task_id / "spectre" / "spectre.out"
        if candidate.exists():
            return candidate
    return None


def timing_rows(summary: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in summary.get("results", []):
        if not isinstance(item, dict):
            continue
        raw = item.get("raw_result", {})
        if not isinstance(raw, dict):
            raw = {}
        timing = raw.get("timing", {})
        if not isinstance(timing, dict):
            timing = {}
        if "evas_wall_time_s" not in timing or "spectre_wall_time_s" not in timing:
            continue
        evas = raw.get("evas", {})
        if not isinstance(evas, dict):
            evas = {}
        evas_timing = evas.get("timing", {})
        if not isinstance(evas_timing, dict):
            evas_timing = {}
        spectre_timing = parse_spectre_timing(spectre_out_path(raw, item))
        evas_wall = float(timing["evas_wall_time_s"])
        spectre_wall = float(timing["spectre_wall_time_s"])
        evas_total = float_or_none(evas_timing.get("total_elapsed_s"))
        evas_tran = float_or_none(evas_timing.get("tran_elapsed_s"))
        spectre_total = float_or_none(spectre_timing["total_elapsed_s"])
        spectre_tran = float_or_none(spectre_timing["tran_elapsed_s"])
        rows.append(
            {
                "entry_id": item.get("entry_id"),
                "form": item.get("form"),
                "variant": item.get("variant"),
                "raw_status": raw.get("status"),
                "evas_wall_time_s": evas_wall,
                "spectre_wall_time_s": spectre_wall,
                "combined_wall_time_s": float(timing.get("combined_wall_time_s", 0.0)),
                "evas_reported_total_elapsed_s": evas_total,
                "evas_reported_tran_elapsed_s": evas_tran,
                "evas_accepted_tran_steps": float_or_none(evas_timing.get("accepted_tran_steps")),
                "spectre_reported_total_elapsed_s": spectre_total,
                "spectre_reported_tran_elapsed_s": spectre_tran,
                "spectre_reported_wall_clock_elapsed_s": float_or_none(
                    spectre_timing["wall_clock_elapsed_s"]
                ),
                "spectre_timing_source": spectre_timing["source"],
                "wrapper_spectre_over_evas_speedup": ratio_or_none(spectre_wall, evas_wall),
                "reported_total_spectre_over_evas_speedup": ratio_or_none(spectre_total, evas_total),
                "tran_spectre_over_evas_speedup": ratio_or_none(spectre_tran, evas_tran),
            }
        )
    return rows


def discover_summaries(
    import_report: dict[str, object],
) -> tuple[list[tuple[Path, dict[str, object]]], dict[str, object]]:
    imported_path = imported_summary_path(import_report)
    imported = read_json(imported_path)
    candidates: list[tuple[float, Path, dict[str, object], list[dict[str, object]]]] = []
    for path in sorted((ROOT / "results").glob("vabench-release-v1-dual-rerun*/summary.json")):
        if not is_release_speed_summary(path, imported_path):
            continue
        summary = read_json(path)
        rows = timing_rows(summary)
        if summary.get("status") == "complete" and rows and not summary.get("dry_run", False):
            candidates.append((path.stat().st_mtime, path, summary, rows))
    imported_rows = timing_rows(imported)
    if imported.get("status") == "complete" and imported_rows and not imported.get("dry_run", False):
        return (
            [(imported_path, imported)],
            {
                "source": "dual_rerun_import",
                "imported_summary": rel(imported_path),
                "imported_summary_rejected_reason": "",
                "selected_summaries": [rel(imported_path)],
            },
        )
    if candidates:
        candidates.sort(key=lambda item: item[0])
        reject_reason = ""
        if imported.get("dry_run", False):
            reject_reason = "imported summary is a dry-run sample"
        elif imported.get("status") != "complete":
            reject_reason = f"imported summary status is {imported.get('status', 'missing')}"
        elif not imported_rows:
            reject_reason = "imported summary has no per-row timing fields"
        return (
            [(path, summary) for _, path, summary, _ in candidates],
            {
                "source": "merged_complete_timing_summaries",
                "imported_summary": rel(imported_path) if imported_path.exists() else "",
                "imported_summary_rejected_reason": reject_reason,
                "selected_summaries": [rel(path) for _, path, _, _ in candidates],
            },
        )
    return (
        [(imported_path, imported)],
        {
            "source": "dual_rerun_import",
            "imported_summary": rel(imported_path) if imported_path.exists() else "",
            "imported_summary_rejected_reason": "",
            "selected_summaries": [rel(imported_path)] if imported_path.exists() else [],
        },
    )


def merged_timing_rows(summaries: list[tuple[Path, dict[str, object]]]) -> list[dict[str, object]]:
    rows_by_key: dict[tuple[str, str, str], dict[str, object]] = {}
    for path, summary in summaries:
        for row in timing_rows(summary):
            row["summary_source"] = rel(path)
            key = (str(row.get("entry_id", "")), str(row.get("form", "")), str(row.get("variant", "")))
            rows_by_key[key] = row
    return [
        rows_by_key[key]
        for key in sorted(rows_by_key, key=lambda item: (item[0], item[1], item[2]))
    ]


def count_rows(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(key, "")) for row in rows).items()))


def scored_form_keys() -> set[tuple[str, str]]:
    score = read_json(SCORE_DENOMINATOR_JSON)
    rows = score.get("form_rows", [])
    if not isinstance(rows, list):
        return set()
    return {
        (str(row.get("release_entry_id", "")), str(row.get("form", "")))
        for row in rows
        if isinstance(row, dict) and row.get("counted_in_score") is True
    }


def score_coverage(rows: list[dict[str, object]]) -> dict[str, object]:
    scored = scored_form_keys()
    timed = {(str(row.get("entry_id", "")), str(row.get("form", ""))) for row in rows}
    timed_scored = timed & scored
    missing_scored = scored - timed
    timed_unscored = timed - scored
    scored_count = len(scored)
    return {
        "scored_form_count": scored_count,
        "timed_form_count": len(timed),
        "timed_scored_form_count": len(timed_scored),
        "missing_scored_form_count": len(missing_scored),
        "timed_unscored_form_count": len(timed_unscored),
        "score_denominator_coverage_fraction": (
            len(timed_scored) / scored_count if scored_count else None
        ),
        "full_score_denominator_timed": bool(scored_count) and len(timed_scored) == scored_count,
        "missing_scored_form_examples": [
            {"entry_id": entry_id, "form": form}
            for entry_id, form in sorted(missing_scored)[:10]
        ],
        "timed_unscored_form_examples": [
            {"entry_id": entry_id, "form": form}
            for entry_id, form in sorted(timed_unscored)[:10]
        ],
    }


def present(values: list[float | None]) -> list[float]:
    return [value for value in values if value is not None and math.isfinite(value)]


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * p))
    return ordered[index]


def median(values: list[float]) -> float | None:
    return percentile(values, 0.5)


def geomean(values: list[float]) -> float | None:
    positives = [value for value in values if value > 0]
    if not positives:
        return None
    return math.exp(sum(math.log(value) for value in positives) / len(positives))


def sum_field(rows: list[dict[str, object]], field: str) -> float | None:
    values = present([float_or_none(row.get(field)) for row in rows])
    return sum(values) if values else None


def ratio_stats(rows: list[dict[str, object]], field: str) -> dict[str, object]:
    values = present([float_or_none(row.get(field)) for row in rows])
    return {
        "count": len(values),
        "median": median(values),
        "geomean": geomean(values),
        "p10": percentile(values, 0.1),
        "p90": percentile(values, 0.9),
        "rows_evas_faster": sum(1 for value in values if value > 1.0),
        "rows_evas_slower": sum(1 for value in values if value < 1.0),
        "rows_equal": sum(1 for value in values if value == 1.0),
    }


def row_digest(row: dict[str, object]) -> dict[str, object]:
    return {
        "entry_id": row.get("entry_id"),
        "form": row.get("form"),
        "variant": row.get("variant"),
        "evas_wall_time_s": row.get("evas_wall_time_s"),
        "spectre_wall_time_s": row.get("spectre_wall_time_s"),
        "wrapper_spectre_over_evas_speedup": row.get("wrapper_spectre_over_evas_speedup"),
        "evas_reported_total_elapsed_s": row.get("evas_reported_total_elapsed_s"),
        "spectre_reported_total_elapsed_s": row.get("spectre_reported_total_elapsed_s"),
        "reported_total_spectre_over_evas_speedup": row.get(
            "reported_total_spectre_over_evas_speedup"
        ),
        "evas_accepted_tran_steps": row.get("evas_accepted_tran_steps"),
    }


def timing_distribution(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "wrapper_ratio": ratio_stats(rows, "wrapper_spectre_over_evas_speedup"),
        "reported_total_ratio": ratio_stats(rows, "reported_total_spectre_over_evas_speedup"),
        "tran_ratio": ratio_stats(rows, "tran_spectre_over_evas_speedup"),
        "top_evas_wall_rows": [
            row_digest(row)
            for row in sorted(rows, key=lambda row: float(row["evas_wall_time_s"]), reverse=True)[:8]
        ],
        "worst_wrapper_speedup_rows": [
            row_digest(row)
            for row in sorted(
                rows,
                key=lambda row: float_or_none(row.get("wrapper_spectre_over_evas_speedup")) or 0.0,
            )[:8]
        ],
    }


def measurement_plan(
    *,
    summary: dict[str, object],
    staging: dict[str, object],
    queue: dict[str, object],
    bridge: dict[str, object],
) -> dict[str, object]:
    bundles = [row for row in staging.get("bundles", []) if isinstance(row, dict)]
    queue_rows = [row for row in queue.get("rows", []) if isinstance(row, dict)]
    bridge_ready = bridge.get("status") == "ready" and bool(bridge.get("ready_profiles", []))
    staging_ready = (
        staging.get("status") == "complete"
        or (
            staging.get("status") == "ready"
            and int(staging.get("blocked_bundle_count", 0) or 0) == 0
            and int(staging.get("queue_rows_with_ready_primary_bundle", 0) or 0)
            == int(staging.get("queue_row_count", 0) or 0)
        )
    )
    if summary.get("status") == "complete":
        status = "measured_or_ready_to_import"
    elif bridge_ready and staging_ready:
        status = "ready_to_measure"
    elif staging_ready:
        status = "blocked_by_bridge"
    else:
        status = "blocked_by_staging"
    summary_complete = summary.get("status") == "complete"
    return {
        "status": status,
        "bridge_ready": bridge_ready,
        "bridge_status": bridge.get("status", "missing"),
        "bridge_ready_profiles": bridge.get("ready_profiles", []),
        "summary_status": summary.get("status", "missing"),
        "primary_queue_rows": queue.get("queue_count", 0),
        "ready_primary_queue_rows": queue.get("ready_count", 0),
        "staged_bundle_count": staging.get("bundle_count", 0),
        "ready_staged_bundle_count": staging.get("ready_bundle_count", 0),
        "blocked_staged_bundle_count": staging.get("blocked_bundle_count", 0),
        "bundle_variant_counts": count_rows(bundles, "variant"),
        "bundle_expected_result_counts": count_rows(bundles, "expected_result"),
        "bundle_form_counts": count_rows(bundles, "form"),
        "primary_form_counts": count_rows(queue_rows, "form"),
        "primary_category_counts": count_rows(queue_rows, "category"),
        "commands": [
            "python3 runners/finish_vabench_release_after_bridge.py",
            "./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180",
            "python3 runners/report_vabench_release_speed_debug.py",
        ],
        "required_timing_fields": [
            "raw_result.timing.evas_wall_time_s",
            "raw_result.timing.spectre_wall_time_s",
            "raw_result.timing.combined_wall_time_s",
        ],
        "claim_blockers": [
            *(["bridge profile is not ready"] if not summary_complete and not bridge_ready else []),
            *(["fresh dual rerun summary is not complete"] if not summary_complete else []),
            *(["rerun staging is not ready"] if not summary_complete and not staging_ready else []),
        ],
    }


def build_report() -> dict[str, object]:
    import_report = read_json(IMPORT_JSON)
    summaries, summary_selection = discover_summaries(import_report)
    summary_path, summary = summaries[-1]
    staging = read_json(STAGING_MANIFEST_JSON)
    queue = read_json(QUEUE_JSON)
    bridge = read_json(BRIDGE_JSON)
    queue_count = int(queue.get("queue_count", 0) or 0)
    selected_complete = all(item.get("status") == "complete" for _, item in summaries)
    rows = merged_timing_rows(summaries) if selected_complete else timing_rows(summary)
    summary_task_count = len(rows) if selected_complete and rows else int(summary.get("tasks_total", 0) or 0)
    stale_summary = (
        len(summaries) == 1
        and summary.get("status") == "complete"
        and queue_count > 0
        and summary_task_count != queue_count
    )
    effective_summary = {
        **dict(summary),
        "status": "complete" if selected_complete and rows else summary.get("status", "missing"),
        "tasks_total": summary_task_count,
    }
    if stale_summary:
        effective_summary["status"] = "stale"
        rows = []
    coverage = score_coverage(rows)
    plan = measurement_plan(summary=effective_summary, staging=staging, queue=queue, bridge=bridge)
    complete = effective_summary.get("status") == "complete"
    all_pass = bool(rows) and all(row["raw_status"] == "PASS" for row in rows)
    if complete and rows:
        evas_total = sum(row["evas_wall_time_s"] for row in rows)
        spectre_total = sum(row["spectre_wall_time_s"] for row in rows)
        speedup = spectre_total / evas_total if evas_total > 0 else None
        full_denominator_timed = bool(coverage["full_score_denominator_timed"])
        status = (
            "measured_with_failures"
            if not all_pass
            else "measured"
            if full_denominator_timed
            else "measured_subset"
        )
        if not all_pass:
            reason = "Timing exists, but at least one rerun row did not PASS."
        elif not full_denominator_timed:
            reason = (
                "Timing exists for a subset only: "
                f"{len(rows)} timed rows cover "
                f"{coverage['timed_scored_form_count']}/{coverage['scored_form_count']} scored forms. "
                f"Wrapper aggregate Spectre/EVAS speedup is {speedup:.3f}; "
                "do not claim release-wide EVAS speedup yet."
            )
        elif speedup is not None and speedup <= 1.0:
            reason = "Timing exists, but this slice does not show an EVAS speedup over Spectre."
        else:
            reason = ""
    else:
        evas_total = None
        spectre_total = None
        speedup = None
        status = "pending_measurement"
        if stale_summary:
            reason = (
                "Stale dual rerun timing summary rejected: "
                f"summary tasks_total={summary_task_count}, current queue_count={queue_count}."
            )
        else:
            reason = (
                "No same-slice release timing artifact is available yet; "
                f"dual rerun summary status is {summary.get('status', 'missing')}."
            )
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "claim_allowed": status == "measured" and speedup is not None and speedup > 1.0,
        "reason": reason,
        "measurement_scope": {
            "summary": rel(summary_path) if summary_path.exists() and summary_path.is_relative_to(ROOT) else "",
            "summaries": [rel(path) for path, _ in summaries if path.exists()],
            "summary_selection": summary_selection,
            "staging_manifest": rel(STAGING_MANIFEST_JSON) if STAGING_MANIFEST_JSON.exists() else "",
            "queue_manifest": rel(QUEUE_JSON) if QUEUE_JSON.exists() else "",
            "planned_primary_rerun_rows": (
                summary_task_count
                if complete
                else queue_count
            ),
            "planned_staged_bundles": staging.get("ready_bundle_count", 0),
            "timed_rows": len(rows),
            "stale_summary_rejected": stale_summary,
            **coverage,
        },
        "measurement_plan": plan,
        "timing_totals": {
            "evas_wall_time_s": evas_total,
            "spectre_wall_time_s": spectre_total,
            "spectre_over_evas_speedup": speedup,
            "evas_reported_total_elapsed_s": sum_field(rows, "evas_reported_total_elapsed_s"),
            "spectre_reported_total_elapsed_s": sum_field(rows, "spectre_reported_total_elapsed_s"),
            "reported_total_spectre_over_evas_speedup": ratio_or_none(
                sum_field(rows, "spectre_reported_total_elapsed_s"),
                sum_field(rows, "evas_reported_total_elapsed_s"),
            ),
            "evas_reported_tran_elapsed_s": sum_field(rows, "evas_reported_tran_elapsed_s"),
            "spectre_reported_tran_elapsed_s": sum_field(rows, "spectre_reported_tran_elapsed_s"),
            "tran_spectre_over_evas_speedup": ratio_or_none(
                sum_field(rows, "spectre_reported_tran_elapsed_s"),
                sum_field(rows, "evas_reported_tran_elapsed_s"),
            ),
        },
        "timing_distribution": timing_distribution(rows),
        "required_to_claim": [
            "Run same-slice EVAS/Spectre timing for every scored release form, or state a narrower subset-only claim.",
            "Stratify or fix EVAS slow outliers before claiming aggregate speedup on the release package.",
            "Keep per-row EVAS and Spectre wall-clock timings from run_gold_dual_suite timing fields.",
            "Keep Spectre-reported runtime from spectre.out alongside wrapper wall-clock timings.",
            "Report machine/bridge/Cadence configuration with the timing artifact.",
            "Do not compute speedup from historical main120 summaries because they lack same-slice runtime metadata.",
        ],
        "debug_triage_order": [
            "bridge_profile_diagnostics.json for SSH/tunnel readiness",
            "external_blockers.json for claim-boundary blocker chain",
            "dual_rerun_staging_manifest.json for per-bundle staging blockers",
            "imported dual rerun summary for per-row simulator/checker failures",
            "dual_rerun_import.json for stale or incomplete import blockers",
        ],
        "rows": rows,
    }


def write_markdown(report: dict[str, object]) -> None:
    totals = report["timing_totals"]
    scope = report["measurement_scope"]
    plan = report["measurement_plan"]
    distribution = report["timing_distribution"]
    wrapper_ratio = distribution["wrapper_ratio"]
    reported_ratio = distribution["reported_total_ratio"]
    lines = [
        "# vaBench Release Speed / Debug Artifact",
        "",
        f"Date: {report['date']}",
        "",
        "This artifact gates any EVAS speed/debug claim. It requires same-slice",
        "EVAS and Spectre timing collected by the release dual rerun runner.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| claim allowed | `{report['claim_allowed']}` |",
        f"| planned primary rerun rows | {scope['planned_primary_rerun_rows']} |",
        f"| planned staged bundles | {scope['planned_staged_bundles']} |",
        f"| timed rows | {scope['timed_rows']} |",
        f"| timed scored forms | {scope['timed_scored_form_count']} / {scope['scored_form_count']} |",
        f"| full score denominator timed | `{scope['full_score_denominator_timed']}` |",
        f"| measurement plan | `{plan['status']}` |",
        f"| EVAS wall time | {totals['evas_wall_time_s']} |",
        f"| Spectre wall time | {totals['spectre_wall_time_s']} |",
        f"| Spectre/EVAS speedup | {totals['spectre_over_evas_speedup']} |",
        f"| median per-row wrapper speedup | {wrapper_ratio['median']} |",
        f"| geomean per-row wrapper speedup | {wrapper_ratio['geomean']} |",
        f"| EVAS reported total time | {totals['evas_reported_total_elapsed_s']} |",
        f"| Spectre reported total time | {totals['spectre_reported_total_elapsed_s']} |",
        f"| reported-total Spectre/EVAS speedup | {totals['reported_total_spectre_over_evas_speedup']} |",
        f"| median per-row reported-total speedup | {reported_ratio['median']} |",
    ]
    if report["reason"]:
        lines.extend(["", f"Reason: {report['reason']}"])
    lines.extend(
        [
            "",
            "## Measurement Scope",
            "",
            f"- Selected summary: `{scope['summary']}`",
            f"- Summary selection: `{json.dumps(scope['summary_selection'], sort_keys=True)}`",
            f"- Missing scored-form examples: `{json.dumps(scope['missing_scored_form_examples'], sort_keys=True)}`",
            f"- Timed unscored-form examples: `{json.dumps(scope['timed_unscored_form_examples'], sort_keys=True)}`",
            "",
            "## Slowest EVAS Wrapper Rows",
            "",
            "| entry | form | variant | EVAS s | Spectre s | speedup | steps |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in distribution["top_evas_wall_rows"]:
        lines.append(
            "| {entry} | {form} | {variant} | {evas} | {spectre} | {speedup} | {steps} |".format(
                entry=row.get("entry_id"),
                form=row.get("form"),
                variant=row.get("variant"),
                evas=row.get("evas_wall_time_s"),
                spectre=row.get("spectre_wall_time_s"),
                speedup=row.get("wrapper_spectre_over_evas_speedup"),
                steps=row.get("evas_accepted_tran_steps"),
            )
        )
    lines.extend(
        [
            "",
            "## Measurement Plan",
            "",
            f"- Bridge ready: `{plan['bridge_ready']}`",
            f"- Bundle variants: `{json.dumps(plan['bundle_variant_counts'], sort_keys=True)}`",
            f"- Bundle expected results: `{json.dumps(plan['bundle_expected_result_counts'], sort_keys=True)}`",
            f"- Claim blockers: `{json.dumps(plan['claim_blockers'])}`",
            "",
            "## Debug Triage Order",
            "",
        ]
    )
    for item in report["debug_triage_order"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Required To Claim", ""])
    for item in report["required_to_claim"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote speed/debug artifact: status={status}; timed_rows={rows}".format(
            status=report["status"],
            rows=report["measurement_scope"]["timed_rows"],
        )
    )


if __name__ == "__main__":
    main()
