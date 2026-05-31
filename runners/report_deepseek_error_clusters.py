#!/usr/bin/env python3
"""Cluster DeepSeek full-release failures into audit-ready error families."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "benchmark-vabench-release-v1" / "reports"
DEFAULT_INPUT = REPORTS / "deepseek_full236_latest_after_wrapper_v5_overlay_20260528.json"

OUT_JSON = REPORTS / "deepseek_error_clusters_20260528.json"
OUT_CSV = REPORTS / "deepseek_error_clusters_20260528.csv"
OUT_ROWS_CSV = REPORTS / "deepseek_error_cluster_rows_20260528.csv"
OUT_MD = REPORTS / "deepseek_error_clusters_20260528.md"


@dataclass(frozen=True)
class Cluster:
    cluster_id: str
    axis: str
    label: str
    interpretation: str
    recommended_action: str


CLUSTERS: dict[str, Cluster] = {
    "B01": Cluster(
        "B01",
        "behavior",
        "Static transfer/reference/RF/power macro behavior",
        "The candidate compiles but misses an analog static transfer, reference, regulation, or RF/AFE macromodel contract.",
        "Use checker evidence to inspect whether the prompt underspecified operating points; otherwise count as model circuit-behavior failure.",
    ),
    "B02": Cluster(
        "B02",
        "behavior",
        "Dynamic response/filter/baseband behavior",
        "The candidate compiles but misses time-domain response shape such as settling, lag, integration, slew limiting, or envelope behavior.",
        "Check whether the public prompt names required dynamic observables; if yes, this is model dynamic-behavior failure.",
    ),
    "B03": Cluster(
        "B03",
        "behavior",
        "State/reset/enable/stuck-output behavior",
        "The candidate output is stuck or mishandles reset, enable, hold, release, or lock state.",
        "Audit prompt state contracts and checker windows; then treat remaining rows as state-machine or initialization failures.",
    ),
    "B04": Cluster(
        "B04",
        "behavior",
        "Event/timing/stimulus coverage behavior",
        "The generated DUT/TB misses required clocks, edges, pulse windows, phase windows, or stimulus coverage.",
        "Inspect whether edge counts and timing windows are explicit in public prompts; this cluster is sensitive to prompt observability.",
    ),
    "B05": Cluster(
        "B05",
        "behavior",
        "Decision/code/quantization sequence behavior",
        "The generated model produces the wrong comparator decisions, code sequence, DAC/ADC levels, or residue/quantization schedule.",
        "Use row-level evidence for manual circuit review; these rows usually reflect functional reasoning failures.",
    ),
    "B06": Cluster(
        "B06",
        "behavior",
        "Calibration/DEM/control algorithm behavior",
        "The generated model misses trim direction, deadband behavior, DEM rotation, calibration search, or controller sequencing.",
        "These are high-value failures for L2/L1-control claims; inspect whether algorithmic steps are fully specified.",
    ),
    "B07": Cluster(
        "B07",
        "behavior",
        "Sample/hold/aperture/droop behavior",
        "The candidate misses sampling instant, hold value, aperture delay, droop/leakage, or acquisition-window behavior.",
        "Check prompt timing contracts first; otherwise count as model sampled-analog-memory failure.",
    ),
    "B99": Cluster(
        "B99",
        "behavior",
        "Other behavior mismatch",
        "The row is a behavior mismatch but did not match a more specific deterministic rule.",
        "Manually inspect before using it as a named paper-facing failure family.",
    ),
    "C01": Cluster(
        "C01",
        "compile",
        "Verilog-A local/embedded declaration placement",
        "The candidate uses Spectre-incompatible local or embedded declarations inside analog/procedural statements.",
        "This is a model Verilog-A subset failure; public/wrapper rules already need to discourage this pattern.",
    ),
    "C02": Cluster(
        "C02",
        "compile",
        "Guarded transition() contribution",
        "The candidate places transition() contributions inside conditional/event/loop/case control.",
        "This is a model Verilog-A/Spectre subset failure and an EVAS/Spectre compatibility rule to keep explicit.",
    ),
    "C03": Cluster(
        "C03",
        "compile",
        "Restricted cross/operator placement",
        "The candidate uses cross or another restricted analog operator inside conditionally executed code.",
        "This is a model Verilog-A subset failure; future prompts can keep the operator-placement rule in the wrapper/EVAS rules.",
    ),
    "C04": Cluster(
        "C04",
        "compile",
        "Indexed/vector procedural syntax",
        "The candidate emits indexed analog/vector/procedural syntax that the evaluator/Spectre parser rejects.",
        "Treat as a syntax/subset failure unless a row-specific checker indicates an extraction bug.",
    ),
    "C05": Cluster(
        "C05",
        "compile",
        "Digital Verilog syntax in Verilog-A",
        "The candidate emits digital Verilog constructs that are not accepted in the Verilog-A evaluator path.",
        "Treat as model language-mode failure under the current benchmark contract.",
    ),
    "C06": Cluster(
        "C06",
        "compile",
        "Spectre testbench instance/source syntax",
        "The candidate testbench has malformed Spectre instance, source, include, or save syntax.",
        "This is model TB-generation failure when wrapper extraction/staging is already ruled out.",
    ),
    "C07": Cluster(
        "C07",
        "compile",
        "Unsupported event-loop/timer form",
        "The candidate uses an event-loop form unsupported by the current evaluator/Spectre-compatible subset.",
        "Keep as model subset failure unless an EVAS core regression reproduces a Spectre-accepted construct.",
    ),
    "C99": Cluster(
        "C99",
        "compile",
        "Other compile failure",
        "The row failed compilation but did not match a more specific deterministic compile rule.",
        "Inspect manually before turning it into a benchmark or model claim.",
    ),
    "G01": Cluster(
        "G01",
        "generation",
        "Incomplete generation under fixed output budget",
        "The model hit the output budget or extraction ended with no usable artifact.",
        "Count as model failure under the fixed baseline budget, but keep separate from Verilog-A competence.",
    ),
}


ROW_FIELDS = [
    "cluster_id",
    "cluster_axis",
    "cluster_label",
    "release_task_id",
    "release_entry_id",
    "form",
    "level",
    "difficulty",
    "track",
    "category",
    "base_function",
    "status",
    "dual_status",
    "evas_status",
    "primary_attribution",
    "root_cause_family",
    "evidence",
    "source_result_json",
]

SUMMARY_FIELDS = [
    "cluster_id",
    "axis",
    "label",
    "count",
    "share_of_failures",
    "dominant_category",
    "dominant_form",
    "dominant_level",
    "top_categories",
    "top_forms",
    "top_levels",
    "example_task",
    "example_evidence",
    "interpretation",
    "recommended_action",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def compact(text: Any, limit: int = 220) -> str:
    value = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def lower_join(row: dict[str, Any], fields: list[str]) -> str:
    return " ".join(str(row.get(field, "")) for field in fields).lower()


def has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def classify_compile(row: dict[str, Any]) -> str:
    text = lower_join(
        row,
        ["release_task_id", "status", "dual_status", "evas_status", "root_cause_family", "evidence"],
    )
    if "local declaration" in text or "embedded declaration" in text:
        return "C01"
    if "transition() contribution is inside" in text or (
        "transition" in text and "conditional" in text
    ):
        return "C02"
    if "cross inside" in text or "restricted operator" in text:
        return "C03"
    if "dynamic_analog_vector_index" in text or (
        "expected assign" in text and "got ident ('i')" in text
    ):
        return "C04"
    if has_any(text, ["always @", "posedge", "negedge", "assign "]) and "verilog-a" not in text:
        return "C05"
    if has_any(text, ["failed to parse tb_", "instance/source syntax", "spectre tb syntax"]):
        return "C06"
    if "unsupported_unbounded_event_loop" in text:
        return "C07"
    return "C99"


def classify_behavior(row: dict[str, Any]) -> str:
    root = str(row.get("root_cause_family", "")).lower()
    evidence = str(row.get("evidence", "")).lower()
    category = str(row.get("category", "")).lower()
    text = lower_join(
        row,
        ["release_task_id", "release_entry_id", "category", "base_function", "root_cause_family", "evidence"],
    )

    if "calibration/control algorithm" in root or "calibration, dem" in category or has_any(
        text,
        [
            "calibration",
            "deadband",
            "dwa",
            "element_shuffler",
            "gain_trim",
            "trim_controller",
            "sar_cal",
            "active_sequence",
            "ptr_unique",
            "wrap_events",
        ],
    ):
        return "B06"
    if "sample/hold" in root:
        return "B07"
    if "wrong decision/code sequence" in root:
        return "B05"
    if "missing/incorrect event timing" in root:
        return "B04"
    if "output stuck or reset/hold" in root:
        return "B03"
    if "analog transfer/reference macro" in root:
        return "B01"

    if has_any(
        evidence,
        [
            "reset_out=",
            "reset_clear=false",
            "reset_sequence=false",
            "post_reset_restarts=false",
            "not_released",
            "not_disabled",
            "never",
            "span=0.000",
            "outputs_do_not_toggle",
            "hold_failed",
            "not_held_low",
            "lock_final",
            "out_p_not_low",
            "out_p_never",
        ],
    ):
        return "B03"
    if "sampling and analog memory" in category or has_any(
        text,
        [
            "sample-and-hold",
            "sample_and_hold",
            "track-and-hold",
            "track_and_hold",
            "aperture",
            "acq_hold",
            "held_samples",
            "vin_samples",
            "hold_window",
        ],
    ):
        return "B07"
    if "pll clock" in category or has_any(
        evidence,
        [
            "too_few",
            "edge",
            "edges",
            "clk_edges",
            "clock",
            "intervals",
            "lead_window",
            "window",
            "pulses",
            "data_edges",
            "settled_samples",
            "phase_",
            "sample_windows",
            "hop_t",
        ],
    ):
        return "B04"
    if "data converter" in category or "comparator" in category or has_any(
        text,
        [
            "observed_codes",
            "expected_codes",
            "decision",
            "decisions",
            "sar_rdy",
            "thermometer",
            "dac_levels",
            "binary_dac",
            "segmented_dac",
            "stage_bit",
            "residue",
            "offset_decisions",
            "window_fracs",
        ],
    ):
        return "B05"
    if "baseband" in category or has_any(
        text,
        [
            "lowpass",
            "filter",
            "two_pole",
            "integrator",
            "slew",
            "rectifier",
            "envelope",
            "pga",
            "amplifier",
            "limiter",
        ],
    ):
        return "B02"
    if "bias reference" in category or "rf and afe" in category or has_any(
        text,
        [
            "bandgap",
            "bias",
            "ldo",
            "ptat",
            "ctat",
            "reference",
            "uvlo",
            "brownout",
            "regulation",
            "por",
            "lna",
            "pa_",
            "rssi",
            "mixer",
            "agc",
            "compression",
            "gain_wrong",
            "unclamped_range",
        ],
    ):
        return "B01"
    return "B99"


def classify_cluster(row: dict[str, Any]) -> str:
    primary = row.get("primary_attribution")
    if primary == "model_behavior_failure":
        return classify_behavior(row)
    if primary == "model_veriloga_subset_failure":
        return classify_compile(row)
    if primary == "model_incomplete_generation":
        return "G01"
    raise ValueError(f"Cannot cluster non-failure row {row.get('release_task_id')}: {primary}")


def top_counts(rows: list[dict[str, Any]], field: str, limit: int = 4) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(field, "")) for row in rows)
    return [{"name": name, "count": count} for name, count in counter.most_common(limit)]


def dominant(rows: list[dict[str, Any]], field: str) -> str:
    counts = Counter(str(row.get(field, "")) for row in rows)
    if not counts:
        return ""
    name, count = counts.most_common(1)[0]
    return f"{name} ({count})"


def percent(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def row_with_cluster(row: dict[str, Any], cluster_id: str) -> dict[str, Any]:
    cluster = CLUSTERS[cluster_id]
    out = {field: row.get(field, "") for field in ROW_FIELDS}
    out.update(
        cluster_id=cluster_id,
        cluster_axis=cluster.axis,
        cluster_label=cluster.label,
        evidence=compact(row.get("evidence", "")),
    )
    return out


def build_report(data: dict[str, Any], input_path: Path) -> dict[str, Any]:
    rows = data.get("rows", [])
    failed_rows = [row for row in rows if row.get("primary_attribution") != "pass"]
    clustered_rows = [row_with_cluster(row, classify_cluster(row)) for row in failed_rows]

    rows_by_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in clustered_rows:
        rows_by_cluster[row["cluster_id"]].append(row)

    cluster_summaries: list[dict[str, Any]] = []
    for cluster_id, members in rows_by_cluster.items():
        cluster = CLUSTERS[cluster_id]
        example = members[0]
        cluster_summaries.append(
            {
                "cluster_id": cluster_id,
                "axis": cluster.axis,
                "label": cluster.label,
                "count": len(members),
                "share_of_failures": percent(len(members), len(failed_rows)),
                "dominant_category": dominant(members, "category"),
                "dominant_form": dominant(members, "form"),
                "dominant_level": dominant(members, "level"),
                "top_categories": top_counts(members, "category"),
                "top_forms": top_counts(members, "form"),
                "top_levels": top_counts(members, "level"),
                "example_task": example.get("release_task_id", ""),
                "example_evidence": example.get("evidence", ""),
                "interpretation": cluster.interpretation,
                "recommended_action": cluster.recommended_action,
            }
        )

    axis_order = {"behavior": 0, "compile": 1, "generation": 2}
    cluster_summaries.sort(
        key=lambda item: (
            axis_order.get(str(item["axis"]), 99),
            -int(item["count"]),
            str(item["cluster_id"]),
        )
    )
    clustered_rows.sort(key=lambda row: (row["cluster_axis"], row["cluster_id"], row["release_task_id"]))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_report": str(input_path.relative_to(ROOT)),
        "method": {
            "name": "deterministic_structured_error_clustering",
            "rationale": (
                "The current vaBench baseline already has structured evaluator status, "
                "primary attribution, root-cause labels, checker evidence, forms, and categories. "
                "This report therefore uses deterministic rules first, instead of an unsupervised "
                "embedding pass, so each cluster is directly auditable."
            ),
            "cvdp_alignment": (
                "CVDP clusters failed cases after LLM reflection and embeddings. "
                "For vaBench we keep the same goal, failure-family analysis, but use evaluator "
                "evidence as the primary signal. A future residual analysis can add sentence "
                "embeddings for B99/C99 rows or for deeper behavior subclusters."
            ),
        },
        "total_rows": len(rows),
        "pass_rows": len(rows) - len(failed_rows),
        "failed_rows": len(failed_rows),
        "axis_counts": dict(Counter(row["cluster_axis"] for row in clustered_rows)),
        "cluster_counts": dict(Counter(row["cluster_id"] for row in clustered_rows)),
        "status_counts_failures": dict(Counter(str(row.get("status", "")) for row in failed_rows)),
        "evas_status_counts_failures": dict(Counter(str(row.get("evas_status", "")) for row in failed_rows)),
        "primary_attribution_counts_failures": dict(
            Counter(str(row.get("primary_attribution", "")) for row in failed_rows)
        ),
        "cluster_summaries": cluster_summaries,
        "rows": clustered_rows,
    }


def format_top(items: list[dict[str, Any]]) -> str:
    return ", ".join(f"{item['name']} ({item['count']})" for item in items)


def write_summary_csv(path: Path, summaries: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        for row in summaries:
            out = row.copy()
            out["top_categories"] = format_top(row["top_categories"])
            out["top_forms"] = format_top(row["top_forms"])
            out["top_levels"] = format_top(row["top_levels"])
            writer.writerow({field: out.get(field, "") for field in SUMMARY_FIELDS})


def write_rows_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=ROW_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in ROW_FIELDS})


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# DeepSeek v4-pro vaBench Error Cluster Analysis",
        "",
        f"- Input report: `{report['input_report']}`",
        f"- Total rows: {report['total_rows']}",
        f"- Pass rows: {report['pass_rows']}",
        f"- Failed rows clustered: {report['failed_rows']}",
        f"- Axis counts: {json.dumps(report['axis_counts'], sort_keys=True)}",
        "",
        "## Cluster Summary",
        "",
        "| Cluster | Axis | Count | Share | Dominant category | Dominant form | Example |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in report["cluster_summaries"]:
        share = f"{100 * row['share_of_failures']:.1f}%"
        example = f"`{row['example_task']}`: {compact(row['example_evidence'], 120)}"
        lines.append(
            "| {cluster_id} {label} | {axis} | {count} | {share} | {category} | {form} | {example} |".format(
                cluster_id=row["cluster_id"],
                label=row["label"],
                axis=row["axis"],
                count=row["count"],
                share=share,
                category=row["dominant_category"],
                form=row["dominant_form"],
                example=example.replace("|", "\\|"),
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )
    for row in report["cluster_summaries"]:
        lines.extend(
            [
                f"### {row['cluster_id']} {row['label']}",
                "",
                f"- Count: {row['count']} ({100 * row['share_of_failures']:.1f}% of failures)",
                f"- Top categories: {format_top(row['top_categories'])}",
                f"- Top forms: {format_top(row['top_forms'])}",
                f"- Interpretation: {row['interpretation']}",
                f"- Recommended action: {row['recommended_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Notes",
            "",
            "- This is a deterministic, evidence-driven clustering pass over the current full236 overlay.",
            "- Pass rows are excluded from the cluster denominator.",
            "- Incomplete generations are counted as model failures under the fixed output budget, but are separated from Verilog-A syntax and circuit behavior failures.",
            "- No runner/evaluator inconclusive rows and no EVAS/Spectre parity-debt rows are present in this input report.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = load_json(DEFAULT_INPUT)
    report = build_report(data, DEFAULT_INPUT)
    write_json(OUT_JSON, report)
    write_summary_csv(OUT_CSV, report["cluster_summaries"])
    write_rows_csv(OUT_ROWS_CSV, report["rows"])
    write_markdown(OUT_MD, report)
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_ROWS_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
