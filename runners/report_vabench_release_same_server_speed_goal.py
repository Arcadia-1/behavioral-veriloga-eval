#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
REPORTS_ROOT = ROOT / "speed-optimization" / "reports"
DEFAULT_REPORT_MD = REPORTS_ROOT / f"same_server_speed_goal_summary_{date.today().isoformat().replace('-', '')}.md"
DEFAULT_REPORT_JSON = REPORTS_ROOT / f"same_server_speed_goal_summary_{date.today().isoformat().replace('-', '')}.json"
DEFAULT_SELF_CONSISTENCY_JSON = (
    REPORTS_ROOT / "spectre_ax_classic_self_consistency_clean_repeats_20260522.json"
)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def float_or_none(value: object) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def relative_rms_value(row: dict[str, object], aggregate: str) -> float | None:
    if aggregate == "max":
        value = float_or_none(row.get("max_relative_rms_error"))
        return value if value is not None else float_or_none(row.get("max_nrmse"))
    if aggregate == "mean":
        value = float_or_none(row.get("mean_relative_rms_error"))
        return value if value is not None else float_or_none(row.get("mean_nrmse"))
    raise ValueError(f"unknown aggregate: {aggregate}")


def geomean(values: Iterable[float]) -> float | None:
    positives = [value for value in values if value > 0.0 and math.isfinite(value)]
    if not positives:
        return None
    return math.exp(sum(math.log(value) for value in positives) / len(positives))


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * pct
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    frac = pos - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def stats(values: Iterable[float]) -> dict[str, float | int | None]:
    vals = [value for value in values if value > 0.0 and math.isfinite(value)]
    if not vals:
        return {
            "n": 0,
            "geomean": None,
            "mean": None,
            "median": None,
            "p10": None,
            "p90": None,
            "min": None,
            "max": None,
            "stdev": None,
            "cv": None,
        }
    mean = statistics.fmean(vals)
    stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return {
        "n": len(vals),
        "geomean": geomean(vals),
        "mean": mean,
        "median": statistics.median(vals),
        "p10": percentile(vals, 0.10),
        "p90": percentile(vals, 0.90),
        "min": min(vals),
        "max": max(vals),
        "stdev": stdev,
        "cv": stdev / mean if mean > 0 else None,
    }


def fmt(value: object, digits: int = 3) -> str:
    number = float_or_none(value)
    if number is None:
        return "-"
    if digits == 0:
        return f"{number:.0f}"
    if abs(number) >= 100:
        return f"{number:.1f}"
    if abs(number) >= 10:
        return f"{number:.2f}"
    return f"{number:.{digits}f}"


def load_report(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["_path"] = rel(path)
    data["_label"] = path.stem
    return data


def load_self_consistency_anchor(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    resolved = path if path.is_absolute() else ROOT / path
    if not resolved.exists():
        return None
    data = json.loads(resolved.read_text(encoding="utf-8"))
    summary = data.get("summary", {})
    if not isinstance(summary, dict):
        return None
    simulator_summary = summary.get("simulator_style_summary", {})
    rel_info = simulator_summary.get("relative_rms_error", {}) if isinstance(simulator_summary, dict) else {}
    abs_v = simulator_summary.get("absolute_voltage_error", {}) if isinstance(simulator_summary, dict) else {}
    metrics = summary.get("metrics", {})
    if isinstance(metrics, dict):
        max_relative = metrics.get("max_relative_rms_error", {}) or metrics.get("max_nrmse", {})
    else:
        max_relative = {}
    max_rms = metrics.get("max_rmse_v", {}) if isinstance(metrics, dict) else {}
    max_abs = metrics.get("max_abs_v", {}) if isinstance(metrics, dict) else {}
    return {
        "path": rel(resolved),
        "mode_a": data.get("mode_a"),
        "mode_b": data.get("mode_b"),
        "total_pairs": summary.get("total_pairs"),
        "passed_pairs": summary.get("passed_pairs"),
        "needs_review_pairs": summary.get("needs_review_pairs"),
        "blocked_pairs": summary.get("blocked_pairs"),
        "relative_rms_worst_signal_max": rel_info.get("worst_signal_max")
        if isinstance(rel_info, dict)
        else max_relative.get("max")
        if isinstance(max_relative, dict)
        else None,
        "absolute_rms_error_max_v": abs_v.get("max_rms_v")
        if isinstance(abs_v, dict)
        else max_rms.get("max")
        if isinstance(max_rms, dict)
        else None,
        "absolute_point_error_max_v": abs_v.get("max_point_v")
        if isinstance(abs_v, dict)
        else max_abs.get("max")
        if isinstance(max_abs, dict)
        else None,
    }


def report_mode_summary(report: dict[str, object]) -> dict[tuple[str, str], dict[str, object]]:
    summary = report.get("summary", {})
    if not isinstance(summary, dict):
        return {}
    rows = summary.get("mode_summary", [])
    out: dict[tuple[str, str], dict[str, object]] = {}
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            out[(str(row.get("backend")), str(row.get("mode")))] = row
    return out


def report_gate_summary(report: dict[str, object]) -> dict[str, dict[str, object]]:
    summary = report.get("summary", {})
    if not isinstance(summary, dict):
        return {}
    rows = summary.get("equivalence_gate_summary") or summary.get("accuracy_gate_summary", [])
    out: dict[str, dict[str, object]] = {}
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                out[str(row.get("mode"))] = row
    return out


def speedup_rows(report: dict[str, object], gated: bool) -> list[dict[str, object]]:
    summary = report.get("summary", {})
    if not isinstance(summary, dict):
        return []
    if gated:
        rows = summary.get("equivalence_gated_speedups") or summary.get("accuracy_gated_speedups", [])
    else:
        rows = summary.get("speedups", [])
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def result_rows(report: dict[str, object]) -> list[dict[str, object]]:
    rows = report.get("results", [])
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def grouped_key(row: dict[str, object]) -> tuple[str, str, str, str]:
    return (
        str(row.get("entry_id")),
        str(row.get("form")),
        str(row.get("variant") or "gold"),
        str(row.get("task_id")),
    )


def per_report_speedup_stats(reports: list[dict[str, object]], gated: bool) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for report in reports:
        by_pair: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in speedup_rows(report, gated=gated):
            value = float_or_none(row.get("spectre_over_evas_speedup"))
            if value is None or value <= 0:
                continue
            by_pair[(str(row.get("spectre_mode")), str(row.get("evas_mode")))].append(value)
        for (spectre_mode, evas_mode), values in sorted(by_pair.items()):
            item = stats(values)
            rows.append(
                {
                    "report": report["_label"],
                    "report_path": report["_path"],
                    "spectre_mode": spectre_mode,
                    "evas_mode": evas_mode,
                    **item,
                }
            )
    return rows


def combined_speedup_stats(reports: list[dict[str, object]], gated: bool) -> list[dict[str, object]]:
    by_pair: dict[tuple[str, str], list[float]] = defaultdict(list)
    for report in reports:
        for row in speedup_rows(report, gated=gated):
            value = float_or_none(row.get("spectre_over_evas_speedup"))
            if value is None or value <= 0:
                continue
            by_pair[(str(row.get("spectre_mode")), str(row.get("evas_mode")))].append(value)
    return [
        {
            "spectre_mode": spectre_mode,
            "evas_mode": evas_mode,
            **stats(values),
        }
        for (spectre_mode, evas_mode), values in sorted(by_pair.items())
    ]


def combined_mode_time_stats(reports: list[dict[str, object]]) -> list[dict[str, object]]:
    by_pair: dict[tuple[str, str], list[float]] = defaultdict(list)
    pass_counts: dict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
    for report in reports:
        for key, row in report_mode_summary(report).items():
            value = float_or_none(row.get("geomean_wall_time_s"))
            if value is not None:
                by_pair[key].append(value)
            pass_counts[key].append((int(row.get("pass_count", 0)), int(row.get("runs", 0))))
    out: list[dict[str, object]] = []
    for (backend, mode), values in sorted(by_pair.items()):
        total_pass = sum(item[0] for item in pass_counts[(backend, mode)])
        total_runs = sum(item[1] for item in pass_counts[(backend, mode)])
        out.append(
            {
                "backend": backend,
                "mode": mode,
                "reports": len(values),
                "pass_count": total_pass,
                "runs": total_runs,
                **stats(values),
            }
        )
    return out


def fast_over_strict_stats(reports: list[dict[str, object]]) -> dict[str, object]:
    ratios: list[float] = []
    for report in reports:
        by_case: dict[tuple[str, str, str, str], dict[str, float]] = defaultdict(dict)
        for row in result_rows(report):
            if row.get("backend") != "evas" or row.get("ok") is not True:
                continue
            mode = str(row.get("mode"))
            if mode not in {"strict_current", "profile_fast_skip_source_error_control"}:
                continue
            value = float_or_none(row.get("wall_time_s"))
            if value is not None and value > 0:
                by_case[grouped_key(row)][mode] = value
        for cells in by_case.values():
            strict = cells.get("strict_current")
            fast = cells.get("profile_fast_skip_source_error_control")
            if strict is not None and fast is not None and fast > 0:
                ratios.append(strict / fast)
    return stats(ratios)


def nonpass_rows(reports: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for report in reports:
        for row in result_rows(report):
            if row.get("ok") is True:
                continue
            gate = row.get("equivalence_gate") or row.get("accuracy_gate", {})
            rows.append(
                {
                    "report": report["_label"],
                    "entry_id": row.get("entry_id"),
                    "form": row.get("form"),
                    "backend": row.get("backend"),
                    "mode": row.get("mode"),
                    "status": row.get("status"),
                    "notes": row.get("notes", []),
                    "equivalence_gate": gate,
                    "accuracy_gate": gate,
                }
            )
    return rows


def iter_waveform_parities(
    reports: list[dict[str, object]],
    *,
    evas_mode: str = "profile_fast_skip_source_error_control",
) -> Iterable[dict[str, object]]:
    for report in reports:
        for row in result_rows(report):
            if row.get("backend") != "evas" or row.get("mode") != evas_mode:
                continue
            gate = row.get("equivalence_gate") or row.get("accuracy_gate", {})
            if not isinstance(gate, dict):
                continue
            strict = gate.get("strict_evas_parity")
            if isinstance(strict, dict):
                yield {
                    "report": report["_label"],
                    "target": "strict_evas",
                    "entry_id": row.get("entry_id"),
                    "form": row.get("form"),
                    "task_id": row.get("task_id"),
                    "parity": strict,
                }
            spectre_parity = gate.get("spectre_parity", {})
            if isinstance(spectre_parity, dict):
                for spectre_mode, parity in sorted(spectre_parity.items()):
                    if isinstance(parity, dict):
                        yield {
                            "report": report["_label"],
                            "target": f"spectre_{spectre_mode}",
                            "entry_id": row.get("entry_id"),
                            "form": row.get("form"),
                            "task_id": row.get("task_id"),
                            "parity": parity,
                        }


def waveform_diagnostic_stats(reports: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    non_waveform: dict[str, int] = defaultdict(int)
    for item in iter_waveform_parities(reports):
        parity = item["parity"]
        if not isinstance(parity, dict):
            continue
        if relative_rms_value(parity, "max") is None:
            non_waveform[str(item["target"])] += 1
            continue
        grouped[str(item["target"])].append(parity)

    out: list[dict[str, object]] = []
    for target in sorted(set(grouped) | set(non_waveform)):
        rows = grouped.get(target, [])
        base = {
            "target": target,
            "waveform_rows": len(rows),
            "non_waveform_rows": non_waveform.get(target, 0),
            "current_passed_rows": sum(1 for row in rows if row.get("status") == "passed"),
            "max_relative_rms": max(
                (value for row in rows if (value := relative_rms_value(row, "max")) is not None),
                default=None,
            ),
            "max_row_mean_relative_rms": max(
                (value for row in rows if (value := relative_rms_value(row, "mean")) is not None),
                default=None,
            ),
            "max_rms_v": max(
                (float(row["max_rmse_v"]) for row in rows if float_or_none(row.get("max_rmse_v")) is not None),
                default=None,
            ),
            "max_abs_v": max(
                (float(row["max_abs_v"]) for row in rows if float_or_none(row.get("max_abs_v")) is not None),
                default=None,
            ),
        }
        out.append(base)
    return out


def outlier_rows(reports: list[dict[str, object]], limit: int) -> dict[str, list[dict[str, object]]]:
    speedups: list[dict[str, object]] = []
    for report in reports:
        result_index: dict[tuple[str, str, str, str, str, str], dict[str, object]] = {}
        for result in result_rows(report):
            key = (
                str(result.get("entry_id")),
                str(result.get("form")),
                str(result.get("variant") or "gold"),
                str(result.get("task_id")),
                str(result.get("backend")),
                str(result.get("mode")),
            )
            result_index[key] = result
        for row in speedup_rows(report, gated=True):
            if (
                row.get("spectre_mode") == "ax"
                and row.get("evas_mode") == "profile_fast_skip_source_error_control"
            ):
                value = float_or_none(row.get("spectre_over_evas_speedup"))
                if value is None:
                    continue
                key_prefix = (
                    str(row.get("entry_id")),
                    str(row.get("form")),
                    str(row.get("variant") or "gold"),
                    str(row.get("task_id")),
                )
                evas = result_index.get((*key_prefix, "evas", "profile_fast_skip_source_error_control"), {})
                spectre = result_index.get((*key_prefix, "spectre", "ax"), {})
                speedups.append(
                    {
                        "report": report["_label"],
                        **row,
                        "evas_steps": (evas.get("timing") or {}).get("accepted_tran_steps")
                        if isinstance(evas.get("timing"), dict)
                        else None,
                        "spectre_steps": (spectre.get("timing") or {}).get("accepted_tran_steps")
                        if isinstance(spectre.get("timing"), dict)
                        else None,
                    }
                )

    fast_times: list[dict[str, object]] = []
    for report in reports:
        for row in result_rows(report):
            if row.get("backend") != "evas" or row.get("mode") != "profile_fast_skip_source_error_control":
                continue
            value = float_or_none(row.get("wall_time_s"))
            if value is None:
                continue
            fast_times.append(
                {
                    "report": report["_label"],
                    **row,
                    "evas_steps": (row.get("timing") or {}).get("accepted_tran_steps")
                    if isinstance(row.get("timing"), dict)
                    else None,
                }
            )

    return {
        "smallest_ax_fast_speedups": sorted(
            speedups,
            key=lambda row: float(row["spectre_over_evas_speedup"]),
        )[:limit],
        "largest_ax_fast_speedups": sorted(
            speedups,
            key=lambda row: float(row["spectre_over_evas_speedup"]),
            reverse=True,
        )[:limit],
        "slowest_fast_skip_cases": sorted(
            fast_times,
            key=lambda row: float(row["wall_time_s"]),
            reverse=True,
        )[:limit],
    }


def write_markdown(payload: dict[str, object], path: Path) -> None:
    reports = payload["reports"]
    mode_stats = payload["combined_mode_time_stats"]
    gated_stats = payload["combined_equivalence_gated_speedup_stats"]
    raw_stats = payload["combined_raw_speedup_stats"]
    per_report = payload["per_report_equivalence_gated_speedup_stats"]
    nonpasses = payload["nonpass_rows"]
    outliers = payload["outliers"]
    fast_vs_strict = payload["fast_over_strict_stats"]
    tolerance = payload["waveform_diagnostic_stats"]

    lines: list[str] = []
    lines.append("# vaBench 同服务器速度目标汇总")
    lines.append("")
    lines.append(f"- 生成时间: {payload['generated_at']}")
    lines.append(f"- 输入报告数: {len(reports)}")
    for report in reports:
        lines.append(
            f"  - `{report['_label']}`: 行数={report.get('selected_rows')} "
            f"并发任务={report.get('jobs')} 路径=`{report['_path']}`"
        )
    lines.append("")
    lines.append("## 等价性策略")
    lines.append("")
    lines.append(
        "速度统计行先由任务行为检查门控，再与 Spectre 参考结果做波形等价性检查。"
        "这是 Spectre 等价性接受准则，不是说 EVAS 要比 Spectre 更精确。"
    )
    lines.append("")
    lines.append(
        "实现注释：波形等价性用仿真器常见条件报告：row-mean relative RMS error、"
        "worst-signal relative RMS error、max RMS voltage error、max point voltage error，"
        "以及 event/digital mismatch。这些指标替代面向论文报告里的百分位简写。"
    )
    lines.append("")
    lines.append(
        "`spectre/ax` 是主要的官方快速 Spectre 速度基线；`spectre/classic` 是更保守的 "
        "non-X reference path。AX/classic 在事件驱动 behavioral 任务上出现波形差异是正常的，"
        "因此 EVAS 的容差应锚定 Spectre 自身一致性，而不是单一“绝对真值波形”。"
    )
    anchor = payload.get("spectre_self_consistency_anchor")
    if isinstance(anchor, dict):
        lines.append("")
        lines.append(
            f"配套自一致性报告 `{anchor.get('path')}` 在同一 row 集合上直接比较 "
            f"Spectre {anchor.get('mode_a')}/Spectre {anchor.get('mode_b')}："
            f"{anchor.get('passed_pairs')}/{anchor.get('total_pairs')} row pairs 通过，"
            f"{anchor.get('needs_review_pairs')} 个 needs-review，{anchor.get('blocked_pairs')} 个 blocked。"
            f"最差 signal relative RMS error 为 {fmt(anchor.get('relative_rms_worst_signal_max'))}；"
            f"max RMS voltage error 为 {fmt(anchor.get('absolute_rms_error_max_v'))} V。"
        )

    lines.append("")
    lines.append("## 按模式汇总的 Wall-Time")
    lines.append("")
    lines.append("| 后端 | 模式 | 报告数 | PASS/Runs | 几何均值 s | 算术均值 s | CV |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for row in mode_stats:
        lines.append(
            f"| {row['backend']} | `{row['mode']}` | {row['reports']} | "
            f"{row['pass_count']}/{row['runs']} | {fmt(row['geomean'])} | "
            f"{fmt(row['mean'])} | {fmt(row['cv'])} |"
        )

    lines.append("")
    lines.append("## Spectre-Equivalence 门控后的总体加速比")
    lines.append("")
    lines.append("| Spectre | EVAS | N | 几何均值 x | 算术均值 x | 中位数 x | 最慢行 x | 最快行 x |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in gated_stats:
        lines.append(
            f"| `{row['spectre_mode']}` | `{row['evas_mode']}` | {row['n']} | "
            f"{fmt(row['geomean'])} | {fmt(row['mean'])} | {fmt(row['median'])} | "
            f"{fmt(row['min'])} | {fmt(row['max'])} |"
        )

    lines.append("")
    lines.append("## 每轮 Repeat 的 Spectre-Equivalence 门控加速比")
    lines.append("")
    lines.append("| 报告 | Spectre | EVAS | N | 几何均值 x | 中位数 x | 最慢行 x | 最快行 x |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for row in per_report:
        lines.append(
            f"| `{row['report']}` | `{row['spectre_mode']}` | `{row['evas_mode']}` | "
            f"{row['n']} | {fmt(row['geomean'])} | {fmt(row['median'])} | "
            f"{fmt(row['min'])} | {fmt(row['max'])} |"
        )

    lines.append("")
    lines.append("## 原始加速比")
    lines.append("")
    lines.append("| Spectre | EVAS | N | 几何均值 x | 算术均值 x | 中位数 x |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
    for row in raw_stats:
        lines.append(
            f"| `{row['spectre_mode']}` | `{row['evas_mode']}` | {row['n']} | "
            f"{fmt(row['geomean'])} | {fmt(row['mean'])} | {fmt(row['median'])} |"
        )

    lines.append("")
    lines.append("## EVAS Fast-Skip 相对 Strict")
    lines.append("")
    lines.append(
        "在成对 EVAS rows 上，`strict_current_wall / profile_fast_skip_source_error_control_wall` "
        f"的几何均值为 {fmt(fast_vs_strict.get('geomean'))}x，中位数为 "
        f"{fmt(fast_vs_strict.get('median'))}x，n={fast_vs_strict.get('n')}。"
    )

    lines.append("")
    lines.append("## 波形等价性诊断")
    lines.append("")
    lines.append(
        "这里复用 `profile_fast_skip_source_error_control` 已保存的 waveform parity metrics；"
        "task-specific semantic comparator 计为 non-waveform rows。指标采用仿真器式表述："
        "relative RMS error 描述尺度归一化波形偏差，absolute voltage error 约束低摆幅或近零信号。"
    )
    lines.append("")
    lines.append(
        "| 目标 | 波形行 | 非波形行 | 当前 PASS | "
        "最差 relative RMS | 最差 row-mean relative RMS | 最差 RMS V | 最差 Abs V |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in tolerance:
        lines.append(
            f"| `{row['target']}` | {row['waveform_rows']} | {row['non_waveform_rows']} | "
            f"{row['current_passed_rows']} | {fmt(row['max_relative_rms'])} | "
            f"{fmt(row['max_row_mean_relative_rms'])} | {fmt(row['max_rms_v'])} | "
            f"{fmt(row['max_abs_v'])} |"
        )

    lines.append("")
    lines.append("## Non-PASS 行")
    lines.append("")
    if nonpasses:
        lines.append("| 报告 | Entry | Form | Backend | Mode | Status | Notes |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for row in nonpasses:
            notes = "; ".join(str(item) for item in row.get("notes", []))
            lines.append(
                f"| `{row['report']}` | `{row['entry_id']}` | `{row['form']}` | "
                f"{row['backend']} | `{row['mode']}` | {row['status']} | {notes} |"
            )
    else:
        lines.append("包含的报告中没有 non-PASS rows。")

    lines.append("")
    lines.append("## 离群行")
    lines.append("")
    for title, key in [
        ("Spectre-AX / Fast-Skip 最小加速比", "smallest_ax_fast_speedups"),
        ("Spectre-AX / Fast-Skip 最大加速比", "largest_ax_fast_speedups"),
        ("Fast-Skip 最慢样例", "slowest_fast_skip_cases"),
    ]:
        lines.append(f"### {title}")
        lines.append("")
        rows = outliers[key]
        if not rows:
            lines.append("无 rows。")
            lines.append("")
            continue
        lines.append("| 报告 | Entry | Form | Task | 数值 | EVAS s | Spectre s | EVAS steps | Spectre steps |")
        lines.append("| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |")
        for row in rows:
            value = row.get("spectre_over_evas_speedup", row.get("wall_time_s"))
            evas_wall = row.get("evas_wall_time_s", row.get("wall_time_s"))
            spectre_wall = row.get("spectre_wall_time_s")
            lines.append(
                f"| `{row.get('report')}` | `{row.get('entry_id')}` | `{row.get('form')}` | "
                f"`{row.get('task_id')}` | {fmt(value)} | {fmt(evas_wall)} | {fmt(spectre_wall)} | "
                f"{fmt(row.get('evas_steps'), 0)} | {fmt(row.get('spectre_steps'), 0)} |"
            )
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_payload(
    paths: list[Path],
    outlier_limit: int,
    *,
    self_consistency_json: Path | None = None,
) -> dict[str, object]:
    reports = [load_report(path) for path in paths]
    combined_equivalence_gated = combined_speedup_stats(reports, gated=True)
    per_report_equivalence_gated = per_report_speedup_stats(reports, gated=True)
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reports": [
            {
                "_label": report["_label"],
                "_path": report["_path"],
                "selected_rows": report.get("selected_rows"),
                "jobs": report.get("jobs"),
                "created_at": report.get("created_at"),
            }
            for report in reports
        ],
        "combined_mode_time_stats": combined_mode_time_stats(reports),
        "combined_equivalence_gated_speedup_stats": combined_equivalence_gated,
        "combined_accuracy_gated_speedup_stats": combined_equivalence_gated,
        "combined_raw_speedup_stats": combined_speedup_stats(reports, gated=False),
        "per_report_equivalence_gated_speedup_stats": per_report_equivalence_gated,
        "per_report_accuracy_gated_speedup_stats": per_report_equivalence_gated,
        "fast_over_strict_stats": fast_over_strict_stats(reports),
        "waveform_diagnostic_stats": waveform_diagnostic_stats(reports),
        "tolerance_sweep_stats": waveform_diagnostic_stats(reports),
        "spectre_self_consistency_anchor": load_self_consistency_anchor(self_consistency_json),
        "nonpass_rows": nonpass_rows(reports),
        "outliers": outlier_rows(reports, outlier_limit),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path, help="same-server speed JSON reports")
    parser.add_argument("--out-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_REPORT_JSON)
    parser.add_argument("--outlier-limit", type=int, default=10)
    parser.add_argument(
        "--self-consistency-json",
        type=Path,
        default=DEFAULT_SELF_CONSISTENCY_JSON,
        help="optional Spectre mode self-consistency artifact to cite",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [path if path.is_absolute() else ROOT / path for path in args.reports]
    missing = [path for path in paths if not path.exists()]
    if missing:
        raise SystemExit("missing reports: " + ", ".join(rel(path) for path in missing))
    self_consistency_json = (
        args.self_consistency_json
        if args.self_consistency_json.is_absolute()
        else ROOT / args.self_consistency_json
    )
    payload = build_payload(
        paths,
        args.outlier_limit,
        self_consistency_json=self_consistency_json,
    )

    out_json = args.out_json if args.out_json.is_absolute() else ROOT / args.out_json
    out_md = args.out_md if args.out_md.is_absolute() else ROOT / args.out_md
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(payload, out_md)
    print(f"wrote {rel(out_json)}")
    print(f"wrote {rel(out_md)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
