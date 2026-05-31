#!/usr/bin/env python3
"""Audit vaBench model-baseline results for benchmark-quality risks.

This is a diagnostic report, not a metadata rewrite tool. It compares model
baseline triage reports and highlights denominator sensitivity, hard categories,
difficulty-label anomalies, and rows that deserve manual benchmark review.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "benchmark-vabench-release-v1" / "reports"

NON_MODEL_OR_INCONCLUSIVE_AXES = {"generation", "runner", "simulation_output_missing"}
BEHAVIOR_READY_AXES = {"pass", "model_behavior"}

CSV_FIELDS = [
    "category",
    "row_count",
    "both_pass",
    "first_only_pass",
    "second_only_pass",
    "both_fail",
    "first_pass_rate_pct",
    "second_pass_rate_pct",
    "common_behavior_fail_rows",
    "common_artifact_or_protocol_fail_rows",
    "risk_label",
    "recommended_action",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def compact(value: Any, limit: int = 180) -> str:
    raw = "" if value is None else str(value)
    text = re.sub(r"\s+", " ", raw).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(100.0 * numerator / denominator, 2)


def stable_task_key(row: dict[str, Any]) -> str:
    return str(row.get("release_task_id") or row.get("task_id") or "")


def is_pass(row: dict[str, Any] | None) -> bool:
    return bool(row and row.get("dual_pass"))


def is_valid_candidate(row: dict[str, Any]) -> bool:
    return str(row.get("triage_axis", "")) not in NON_MODEL_OR_INCONCLUSIVE_AXES


def is_behavior_ready(row: dict[str, Any]) -> bool:
    return str(row.get("triage_axis", "")) in BEHAVIOR_READY_AXES


def score_slice(rows: list[dict[str, Any]], name: str, description: str) -> dict[str, Any]:
    pass_rows = sum(1 for row in rows if is_pass(row))
    return {
        "slice": name,
        "description": description,
        "total_rows": len(rows),
        "strict_dual_pass_rows": pass_rows,
        "strict_dual_pass_rate_pct": pct(pass_rows, len(rows)),
        "non_pass_rows": len(rows) - pass_rows,
    }


def fallback_score_slices(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid = [row for row in rows if is_valid_candidate(row)]
    behavior_ready = [row for row in rows if is_behavior_ready(row)]
    return [
        score_slice(rows, "full_strict", "All rows count in the denominator."),
        score_slice(valid, "valid_candidate", "Rows with a complete artifact and reliable evaluator judgment."),
        score_slice(behavior_ready, "behavior_ready", "Rows that reached the functional checker."),
    ]


def rows_by_key(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {stable_task_key(row): row for row in report.get("rows", []) if stable_task_key(row)}


def model_summary(name: str, report: dict[str, Any]) -> dict[str, Any]:
    rows = list(report.get("rows", []))
    return {
        "model": name,
        "total_rows": len(rows),
        "strict_dual_pass_rows": sum(1 for row in rows if is_pass(row)),
        "strict_dual_pass_rate_pct": pct(sum(1 for row in rows if is_pass(row)), len(rows)),
        "axis_counts": dict(sorted(Counter(str(row.get("triage_axis", "")) for row in rows).items())),
        "score_slices": report.get("score_slices") or fallback_score_slices(rows),
    }


def group_stats(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key, "") or "unknown")].append(row)

    out: dict[str, dict[str, Any]] = {}
    for value, group in sorted(grouped.items()):
        pass_rows = sum(1 for row in group if is_pass(row))
        valid = [row for row in group if is_valid_candidate(row)]
        behavior_ready = [row for row in group if is_behavior_ready(row)]
        behavior_pass = sum(1 for row in behavior_ready if is_pass(row))
        out[value] = {
            key: value,
            "total_rows": len(group),
            "strict_dual_pass_rows": pass_rows,
            "strict_dual_pass_rate_pct": pct(pass_rows, len(group)),
            "valid_candidate_rows": len(valid),
            "behavior_ready_rows": len(behavior_ready),
            "behavior_ready_pass_rows": behavior_pass,
            "behavior_ready_pass_rate_pct": pct(behavior_pass, len(behavior_ready)),
            "non_model_or_inconclusive_rows": len(group) - len(valid),
        }
    return out


def pass_overlap(first_rows: dict[str, dict[str, Any]], second_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    keys = sorted(set(first_rows) | set(second_rows))
    both_pass: list[str] = []
    first_only: list[str] = []
    second_only: list[str] = []
    both_fail: list[str] = []
    missing: list[str] = []
    for key in keys:
        first = first_rows.get(key)
        second = second_rows.get(key)
        if first is None or second is None:
            missing.append(key)
            continue
        first_ok = is_pass(first)
        second_ok = is_pass(second)
        if first_ok and second_ok:
            both_pass.append(key)
        elif first_ok:
            first_only.append(key)
        elif second_ok:
            second_only.append(key)
        else:
            both_fail.append(key)

    return {
        "row_count": len(keys),
        "both_pass": len(both_pass),
        "first_only_pass": len(first_only),
        "second_only_pass": len(second_only),
        "both_fail": len(both_fail),
        "missing_in_one_report": len(missing),
        "both_pass_examples": both_pass[:10],
        "first_only_pass_examples": first_only[:10],
        "second_only_pass_examples": second_only[:10],
        "both_fail_examples": both_fail[:10],
        "missing_examples": missing[:10],
    }


def difficulty_audit(model_reports: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model, report in model_reports.items():
        stats = group_stats(list(report.get("rows", [])), "difficulty")
        d1 = stats.get("D1", {})
        d2 = stats.get("D2", {})
        d3 = stats.get("D3", {})
        d1_rate = float(d1.get("strict_dual_pass_rate_pct", 0.0))
        d2_rate = float(d2.get("strict_dual_pass_rate_pct", 0.0))
        d3_rate = float(d3.get("strict_dual_pass_rate_pct", 0.0))
        flags: list[str] = []
        if d1 and d2 and d1_rate <= d2_rate:
            flags.append("D1_not_easier_than_D2")
        if d2 and d3 and d3_rate >= d2_rate:
            flags.append("D3_not_harder_than_D2")
        if d1 and d1_rate < 50.0:
            flags.append("D1_low_pass_rate")
        rows.append(
            {
                "model": model,
                "D1_pass_rate_pct": d1_rate,
                "D1_rows": int(d1.get("total_rows", 0) or 0),
                "D2_pass_rate_pct": d2_rate,
                "D2_rows": int(d2.get("total_rows", 0) or 0),
                "D3_pass_rate_pct": d3_rate,
                "D3_rows": int(d3.get("total_rows", 0) or 0),
                "flags": flags,
                "interpretation": difficulty_interpretation(flags),
            }
        )
    return rows


def difficulty_interpretation(flags: list[str]) -> str:
    if not flags:
        return "No monotonicity warning from this model alone."
    return (
        "Treat difficulty labels as requiring manual calibration; do not claim calibrated "
        "difficulty tiers from the current baseline rates alone."
    )


def category_audit(
    first_name: str,
    second_name: str,
    first_rows: dict[str, dict[str, Any]],
    second_rows: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for key in sorted(set(first_rows) & set(second_rows)):
        category = str(first_rows[key].get("category") or second_rows[key].get("category") or "unknown")
        grouped[category].append(key)

    out: list[dict[str, Any]] = []
    for category, keys in sorted(grouped.items()):
        both_pass = first_only = second_only = both_fail = 0
        common_behavior = 0
        common_artifact_or_protocol = 0
        for key in keys:
            first = first_rows[key]
            second = second_rows[key]
            first_ok = is_pass(first)
            second_ok = is_pass(second)
            if first_ok and second_ok:
                both_pass += 1
            elif first_ok:
                first_only += 1
            elif second_ok:
                second_only += 1
            else:
                both_fail += 1
                axes = {str(first.get("triage_axis")), str(second.get("triage_axis"))}
                if axes <= {"model_behavior"}:
                    common_behavior += 1
                if axes & (NON_MODEL_OR_INCONCLUSIVE_AXES | {"model_dut_compile", "model_tb_compile", "model_spectre_ahdl_compile", "model_spectre_tb_source", "model_spectre_elab_or_topology"}):
                    common_artifact_or_protocol += 1

        first_pass = both_pass + first_only
        second_pass = both_pass + second_only
        risk_label = "balanced"
        action = "Keep as normal benchmark coverage; inspect row-level failures only if paper wording overclaims."
        if both_pass == 0:
            risk_label = "zero_common_pass"
            action = "Manually audit prompts/checkers and category scope before using this as evidence of calibrated difficulty."
        elif pct(first_pass, len(keys)) < 15.0 and pct(second_pass, len(keys)) < 15.0:
            risk_label = "common_hard_category"
            action = "Check whether the category is under-scaffolded or genuinely hard; keep as hard coverage only with clear prompts/checkers."
        elif common_artifact_or_protocol >= max(2, len(keys) // 5):
            risk_label = "protocol_noise_sensitive"
            action = "Separate language/protocol failures from behavior claims and inspect public contracts for missing syntax constraints."

        out.append(
            {
                "category": category,
                "row_count": len(keys),
                "both_pass": both_pass,
                "first_only_pass": first_only,
                "second_only_pass": second_only,
                "both_fail": both_fail,
                "first_pass_rate_pct": pct(first_pass, len(keys)),
                "second_pass_rate_pct": pct(second_pass, len(keys)),
                "common_behavior_fail_rows": common_behavior,
                "common_artifact_or_protocol_fail_rows": common_artifact_or_protocol,
                "risk_label": risk_label,
                "recommended_action": action,
                "first_model": first_name,
                "second_model": second_name,
            }
        )
    return out


def form_audit(model_reports: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model, report in model_reports.items():
        for form, stats in group_stats(list(report.get("rows", [])), "form").items():
            item = dict(stats)
            item["model"] = model
            item["form"] = form
            out.append(item)
    return out


def relabel_candidates(
    first_name: str,
    second_name: str,
    first_rows: dict[str, dict[str, Any]],
    second_rows: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for key in sorted(set(first_rows) & set(second_rows)):
        first = first_rows[key]
        second = second_rows[key]
        difficulty = str(first.get("difficulty") or second.get("difficulty") or "")
        both_ok = is_pass(first) and is_pass(second)
        both_fail = not is_pass(first) and not is_pass(second)
        if difficulty == "D3" and both_ok:
            reason = "D3 row passed by both baselines; check whether it is truly integration-level or over-labeled."
        elif difficulty == "D1" and both_fail:
            reason = "D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuinely not basic."
        else:
            continue
        candidates.append(
            {
                "release_task_id": key,
                "task_id": first.get("task_id") or second.get("task_id"),
                "difficulty": difficulty,
                "form": first.get("form") or second.get("form"),
                "category": first.get("category") or second.get("category"),
                "reason": reason,
                f"{first_name}_axis": first.get("triage_axis"),
                f"{second_name}_axis": second.get("triage_axis"),
                f"{first_name}_family": first.get("root_cause_family"),
                f"{second_name}_family": second.get("root_cause_family"),
                f"{first_name}_evidence": first.get("evidence"),
                f"{second_name}_evidence": second.get("evidence"),
            }
        )
    return candidates


def common_fail_examples(
    first_name: str,
    second_name: str,
    first_rows: dict[str, dict[str, Any]],
    second_rows: dict[str, dict[str, Any]],
    limit: int = 40,
) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    for key in sorted(set(first_rows) & set(second_rows)):
        first = first_rows[key]
        second = second_rows[key]
        if is_pass(first) or is_pass(second):
            continue
        examples.append(
            {
                "release_task_id": key,
                "task_id": first.get("task_id") or second.get("task_id"),
                "category": first.get("category") or second.get("category"),
                "difficulty": first.get("difficulty") or second.get("difficulty"),
                "form": first.get("form") or second.get("form"),
                f"{first_name}_axis": first.get("triage_axis"),
                f"{second_name}_axis": second.get("triage_axis"),
                f"{first_name}_family": first.get("root_cause_family"),
                f"{second_name}_family": second.get("root_cause_family"),
                f"{first_name}_evidence": first.get("evidence"),
                f"{second_name}_evidence": second.get("evidence"),
            }
        )
    examples.sort(key=lambda row: (str(row.get("category")), str(row.get("difficulty")), str(row.get("release_task_id"))))
    return examples[:limit]


def build_report(model_reports: dict[str, dict[str, Any]], sources: dict[str, Path]) -> dict[str, Any]:
    if len(model_reports) < 2:
        raise ValueError("at least two model reports are required")
    model_names = list(model_reports)
    first_name, second_name = model_names[0], model_names[1]
    first_rows = rows_by_key(model_reports[first_name])
    second_rows = rows_by_key(model_reports[second_name])

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "models": model_names,
        "sources": {name: rel(path) for name, path in sources.items()},
        "summary": {
            "purpose": "Benchmark-quality audit from model-baseline triage reports.",
            "caution": "This report flags manual-review candidates; it does not automatically relabel difficulty or rewrite benchmark metadata.",
        },
        "model_summaries": [model_summary(name, report) for name, report in model_reports.items()],
        "pass_overlap": pass_overlap(first_rows, second_rows),
        "difficulty_audit": difficulty_audit(model_reports),
        "form_audit": form_audit(model_reports),
        "category_audit": category_audit(first_name, second_name, first_rows, second_rows),
        "difficulty_relabel_candidates": relabel_candidates(first_name, second_name, first_rows, second_rows),
        "common_fail_examples": common_fail_examples(first_name, second_name, first_rows, second_rows),
        "recommended_next_actions": [
            "Report full_strict, valid_candidate, and behavior_ready rates separately in model-baseline discussion.",
            "Treat D1/D2/D3 as design-intent labels until manual calibration resolves flagged anomalies.",
            "Audit zero-common-pass and common-hard categories before claiming calibrated benchmark difficulty.",
            "Keep incomplete generation and runner/output inconclusive rows outside circuit-behavior error analysis, while still reporting them under fixed-budget model baselines.",
        ],
    }


def md_table_row(values: list[Any]) -> str:
    return "| " + " | ".join(compact(value, 100).replace("|", "\\|") for value in values) + " |"


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    first_model, second_model = report["models"][:2]
    lines = [
        "# vaBench Model Baseline Quality Audit",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "This report audits benchmark-quality risks exposed by model baselines.",
        "It is diagnostic: flagged rows/categories require human review before metadata changes.",
        "",
        "## Model Score Slices",
        "",
        "| Model | Slice | Rows | Strict dual pass | Pass rate | Meaning |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for summary in report["model_summaries"]:
        for item in summary["score_slices"]:
            lines.append(
                md_table_row(
                    [
                        summary["model"],
                        f"`{item['slice']}`",
                        item["total_rows"],
                        item["strict_dual_pass_rows"],
                        f"{item['strict_dual_pass_rate_pct']:.2f}%",
                        item.get("description", ""),
                    ]
                )
            )

    overlap = report["pass_overlap"]
    lines.extend(
        [
            "",
            "## Pass Overlap",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| row count | {overlap['row_count']} |",
            f"| both pass | {overlap['both_pass']} |",
            f"| {first_model} only pass | {overlap['first_only_pass']} |",
            f"| {second_model} only pass | {overlap['second_only_pass']} |",
            f"| both fail | {overlap['both_fail']} |",
            f"| missing in one report | {overlap['missing_in_one_report']} |",
            "",
            "## Difficulty Calibration Warnings",
            "",
            "| Model | D1 rate | D1 rows | D2 rate | D2 rows | D3 rate | D3 rows | Flags | Interpretation |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for item in report["difficulty_audit"]:
        lines.append(
            md_table_row(
                [
                    item["model"],
                    f"{item['D1_pass_rate_pct']:.2f}%",
                    item["D1_rows"],
                    f"{item['D2_pass_rate_pct']:.2f}%",
                    item["D2_rows"],
                    f"{item['D3_pass_rate_pct']:.2f}%",
                    item["D3_rows"],
                    ", ".join(item["flags"]) or "none",
                    item["interpretation"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Category Risk Audit",
            "",
            f"| Category | Rows | Both pass | {first_model} only | {second_model} only | Both fail | {first_model} rate | {second_model} rate | Common behavior fail | Artifact/protocol fail | Risk | Action |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for item in report["category_audit"]:
        lines.append(
            md_table_row(
                [
                    item["category"],
                    item["row_count"],
                    item["both_pass"],
                    item["first_only_pass"],
                    item["second_only_pass"],
                    item["both_fail"],
                    f"{item['first_pass_rate_pct']:.2f}%",
                    f"{item['second_pass_rate_pct']:.2f}%",
                    item["common_behavior_fail_rows"],
                    item["common_artifact_or_protocol_fail_rows"],
                    f"`{item['risk_label']}`",
                    item["recommended_action"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Form Audit",
            "",
            "| Model | Form | Rows | Strict pass | Strict rate | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in report["form_audit"]:
        lines.append(
            md_table_row(
                [
                    item["model"],
                    f"`{item['form']}`",
                    item["total_rows"],
                    item["strict_dual_pass_rows"],
                    f"{item['strict_dual_pass_rate_pct']:.2f}%",
                    item["behavior_ready_rows"],
                    f"{item['behavior_ready_pass_rate_pct']:.2f}%",
                    item["non_model_or_inconclusive_rows"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Difficulty Relabel Review Candidates",
            "",
            f"| Task | Difficulty | Form | Category | Reason | {first_model} family | {second_model} family |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    if report["difficulty_relabel_candidates"]:
        for item in report["difficulty_relabel_candidates"]:
            family_keys = [key for key in item if key.endswith("_family")]
            lines.append(
                md_table_row(
                    [
                        f"`{item['release_task_id']}`",
                        f"`{item['difficulty']}`",
                        f"`{item['form']}`",
                        item["category"],
                        item["reason"],
                        item.get(family_keys[0], "") if family_keys else "",
                        item.get(family_keys[1], "") if len(family_keys) > 1 else "",
                    ]
                )
            )
    else:
        lines.append("| none |  |  |  |  |  |  |")

    lines.extend(
        [
            "",
            "## Common Failure Examples",
            "",
            f"| Task | Difficulty | Form | Category | {first_model} axis/family | {second_model} axis/family | {first_model} evidence | {second_model} evidence |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in report["common_fail_examples"]:
        axis_keys = [key for key in item if key.endswith("_axis")]
        family_keys = [key for key in item if key.endswith("_family")]
        evidence_keys = [key for key in item if key.endswith("_evidence")]
        lines.append(
            md_table_row(
                [
                    f"`{item['release_task_id']}`",
                    f"`{item['difficulty']}`",
                    f"`{item['form']}`",
                    item["category"],
                    f"{item.get(axis_keys[0], '')}/{item.get(family_keys[0], '')}" if axis_keys and family_keys else "",
                    f"{item.get(axis_keys[1], '')}/{item.get(family_keys[1], '')}" if len(axis_keys) > 1 and len(family_keys) > 1 else "",
                    item.get(evidence_keys[0], "") if evidence_keys else "",
                    item.get(evidence_keys[1], "") if len(evidence_keys) > 1 else "",
                ]
            )
        )

    lines.extend(["", "## Recommended Next Actions", ""])
    for action in report["recommended_next_actions"]:
        lines.append(f"- {action}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CSV_FIELDS})


def default_outputs(tag: str) -> tuple[Path, Path, Path]:
    base = REPORTS / f"vabench_model_baseline_quality_audit_{tag}"
    return base.with_suffix(".json"), base.with_suffix(".md"), base.with_suffix(".csv")


def parse_model_report_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("--model-report must be NAME=PATH")
    name, raw_path = value.split("=", 1)
    if not name:
        raise argparse.ArgumentTypeError("model report name cannot be empty")
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    return name, path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-report", action="append", type=parse_model_report_arg, required=True)
    parser.add_argument("--tag", default=datetime.now(timezone.utc).strftime("%Y%m%d"))
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--output-csv", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_reports: dict[str, dict[str, Any]] = {}
    sources: dict[str, Path] = {}
    for name, path in args.model_report:
        model_reports[name] = load_json(path)
        sources[name] = path

    output_json, output_md, output_csv = default_outputs(args.tag)
    output_json = args.output_json or output_json
    output_md = args.output_md or output_md
    output_csv = args.output_csv or output_csv

    report = build_report(model_reports, sources)
    write_json(output_json, report)
    write_markdown(output_md, report)
    write_csv(output_csv, report["category_audit"])
    print(
        "wrote vaBench model baseline quality audit: "
        f"{rel(output_json)} ({report['pass_overlap']['row_count']} compared rows)"
    )


if __name__ == "__main__":
    main()
