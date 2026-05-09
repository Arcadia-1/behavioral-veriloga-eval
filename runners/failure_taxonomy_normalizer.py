#!/usr/bin/env python3
"""Normalize validation failures without rewriting raw backend statuses.

The validator keeps backend-specific labels such as ``FAIL_DUT_COMPILE`` and
``FAIL_TB_COMPILE`` because they are useful debug evidence.  For experiment
tables, however, EVAS and Spectre can disagree on that raw label while agreeing
on the only paper-level verdict that matters: PASS vs FAIL.

This module adds an analysis-only taxonomy:

- ``normalized_status``: binary PASS/FAIL.
- ``failure_stage``: where the run was blocked or judged.
- ``failure_origin``: the likely owner/source of the failure.
- ``failure_reason``: a stable reason bucket for aggregation.

It intentionally does not mutate or reinterpret the original ``status``.
"""
from __future__ import annotations

from typing import Any


def notes_list(result: dict[str, Any]) -> list[str]:
    """Return notes from either validator results or score model results."""
    raw = result.get("notes")
    if raw is None:
        raw = result.get("evas_notes")
    if raw is None:
        raw = []
    if isinstance(raw, str):
        notes = [raw]
    else:
        notes = [str(item) for item in raw]
    # Backend diagnostics often carry the concrete reason hidden behind a coarse
    # FAIL_DUT_COMPILE label.  Keep warnings out to avoid classifying harmless
    # simulator notices as failures.
    for key in ("spectre_errors", "errors", "stderr_tail", "stdout_tail", "evas_stdout_tail"):
        extra = result.get(key)
        if extra is None:
            continue
        if isinstance(extra, str):
            notes.append(extra)
        else:
            notes.extend(str(item) for item in extra)
    return notes


def notes_text(result: dict[str, Any]) -> str:
    return "\n".join(notes_list(result)).lower()


def pass_binary(result: dict[str, Any]) -> bool:
    """Return the backend-level PASS/FAIL verdict used in parity audits."""
    return str(result.get("status", "UNKNOWN")) == "PASS"


def _payload(
    result: dict[str, Any],
    *,
    stage: str,
    origin: str,
    reason: str,
    confidence: float,
    evidence: str,
    blocking: bool = True,
) -> dict[str, Any]:
    raw_status = str(result.get("status", "UNKNOWN"))
    passed = pass_binary(result)
    return {
        "raw_status": raw_status,
        "normalized_status": "PASS" if passed else "FAIL",
        "failure_stage": "pass" if passed else stage,
        "failure_origin": "none" if passed else origin,
        "failure_reason": "pass" if passed else reason,
        "confidence": 1.0 if passed else confidence,
        "blocking": False if passed else blocking,
        "evidence": "status=PASS" if passed else evidence,
    }


def normalize_failure(result: dict[str, Any]) -> dict[str, Any]:
    """Classify a single backend result into a stable analysis taxonomy."""
    if pass_binary(result):
        return _payload(
            result,
            stage="pass",
            origin="none",
            reason="pass",
            confidence=1.0,
            evidence="status=PASS",
            blocking=False,
        )

    status = str(result.get("status", "UNKNOWN"))
    text = notes_text(result)

    if "missing_generated_files" in text or "missing_generated_sample" in text:
        return _payload(
            result,
            stage="artifact_missing",
            origin="generated_artifact",
            reason="missing_generated_files",
            confidence=0.98,
            evidence="missing generated DUT/testbench artifacts",
        )

    if "timeout" in text:
        return _payload(
            result,
            stage="simulator_runtime",
            origin="verification_pipeline",
            reason="timeout",
            confidence=0.9,
            evidence="timeout marker in validator notes",
        )

    if "sourced_port_voltage_drive" in text:
        return _payload(
            result,
            stage="interface_preflight",
            origin="interface_contract",
            reason="interface_source_drive",
            confidence=0.98,
            evidence="source drives a port that is classified as DUT-driven/output",
        )

    tb_source_markers = (
        "pwl wave must contain",
        "uncontinued_multiline_source",
        "unsupported_tb_directives",
        "invalid source",
        "invalid_source",
    )
    if any(marker in text for marker in tb_source_markers):
        return _payload(
            result,
            stage="tb_source_parse",
            origin="testbench_source",
            reason="tb_source_or_netlist_parse",
            confidence=0.95,
            evidence="testbench/source parser rejected source syntax or waveform syntax",
        )

    if "conditional_transition" in text or "transition() contribution is inside" in text:
        return _payload(
            result,
            stage="source_semantics_preflight",
            origin="dut_source",
            reason="conditional_transition_semantics",
            confidence=0.95,
            evidence="transition() appears inside conditional/event/loop/case control flow",
        )

    unsupported_symbol_markers = (
        "$abstime_step",
        "keyerror: 'abstime'",
        'keyerror: "$abstime',
        "undefined function $abstime_step",
        "undefined symbol $abstime_step",
    )
    if any(marker in text for marker in unsupported_symbol_markers) or ("vacomp" in text and "abstime" in text):
        return _payload(
            result,
            stage="source_unsupported_symbol",
            origin="dut_source",
            reason="unsupported_or_nonstandard_symbol",
            confidence=0.92,
            evidence="unsupported/nonstandard time symbol appears in source or runtime trace",
        )

    if "spectre_returncode=2" in text or status == "FAIL_DUT_COMPILE":
        return _payload(
            result,
            stage="compile_or_elaboration",
            origin="dut_source",
            reason="dut_compile_or_elaboration_failure",
            confidence=0.82,
            evidence="DUT compile/elaboration failed before a behavior verdict",
        )

    if "tran.csv missing" in text or "spectre_data_missing_time" in text:
        return _payload(
            result,
            stage="waveform_missing",
            origin="spectre_backend" if "spectre" in text else "verification_pipeline",
            reason="missing_waveform",
            confidence=0.88,
            evidence="simulation did not produce a usable transient waveform CSV",
        )

    if status == "FAIL_TB_COMPILE":
        return _payload(
            result,
            stage="tb_compile_or_elaboration",
            origin="testbench_source",
            reason="tb_compile_or_elaboration_failure",
            confidence=0.82,
            evidence="testbench compile/elaboration failed before a behavior verdict",
        )

    if "evas_runtime_error" in text or "traceback" in text or "keyerror" in text:
        return _payload(
            result,
            stage="simulator_runtime",
            origin="simulator_kernel",
            reason="evas_runtime_error",
            confidence=0.85,
            evidence="EVAS runtime exception blocked a stable verdict",
        )

    if status == "FAIL_INFRA":
        return _payload(
            result,
            stage="infrastructure",
            origin="verification_pipeline",
            reason="infra_failure",
            confidence=0.8,
            evidence="validator reported infrastructure failure",
        )

    if status == "FAIL_SIM_CORRECTNESS":
        return _payload(
            result,
            stage="behavior_check",
            origin="candidate_behavior",
            reason="checker_behavior_failure",
            confidence=0.9,
            evidence="simulation completed and checker reported a behavior mismatch",
            blocking=False,
        )

    return _payload(
        result,
        stage="unknown",
        origin="unknown",
        reason="unknown_failure",
        confidence=0.5,
        evidence="no taxonomy marker matched",
    )


def normalize_pair(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Classify an EVAS/Spectre comparison using combined evidence.

    Pair-level normalization is deliberately separate from per-backend
    normalization.  For example, Spectre may only report ``returncode=2`` while
    EVAS notes expose the concrete source construct that caused the failure.
    The pair bucket can use both sides to explain the raw-label mismatch.
    """
    left_norm = normalize_failure(left)
    right_norm = normalize_failure(right)
    binary_mismatch = left_norm["normalized_status"] != right_norm["normalized_status"]
    text = f"{notes_text(left)}\n{notes_text(right)}"

    if not binary_mismatch and left_norm["normalized_status"] == "PASS":
        reason = "pass"
        stage = "pass"
        origin = "none"
        confidence = 1.0
    elif "pwl wave must contain" in text or "uncontinued_multiline_source" in text or "unsupported_tb_directives" in text or "invalid source" in text:
        reason = "tb_source_or_netlist_parse"
        stage = "tb_source_parse"
        origin = "testbench_source"
        confidence = 0.95
    elif "sourced_port_voltage_drive" in text:
        reason = "interface_source_drive"
        stage = "interface_preflight"
        origin = "interface_contract"
        confidence = 0.98
    elif "$abstime_step" in text or "keyerror: 'abstime'" in text or 'keyerror: "$abstime' in text:
        reason = "unsupported_or_nonstandard_symbol"
        stage = "source_unsupported_symbol"
        origin = "dut_source"
        confidence = 0.92
    elif "conditional_transition" in text or "transition() contribution is inside" in text:
        reason = "conditional_transition_semantics"
        stage = "source_semantics_preflight"
        origin = "dut_source"
        confidence = 0.95
    elif "spectre_returncode=2" in text:
        reason = "dut_compile_or_elaboration_failure"
        stage = "compile_or_elaboration"
        origin = "dut_source"
        confidence = 0.82
    elif "tran.csv missing" in text or "spectre_data_missing_time" in text:
        reason = "missing_waveform"
        stage = "waveform_missing"
        origin = "verification_pipeline"
        confidence = 0.85
    elif "count_range" in text or "checker" in text:
        reason = "checker_behavior_failure"
        stage = "behavior_check"
        origin = "candidate_behavior"
        confidence = 0.88
    elif binary_mismatch:
        reason = "binary_verdict_mismatch"
        stage = "backend_verdict_disagreement"
        origin = "evas_spectre_parity"
        confidence = 0.75
    else:
        reason = left_norm["failure_reason"] if left_norm["failure_reason"] == right_norm["failure_reason"] else "label_only_mismatch_uncategorized"
        stage = left_norm["failure_stage"] if left_norm["failure_stage"] == right_norm["failure_stage"] else "label_only_mismatch"
        origin = left_norm["failure_origin"] if left_norm["failure_origin"] == right_norm["failure_origin"] else "mixed"
        confidence = min(float(left_norm["confidence"]), float(right_norm["confidence"]), 0.75)

    return {
        "normalized_status_pair": "MISMATCH" if binary_mismatch else left_norm["normalized_status"],
        "binary_mismatch": binary_mismatch,
        "failure_stage": stage,
        "failure_origin": origin,
        "failure_reason": reason,
        "confidence": confidence,
        "left": left_norm,
        "right": right_norm,
    }
