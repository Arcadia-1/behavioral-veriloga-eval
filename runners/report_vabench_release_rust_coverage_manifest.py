#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = ROOT.parent
EVAS_ROOT = WORKSPACE_ROOT / "EVAS"
if EVAS_ROOT.exists() and str(EVAS_ROOT) not in sys.path:
    sys.path.insert(0, str(EVAS_ROOT))

from evas.compiler import ast_nodes as va_ast
from evas.netlist.runner import _compile_va
from evas.simulator.whole_segment import (
    CANDIDATE_SCHEMA_VERSION,
    validate_whole_segment_candidate,
)


PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
PACKAGE_MANIFEST = PACKAGE_ROOT / "MANIFEST.json"
SPEED_OPT_ROOT = ROOT / "speed-optimization"
RUST_KERNEL_ROOT = SPEED_OPT_ROOT / "rust-kernel"
BEHAVIOR_COVERAGE_MAP = RUST_KERNEL_ROOT / "behavior-coverage-map.v1.json"
REPORTS_ROOT = SPEED_OPT_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "current_release_rust_coverage_manifest_20260604.json"
REPORT_MD = REPORTS_ROOT / "current_release_rust_coverage_manifest_20260604.md"

SCHEMA_VERSION = "evas-release-rust-coverage-manifest.v1"

BEHAVIOR_WEIGHTS = {
    "B01": 8.0,
    "B02": 7.0,
    "B03": 7.0,
    "B04": 6.0,
    "B05": 6.0,
    "B06": 7.0,
    "B07": 6.0,
    "B08": 8.0,
    "B09": 8.0,
    "B10": 10.0,
    "B11": 8.0,
    "B12": 5.0,
    "B13": 4.0,
    "B14": 3.0,
    "B15": 4.0,
    "B16": 2.0,
    "B17": 3.0,
    "B18": 1.0,
}

STATUS_SCORE = {
    "implemented": 0.60,
    "shadow_only": 0.20,
    "partial": 0.35,
    "python_only": 0.0,
    "python_fallback": 0.0,
    "not_implemented": 0.0,
    "unsupported": 0.0,
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_gold_va_files(
    *,
    entries: set[str] | None = None,
    forms: set[str] | None = None,
    max_models: int | None = None,
) -> list[Path]:
    paths = sorted(TASKS_ROOT.glob("*/*/forms/*/gold/*.va"))

    selected: list[Path] = []
    for path in paths:
        info = path_info(path)
        if entries and info["entry_id"] not in entries:
            continue
        if forms and info["form"] not in forms:
            continue
        selected.append(path)
        if max_models is not None and len(selected) >= max_models:
            break
    return selected


def path_info(path: Path) -> dict[str, str]:
    parts = path.relative_to(TASKS_ROOT).parts
    category = parts[0] if len(parts) > 0 else ""
    entry_id = parts[1] if len(parts) > 1 else ""
    form = parts[3] if len(parts) > 3 and parts[2] == "forms" else ""
    return {
        "category_dir": category,
        "entry_id": entry_id,
        "form": form,
        "file": path.name,
    }


def entry_metadata() -> dict[str, dict[str, Any]]:
    manifest = read_json(PACKAGE_MANIFEST)
    out: dict[str, dict[str, Any]] = {}
    for entry in manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        entry_id = str(entry.get("release_entry_id", "") or "")
        if not entry_id:
            continue
        out[entry_id] = {
            "level": entry.get("level", ""),
            "track": entry.get("track", ""),
            "difficulty": entry.get("difficulty", ""),
            "category": entry.get("category", ""),
            "counted_in_score": bool(entry.get("counted_in_score", False)),
        }
    return out


def seed_behavior_status() -> dict[str, dict[str, Any]]:
    seed = read_json(BEHAVIOR_COVERAGE_MAP)
    out: dict[str, dict[str, Any]] = {}
    for row in seed.get("behavior_catalog", []):
        if not isinstance(row, dict):
            continue
        bid = str(row.get("id", "") or "")
        if bid:
            out[bid] = row
    return out


def engineering_completion_percent(seed: dict[str, dict[str, Any]]) -> float:
    total = 0.0
    score = 0.0
    for bid, weight in BEHAVIOR_WEIGHTS.items():
        status = str(seed.get(bid, {}).get("current_status", "not_implemented"))
        total += weight
        score += weight * STATUS_SCORE.get(status, 0.0)
    return round(100.0 * score / total, 1) if total else 0.0


def iter_event_exprs(event: Any):
    if event is None:
        return
    if isinstance(event, va_ast.EventExpr):
        yield event
    elif isinstance(event, va_ast.CombinedEvent):
        for child in event.events:
            yield from iter_event_exprs(child)


def iter_exprs(expr: Any):
    if expr is None:
        return
    yield expr
    if isinstance(expr, va_ast.FunctionCall):
        for arg in expr.args:
            yield from iter_exprs(arg)
    elif isinstance(expr, va_ast.MethodCall):
        for arg in expr.args:
            yield from iter_exprs(arg)
    elif isinstance(expr, va_ast.BinaryExpr):
        yield from iter_exprs(expr.left)
        yield from iter_exprs(expr.right)
    elif isinstance(expr, va_ast.UnaryExpr):
        yield from iter_exprs(expr.operand)
    elif isinstance(expr, va_ast.TernaryExpr):
        yield from iter_exprs(expr.cond)
        yield from iter_exprs(expr.true_expr)
        yield from iter_exprs(expr.false_expr)
    elif isinstance(expr, va_ast.ArrayAccess):
        yield from iter_exprs(expr.index)
    elif isinstance(expr, va_ast.BranchAccess):
        yield from iter_exprs(expr.node1_index)
        yield from iter_exprs(expr.node2_index)
        yield from iter_exprs(expr.node1_index2)
        yield from iter_exprs(expr.node2_index2)


def iter_stmt_exprs(stmt: Any):
    if stmt is None:
        return
    if isinstance(stmt, va_ast.Assignment):
        yield from iter_exprs(stmt.target)
        yield from iter_exprs(stmt.value)
    elif isinstance(stmt, va_ast.Contribution):
        yield from iter_exprs(stmt.branch)
        yield from iter_exprs(stmt.expr)
    elif isinstance(stmt, va_ast.EventStatement):
        for event in iter_event_exprs(stmt.event):
            for arg in event.args:
                yield from iter_exprs(arg)
            yield from iter_exprs(event.time_tol_expr)
            yield from iter_exprs(event.expr_tol_expr)
        yield from iter_stmt_exprs(stmt.body)
    elif isinstance(stmt, va_ast.Block):
        for child in stmt.statements:
            yield from iter_stmt_exprs(child)
    elif isinstance(stmt, va_ast.IfStatement):
        yield from iter_exprs(stmt.cond)
        yield from iter_stmt_exprs(stmt.then_body)
        yield from iter_stmt_exprs(stmt.else_body)
    elif isinstance(stmt, va_ast.ForStatement):
        yield from iter_stmt_exprs(stmt.init)
        yield from iter_exprs(stmt.cond)
        yield from iter_stmt_exprs(stmt.update)
        yield from iter_stmt_exprs(stmt.body)
    elif isinstance(stmt, va_ast.WhileStatement):
        yield from iter_exprs(stmt.cond)
        yield from iter_stmt_exprs(stmt.body)
    elif isinstance(stmt, va_ast.CaseStatement):
        yield from iter_exprs(stmt.expr)
        for item in stmt.items:
            for value in item.values:
                yield from iter_exprs(value)
            yield from iter_stmt_exprs(item.body)
    elif isinstance(stmt, va_ast.SystemTask):
        for arg in stmt.args:
            yield from iter_exprs(arg)


def iter_statements(stmt: Any):
    if stmt is None:
        return
    yield stmt
    if isinstance(stmt, va_ast.Block):
        for child in stmt.statements:
            yield from iter_statements(child)
    elif isinstance(stmt, va_ast.EventStatement):
        yield from iter_statements(stmt.body)
    elif isinstance(stmt, va_ast.IfStatement):
        yield from iter_statements(stmt.then_body)
        yield from iter_statements(stmt.else_body)
    elif isinstance(stmt, va_ast.ForStatement):
        yield from iter_statements(stmt.init)
        yield from iter_statements(stmt.update)
        yield from iter_statements(stmt.body)
    elif isinstance(stmt, va_ast.WhileStatement):
        yield from iter_statements(stmt.body)
    elif isinstance(stmt, va_ast.CaseStatement):
        for item in stmt.items:
            yield from iter_statements(item.body)


def ast_behavior_summary(module: Any) -> dict[str, Any]:
    stmt_counts: Counter[str] = Counter()
    function_calls: Counter[str] = Counter()
    system_tasks: Counter[str] = Counter()
    event_counts: Counter[str] = Counter()
    branch_counts: Counter[str] = Counter()
    array_accesses = 0
    dynamic_branch_accesses = 0

    body = module.analog_block.body if module.analog_block else None
    for stmt in iter_statements(body):
        stmt_counts[type(stmt).__name__] += 1
        if isinstance(stmt, va_ast.EventStatement):
            for event in iter_event_exprs(stmt.event):
                event_counts[event.event_type.name.lower()] += 1
        elif isinstance(stmt, va_ast.SystemTask):
            system_tasks[stmt.name.lower()] += 1

    for expr in iter_stmt_exprs(body):
        if isinstance(expr, va_ast.FunctionCall):
            function_calls[expr.name.lower()] += 1
        elif isinstance(expr, va_ast.MethodCall):
            function_calls[f"{expr.obj}.{expr.method}".lower()] += 1
        elif isinstance(expr, va_ast.BranchAccess):
            branch_counts[expr.access_type.upper()] += 1
            if any(
                item is not None
                for item in (
                    expr.node1_index,
                    expr.node2_index,
                    expr.node1_index2,
                    expr.node2_index2,
                )
            ):
                dynamic_branch_accesses += 1
        elif isinstance(expr, va_ast.ArrayAccess):
            array_accesses += 1

    scalar_states = [v.name for v in module.variables if not v.is_array]
    array_states = [v.name for v in module.variables if v.is_array]
    integer_states = [
        v.name
        for v in module.variables
        if v.var_type == va_ast.ParamType.INTEGER or v.is_genvar
    ]

    behaviors = {
        "B01": bool(module.analog_block),
        "B02": branch_counts.get("V", 0) > 0,
        "B03": bool(scalar_states),
        "B04": bool(array_states) or array_accesses > 0,
        "B05": any(stmt_counts.get(name, 0) > 0 for name in ("IfStatement", "ForStatement", "WhileStatement", "CaseStatement")),
        "B06": any(
            isinstance(stmt, va_ast.Contribution) and stmt.branch.access_type.upper() == "V"
            for stmt in iter_statements(body)
        ),
        "B07": function_calls.get("transition", 0) > 0,
        "B08": function_calls.get("transition", 0) > 0,
        "B09": event_counts.get("cross", 0) > 0 or event_counts.get("above", 0) > 0,
        "B10": stmt_counts.get("EventStatement", 0) > 0,
        "B11": event_counts.get("timer", 0) > 0,
        "B12": system_tasks.get("$bound_step", 0) > 0 or system_tasks.get("bound_step", 0) > 0,
        "B13": False,
        "B14": False,
        "B15": False,
        "B16": bool(system_tasks) or any(name in function_calls for name in ("$random", "$dist_uniform", "$rdist_normal", "$fopen")),
        "B17": bool(module.instances) or dynamic_branch_accesses > 0,
        "B18": bool(module.analog_block),
    }

    return {
        "statement_counts": dict(sorted(stmt_counts.items())),
        "function_calls": dict(sorted(function_calls.items())),
        "system_tasks": dict(sorted(system_tasks.items())),
        "event_counts": dict(sorted(event_counts.items())),
        "branch_counts": dict(sorted(branch_counts.items())),
        "state_counts": {
            "scalar": len(scalar_states),
            "array": len(array_states),
            "integer": len(integer_states),
        },
        "array_access_count": array_accesses,
        "dynamic_branch_access_count": dynamic_branch_accesses,
        "instance_count": len(module.instances),
        "behaviors_present": behaviors,
    }


def safe_len(value: Any) -> int:
    try:
        return len(value)
    except TypeError:
        return 0


def compiled_rust_summary(model_cls: type) -> dict[str, Any]:
    ordered = getattr(model_cls, "_ordered_transition_segment_ir_ops", ((), ()))
    if isinstance(ordered, tuple) and len(ordered) == 2:
        ordered_static_ops = safe_len(ordered[0])
        ordered_transition_ops = safe_len(ordered[1])
    else:
        ordered_static_ops = 0
        ordered_transition_ops = 0

    whole = tuple(getattr(model_cls, "_whole_segment_candidates", ()) or ())
    contracts = [
        validate_whole_segment_candidate(item).to_dict()
        for item in whole
        if item
    ]
    return {
        "static_affine_ops": safe_len(getattr(model_cls, "_rust_static_affine_ops", ())),
        "static_linear_ops": safe_len(getattr(model_cls, "_evaluate_ir_static_linear_ops", ())),
        "static_linear_rejections": list(getattr(model_cls, "_evaluate_ir_static_linear_rejections", ()) or ()),
        "transition_target_ops": safe_len(getattr(model_cls, "_transition_target_ir_ops", ())),
        "ordered_transition_static_ops": ordered_static_ops,
        "ordered_transition_target_ops": ordered_transition_ops,
        "event_lfsr_shift_ops": safe_len(getattr(model_cls, "_event_lfsr_shift_ir_ops", ())),
        "event_lfsr_output_hold_states": safe_len(getattr(model_cls, "_event_lfsr_output_hold_states", ())),
        "state_owned_timer_targets": safe_len(getattr(model_cls, "_state_owned_timer_targets", ())),
        "whole_segment_candidates": [str(item[0]) for item in whole if item],
        "whole_segment_candidate_count": len(whole),
        "whole_segment_contract_schema_version": CANDIDATE_SCHEMA_VERSION,
        "whole_segment_candidate_contracts": contracts,
        "whole_segment_invalid_candidate_count": sum(
            1 for item in contracts if not item.get("valid", False)
        ),
        "uses_bound_step": bool(getattr(model_cls, "_uses_bound_step", False)),
        "has_dynamic_breakpoints": bool(getattr(model_cls, "_has_dynamic_breakpoints", False)),
        "has_post_update_events": bool(getattr(model_cls, "_has_post_update_events", False)),
        "needs_future_node_voltages": bool(getattr(model_cls, "_needs_future_node_voltages", False)),
        "dynamic_branch_accesses": safe_len(getattr(model_cls, "_dynamic_branch_accesses", ())),
        "dynamic_voltage_read_count": int(getattr(model_cls, "_dynamic_voltage_read_count", 0) or 0),
        "dynamic_output_write_count": int(getattr(model_cls, "_dynamic_output_write_count", 0) or 0),
    }


def module_shape_summary(module: Any) -> dict[str, Any]:
    return {
        "ports": list(module.ports),
        "parameters": [param.name for param in module.parameters],
        "state_arrays": [var.name for var in module.variables if var.is_array],
    }


def row_rust_signals(summary: dict[str, Any]) -> list[str]:
    signals: list[str] = []
    if summary["static_linear_ops"]:
        signals.append("static_linear_ir")
    if summary["transition_target_ops"]:
        signals.append("transition_target_ir")
    if summary["ordered_transition_static_ops"] or summary["ordered_transition_target_ops"]:
        signals.append("ordered_transition_shadow")
    if summary["event_lfsr_shift_ops"]:
        signals.append("event_lfsr_batch")
    if summary["state_owned_timer_targets"]:
        signals.append("state_owned_timer_fastpath")
    if summary["whole_segment_candidate_count"]:
        signals.append("whole_segment_candidate")
    if summary["dynamic_branch_accesses"]:
        signals.append("dynamic_bus_metadata")
    return signals


def analyze_model(path: Path, metadata: dict[str, dict[str, Any]]) -> dict[str, Any]:
    info = path_info(path)
    row: dict[str, Any] = {
        **info,
        **metadata.get(info["entry_id"], {}),
        "path": rel(path),
        "sha256": sha256_file(path),
        "compile_status": "unknown",
    }
    try:
        model_cls, module = _compile_va(str(path), source_dir=str(path.parent))
        ast = ast_behavior_summary(module)
        rust = compiled_rust_summary(model_cls)
        row.update(
            {
                "module": module.name,
                "module_shape": module_shape_summary(module),
                "compile_status": "pass",
                "port_count": len(module.ports),
                "parameter_count": len(module.parameters),
                "variable_count": len(module.variables),
                "ast": ast,
                "rust": rust,
                "rust_signals": row_rust_signals(rust),
            }
        )
    except Exception as exc:  # noqa: BLE001 - manifest records compiler blocker.
        row.update(
            {
                "compile_status": "fail",
                "compile_error_type": type(exc).__name__,
                "compile_error": str(exc)[:1000],
                "ast": {},
                "rust": {},
                "rust_signals": [],
            }
        )
    return row


def _row_matches_module_shape(
    row: dict[str, Any],
    *,
    ports: tuple[str, ...],
    parameters: tuple[str, ...],
    state_arrays: tuple[str, ...] = (),
) -> bool:
    if row.get("compile_status") != "pass":
        return False
    shape = row.get("module_shape", {})
    if not isinstance(shape, dict):
        return False
    row_ports = set(shape.get("ports", []) or [])
    row_parameters = set(shape.get("parameters", []) or [])
    row_arrays = set(shape.get("state_arrays", []) or [])
    return (
        row_ports == set(ports)
        and set(parameters).issubset(row_parameters)
        and set(state_arrays).issubset(row_arrays)
    )


def _find_module_shape_rows(
    rows: list[dict[str, Any]],
    *,
    ports: tuple[str, ...],
    parameters: tuple[str, ...],
    state_arrays: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if _row_matches_module_shape(
            row,
            ports=ports,
            parameters=parameters,
            state_arrays=state_arrays,
        )
    ]


def whole_flow_fastpath_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Detect release-form level whole-flow Rust candidates.

    Compiled-model metadata is single-file. Some production Rust paths, such as
    gain measurement flow, are intentionally recognized at simulator runtime
    from multiple connected models. The manifest therefore records only a
    conservative source-shape candidate; the engine still owns the final wiring,
    source, and recorded-signal gate.
    """

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row.get("entry_id", "")), str(row.get("form", "")))].append(row)

    candidates: list[dict[str, Any]] = []
    for (entry_id, form), form_rows in sorted(grouped.items()):
        vin = _find_module_shape_rows(
            form_rows,
            ports=("CLK", "RST_N", "VOUT_P", "VOUT_N"),
            parameters=("vdd", "vth", "ampl", "freq", "sigma", "SEED"),
        )
        lfsr = _find_module_shape_rows(
            form_rows,
            ports=("DPN", "VDD", "VSS", "CLK", "EN", "RSTB"),
            parameters=("seed",),
            state_arrays=("lfsr_r", "tmp_lfsr_r"),
        )
        dither = _find_module_shape_rows(
            form_rows,
            ports=("VRES_P", "VRES_N", "DPN", "VOUT_P", "VOUT_N"),
            parameters=("vth", "DITHER_AMP"),
        )
        amp = _find_module_shape_rows(
            form_rows,
            ports=("VIN_P", "VIN_N", "VOUT_P", "VOUT_N"),
            parameters=("vdd", "ACTUAL_GAIN"),
        )
        if not (len(vin) == len(lfsr) == len(dither) == len(amp) == 1):
            continue
        model_rows = [vin[0], lfsr[0], dither[0], amp[0]]
        candidates.append(
            {
                "kind": "gain_measurement_flow_v1",
                "entry_id": entry_id,
                "form": form,
                "production_abi": "evas_rust_gain_measurement_flow_trace",
                "model_paths": [row["path"] for row in model_rows],
                "runtime_gate": "Simulator._try_gain_measurement_flow_fastpath validates wiring, source waveforms, parameters, and recorded signals.",
            }
        )
    return candidates


def summarize_rows(rows: list[dict[str, Any]], seed: dict[str, dict[str, Any]]) -> dict[str, Any]:
    compile_counts = Counter(str(row["compile_status"]) for row in rows)
    signal_counts: Counter[str] = Counter()
    whole_segment_counts: Counter[str] = Counter()
    rejection_counts: Counter[str] = Counter()
    invalid_candidate_count = 0
    behavior_counts: dict[str, int] = defaultdict(int)
    blocker_counts: Counter[str] = Counter()
    form_counts: Counter[str] = Counter()
    entry_ids: set[str] = set()
    hashes: Counter[str] = Counter()
    whole_flow_candidates = whole_flow_fastpath_candidates(rows)
    whole_flow_counts = Counter(str(item["kind"]) for item in whole_flow_candidates)

    for row in rows:
        form_counts[str(row.get("form", ""))] += 1
        entry_ids.add(str(row.get("entry_id", "")))
        if row.get("sha256"):
            hashes[str(row["sha256"])] += 1
        for signal in row.get("rust_signals", []):
            signal_counts[str(signal)] += 1
        rust = row.get("rust", {})
        if isinstance(rust, dict):
            for item in rust.get("whole_segment_candidates", []):
                whole_segment_counts[str(item)] += 1
            invalid_candidate_count += int(
                rust.get("whole_segment_invalid_candidate_count", 0) or 0
            )
            for item in rust.get("static_linear_rejections", []):
                rejection_counts[str(item)] += 1
        ast = row.get("ast", {})
        if isinstance(ast, dict):
            present = ast.get("behaviors_present", {})
            if isinstance(present, dict):
                for bid, value in present.items():
                    if value:
                        behavior_counts[str(bid)] += 1

    for bid, count in behavior_counts.items():
        status = str(seed.get(bid, {}).get("current_status", "not_implemented"))
        if status in {"python_only", "not_implemented", "shadow_only"}:
            blocker_counts[f"{bid}:{status}"] += count
        elif status == "partial":
            blocker_counts[f"{bid}:partial"] += count

    unique_hashes = len(hashes)
    duplicate_rows = sum(count - 1 for count in hashes.values() if count > 1)

    return {
        "model_rows": len(rows),
        "entry_count": len(entry_ids),
        "compile_status_counts": dict(sorted(compile_counts.items())),
        "form_counts": dict(sorted(form_counts.items())),
        "unique_gold_source_hashes": unique_hashes,
        "duplicate_gold_source_rows": duplicate_rows,
        "rust_signal_counts": dict(sorted(signal_counts.items())),
        "whole_segment_candidate_counts": dict(sorted(whole_segment_counts.items())),
        "whole_flow_fastpath_counts": dict(sorted(whole_flow_counts.items())),
        "whole_flow_fastpath_candidates": whole_flow_candidates,
        "whole_segment_invalid_candidate_count": invalid_candidate_count,
        "static_linear_rejection_counts": dict(rejection_counts.most_common(25)),
        "behavior_present_counts": dict(sorted(behavior_counts.items())),
        "top_rust_blockers": dict(blocker_counts.most_common(20)),
    }


def behavior_table(seed: dict[str, dict[str, Any]], summary: dict[str, Any]) -> list[dict[str, Any]]:
    present_counts = summary.get("behavior_present_counts", {})
    rows: list[dict[str, Any]] = []
    for bid in sorted(BEHAVIOR_WEIGHTS):
        seed_row = seed.get(bid, {})
        rows.append(
            {
                "id": bid,
                "name": seed_row.get("name", ""),
                "current_status": seed_row.get("current_status", "not_implemented"),
                "present_model_rows": int(present_counts.get(bid, 0) or 0),
                "rust_primitive": seed_row.get("rust_primitive"),
                "fallback_reasons": seed_row.get("fallback_reasons", []),
            }
        )
    return rows


def build_report(
    *,
    entries: set[str] | None = None,
    forms: set[str] | None = None,
    max_models: int | None = None,
) -> dict[str, Any]:
    seed = seed_behavior_status()
    metadata = entry_metadata()
    paths = iter_gold_va_files(entries=entries, forms=forms, max_models=max_models)
    rows = [analyze_model(path, metadata) for path in paths]
    summary = summarize_rows(rows, seed)
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "engineering_rust_coverage_manifest",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "claim_policy": {
            "paper_speed_claim_allowed": False,
            "reason": "This is compile-level Rust coverage evidence, not same-slice EVAS/Spectre timing.",
        },
        "scope": {
            "tasks_root": rel(TASKS_ROOT),
            "entries_filter": sorted(entries) if entries else [],
            "forms_filter": sorted(forms) if forms else [],
            "max_models": max_models,
            "model_rows_scanned": len(rows),
        },
        "rustification_completion_estimate": {
            "percent": engineering_completion_percent(seed),
            "basis": "weighted B01-B18 seed status estimate; not a speed or correctness claim",
        },
        "summary": summary,
        "behavior_table": behavior_table(seed, summary),
        "models": rows,
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    estimate = report["rustification_completion_estimate"]
    lines = [
        "# Release Rust Coverage Manifest",
        "",
        f"Created: `{report['created_at']}`",
        f"Paper speed claim allowed: `{report['claim_policy']['paper_speed_claim_allowed']}`",
        f"Reason: {report['claim_policy']['reason']}",
        "",
        "## Scope",
        "",
        f"- Tasks root: `{report['scope']['tasks_root']}`",
        f"- Model rows scanned: `{report['scope']['model_rows_scanned']}`",
        f"- Entry count: `{summary['entry_count']}`",
        f"- Unique gold source hashes: `{summary['unique_gold_source_hashes']}`",
        f"- Duplicate gold source rows: `{summary['duplicate_gold_source_rows']}`",
        f"- Whole-segment invalid candidates: `{summary['whole_segment_invalid_candidate_count']}`",
        "",
        "## Rustification Estimate",
        "",
        f"- Engineering completion estimate: `{estimate['percent']}%`",
        f"- Basis: {estimate['basis']}",
        "- This number is deliberately conservative: shadow-only and partial helpers do not count as full Rust production.",
        "",
        "## Compile Status",
        "",
        "| Status | Model rows |",
        "|---|---:|",
    ]
    for status, count in summary["compile_status_counts"].items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Rust Signals", "", "| Signal | Model rows |", "|---|---:|"])
    for signal, count in summary["rust_signal_counts"].items():
        lines.append(f"| `{signal}` | {count} |")
    if not summary["rust_signal_counts"]:
        lines.append("| none | 0 |")

    lines.extend(["", "## Whole-Segment Candidates", "", "| Candidate | Model rows |", "|---|---:|"])
    for candidate, count in summary["whole_segment_candidate_counts"].items():
        lines.append(f"| `{candidate}` | {count} |")
    if not summary["whole_segment_candidate_counts"]:
        lines.append("| none | 0 |")

    lines.extend(["", "## Whole-Flow Fastpaths", "", "| Candidate | Release forms |", "|---|---:|"])
    for candidate, count in summary["whole_flow_fastpath_counts"].items():
        lines.append(f"| `{candidate}` | {count} |")
    if not summary["whole_flow_fastpath_counts"]:
        lines.append("| none | 0 |")

    flow_rows = summary.get("whole_flow_fastpath_candidates", [])
    if flow_rows:
        lines.extend(
            [
                "",
                "| Candidate | Entry | Form | Production ABI |",
                "|---|---|---|---|",
            ]
        )
        for item in flow_rows:
            lines.append(
                f"| `{item['kind']}` | `{item['entry_id']}` | `{item['form']}` | `{item['production_abi']}` |"
            )
        lines.extend(
            [
                "",
                "Note: whole-flow rows are source-shape candidates. The simulator runtime gate still validates wiring, sources, parameters, and recorded signals before enabling production Rust.",
            ]
        )

    lines.extend(["", "## Behavior Coverage", "", "| ID | Status | Present rows | Rust primitive |", "|---|---|---:|---|"])
    for row in report["behavior_table"]:
        primitive = row["rust_primitive"] or ""
        lines.append(
            f"| `{row['id']}` | `{row['current_status']}` | {row['present_model_rows']} | `{primitive}` |"
        )

    lines.extend(["", "## Top Blockers", "", "| Blocker | Weighted model rows |", "|---|---:|"])
    for blocker, count in summary["top_rust_blockers"].items():
        lines.append(f"| `{blocker}` | {count} |")
    if not summary["top_rust_blockers"]:
        lines.append("| none | 0 |")

    lines.extend(["", "## Static Linear Rejections", "", "| Rejection | Model rows |", "|---|---:|"])
    for reason, count in summary["static_linear_rejection_counts"].items():
        lines.append(f"| `{reason}` | {count} |")
    if not summary["static_linear_rejection_counts"]:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Next Engineering Use",
            "",
            "- Use `whole_segment_candidate_counts` to drive 068/069 Rust ABI work.",
            "- Use `top_rust_blockers` to prioritize event/timer/transition/evaluate IR lowering.",
            "- Do not use this artifact as EVAS-vs-Spectre speed evidence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build release-wide EVAS Rust coverage manifest.")
    parser.add_argument("--entry", action="append", default=[], help="Release entry id to include; repeatable.")
    parser.add_argument("--form", action="append", default=[], help="Release form to include; repeatable.")
    parser.add_argument("--max-models", type=int, default=None, help="Limit scanned gold VA rows for smoke tests.")
    parser.add_argument("--report-json", default=str(REPORT_JSON))
    parser.add_argument("--report-md", default=str(REPORT_MD))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report_json = Path(args.report_json)
    if not report_json.is_absolute():
        report_json = ROOT / report_json
    report_md = Path(args.report_md)
    if not report_md.is_absolute():
        report_md = ROOT / report_md
    report = build_report(
        entries=set(args.entry) if args.entry else None,
        forms=set(args.form) if args.form else None,
        max_models=args.max_models,
    )
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(report, report_md)
    print(
        "wrote release rust coverage manifest: rows={rows} compile={compile_counts} estimate={estimate}% report={report}".format(
            rows=report["summary"]["model_rows"],
            compile_counts=report["summary"]["compile_status_counts"],
            estimate=report["rustification_completion_estimate"]["percent"],
            report=rel(report_json),
        )
    )


if __name__ == "__main__":
    main()
