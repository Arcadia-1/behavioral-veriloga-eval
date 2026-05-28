#!/usr/bin/env python3
"""Generate a failure-attribution table for the DeepSeek vaBench baseline.

This report intentionally separates model failures from benchmark/runner/EVAS
failures. The input candidates are the wrapper-v1 DeepSeek generations that
were rejudged by the current EVAS/Spectre dual runner, plus the v4 preflight
rerun for the propagation-delay comparator DUT row.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "benchmark-vabench-release-v1" / "reports"
FULL_RESULTS = (
    ROOT
    / "results"
    / "vabench-release-v1-baseline-dual-deepseek-v4-pro-20260528-wrapper-v3-samecandidates-full-rejudge"
    / "results"
)
PATCH_RESULT = (
    ROOT
    / "results"
    / "vabench-release-v1-baseline-dual-deepseek-v4-pro-20260528-wrapper-v4-samecandidates-propdelay-dut-preflight"
    / "results"
    / "vbr1_l1_propagation_delay_comparator_dut"
    / "result.json"
)
SCORE_MANIFEST = REPORTS / "score_denominator_manifest.json"

OUT_JSON = REPORTS / "deepseek_failure_attribution_20260528.json"
OUT_CSV = REPORTS / "deepseek_failure_attribution_20260528.csv"
OUT_FAILURE_CSV = REPORTS / "deepseek_failure_attribution_failures_20260528.csv"
OUT_INCONCLUSIVE_CSV = REPORTS / "deepseek_failure_attribution_inconclusive_20260528.csv"
OUT_INCONCLUSIVE_MD = REPORTS / "deepseek_failure_attribution_inconclusive_20260528.md"
OUT_MD = REPORTS / "deepseek_failure_attribution_20260528.md"


CSV_FIELDS = [
    "task_id",
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
    "spectre_checker_pass",
    "dual_pass",
    "is_clean_dual_failure",
    "primary_attribution",
    "secondary_attribution",
    "root_cause_family",
    "root_cause_detail",
    "attribution_confidence",
    "counts_as_direct_model_failure",
    "counts_as_model_spectre_pass",
    "evidence",
    "recommended_action",
    "source_result_json",
    "sample_dir",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_score_metadata() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    data = load_json(SCORE_MANIFEST)
    entry_rows = {row["release_entry_id"]: row for row in data.get("entry_rows", [])}
    form_rows = {row["task_id"]: row for row in data.get("form_rows", [])}
    return entry_rows, form_rows


def load_result_rows() -> dict[str, tuple[Path, dict[str, Any]]]:
    if not FULL_RESULTS.exists():
        raise FileNotFoundError(FULL_RESULTS)
    rows: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(FULL_RESULTS.glob("*/result.json")):
        data = load_json(path)
        rows[data["task_id"]] = (path, data)
    if PATCH_RESULT.exists():
        patched = load_json(PATCH_RESULT)
        rows[patched["task_id"]] = (PATCH_RESULT, patched)
    return rows


def flatten_text(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(flatten_text(item))
        return out
    if isinstance(value, dict):
        return [json.dumps(value, sort_keys=True)]
    return [str(value)]


def generation_meta(row: dict[str, Any]) -> dict[str, Any]:
    sample_dir = row.get("sample_dir")
    if not sample_dir:
        return {}
    path = ROOT / sample_dir / "generation_meta.json"
    if not path.exists():
        return {}
    try:
        return load_json(path)
    except json.JSONDecodeError:
        return {}


def combined_text(row: dict[str, Any], meta: dict[str, Any]) -> str:
    dual = row.get("dual_result") or {}
    evas = dual.get("evas") or {}
    spectre = dual.get("spectre") or {}
    chunks: list[str] = []
    for source in [
        row.get("error"),
        row.get("skip_reason"),
        row.get("stage"),
        evas.get("notes"),
        evas.get("stdout_tail"),
        spectre.get("errors"),
        spectre.get("stdout_tail"),
        spectre.get("behavior_notes"),
        meta,
    ]:
        chunks.extend(flatten_text(source))
    return "\n".join(chunks)


def first_matching_line(text: str, patterns: list[str]) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for pattern in patterns:
        needle = pattern.lower()
        for line in lines:
            if needle in line.lower():
                return compact(line)
    for line in lines:
        if line.lower().startswith(("error", "warning")):
            return compact(line)
    return compact(lines[0]) if lines else ""


def compact(text: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def behavior_note(row: dict[str, Any], text: str) -> str:
    dual = row.get("dual_result") or {}
    evas = dual.get("evas") or {}
    notes = [
        note
        for note in flatten_text(evas.get("notes"))
        if note and note != "returncode=0"
    ]
    if notes:
        return compact(" ; ".join(notes), 220)
    return first_matching_line(text, ["checker", "wrong", "missing", "span", "range"])


def parity_evidence(row: dict[str, Any]) -> str:
    parity = ((row.get("dual_result") or {}).get("parity") or {})
    parts = []
    for key in ["max_rmse_v", "max_abs_v", "mean_relative_rms_error", "max_relative_rms_error"]:
        if key in parity:
            value = parity[key]
            if isinstance(value, float):
                parts.append(f"{key}={value:.4g}")
            else:
                parts.append(f"{key}={value}")
    return compact(" ; ".join(parts) or json.dumps(parity, sort_keys=True), 220)


def classify(row: dict[str, Any], text: str, meta: dict[str, Any]) -> dict[str, Any]:
    classification = row.get("classification") or {}
    status = row.get("status") or "missing"
    dual_status = classification.get("dual_status") or (
        "missing" if status in {"SKIPPED", "ERROR"} else "unknown"
    )
    evas_status = classification.get("evas_status") or (
        "FAIL_INFRA" if status == "SKIPPED" else "missing"
    )
    spectre_checker_pass = bool(classification.get("spectre_checker_pass"))
    dual_pass = bool(classification.get("dual_pass") or dual_status == "PASS")
    lower = text.lower()

    result = {
        "primary_attribution": "needs_manual_review",
        "secondary_attribution": "",
        "root_cause_family": "unclassified",
        "root_cause_detail": "unclassified_failure",
        "attribution_confidence": "medium",
        "counts_as_direct_model_failure": False,
        "counts_as_model_spectre_pass": spectre_checker_pass,
        "evidence": first_matching_line(text, ["error", "fail", "missing"]),
        "recommended_action": "Manual triage before using this row in model-error claims.",
    }

    if dual_pass:
        result.update(
            primary_attribution="pass",
            root_cause_family="pass",
            root_cause_detail="clean_evas_spectre_dual_pass",
            attribution_confidence="high",
            counts_as_model_spectre_pass=True,
            evidence=behavior_note(row, text),
            recommended_action="No failure action.",
        )
        return result

    if dual_status == "FAIL_PARITY":
        detail = "waveform_parity_gate_failed"
        action = "Add or fix an EVAS core regression; do not treat this as model circuit failure."
        if "clocked_adc_quantizer" in row.get("release_entry_id", ""):
            detail = "evas_spectre_real_to_integer_cast_semantics"
        elif "digital_phase_accumulator" in row.get("release_entry_id", ""):
            detail = "evas_spectre_timer_zero_start_ordering"
        result.update(
            primary_attribution="evas_core_parity_debt",
            root_cause_family="evas_spectre_semantics",
            root_cause_detail=detail,
            attribution_confidence="high",
            counts_as_direct_model_failure=False,
            counts_as_model_spectre_pass=True,
            evidence=parity_evidence(row),
            recommended_action=action,
        )
        return result

    if status == "SKIPPED" or evas_status == "FAIL_INFRA":
        detail = "missing_candidate_files"
        evidence = row.get("skip_reason") or "missing_candidate_files"
        if meta.get("status") == "no_code_extracted":
            detail = "no_code_extracted_finish_reason_" + str(meta.get("finish_reason", "unknown"))
            evidence = f"generation_status={meta.get('status')} finish_reason={meta.get('finish_reason')}"
        elif meta:
            evidence = compact(json.dumps(meta, sort_keys=True))
        result.update(
            primary_attribution="runner_infra_extraction",
            root_cause_family="runner_or_api_artifact",
            root_cause_detail=detail,
            attribution_confidence="high",
            evidence=compact(evidence),
            recommended_action="Exclude from model-ability denominator and rerun generation/extraction with a token/output guard.",
        )
        return result

    if evas_status == "FAIL_SIM_CORRECTNESS":
        if any(token in lower for token in ["tran.csv missing", "zerodivisionerror", "keyerror", "traceback"]):
            result.update(
                primary_attribution="evaluator_runner_review",
                root_cause_family="simulation_output_missing",
                root_cause_detail="simulator_or_checker_crash_before_waveform",
                attribution_confidence="medium",
                evidence=first_matching_line(text, ["zerodivisionerror", "keyerror", "tran.csv missing", "traceback"]),
                recommended_action="Triage as EVAS/checker runner robustness before counting as model behavior failure.",
            )
        else:
            result.update(
                primary_attribution="model_behavior_failure",
                root_cause_family="behavior_checker_mismatch",
                root_cause_detail="compiled_and_ran_but_failed_hidden_behavior_checker",
                attribution_confidence="high",
                counts_as_direct_model_failure=True,
                evidence=behavior_note(row, text),
                recommended_action="Keep as model functional failure unless manual checker audit finds an oracle issue.",
            )
        return result

    if evas_status in {"FAIL_DUT_COMPILE", "FAIL_TB_COMPILE"}:
        is_pwl = "pwl" in lower or "invalid source" in lower
        is_missing_disc = "missing_disciplines_vams" in lower or (
            "cannot resolve discipline" in lower and "electrical" in lower
        )
        is_local_decl = "local declaration" in lower or "embedded declaration" in lower
        is_cond_cross = "conditional_cross" in lower or (
            "cross" in lower and "conditionally" in lower
        )
        is_cond_transition = "conditional_transition" in lower or (
            "transition" in lower and "condition" in lower
        )
        is_unbounded = "unsupported_unbounded_event_loop" in lower or "while(1)" in lower or "forever" in lower
        is_digital = "digital_verilog_syntax" in lower or "always @(" in lower
        is_dynamic_index = "dynamic_analog_vector_index" in lower
        is_missing_include = any(
            token in lower
            for token in ["cannot find va file", "undefined_module", "unknown subcircuit", "missing include"]
        )
        is_parse = "parse error" in lower or "expected assign" in lower

        if is_missing_disc:
            result.update(
                primary_attribution="prompt_contract_gap_old_wrapper",
                secondary_attribution="model_veriloga_subset_failure" if is_local_decl or is_cond_cross else "",
                root_cause_family="public_contract_missing_include",
                root_cause_detail="missing_disciplines_vams_in_old_wrapper_candidate",
                attribution_confidence="high",
                evidence=first_matching_line(text, ["missing_disciplines_vams", "cannot resolve discipline"]),
                recommended_action="Do not count as direct model ability failure for wrapper-v1 candidates; rerun under wrapper-v4 include rules.",
            )
            return result

        if is_pwl and not (is_local_decl or is_cond_cross or is_cond_transition):
            result.update(
                primary_attribution="prompt_contract_gap_old_wrapper",
                root_cause_family="spectre_scs_source_contract",
                root_cause_detail="invalid_or_incomplete_pwl_source_syntax",
                attribution_confidence="medium",
                evidence=first_matching_line(text, ["Invalid source", "PWL", "wave"]),
                recommended_action="Rerun with wrapper-v4 SCS/PWL scaffold before counting as a direct model failure.",
            )
            return result

        if is_missing_include and not (is_local_decl or is_cond_cross or is_cond_transition):
            result.update(
                primary_attribution="prompt_contract_gap_old_wrapper",
                root_cause_family="spectre_scs_harness_contract",
                root_cause_detail="missing_include_or_invalid_primitive_instance",
                attribution_confidence="medium",
                evidence=first_matching_line(text, ["Cannot find VA file", "undefined_module", "unknown subcircuit"]),
                recommended_action="Rerun with wrapper-v4 artifact/include and source-instance rules before counting as direct model failure.",
            )
            return result

        if is_local_decl or is_cond_cross or is_cond_transition or is_unbounded or is_digital or is_dynamic_index or is_parse:
            detail_parts = []
            if is_local_decl:
                detail_parts.append("local_declaration_inside_analog_or_procedural_block")
            if is_cond_cross:
                detail_parts.append("conditional_cross_operator")
            if is_cond_transition:
                detail_parts.append("conditional_transition_operator")
            if is_unbounded:
                detail_parts.append("unbounded_event_loop")
            if is_digital:
                detail_parts.append("digital_verilog_syntax_in_va")
            if is_dynamic_index:
                detail_parts.append("dynamic_analog_vector_index")
            if is_parse:
                detail_parts.append("spectre_veriloga_parse_error")
            result.update(
                primary_attribution="model_veriloga_subset_failure",
                secondary_attribution="prompt_contract_gap_old_wrapper" if is_pwl else "",
                root_cause_family="veriloga_spectre_subset_violation",
                root_cause_detail="+".join(detail_parts),
                attribution_confidence="high" if not is_pwl else "medium",
                counts_as_direct_model_failure=True,
                evidence=first_matching_line(
                    text,
                    [
                        "local declaration",
                        "embedded declaration",
                        "conditional_cross",
                        "conditional_transition",
                        "unsupported_unbounded_event_loop",
                        "digital_verilog_syntax",
                        "dynamic_analog_vector_index",
                        "Parse error",
                        "ERROR",
                    ],
                ),
                recommended_action="Count as syntax/subset model failure after wrapper-v4 contract; add focused prompt examples only as runner variants, not hidden checker leakage.",
            )
            return result

        result.update(
            primary_attribution="needs_manual_review",
            root_cause_family="compile_failure_unclassified",
            root_cause_detail=f"{evas_status.lower()}_without_specific_signature",
            attribution_confidence="low",
            evidence=first_matching_line(text, ["ERROR", "returncode=1", "tran.csv missing"]),
            recommended_action="Inspect staged candidate and simulator log before assigning to model or benchmark.",
        )
        return result

    result.update(
        evidence=first_matching_line(text, ["ERROR", "returncode", "missing"]),
        recommended_action="Manual triage required.",
    )
    return result


def enriched_rows() -> list[dict[str, Any]]:
    entry_meta, form_meta = load_score_metadata()
    rows = []
    for path, row in load_result_rows().values():
        release_task_id = row.get("release_task_id", "")
        release_entry_id = row.get("release_entry_id", "")
        form = row.get("form", "")
        form_info = form_meta.get(release_task_id, {})
        entry_info = entry_meta.get(release_entry_id, {})
        meta = generation_meta(row)
        text = combined_text(row, meta)
        classification = row.get("classification") or {}
        dual_status = classification.get("dual_status") or (
            "missing" if row.get("status") in {"SKIPPED", "ERROR"} else "unknown"
        )
        evas_status = classification.get("evas_status") or (
            "FAIL_INFRA" if row.get("status") == "SKIPPED" else "missing"
        )
        spectre_checker_pass = bool(classification.get("spectre_checker_pass"))
        dual_pass = bool(classification.get("dual_pass") or dual_status == "PASS")
        attribution = classify(row, text, meta)
        rows.append(
            {
                "task_id": row.get("task_id", ""),
                "release_task_id": release_task_id,
                "release_entry_id": release_entry_id,
                "form": form,
                "level": entry_info.get("level") or form_info.get("level") or infer_level(release_entry_id),
                "difficulty": row.get("difficulty") or entry_info.get("difficulty") or form_info.get("difficulty", ""),
                "track": entry_info.get("track") or form_info.get("track", ""),
                "category": row.get("category") or entry_info.get("category") or form_info.get("category", ""),
                "base_function": entry_info.get("base_function", ""),
                "status": row.get("status", ""),
                "dual_status": dual_status,
                "evas_status": evas_status,
                "spectre_checker_pass": spectre_checker_pass,
                "dual_pass": dual_pass,
                "is_clean_dual_failure": not dual_pass,
                "source_result_json": rel(path),
                "sample_dir": row.get("sample_dir", ""),
                **attribution,
            }
        )
    rows.sort(key=lambda item: (item["category"], item["release_entry_id"], item["form"], item["task_id"]))
    return rows


def infer_level(entry_id: str) -> str:
    if "_l2_" in entry_id:
        return "L2"
    if "_l1_" in entry_id or entry_id.startswith("vbm1_"):
        return "L1"
    return ""


def counter(rows: list[dict[str, Any]], key: str, *, failures_only: bool = False) -> Counter[str]:
    items = rows
    if failures_only:
        items = [row for row in rows if row["is_clean_dual_failure"]]
    return Counter(str(row.get(key, "")) for row in items)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in CSV_FIELDS})


def pct(count: int, total: int) -> str:
    return "0.00%" if total == 0 else f"{count / total:.2%}"


def md_table(headers: list[str], body: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def write_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    failures = [row for row in rows if row["is_clean_dual_failure"]]
    lines: list[str] = [
        "# DeepSeek Failure Attribution - 2026-05-28",
        "",
        "Scope: wrapper-v1 DeepSeek v4-pro candidates rejudged by the current EVAS/Spectre dual runner, with the propagation-delay comparator DUT row replaced by the wrapper-v4 preflight rerun.",
        "",
        "Interpretation rule: Spectre checker pass is the model score signal; EVAS/Spectre waveform parity debt is an EVAS-core issue; old wrapper include/PWL/scaffold gaps are not counted as direct model ability failures until a fresh wrapper-v4 generation is run.",
        "",
        "## Count Sanity",
        "",
    ]
    lines.extend(
        md_table(
            ["Metric", "Count", "Rate"],
            [
                ["Total scored forms", summary["total_rows"], "100.00%"],
                ["Clean dual pass", summary["dual_pass"], pct(summary["dual_pass"], summary["total_rows"])],
                ["Clean dual non-pass", summary["clean_dual_failures"], pct(summary["clean_dual_failures"], summary["total_rows"])],
                ["Spectre-final model pass", summary["spectre_final_pass"], pct(summary["spectre_final_pass"], summary["total_rows"])],
                ["EVAS parity debt among Spectre passes", summary["evas_core_parity_debt"], pct(summary["evas_core_parity_debt"], summary["total_rows"])],
            ],
        )
    )
    lines.extend(["", "## Attribution Summary", ""])
    attr_rows = []
    for key, count in summary["by_primary_attribution"].items():
        if key == "pass":
            continue
        attr_rows.append([f"`{key}`", count, pct(count, summary["clean_dual_failures"])])
    lines.extend(md_table(["Primary attribution", "Rows", "Share of clean-dual failures"], attr_rows))

    lines.extend(["", "## Root Cause Families", ""])
    root_rows = [
        [f"`{key}`", count, pct(count, summary["clean_dual_failures"])]
        for key, count in summary["by_root_cause_family_failures"].items()
    ]
    lines.extend(md_table(["Root cause family", "Rows", "Share of clean-dual failures"], root_rows))

    lines.extend(["", "## Model-Ability View", ""])
    lines.extend(
        md_table(
            ["Bucket", "Rows", "Meaning"],
            [
                [
                    "Direct model failures",
                    summary["direct_model_failures"],
                    "Behavior-check mismatches plus clear Verilog-A/Spectre subset violations.",
                ],
                [
                    "Spectre-final model passes",
                    summary["spectre_final_pass"],
                    "Includes two rows that still fail EVAS waveform parity.",
                ],
                [
                    "Inconclusive/non-model rows",
                    summary["inconclusive_or_non_model_rows"],
                    "Old prompt-contract gaps, extraction infra, or evaluator-review rows; parity-debt rows are already counted as Spectre-final passes.",
                ],
            ],
        )
    )

    lines.extend(["", "## Raw Evaluator Status", ""])
    raw_rows = [
        [f"`{key}`", count]
        for key, count in summary["by_evas_status"].items()
    ]
    lines.extend(md_table(["EVAS status", "Rows"], raw_rows))

    lines.extend(["", "## Failure Rows", ""])
    lines.append(
        "The CSV/JSON files contain the full audit columns. This Markdown table keeps the evidence field compact for review."
    )
    lines.append("")
    failure_rows = []
    for row in failures:
        failure_rows.append(
            [
                f"`{row['release_task_id']}`",
                f"`{row['form']}`",
                f"`{row['dual_status']}`",
                f"`{row['evas_status']}`",
                f"`{row['primary_attribution']}`",
                f"`{row['root_cause_detail']}`",
                compact(row["evidence"], 120).replace("|", "\\|"),
            ]
        )
    lines.extend(
        md_table(
            [
                "Release task",
                "Form",
                "Dual",
                "EVAS",
                "Attribution",
                "Root detail",
                "Evidence",
            ],
            failure_rows,
        )
    )
    lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n")


def write_inconclusive_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    inconclusive = [
        row
        for row in rows
        if not row["counts_as_model_spectre_pass"] and not row["counts_as_direct_model_failure"]
    ]
    lines: list[str] = [
        "# DeepSeek Inconclusive Rows - 2026-05-28",
        "",
        "Scope: the 60/236 rows that should not currently be counted as either Spectre-final model passes or direct model failures.",
        "",
        "Interpretation: these rows need a wrapper-v4 regeneration/rerun or runner/evaluator triage before they are used as model-capability evidence.",
        "",
        "## Breakdown",
        "",
    ]
    rows_by_attr = Counter(row["primary_attribution"] for row in inconclusive)
    rows_by_root = Counter(row["root_cause_detail"] for row in inconclusive)
    lines.extend(
        md_table(
            ["Primary attribution", "Rows"],
            [[f"`{key}`", value] for key, value in rows_by_attr.most_common()],
        )
    )
    lines.extend(["", "## Root Details", ""])
    lines.extend(
        md_table(
            ["Root detail", "Rows"],
            [[f"`{key}`", value] for key, value in rows_by_root.most_common()],
        )
    )
    lines.extend(["", "## Rows", ""])
    body = []
    for row in inconclusive:
        body.append(
            [
                f"`{row['release_task_id']}`",
                f"`{row['form']}`",
                row["category"],
                f"`{row['primary_attribution']}`",
                f"`{row['root_cause_detail']}`",
                compact(row["evidence"], 140).replace("|", "\\|"),
            ]
        )
    lines.extend(
        md_table(
            ["Release task", "Form", "Category", "Attribution", "Root detail", "Evidence"],
            body,
        )
    )
    lines.append("")
    OUT_INCONCLUSIVE_MD.write_text("\n".join(lines) + "\n")


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    failures = [row for row in rows if row["is_clean_dual_failure"]]
    by_attr = counter(rows, "primary_attribution")
    by_attr_failures = counter(rows, "primary_attribution", failures_only=True)
    by_root_failures = counter(rows, "root_cause_family", failures_only=True)
    by_evas = counter(rows, "evas_status")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_full_results": rel(FULL_RESULTS.parent),
        "source_patch_result": rel(PATCH_RESULT) if PATCH_RESULT.exists() else "",
        "total_rows": total,
        "clean_dual_failures": len(failures),
        "dual_pass": sum(1 for row in rows if row["dual_pass"]),
        "spectre_final_pass": sum(1 for row in rows if row["counts_as_model_spectre_pass"]),
        "direct_model_failures": sum(1 for row in rows if row["counts_as_direct_model_failure"]),
        "not_direct_model_dual_failures": sum(
            1
            for row in rows
            if row["is_clean_dual_failure"] and not row["counts_as_direct_model_failure"]
        ),
        "inconclusive_or_non_model_rows": sum(
            1
            for row in rows
            if not row["counts_as_model_spectre_pass"] and not row["counts_as_direct_model_failure"]
        ),
        "evas_core_parity_debt": by_attr.get("evas_core_parity_debt", 0),
        "by_primary_attribution": dict(by_attr),
        "by_primary_attribution_failures": dict(by_attr_failures),
        "by_root_cause_family_failures": dict(by_root_failures),
        "by_evas_status": dict(by_evas),
        "by_form_failures": dict(counter(failures, "form")),
        "by_category_failures": dict(counter(failures, "category")),
    }


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = enriched_rows()
    summary = build_summary(rows)
    payload = {
        "report": "deepseek_failure_attribution_20260528",
        "summary": summary,
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    write_csv(OUT_CSV, rows)
    write_csv(OUT_FAILURE_CSV, [row for row in rows if row["is_clean_dual_failure"]])
    write_csv(
        OUT_INCONCLUSIVE_CSV,
        [
            row
            for row in rows
            if not row["counts_as_model_spectre_pass"] and not row["counts_as_direct_model_failure"]
        ],
    )
    write_markdown(rows, summary)
    write_inconclusive_markdown(rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
