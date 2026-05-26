#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_gold_dual_suite import compare_waveforms

try:
    from run_gold_dual_suite import WAVEFORM_EQUIVALENCE_POLICY
except ImportError:
    WAVEFORM_EQUIVALENCE_POLICY = {
        "policy": "spectre_equivalence_core_v1",
        "basis": (
            "Behavior checks are primary; waveform metrics are an acceptance gate "
            "for Spectre-equivalent behavioral output, not a claim of higher-than-Spectre precision."
        ),
        "reporting_terms": (
            "Report simulator-style checks: behavior/spec pass, event consistency, "
            "relative RMS waveform error, absolute voltage error, and digital mismatch."
        ),
        "small_absolute_gate": "max_rmse_v<=0.05 and max_abs_v<=0.30",
        "relative_rms_gate": (
            "row_mean_relative_rms_error<=0.10 and worst_signal_relative_rms_error<=0.22; "
            "or row_mean_relative_rms_error<=0.08 and worst_signal_relative_rms_error<=0.25"
        ),
    }


DEFAULT_OUT_JSON = Path(
    "speed-optimization/reports/spectre_ax_classic_self_consistency_clean_repeats_20260522.json"
)
DEFAULT_OUT_MD = Path(
    "speed-optimization/reports/spectre_ax_classic_self_consistency_clean_repeats_20260522.md"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


def grouped_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row.get("entry_id")),
        str(row.get("form")),
        str(row.get("variant") or "gold"),
        str(row.get("task_id")),
    )


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * pct / 100.0
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    weight = pos - lo
    return ordered[lo] * (1.0 - weight) + ordered[hi] * weight


def metric_stats(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    values = [
        float(row[key])
        for row in rows
        if isinstance(row.get(key), (int, float)) and math.isfinite(float(row[key]))
    ]
    return {
        "count": len(values),
        "min": min(values) if values else None,
        "p25": percentile(values, 25),
        "median": percentile(values, 50),
        "p75": percentile(values, 75),
        "max": max(values) if values else None,
    }


def simulator_style_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    compared = [row for row in rows if row.get("status") in {"passed", "needs_review"}]
    metrics = {
        key: metric_stats(compared, key)
        for key in (
            "mean_nrmse",
            "max_nrmse",
            "max_rmse_v",
            "max_abs_v",
            "signals_compared",
            "common_window_duration_s",
        )
    }
    # Public reports use simulator-style terms:
    # - relative RMS error is scale-normalized, analogous to a reltol-style check.
    # - absolute voltage error keeps near-zero or low-swing signals from being dominated by ratios.
    # - digital-like signals are represented by mismatch ratio inside the
    #   worst-signal relative RMS aggregate.
    return {
        "behavior": {
            "definition": "both Spectre modes pass the task behavior checker",
            "pass_pairs": sum(1 for row in rows if row.get("behavior_pair_status") == "pass"),
            "fail_pairs": sum(1 for row in rows if row.get("behavior_pair_status") == "fail"),
            "blocked_pairs": sum(1 for row in rows if row.get("behavior_pair_status") == "blocked"),
        },
        "waveform": {
            "definition": "same-row Spectre mode waveform comparison on common saved signals",
            "compared_pairs": len(compared),
            "pass_pairs": sum(1 for row in compared if row.get("status") == "passed"),
            "needs_review_pairs": sum(1 for row in compared if row.get("status") == "needs_review"),
        },
        "relative_rms_error": {
            "definition": "RMS(mode_a - mode_b) divided by signal span",
            "row_mean_max": metrics["mean_nrmse"]["max"],
            "worst_signal_max": metrics["max_nrmse"]["max"],
            "worst_signal_median": metrics["max_nrmse"]["median"],
        },
        "absolute_voltage_error": {
            "definition": "voltage-domain absolute error on common sampled points",
            "max_rms_v": metrics["max_rmse_v"]["max"],
            "max_point_v": metrics["max_abs_v"]["max"],
            "median_rms_v": metrics["max_rmse_v"]["median"],
        },
        "timing_window": {
            "definition": "common transient window used for waveform comparison",
            "max_duration_s": metrics["common_window_duration_s"]["max"],
            "median_duration_s": metrics["common_window_duration_s"]["median"],
        },
    }


def behavior_pair_status(left: dict[str, Any], right: dict[str, Any]) -> str:
    if left.get("behavior_check_available") is not True or right.get("behavior_check_available") is not True:
        return "blocked"
    if left.get("behavior_ok") is True and right.get("behavior_ok") is True:
        return "pass"
    return "fail"


def compact_comparison(comparison: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "status": comparison.get("status"),
        "reason": comparison.get("reason"),
    }
    for key in (
        "signals_compared",
        "samples",
        "max_rmse_v",
        "max_abs_v",
        "mean_relative_rms_error",
        "max_relative_rms_error",
        "mean_nrmse",
        "max_nrmse",
    ):
        if key in comparison:
            out[key] = comparison[key]
    window = comparison.get("common_window_s")
    if isinstance(window, list) and len(window) == 2:
        out["common_window_s"] = window
        try:
            out["common_window_duration_s"] = float(window[1]) - float(window[0])
        except (TypeError, ValueError):
            pass
    per_signal = comparison.get("per_signal")
    if isinstance(per_signal, dict) and per_signal:
        candidates = [
            (name, metrics)
            for name, metrics in per_signal.items()
            if isinstance(metrics, dict) and isinstance(metrics.get("nrmse"), (int, float))
        ]
        if candidates:
            name, metrics = max(candidates, key=lambda item: float(item[1].get("nrmse", 0.0)))
            out["worst_signal_by_relative_rms"] = {
                "signal": name,
                "kind": metrics.get("kind"),
                "relative_rms_error": metrics.get("nrmse"),
                "rmse_v": metrics.get("rmse_v"),
                "max_abs_v": metrics.get("max_abs_v"),
                "mismatch_ratio": metrics.get("mismatch_ratio"),
            }
    return out


def compare_report(
    *,
    report_path: Path,
    root: Path,
    mode_a: str,
    mode_b: str,
    sample_n: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    report = load_json(report_path)
    label = report_path.stem
    by_case: dict[tuple[str, str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in report.get("results", []):
        if not isinstance(row, dict):
            continue
        if row.get("backend") != "spectre":
            continue
        mode = str(row.get("mode"))
        if mode in {mode_a, mode_b}:
            by_case[grouped_key(row)][mode] = row

    rows: list[dict[str, Any]] = []
    for key, cells in sorted(by_case.items()):
        entry_id, form, variant, task_id = key
        left = cells.get(mode_a)
        right = cells.get(mode_b)
        base: dict[str, Any] = {
            "report": label,
            "entry_id": entry_id,
            "form": form,
            "variant": variant,
            "task_id": task_id,
            "mode_a": mode_a,
            "mode_b": mode_b,
        }
        if left is None or right is None:
            rows.append({**base, "status": "blocked", "reason": "missing Spectre mode result"})
            continue
        base.update(
            {
                "mode_a_status": left.get("status"),
                "mode_b_status": right.get("status"),
                "mode_a_behavior_ok": left.get("behavior_ok"),
                "mode_b_behavior_ok": right.get("behavior_ok"),
                "behavior_pair_status": behavior_pair_status(left, right),
                "mode_a_csv_path": left.get("csv_path"),
                "mode_b_csv_path": right.get("csv_path"),
            }
        )
        if left.get("simulation_ok") is not True or right.get("simulation_ok") is not True:
            rows.append({**base, "status": "blocked", "reason": "simulation_not_ok"})
            continue
        left_csv = resolve_path(root, left.get("csv_path"))
        right_csv = resolve_path(root, right.get("csv_path"))
        if left_csv is None or right_csv is None:
            rows.append({**base, "status": "blocked", "reason": "missing csv path"})
            continue
        if not left_csv.exists() or not right_csv.exists():
            rows.append(
                {
                    **base,
                    "status": "blocked",
                    "reason": "csv file not found",
                    "mode_a_csv_exists": left_csv.exists(),
                    "mode_b_csv_exists": right_csv.exists(),
                }
            )
            continue
        try:
            comparison = compare_waveforms(task_id, left_csv, right_csv, sample_n=sample_n)
        except Exception as exc:  # noqa: BLE001 - keep artifact data-bearing.
            rows.append({**base, "status": "blocked", "reason": f"{type(exc).__name__}: {exc}"})
            continue
        rows.append({**base, **compact_comparison(comparison)})

    source = {
        "label": label,
        "path": str(report_path),
        "created_at": report.get("created_at"),
        "selected_rows": report.get("selected_rows"),
        "jobs": report.get("jobs"),
        "spectre_modes": report.get("spectre_modes"),
        "case_pairs_seen": len(by_case),
    }
    return source, rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    compared = [row for row in rows if row.get("status") in {"passed", "needs_review"}]
    passed = [row for row in compared if row.get("status") == "passed"]
    needs_review = [row for row in compared if row.get("status") == "needs_review"]
    blocked = [row for row in rows if row.get("status") == "blocked"]
    behavior_pass = [row for row in rows if row.get("behavior_pair_status") == "pass"]
    behavior_blocked = [row for row in rows if row.get("behavior_pair_status") == "blocked"]
    behavior_fail = [row for row in rows if row.get("behavior_pair_status") == "fail"]
    return {
        "total_pairs": len(rows),
        "compared_pairs": len(compared),
        "passed_pairs": len(passed),
        "needs_review_pairs": len(needs_review),
        "blocked_pairs": len(blocked),
        "behavior_pass_pairs": len(behavior_pass),
        "behavior_blocked_pairs": len(behavior_blocked),
        "behavior_fail_pairs": len(behavior_fail),
        "pass_fraction_compared": len(passed) / len(compared) if compared else None,
        "artifact_claim_allowed": bool(compared) and not needs_review and not blocked,
        "simulator_style_summary": simulator_style_summary(rows),
        "metrics": {
            key: metric_stats(compared, key)
            for key in (
                "max_nrmse",
                "mean_nrmse",
                "max_rmse_v",
                "max_abs_v",
                "signals_compared",
                "common_window_duration_s",
            )
        },
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve()
    reports: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []
    for report_path in args.reports:
        source, rows = compare_report(
            report_path=report_path,
            root=root,
            mode_a=args.mode_a,
            mode_b=args.mode_b,
            sample_n=args.sample_n,
        )
        reports.append(source)
        all_rows.extend(rows)

    ranked = sorted(
        all_rows,
        key=lambda row: (
            row.get("status") != "needs_review",
            -(float(row.get("max_nrmse") or 0.0)),
            -(float(row.get("mean_nrmse") or 0.0)),
        ),
    )
    return {
        "schema_version": "spectre-self-consistency.v1",
        "artifact_kind": "spectre_mode_waveform_self_consistency",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "mode_a": args.mode_a,
        "mode_b": args.mode_b,
        "sample_n": args.sample_n,
        "source_reports": reports,
        "policy": {
            "purpose": (
                "Measure official Spectre mode self-consistency on the same row slice, "
                "so EVAS waveform tolerance is anchored to Spectre AX/classic variation."
            ),
            "mode_a_role": "fast official Spectre speed baseline",
            "mode_b_role": "conservative non-X Spectre reference path",
            "waveform_equivalence_policy": WAVEFORM_EQUIVALENCE_POLICY,
        },
        "summary": summarize(all_rows),
        "outliers": ranked[: args.outlier_limit],
        "rows": all_rows,
    }


def fmt(value: object, digits: int = 4) -> str:
    if value is None:
        return "-"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.{digits}g}"
    return str(value)


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    metrics = summary["metrics"]
    sim = summary["simulator_style_summary"]
    lines: list[str] = []
    lines.append("# Spectre AX/Classic 自一致性报告")
    lines.append("")
    lines.append(f"生成时间: {payload['generated_at']}")
    lines.append("")
    lines.append("## 策略")
    lines.append("")
    lines.append(
        "`spectre/ax` 作为官方快速 Spectre 速度基线；`spectre/classic` 作为更保守的 "
        "non-X reference path。本报告在同一批 rows 上直接比较两种 Spectre 模式的波形，"
        "并只把当前 waveform equivalence policy 作为接受性判定视角使用。"
    )
    policy = payload["policy"]["waveform_equivalence_policy"]
    if isinstance(policy, dict):
        lines.append("")
        lines.append(
            f"实现注释：relative gate `{policy.get('relative_rms_gate')}`；"
            f"absolute gate `{policy.get('small_absolute_gate')}`。这些是 "
            "Spectre 等价性接受阈值，不是更高精度声明。"
        )
    lines.append("")
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("| --- | ---: |")
    for key in (
        "total_pairs",
        "compared_pairs",
        "passed_pairs",
        "needs_review_pairs",
        "blocked_pairs",
        "behavior_pass_pairs",
        "behavior_blocked_pairs",
        "behavior_fail_pairs",
    ):
        lines.append(f"| {key} | {fmt(summary.get(key))} |")
    lines.append(f"| pass_fraction_compared | {fmt(summary.get('pass_fraction_compared'))} |")
    lines.append(f"| artifact_claim_allowed | `{summary.get('artifact_claim_allowed')}` |")
    lines.append("")
    lines.append("## 仿真器式接受性检查")
    lines.append("")
    lines.append("| 检查项 | 定义 | 观测值 |")
    lines.append("| --- | --- | ---: |")
    behavior = sim["behavior"]
    waveform = sim["waveform"]
    rel = sim["relative_rms_error"]
    abs_v = sim["absolute_voltage_error"]
    timing = sim["timing_window"]
    lines.append(
        f"| behavior/spec | 两种 Spectre 模式均通过任务行为 checker | "
        f"{behavior['pass_pairs']} pass / {summary.get('total_pairs')} pairs |"
    )
    lines.append(
        f"| waveform equivalence | 同一 row、共同保存信号上的 Spectre mode 波形比较 | "
        f"{waveform['pass_pairs']} pass / {waveform['compared_pairs']} compared |"
    )
    lines.append(
        f"| relative RMS error | RMS(mode_a - mode_b) 除以信号摆幅 | "
        f"worst signal max {fmt(rel['worst_signal_max'])}; row-mean max {fmt(rel['row_mean_max'])} |"
    )
    lines.append(
        f"| absolute voltage error | 共同采样点上的电压域绝对误差 | "
        f"max RMS {fmt(abs_v['max_rms_v'])} V; max point {fmt(abs_v['max_point_v'])} V |"
    )
    lines.append(
        f"| comparison window | 波形比较使用的共同 transient 时间窗口 | "
        f"median {fmt(timing['median_duration_s'])} s; max {fmt(timing['max_duration_s'])} s |"
    )
    lines.append("")
    lines.append("## 原始指标分布")
    lines.append("")
    lines.append("| 指标 | N | 中位数 | 最大值 |")
    lines.append("| --- | ---: | ---: | ---: |")
    display_metrics = {
        "row mean relative RMS error": "mean_nrmse",
        "worst-signal relative RMS error": "max_nrmse",
        "worst RMS voltage error": "max_rmse_v",
        "worst point voltage error": "max_abs_v",
        "比较信号数": "signals_compared",
        "比较窗口时长 s": "common_window_duration_s",
    }
    for label, key in display_metrics.items():
        row = metrics[key]
        lines.append(f"| {label} | {fmt(row.get('count'))} | {fmt(row.get('median'))} | {fmt(row.get('max'))} |")
    lines.append("")
    lines.append("## 来源报告")
    lines.append("")
    lines.append("| 报告 | 行数 | 并发任务 | 创建时间 |")
    lines.append("| --- | ---: | ---: | --- |")
    for report in payload["source_reports"]:
        lines.append(
            f"| `{report['label']}` | {fmt(report.get('selected_rows'))} | "
            f"{fmt(report.get('jobs'))} | {report.get('created_at')} |"
        )
    lines.append("")
    lines.append("## 差异最大的 Rows")
    lines.append("")
    lines.append("| 报告 | Entry | Form | Task | Status | 最差 relative RMS | RMS V | Max Abs V | 最差信号 |")
    lines.append("| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |")
    for row in payload["outliers"]:
        worst = row.get("worst_signal_by_relative_rms")
        if isinstance(worst, dict):
            worst_label = f"{worst.get('signal')} ({worst.get('kind')})"
        else:
            worst_label = "-"
        lines.append(
            f"| `{row.get('report')}` | `{row.get('entry_id')}` | `{row.get('form')}` | "
            f"`{row.get('task_id')}` | `{row.get('status')}` | {fmt(row.get('max_nrmse'))} | "
            f"{fmt(row.get('max_rmse_v'))} | {fmt(row.get('max_abs_v'))} | {worst_label} |"
        )
    lines.append("")
    lines.append("## 解释")
    lines.append("")
    lines.append(
        "当 `needs_review_pairs` 和 `blocked_pairs` 都为 0 时，说明当前 waveform gate "
        "至少与这批任务上的官方 Spectre AX/classic 差异相一致。因此 EVAS 应按 "
        "Spectre-equivalent behavior 判断，而不是按更严格的单一波形精度目标判断。"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path, help="same-server speed JSON reports")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repo root used to resolve CSV paths")
    parser.add_argument("--mode-a", default="ax", help="first Spectre mode")
    parser.add_argument("--mode-b", default="classic", help="second Spectre mode")
    parser.add_argument("--sample-n", type=int, default=1200, help="samples per waveform comparison")
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    parser.add_argument("--outlier-limit", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_payload(args)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(payload, args.out_md)
    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_md}")


if __name__ == "__main__":
    main()
