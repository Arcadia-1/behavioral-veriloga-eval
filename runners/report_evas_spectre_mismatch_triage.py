#!/usr/bin/env python3
"""Triage EVAS/Spectre dual-run results into actionable parity families.

This report is intentionally evaluator-facing. It separates model failures from
runner/staging issues and EVAS/Spectre semantic mismatches, then points any
simulator mismatch toward a minimal L0 conformance fixture.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "benchmark-vabench-release-v1" / "reports"

AXIS_DESCRIPTIONS = {
    "pass": "Strict EVAS+Spectre pass.",
    "generation": "The model did not produce a complete usable artifact.",
    "runner": "Evaluation infrastructure, staging, or external backend did not produce a reliable judgment.",
    "evas_spectre_mismatch": "EVAS and Spectre disagree on the same candidate; reduce to L0 conformance.",
    "parity": "Both sides may pass behavior, but waveform parity needs a conformance/checker-window audit.",
    "model_dut_compile": "EVAS/static front-end rejected the generated Verilog-A DUT.",
    "model_tb_compile": "EVAS/static front-end rejected the generated Spectre testbench.",
    "model_spectre_ahdl_compile": "Spectre final judge rejected generated Verilog-A syntax/scope/operator usage.",
    "model_spectre_tb_source": "Spectre final judge rejected generated testbench source/waveform syntax.",
    "model_spectre_elab_or_topology": "Spectre final judge rejected parameter binding, range, or topology.",
    "simulation_output_missing": "The run did not materialize required waveform artifacts such as tran.csv.",
    "model_behavior": "The candidate compiled and ran but failed the functional checker.",
}

NON_MODEL_OR_INCONCLUSIVE_AXES = {"generation", "runner", "simulation_output_missing"}
BEHAVIOR_READY_AXES = {"pass", "model_behavior"}

ROW_FIELDS = [
    "source",
    "result_json",
    "task_id",
    "release_task_id",
    "release_entry_id",
    "form",
    "category",
    "difficulty",
    "status",
    "dual_status",
    "evas_status",
    "spectre_status",
    "spectre_checker_pass",
    "dual_pass",
    "evas_pass_spectre_fail",
    "spectre_pass_evas_fail",
    "triage_axis",
    "root_cause_family",
    "root_cause_detail",
    "recommended_action",
    "conformance_seed_suggestion",
    "evidence",
    "sample_dir",
    "staged_dut",
    "staged_tb",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def compact(value: Any, limit: int = 240) -> str:
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


def has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def first_evidence_line(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if not stripped:
            continue
        if lower in {"returncode=0", "success", "error"}:
            continue
        if "evas completes with 0 errors" in lower:
            continue
        if "vacomp-2435" in lower or "cds_ahdlcmi_enable" in lower:
            continue
        if "no longer supported" in lower and "compiled c code flow" in lower:
            continue
        lines.append(stripped)
    priority = [
        "error (vacomp",
        "fatal (vacomp",
        "error (cmi",
        "fatal (cmi",
        "error (sfe",
        "fatal (sfe",
        "fatal (asl",
        "falls below lower bound",
        "rigid branches",
        "unknown parameter",
        "from range",
        "vacomp-",
        "cmi-",
        "sfe-",
        "asl-",
        "fatal",
        "spectre_failed",
        "undeclared identifier",
        "syntax error",
        "waveform type",
        "pwl waveform",
        "bit source pattern",
        "keyerror",
        "typeerror",
        "tran.csv missing",
        "no_code_extracted",
        "finish_reason",
        "hold_missing",
        "not_",
        "too_low",
        "max_rmse",
        "max_abs",
        "checker",
        "mismatch",
        "fail",
        "error",
        "cross",
        "timer",
        "transition",
    ]
    for needle in priority:
        for line in lines:
            if needle in line.lower():
                return compact(line)
    return compact(lines[0]) if lines else ""


def result_files_for_input(path: Path) -> tuple[str, list[Path]]:
    if path.is_file():
        if path.name == "result.json":
            return path.parent.name, [path]
        if path.name == "summary.json":
            result_dir = path.parent / "results"
            if result_dir.is_dir():
                return path.parent.name, sorted(result_dir.glob("*/result.json"))
        raise FileNotFoundError(f"unsupported input file: {path}")

    if (path / "results").is_dir():
        return path.name, sorted((path / "results").glob("*/result.json"))

    direct = sorted(path.glob("*/result.json"))
    if direct:
        source = path.parent.name if path.name == "results" else path.name
        return source, direct

    raise FileNotFoundError(f"no result.json files found under {path}")


def combined_text(row: dict[str, Any]) -> str:
    dual = row.get("dual_result") or {}
    evas = dual.get("evas") or {}
    spectre = dual.get("spectre") or {}
    parity = dual.get("parity") or {}
    chunks: list[str] = []
    for source in [
        row.get("error"),
        row.get("skip_reason"),
        row.get("incomplete_reason"),
        row.get("generation_status"),
        row.get("generation_finish_reason"),
        row.get("stage"),
        dual.get("notes"),
        evas.get("status"),
        evas.get("notes"),
        evas.get("stdout_tail"),
        spectre.get("status"),
        spectre.get("errors"),
        spectre.get("warnings"),
        spectre.get("behavior_notes"),
        spectre.get("stdout_tail"),
        parity,
    ]:
        chunks.extend(flatten_text(source))
    return "\n".join(chunks)


def spectre_checker_pass(row: dict[str, Any]) -> bool:
    classification = row.get("classification") or {}
    if "spectre_checker_pass" in classification:
        return bool(classification["spectre_checker_pass"])
    spectre = ((row.get("dual_result") or {}).get("spectre") or {})
    return bool(spectre.get("ok")) and float(spectre.get("behavior_score") or 0.0) >= 1.0


def row_statuses(row: dict[str, Any]) -> dict[str, Any]:
    classification = row.get("classification") or {}
    dual = row.get("dual_result") or {}
    evas = dual.get("evas") or {}
    spectre = dual.get("spectre") or {}

    evas_status = classification.get("evas_status") or evas.get("status") or row.get("baseline_evas_status") or "missing"
    dual_status = classification.get("dual_status") or dual.get("status") or "missing"
    spectre_status = spectre.get("status") or "missing"
    spass = spectre_checker_pass(row)
    evas_pass = evas_status == "PASS"
    dual_pass = bool(classification.get("dual_pass")) or dual_status == "PASS"
    backend_inconclusive = bool(classification.get("spectre_backend_inconclusive"))

    return {
        "status": row.get("status") or "missing",
        "dual_status": dual_status,
        "evas_status": evas_status,
        "spectre_status": spectre_status,
        "spectre_checker_pass": spass,
        "dual_pass": dual_pass,
        "spectre_backend_inconclusive": backend_inconclusive,
        "evas_pass_spectre_fail": (
            not backend_inconclusive
            and (bool(classification.get("evas_pass_spectre_fail")) or (evas_pass and not spass))
        ),
        "spectre_pass_evas_fail": bool(classification.get("spectre_pass_evas_fail")) or (spass and not evas_pass),
    }


def compile_family(text: str, evas_status: str) -> str:
    if missing_output_without_compile_signal(text):
        return "simulation_output_missing_after_run"
    if "local declaration" in text or "embedded declaration" in text:
        return "veriloga_embedded_declaration"
    if "transition" in text and ("conditional" in text or "inside" in text):
        return "guarded_transition_contribution"
    if "restricted operator" in text or "cross inside" in text:
        return "restricted_analog_operator_placement"
    if has_any(text, ["round(", "$itor", "log10(", "fabs("]):
        return "unsupported_math_or_cast_function"
    if has_any(text, ["event ", "event\t", "wait("]):
        return "unsupported_event_variable_or_wait"
    if "unsupported_unbounded_event_loop" in text or "unbounded event loop" in text:
        return "unsupported_event_loop_form"
    if has_any(text, ["always @", "posedge", "negedge", "reg ", "assign "]):
        return "digital_verilog_in_veriloga"
    if evas_status == "FAIL_TB_COMPILE" or has_any(text, ["failed to parse tb_", "spectre tb syntax", "unknown source"]):
        return "spectre_testbench_syntax"
    return "other_compile_failure"


def missing_output_without_compile_signal(text: str) -> bool:
    if "tran.csv missing" not in text and "simulation output missing" not in text:
        return False
    return not has_any(
        text,
        [
            "vacomp-",
            "cmi-",
            "sfe-",
            "asl-",
            "failed to compile",
            "failed to parse",
            "parse error",
            "syntax error",
            "fatal error found by spectre",
        ],
    )


def spectre_error_family(text: str) -> dict[str, str]:
    """Classify Spectre final-judge errors without calling them backend debt."""
    signal_text = "\n".join(
        line
        for line in text.splitlines()
        if "vacomp-2435" not in line
        and "cds_ahdlcmi_enable" not in line
        and "compiled c code flow" not in line
    )
    if has_any(
        signal_text,
        [
            "license checkout",
            "license check out",
            "license checkout failed",
            "failed to check out",
            "no license",
            "license server down",
            "sui_direct_timeout_after_s",
            "connection timed out during banner exchange",
            "connection closed by unknown",
            "remote_workdir_create_failed",
            "remote_workdir_unresolved",
        ],
    ):
        return {
            "triage_axis": "runner",
            "root_cause_family": "spectre_license_or_backend_unavailable",
            "root_cause_detail": "Spectre could not be run reliably because the execution backend or license was unavailable.",
            "recommended_action": "Rerun after backend/license recovery; do not assign model capability until Spectre produces a judgment.",
        }

    if has_any(
        signal_text,
        [
            "cmi-2194",
            "cmi-2204",
            "cmi-2212",
            "waveform type must be specified",
            "pwl waveform",
            "bit source pattern",
            "parameter `type': `sin'",
            "type' is invalid value",
        ],
    ):
        return {
            "triage_axis": "model_spectre_tb_source",
            "root_cause_family": "spectre_tb_source_or_waveform_reject",
            "root_cause_detail": "Spectre rejected the generated testbench/source deck before behavior could be judged.",
            "recommended_action": "Count as model TB/Spectre-deck failure; inspect prompt only if the public TB contract omitted required source syntax.",
        }

    if has_any(
        signal_text,
        [
            "vacomp-",
            "error found by spectre during ahdl read-in",
            "error found by spectre during ahdl compilation",
            "exiting ahdl compilation",
            "undeclared identifier",
            "reserved name",
            "syntax error",
            "illegal value for direction",
            "cross statement",
        ],
    ):
        return {
            "triage_axis": "model_spectre_ahdl_compile",
            "root_cause_family": "spectre_ahdl_syntax_scope_or_operator_reject",
            "root_cause_detail": "Spectre rejected the generated Verilog-A syntax, scoping, parameter usage, or analog-operator form.",
            "recommended_action": "Count as model Spectre-compatible Verilog-A failure; consider EVAS preflight hardening only as a diagnostic improvement.",
        }

    if has_any(
        signal_text,
        [
            "sfe-1997",
            "rigid branches",
            "topology check",
            "unknown parameter",
            "falls below lower bound",
            "from range limit",
        ],
    ):
        return {
            "triage_axis": "model_spectre_elab_or_topology",
            "root_cause_family": "spectre_elaboration_parameter_or_topology_reject",
            "root_cause_detail": "Spectre rejected the candidate during elaboration, parameter binding, range checking, or topology checks.",
            "recommended_action": "Count as model integration/netlist failure; audit harness only if the staged gold parameters differ from the public contract.",
        }

    return {
        "triage_axis": "runner",
        "root_cause_family": "spectre_run_inconclusive",
        "root_cause_detail": "Spectre returned an error that the triage script cannot yet attribute to model code, testbench code, or infrastructure.",
        "recommended_action": "Inspect the Spectre log, add a taxonomy rule if it is a model-side failure, then rerun the report.",
    }


def behavior_family(row: dict[str, Any], text: str) -> str:
    category = str(row.get("category", "")).lower()
    task = f"{row.get('release_task_id', '')} {row.get('release_entry_id', '')}".lower()
    combined = f"{task} {category} {text}"

    if "data converter" in category:
        return "converter_code_or_transfer_behavior"
    if "comparator" in category or "decision" in category:
        return "decision_threshold_behavior"
    if "sampling" in category or "analog memory" in category:
        return "sample_hold_memory_behavior"
    if "baseband" in category:
        return "baseband_dynamic_behavior"
    if "pll" in category or "clock" in category or "timing" in category:
        return "timing_or_pll_behavior"
    if "calibration" in category or "dem" in category or "control" in category:
        return "calibration_control_behavior"
    if "bias" in category or "reference" in category or "power" in category:
        return "reference_power_behavior"
    if "rf" in category or "afe" in category:
        return "rf_afe_macro_behavior"

    if has_any(combined, ["sample", "hold", "droop", "aperture", "track"]):
        return "sample_hold_memory_behavior"
    if has_any(combined, ["comparator", "threshold", "window", "hysteresis", "offset"]):
        return "decision_threshold_behavior"
    if has_any(combined, ["adc", "dac", "code", "quant", "residue", "sar", "flash"]):
        return "converter_code_or_transfer_behavior"
    if has_any(combined, ["pll", "vco", "phase", "divider", "clock", "timer", "lock"]):
        return "timing_or_pll_behavior"
    if has_any(combined, ["calibration", "trim", "dem", "deadband", "dwa", "controller"]):
        return "calibration_control_behavior"
    if has_any(combined, ["filter", "gain", "limiter", "slew", "integrator", "rectifier"]):
        return "baseband_dynamic_behavior"
    if has_any(combined, ["bandgap", "bias", "ldo", "por", "brownout", "uvlo", "reference"]):
        return "reference_power_behavior"
    if has_any(combined, ["rf", "mixer", "lna", "pa", "rssi", "iq", "agc"]):
        return "rf_afe_macro_behavior"
    return "other_behavior_failure"


def mismatch_family(statuses: dict[str, Any], text: str) -> str:
    if statuses["spectre_pass_evas_fail"]:
        if statuses["evas_status"].startswith("FAIL_DUT_COMPILE"):
            return "evas_rejects_spectre_accepted_dut"
        if statuses["evas_status"].startswith("FAIL_TB_COMPILE"):
            return "evas_rejects_spectre_accepted_tb"
        return "spectre_pass_evas_fail_behavior"

    if statuses["evas_pass_spectre_fail"]:
        if statuses["spectre_status"] == "error" or "spectre_failed" in text:
            return "spectre_rejects_evas_accepted_candidate"
        if has_any(text, ["cross", "threshold", "timer", "event", "sample", "hold", "transition", "brownout"]):
            return "event_or_sampling_semantics"
        return "evas_pass_spectre_fail_behavior"

    if "status" in text and "failed" in text and has_any(text, ["rmse", "max_abs", "waveform", "relative_rms"]):
        return "waveform_parity_gate"
    return "unclassified_mismatch"


def conformance_seed_suggestion(family: str, row: dict[str, Any]) -> str:
    entry = str(row.get("release_entry_id") or row.get("task_id") or "row")
    if family in {
        "evas_rejects_spectre_accepted_dut",
        "evas_rejects_spectre_accepted_tb",
        "spectre_rejects_evas_accepted_candidate",
    }:
        return f"minimize {entry} into L0 syntax/dialect conformance"
    if family in {"event_or_sampling_semantics", "spectre_pass_evas_fail_behavior"}:
        return f"minimize {entry} into L0 event-sampling conformance"
    if family == "waveform_parity_gate":
        return f"minimize {entry} into L0 waveform/checker-window conformance"
    if "file" in family:
        return f"minimize {entry} into L0 file-IO conformance"
    return ""


def classify_row(row: dict[str, Any]) -> dict[str, str]:
    statuses = row_statuses(row)
    text = combined_text(row)
    lower = text.lower()
    evidence = first_evidence_line(text)

    if row.get("status") == "INCOMPLETE" or row.get("generation_status") == "no_code_extracted":
        return {
            "triage_axis": "generation",
            "root_cause_family": "incomplete_generation",
            "root_cause_detail": "No usable candidate artifact was extracted under the fixed model output budget.",
            "recommended_action": "Mark as incomplete generation; do not treat as EVAS/Spectre semantic debt.",
            "conformance_seed_suggestion": "",
            "evidence": evidence or "generation_status=no_code_extracted",
        }

    if row.get("status") in {"ERROR", "SKIPPED"} or has_any(lower, ["staging", "missing artifact", "artifact missing"]):
        return {
            "triage_axis": "runner",
            "root_cause_family": "runner_or_staging_inconclusive",
            "root_cause_detail": "The evaluation pipeline did not produce a reliable dual-run judgment.",
            "recommended_action": "Fix staging/runner artifact selection, then rerun before assigning model capability.",
            "conformance_seed_suggestion": "",
            "evidence": evidence,
        }

    if statuses.get("spectre_backend_inconclusive"):
        spectre_error = spectre_error_family(lower)
        return {
            "triage_axis": spectre_error["triage_axis"],
            "root_cause_family": spectre_error["root_cause_family"],
            "root_cause_detail": spectre_error["root_cause_detail"],
            "recommended_action": spectre_error["recommended_action"],
            "conformance_seed_suggestion": "",
            "evidence": evidence,
        }

    if statuses["evas_pass_spectre_fail"] or statuses["spectre_pass_evas_fail"]:
        family = mismatch_family(statuses, lower)
        return {
            "triage_axis": "evas_spectre_mismatch",
            "root_cause_family": family,
            "root_cause_detail": "EVAS and Spectre disagree on the same candidate row.",
            "recommended_action": "Reduce to a minimal L0 conformance fixture, add an EVAS regression, then rerun affected benchmark rows.",
            "conformance_seed_suggestion": conformance_seed_suggestion(family, row),
            "evidence": evidence,
        }

    dual = row.get("dual_result") or {}
    parity = dual.get("parity") or {}
    if statuses["dual_pass"]:
        return {
            "triage_axis": "pass",
            "root_cause_family": "strict_dual_pass",
            "root_cause_detail": "EVAS and Spectre both satisfy the row contract.",
            "recommended_action": "No action.",
            "conformance_seed_suggestion": "",
            "evidence": evidence,
        }

    if parity.get("status") == "failed" or statuses["dual_status"] == "FAIL_PARITY":
        family = "waveform_parity_gate"
        return {
            "triage_axis": "parity",
            "root_cause_family": family,
            "root_cause_detail": "Behavior may pass, but waveform-level parity failed or is too close to the checker boundary.",
            "recommended_action": "Inspect checker windows and waveform metrics; if simulator semantics differ, create an L0 conformance fixture.",
            "conformance_seed_suggestion": conformance_seed_suggestion(family, row),
            "evidence": evidence,
        }

    if missing_output_without_compile_signal(lower):
        return {
            "triage_axis": "simulation_output_missing",
            "root_cause_family": "simulation_output_missing_after_run",
            "root_cause_detail": "The evaluator did not find required waveform output, so behavior could not be judged from this run.",
            "recommended_action": "Inspect the run log to separate model runtime failure from runner artifact collection; rerun if the simulator completed.",
            "conformance_seed_suggestion": "",
            "evidence": evidence,
        }

    evas_status = str(statuses["evas_status"])
    if evas_status in {"FAIL_DUT_COMPILE", "FAIL_TB_COMPILE"}:
        family = compile_family(lower, evas_status)
        axis = "model_dut_compile" if evas_status == "FAIL_DUT_COMPILE" else "model_tb_compile"
        return {
            "triage_axis": axis,
            "root_cause_family": family,
            "root_cause_detail": "The candidate failed the Spectre-compatible Verilog-A/testbench subset before behavior could be judged.",
            "recommended_action": "Count as model syntax/subset failure unless Spectre accepts the same row.",
            "conformance_seed_suggestion": "",
            "evidence": evidence,
        }

    if statuses["spectre_status"] == "error":
        spectre_error = spectre_error_family(lower)
        return {
            "triage_axis": spectre_error["triage_axis"],
            "root_cause_family": spectre_error["root_cause_family"],
            "root_cause_detail": spectre_error["root_cause_detail"],
            "recommended_action": spectre_error["recommended_action"],
            "conformance_seed_suggestion": "",
            "evidence": evidence,
        }

    family = behavior_family(row, lower)
    return {
        "triage_axis": "model_behavior",
        "root_cause_family": family,
        "root_cause_detail": "The candidate compiled but missed the row's functional checker contract.",
        "recommended_action": "Use checker evidence for model error analysis; audit prompt only if the observable contract was underspecified.",
        "conformance_seed_suggestion": "",
        "evidence": evidence,
    }


def row_record(source: str, path: Path, row: dict[str, Any]) -> dict[str, Any]:
    statuses = row_statuses(row)
    triage = classify_row(row)
    stage = row.get("stage") if isinstance(row.get("stage"), dict) else {}
    record = {
        "source": source,
        "result_json": rel(path),
        "task_id": row.get("task_id", path.parent.name),
        "release_task_id": row.get("release_task_id", ""),
        "release_entry_id": row.get("release_entry_id", ""),
        "form": row.get("form", ""),
        "category": row.get("category", ""),
        "difficulty": row.get("difficulty", ""),
        "sample_dir": row.get("sample_dir", ""),
        "staged_dut": stage.get("staged_dut", ""),
        "staged_tb": stage.get("staged_tb", ""),
    }
    record.update(statuses)
    record.update(triage)
    return record


def load_records(inputs: list[Path], *, dedupe_by_task: bool = False) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in inputs:
        source, result_paths = result_files_for_input(path)
        for result_path in result_paths:
            records.append(row_record(source, result_path, load_json(result_path)))

    if not dedupe_by_task:
        return records

    by_task: dict[str, dict[str, Any]] = {}
    for record in records:
        by_task[str(record["task_id"])] = record
    return list(by_task.values())


def family_summaries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    family_counts = Counter(row["root_cause_family"] for row in rows)
    out: list[dict[str, Any]] = []
    for family, count in family_counts.most_common():
        examples = [row for row in rows if row["root_cause_family"] == family]
        form_counts = Counter(str(row["form"]) for row in examples if row.get("form"))
        category_counts = Counter(str(row["category"]) for row in examples if row.get("category"))
        out.append(
            {
                "root_cause_family": family,
                "count": count,
                "triage_axis": examples[0]["triage_axis"],
                "dominant_form": form_counts.most_common(1)[0][0] if form_counts else "",
                "dominant_category": category_counts.most_common(1)[0][0] if category_counts else "",
                "example_task_id": examples[0]["task_id"],
                "example_evidence": examples[0]["evidence"],
            }
        )
    return out


def percent(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(100.0 * numerator / denominator, 2)


def row_in_valid_candidate_slice(row: dict[str, Any]) -> bool:
    return str(row.get("triage_axis", "")) not in NON_MODEL_OR_INCONCLUSIVE_AXES


def row_in_behavior_ready_slice(row: dict[str, Any]) -> bool:
    return str(row.get("triage_axis", "")) in BEHAVIOR_READY_AXES


def score_slice_summary(rows: list[dict[str, Any]], name: str, description: str) -> dict[str, Any]:
    pass_rows = sum(1 for row in rows if row["dual_pass"])
    return {
        "slice": name,
        "description": description,
        "total_rows": len(rows),
        "strict_dual_pass_rows": pass_rows,
        "strict_dual_pass_rate_pct": percent(pass_rows, len(rows)),
        "non_pass_rows": len(rows) - pass_rows,
    }


def score_slices(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_rows = [row for row in rows if row_in_valid_candidate_slice(row)]
    behavior_rows = [row for row in rows if row_in_behavior_ready_slice(row)]
    return [
        score_slice_summary(
            rows,
            "full_strict",
            "All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures.",
        ),
        score_slice_summary(
            valid_rows,
            "valid_candidate",
            "Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failures remain model failures.",
        ),
        score_slice_summary(
            behavior_rows,
            "behavior_ready",
            "Rows that reached the functional checker: strict dual pass plus model_behavior failure rows.",
        ),
    ]


def group_breakdown(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    values = sorted({str(row.get(key, "") or "unknown") for row in rows})
    out: list[dict[str, Any]] = []
    for value in values:
        group = [row for row in rows if str(row.get(key, "") or "unknown") == value]
        valid = [row for row in group if row_in_valid_candidate_slice(row)]
        behavior_ready = [row for row in group if row_in_behavior_ready_slice(row)]
        pass_rows = sum(1 for row in group if row["dual_pass"])
        behavior_pass_rows = sum(1 for row in behavior_ready if row["dual_pass"])
        out.append(
            {
                key: value,
                "total_rows": len(group),
                "strict_dual_pass_rows": pass_rows,
                "strict_dual_pass_rate_pct": percent(pass_rows, len(group)),
                "valid_candidate_rows": len(valid),
                "behavior_ready_rows": len(behavior_ready),
                "behavior_ready_pass_rows": behavior_pass_rows,
                "behavior_ready_pass_rate_pct": percent(behavior_pass_rows, len(behavior_ready)),
                "non_model_or_inconclusive_rows": len(group) - len(valid),
            }
        )
    return out


def build_report(inputs: list[Path], *, dedupe_by_task: bool = False) -> dict[str, Any]:
    rows = load_records(inputs, dedupe_by_task=dedupe_by_task)
    axis_counts = Counter(row["triage_axis"] for row in rows)
    dual_status_counts = Counter(row["dual_status"] for row in rows)
    evas_status_counts = Counter(row["evas_status"] for row in rows)
    mismatch_rows = [
        row
        for row in rows
        if row["triage_axis"] == "evas_spectre_mismatch" or row["triage_axis"] == "parity"
    ]
    conformance_seed_rows = [
        row
        for row in mismatch_rows
        if row.get("conformance_seed_suggestion")
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inputs": [rel(path) for path in inputs],
        "dedupe_by_task": dedupe_by_task,
        "total_rows": len(rows),
        "strict_dual_pass_rows": sum(1 for row in rows if row["dual_pass"]),
        "spectre_checker_pass_rows": sum(1 for row in rows if row["spectre_checker_pass"]),
        "evas_pass_spectre_fail_rows": sum(1 for row in rows if row["evas_pass_spectre_fail"]),
        "spectre_pass_evas_fail_rows": sum(1 for row in rows if row["spectre_pass_evas_fail"]),
        "parity_gate_rows": sum(1 for row in rows if row["triage_axis"] == "parity"),
        "incomplete_generation_rows": sum(1 for row in rows if row["root_cause_family"] == "incomplete_generation"),
        "runner_inconclusive_rows": sum(1 for row in rows if row["triage_axis"] == "runner"),
        "axis_counts": dict(sorted(axis_counts.items())),
        "axis_descriptions": {
            axis: AXIS_DESCRIPTIONS.get(axis, "")
            for axis in sorted(axis_counts)
        },
        "dual_status_counts": dict(sorted(dual_status_counts.items())),
        "evas_status_counts": dict(sorted(evas_status_counts.items())),
        "score_slices": score_slices(rows),
        "breakdowns": {
            "difficulty": group_breakdown(rows, "difficulty"),
            "form": group_breakdown(rows, "form"),
            "category": group_breakdown(rows, "category"),
        },
        "family_summaries": family_summaries(rows),
        "mismatch_rows": mismatch_rows,
        "conformance_seed_rows": conformance_seed_rows,
        "rows": rows,
        "notes": [
            "Spectre remains the final benchmark judge.",
            "Rows with EVAS/Spectre disagreement should become L0 conformance fixtures before being used as model-capability evidence.",
            "Rows where Spectre rejects candidate Verilog-A, source syntax, parameters, or topology are model compatibility failures unless evidence points to runner/license failure.",
            "Report full_strict, valid_candidate, and behavior_ready slices separately so protocol noise is not confused with circuit-behavior ability.",
            "L0 conformance fixtures remain outside scored L1/L2 vaBench denominators.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ROW_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in ROW_FIELDS})


def md_table_row(values: list[Any]) -> str:
    return "| " + " | ".join(compact(value, 100).replace("|", "\\|") for value in values) + " |"


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# EVAS/Spectre Mismatch Triage",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "This report separates model failures, runner inconclusive rows, and",
        "EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics",
        "and are not part of the scored vaBench denominator.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| total rows | {report['total_rows']} |",
        f"| strict dual pass rows | {report['strict_dual_pass_rows']} |",
        f"| Spectre checker pass rows | {report['spectre_checker_pass_rows']} |",
        f"| EVAS PASS / Spectre FAIL rows | {report['evas_pass_spectre_fail_rows']} |",
        f"| Spectre PASS / EVAS FAIL rows | {report['spectre_pass_evas_fail_rows']} |",
        f"| parity gate rows | {report['parity_gate_rows']} |",
        f"| incomplete generation rows | {report['incomplete_generation_rows']} |",
        f"| runner inconclusive rows | {report['runner_inconclusive_rows']} |",
        "",
        "## Score Slices",
        "",
        "| Slice | Rows | Strict dual pass | Pass rate | Meaning |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for item in report.get("score_slices", []):
        lines.append(
            md_table_row(
                [
                    f"`{item['slice']}`",
                    item["total_rows"],
                    item["strict_dual_pass_rows"],
                    f"{item['strict_dual_pass_rate_pct']:.2f}%",
                    item["description"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Difficulty Breakdown",
            "",
            "| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in report.get("breakdowns", {}).get("difficulty", []):
        lines.append(
            md_table_row(
                [
                    f"`{item['difficulty']}`",
                    item["total_rows"],
                    item["strict_dual_pass_rows"],
                    f"{item['strict_dual_pass_rate_pct']:.2f}%",
                    item["valid_candidate_rows"],
                    item["behavior_ready_rows"],
                    f"{item['behavior_ready_pass_rate_pct']:.2f}%",
                    item["non_model_or_inconclusive_rows"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Form Breakdown",
            "",
            "| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in report.get("breakdowns", {}).get("form", []):
        lines.append(
            md_table_row(
                [
                    f"`{item['form']}`",
                    item["total_rows"],
                    item["strict_dual_pass_rows"],
                    f"{item['strict_dual_pass_rate_pct']:.2f}%",
                    item["valid_candidate_rows"],
                    item["behavior_ready_rows"],
                    f"{item['behavior_ready_pass_rate_pct']:.2f}%",
                    item["non_model_or_inconclusive_rows"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Category Breakdown",
            "",
            "| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in report.get("breakdowns", {}).get("category", []):
        lines.append(
            md_table_row(
                [
                    item["category"],
                    item["total_rows"],
                    item["strict_dual_pass_rows"],
                    f"{item['strict_dual_pass_rate_pct']:.2f}%",
                    item["valid_candidate_rows"],
                    item["behavior_ready_rows"],
                    f"{item['behavior_ready_pass_rate_pct']:.2f}%",
                    item["non_model_or_inconclusive_rows"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Axis Counts",
            "",
            "| Axis | Count | Meaning |",
            "| --- | ---: | --- |",
        ]
    )
    for axis, count in report["axis_counts"].items():
        meaning = report.get("axis_descriptions", {}).get(axis, "")
        lines.append(md_table_row([f"`{axis}`", count, meaning]))

    lines.extend(["", "## Failure Families", "", "| Family | Axis | Count | Example | Evidence |", "| --- | --- | ---: | --- | --- |"])
    for item in report["family_summaries"]:
        lines.append(
            md_table_row(
                [
                    f"`{item['root_cause_family']}`",
                    f"`{item['triage_axis']}`",
                    item["count"],
                    f"`{item['example_task_id']}`",
                    item["example_evidence"],
                ]
            )
        )

    lines.extend(["", "## Mismatch / Conformance Seeds", ""])
    if report["mismatch_rows"]:
        lines.extend(
            [
                "| Task | Direction/axis | Family | Suggested L0 action | Evidence |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in report["mismatch_rows"]:
            if row["evas_pass_spectre_fail"]:
                direction = "EVAS PASS / Spectre FAIL"
            elif row["spectre_pass_evas_fail"]:
                direction = "Spectre PASS / EVAS FAIL"
            else:
                direction = row["triage_axis"]
            lines.append(
                md_table_row(
                    [
                        f"`{row['task_id']}`",
                        direction,
                        f"`{row['root_cause_family']}`",
                        row["conformance_seed_suggestion"],
                        row["evidence"],
                    ]
                )
            )
    else:
        lines.append("No EVAS/Spectre mismatch rows were found in the selected inputs.")

    lines.extend(["", "## Inputs", ""])
    for item in report["inputs"]:
        lines.append(f"- `{item}`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def default_outputs(tag: str) -> tuple[Path, Path, Path]:
    base = REPORTS / f"evas_spectre_mismatch_triage_{tag}"
    return base.with_suffix(".json"), base.with_suffix(".md"), base.with_suffix(".csv")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result-root", action="append", type=Path, required=True)
    parser.add_argument("--tag", default=datetime.now(timezone.utc).strftime("%Y%m%d"))
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--output-csv", type=Path)
    parser.add_argument(
        "--dedupe-by-task",
        action="store_true",
        help="When multiple roots contain the same task_id, keep the last input's row.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_json, output_md, output_csv = default_outputs(args.tag)
    output_json = args.output_json or output_json
    output_md = args.output_md or output_md
    output_csv = args.output_csv or output_csv

    report = build_report(args.result_root, dedupe_by_task=args.dedupe_by_task)
    write_json(output_json, report)
    write_markdown(output_md, report)
    write_csv(output_csv, report["rows"])
    print(
        "wrote EVAS/Spectre triage: "
        f"{rel(output_json)} ({report['total_rows']} rows, "
        f"{report['evas_pass_spectre_fail_rows']} EVAS PASS/Spectre FAIL, "
        f"{report['spectre_pass_evas_fail_rows']} Spectre PASS/EVAS FAIL)"
    )


if __name__ == "__main__":
    main()
