#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def status_of(result: dict[str, Any]) -> str:
    raw = result.get("raw_result")
    if isinstance(raw, dict):
        return str(raw.get("status", "UNKNOWN"))
    return "UNKNOWN"


def topic_of(result: dict[str, Any]) -> str:
    meta = result.get("vabench_300")
    if isinstance(meta, dict):
        topic = str(meta.get("topic_id") or "").strip()
        if topic:
            return topic
    return str(result.get("entry_id") or result.get("staged_task_dir") or "unknown")


def form_of(result: dict[str, Any]) -> str:
    return str(result.get("form") or "unknown")


def parity_of(result: dict[str, Any]) -> dict[str, Any]:
    raw = result.get("raw_result")
    if isinstance(raw, dict):
        parity = raw.get("parity")
        if isinstance(parity, dict):
            return parity
    return {}


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def worst_signal(result: dict[str, Any]) -> dict[str, Any]:
    per_signal = parity_of(result).get("per_signal")
    if not isinstance(per_signal, dict):
        return {}
    best: dict[str, Any] = {}
    best_score = -1.0
    for signal, metrics in per_signal.items():
        if not isinstance(metrics, dict):
            continue
        score = finite_float(metrics.get("nrmse"))
        if score is None:
            score = finite_float(metrics.get("max_abs_v"))
        if score is None:
            continue
        if score > best_score:
            best_score = score
            best = {"signal": signal, **metrics}
    return best


def metric_label(metrics: dict[str, Any]) -> str:
    if not metrics:
        return "n/a"
    kind = str(metrics.get("kind") or "")
    if kind == "digital":
        stable = finite_float(metrics.get("stable_mismatch_ratio"))
        raw = finite_float(metrics.get("raw_mismatch_ratio"))
        if stable is not None and raw is not None:
            return f"stable_mismatch={stable:.4g}, raw_mismatch={raw:.4g}"
        mismatch = finite_float(metrics.get("mismatch_ratio"))
        if mismatch is not None:
            return f"mismatch={mismatch:.4g}"
    max_abs = finite_float(metrics.get("max_abs_v"))
    nrmse = finite_float(metrics.get("nrmse"))
    if max_abs is not None and nrmse is not None:
        return f"max_abs={max_abs:.4g} V, rel_rms={nrmse:.4g}"
    if nrmse is not None:
        return f"rel_rms={nrmse:.4g}"
    return "n/a"


TIMING_KEY_RE = re.compile(r"(?:^|_)(?:time|edge|cross|period|lag)(?:_|$)|(?:^|_)delta_s$")


def collect_timing_ps(value: Any, prefix: str = "") -> list[tuple[str, float]]:
    found: list[tuple[str, float]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            child_prefix = f"{prefix}.{key_text}" if prefix else key_text
            number = finite_float(item)
            if number is not None and TIMING_KEY_RE.search(key_text):
                # The parity helpers use seconds for *_s fields; ignore obvious
                # dimensionless ratios and huge values.
                if abs(number) <= 1e-3:
                    found.append((child_prefix, number * 1e12))
            elif isinstance(item, (dict, list)):
                found.extend(collect_timing_ps(item, child_prefix))
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            if isinstance(item, (dict, list)):
                found.extend(collect_timing_ps(item, f"{prefix}[{idx}]"))
    return found


def largest_timing_label(result: dict[str, Any]) -> str:
    candidates = collect_timing_ps(parity_of(result))
    if not candidates:
        return ""
    key, value_ps = max(candidates, key=lambda item: abs(item[1]))
    return f"{key}={value_ps:.3g} ps"


def compact_result(result: dict[str, Any]) -> dict[str, Any]:
    worst = worst_signal(result)
    parity = parity_of(result)
    return {
        "status": status_of(result),
        "topic_id": topic_of(result),
        "entry_id": result.get("entry_id"),
        "form": form_of(result),
        "task_id": (result.get("raw_result") or {}).get("task_id")
        if isinstance(result.get("raw_result"), dict)
        else None,
        "staged_task_dir": result.get("staged_task_dir"),
        "worst_signal": worst.get("signal"),
        "worst_metric": metric_label(worst),
        "timing_hint": largest_timing_label(result),
        "parity_status": parity.get("status"),
        "parity_policy": parity.get("policy"),
        "parity_reason": parity.get("reason"),
    }


def build_report(summary: dict[str, Any]) -> dict[str, Any]:
    results = [item for item in summary.get("results", []) if isinstance(item, dict)]
    status_counts = Counter(status_of(result) for result in results)
    parity_failures = [result for result in results if status_of(result) == "FAIL_PARITY"]
    timing_rows: list[dict[str, Any]] = []
    evas_walls: list[float] = []
    spectre_walls: list[float] = []
    row_speedups: list[float] = []
    for result in results:
        raw = result.get("raw_result")
        timing = raw.get("timing") if isinstance(raw, dict) else None
        if not isinstance(timing, dict):
            continue
        evas_wall = finite_float(timing.get("evas_wall_time_s"))
        spectre_wall = finite_float(timing.get("spectre_wall_time_s"))
        if evas_wall is None or spectre_wall is None or evas_wall <= 0:
            continue
        speedup = spectre_wall / evas_wall
        evas_walls.append(evas_wall)
        spectre_walls.append(spectre_wall)
        row_speedups.append(speedup)
        timing_rows.append(
            {
                "topic_id": topic_of(result),
                "entry_id": result.get("entry_id"),
                "form": form_of(result),
                "status": status_of(result),
                "evas_wall_time_s": evas_wall,
                "spectre_wall_time_s": spectre_wall,
                "row_speedup_spectre_over_evas": speedup,
            }
        )
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in parity_failures:
        grouped[topic_of(result)].append(compact_result(result))

    groups = []
    for topic, rows in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        groups.append(
            {
                "topic_id": topic,
                "count": len(rows),
                "forms": dict(sorted(Counter(row["form"] for row in rows).items())),
                "worst_examples": rows[:5],
            }
        )

    timing_summary: dict[str, Any] = {
        "timed_rows": len(timing_rows),
        "sum_evas_wall_time_s": sum(evas_walls),
        "sum_spectre_wall_time_s": sum(spectre_walls),
        "aggregate_speedup_spectre_over_evas": (sum(spectre_walls) / sum(evas_walls)) if evas_walls else None,
        "median_row_speedup_spectre_over_evas": None,
        "min_row_speedup_spectre_over_evas": min(row_speedups) if row_speedups else None,
        "max_row_speedup_spectre_over_evas": max(row_speedups) if row_speedups else None,
        "slowest_evas_rows": sorted(timing_rows, key=lambda item: item["evas_wall_time_s"], reverse=True)[:20],
    }
    if row_speedups:
        ordered = sorted(row_speedups)
        mid = len(ordered) // 2
        if len(ordered) % 2:
            timing_summary["median_row_speedup_spectre_over_evas"] = ordered[mid]
        else:
            timing_summary["median_row_speedup_spectre_over_evas"] = 0.5 * (ordered[mid - 1] + ordered[mid])

    return {
        "source_status": summary.get("status"),
        "tasks_total": summary.get("tasks_total", len(results)),
        "results_total": len(results),
        "status_counts": dict(sorted(status_counts.items())),
        "raw_status_counts": summary.get("raw_status_counts") or dict(sorted(status_counts.items())),
        "selection": summary.get("selection", {}),
        "selected_expansion_status_counts": summary.get("selected_expansion_status_counts", {}),
        "selected_form_counts": summary.get("selected_form_counts", {}),
        "fail_parity_group_count": len(groups),
        "fail_parity_count": len(parity_failures),
        "fail_parity_groups": groups,
        "timing_summary": timing_summary,
        "nonpass_examples": [
            compact_result(result)
            for result in results
            if status_of(result) != "PASS"
        ][:50],
    }


def render_markdown(report: dict[str, Any], *, source: Path) -> str:
    lines: list[str] = []
    lines.append("# vaBench 300 Dual Summary")
    lines.append("")
    lines.append(f"- source: `{source}`")
    lines.append(f"- source status: `{report.get('source_status')}`")
    lines.append(f"- tasks total: `{report.get('tasks_total')}`")
    lines.append(f"- results total: `{report.get('results_total')}`")
    lines.append("")
    lines.append("## Status Counts")
    for status, count in report.get("raw_status_counts", {}).items():
        lines.append(f"- `{status}`: {count}")
    lines.append("")
    lines.append("## Selection")
    lines.append(f"- expansion status: `{report.get('selected_expansion_status_counts')}`")
    lines.append(f"- forms: `{report.get('selected_form_counts')}`")
    lines.append(f"- filters: `{report.get('selection')}`")
    lines.append("")
    lines.append("## FAIL_PARITY Groups")
    lines.append(f"- groups: `{report.get('fail_parity_group_count')}`")
    lines.append(f"- rows: `{report.get('fail_parity_count')}`")
    for group in report.get("fail_parity_groups", []):
        lines.append("")
        lines.append(f"### `{group['topic_id']}`")
        lines.append(f"- count: {group['count']}")
        lines.append(f"- forms: `{group['forms']}`")
        for row in group.get("worst_examples", []):
            timing = f", {row['timing_hint']}" if row.get("timing_hint") else ""
            lines.append(
                "- "
                f"`{row['form']}` `{row.get('task_id') or row.get('entry_id')}`: "
                f"{row.get('worst_signal') or 'n/a'} {row.get('worst_metric')}{timing}"
            )
    lines.append("")
    lines.append("## Timing")
    timing = report.get("timing_summary", {})
    lines.append(f"- timed rows: `{timing.get('timed_rows')}`")
    lines.append(f"- sum EVAS wall: `{timing.get('sum_evas_wall_time_s'):.6g} s`")
    lines.append(f"- sum Spectre wall: `{timing.get('sum_spectre_wall_time_s'):.6g} s`")
    speedup = timing.get("aggregate_speedup_spectre_over_evas")
    median_speedup = timing.get("median_row_speedup_spectre_over_evas")
    lines.append(f"- aggregate speedup Spectre/EVAS: `{speedup:.6g}x`" if speedup else "- aggregate speedup Spectre/EVAS: `n/a`")
    lines.append(
        f"- median row speedup Spectre/EVAS: `{median_speedup:.6g}x`"
        if median_speedup
        else "- median row speedup Spectre/EVAS: `n/a`"
    )
    lines.append("")
    lines.append("### Slowest EVAS Rows")
    for row in timing.get("slowest_evas_rows", [])[:10]:
        lines.append(
            "- "
            f"`{row['topic_id']}` `{row['form']}` `{row['status']}`: "
            f"EVAS {row['evas_wall_time_s']:.4g}s, "
            f"Spectre {row['spectre_wall_time_s']:.4g}s, "
            f"speedup {row['row_speedup_spectre_over_evas']:.4g}x"
        )
    lines.append("")
    lines.append("## Non-PASS Examples")
    for row in report.get("nonpass_examples", [])[:20]:
        lines.append(
            "- "
            f"`{row['status']}` `{row['topic_id']}` `{row['form']}` "
            f"{row.get('worst_signal') or row.get('parity_reason') or ''} "
            f"{row.get('worst_metric') or ''}"
        )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Summarize a vaBench 300 dual rerun summary.json.")
    ap.add_argument("summary", help="Path to summary.json.")
    ap.add_argument("--output-json", help="Optional compact JSON report path.")
    ap.add_argument("--output-md", help="Optional Markdown report path.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.summary)
    summary = read_json(source)
    report = build_report(summary)
    if args.output_json:
        Path(args.output_json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown = render_markdown(report, source=source)
    if args.output_md:
        Path(args.output_md).write_text(markdown, encoding="utf-8")
    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
