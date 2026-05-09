#!/usr/bin/env python3
"""Materialize controller-routed candidates from compile-tool outputs.

This runner is a small vaEVAS analogue of VisionController-style control mode:
it extracts validator signals, tries cheap local compile tools first, and only
routes selected failure families to an expensive cached LLM/CE tool output.

The cached fallback lets us evaluate the controller policy without spending new
API tokens.  The final generation_meta records projected live LLM cost for the
fallback calls the controller would have made.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import time
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from compile_hard_guard import apply_compile_skill_actions
from generate import list_bench_task_dirs
from run_adaptive_repair import _compile_closure_rank
from score import score_one_task


COMPILE_STATUSES = {"FAIL_DUT_COMPILE", "FAIL_TB_COMPILE", "FAIL_INFRA"}


@dataclass(frozen=True)
class RepairState:
    task_id: str
    status: str
    task_form: str
    core_function: str
    required_axes: list[str]
    failure_families: list[str]
    has_empty_pwl: bool
    has_gold_dut_include: bool
    sourced_port_conflicts: int
    has_undefined_module: bool
    has_conditional_transition: bool
    sim_correct_required: bool
    scores: dict[str, float]
    notes: list[str]


@dataclass(frozen=True)
class ToolDecision:
    tool: str
    route: bool
    reason: str
    expected_effect: str
    max_projected_calls: int
    max_projected_tokens: int
    risk: str


@dataclass(frozen=True)
class RewardConfig:
    pass_weight: float = 10.0
    compile_weight: float = 2.0
    behavior_weight: float = 2.0
    token_weight_per_1k: float = 0.02
    api_second_weight: float = 0.01


def _json_read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy_sample(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for path in sorted(src.glob("*")):
        if path.is_file():
            shutil.copy2(path, dst / path.name)


def _copy_selected_samples(source_root: Path, output_root: Path, *, model: str, sample_idx: int, task_ids: set[str]) -> None:
    if output_root.exists():
        shutil.rmtree(output_root)
    for task_id in sorted(task_ids):
        src = _task_sample_dir(source_root, model, task_id, sample_idx)
        if src.exists():
            _copy_sample(src, _task_sample_dir(output_root, model, task_id, sample_idx))


def _compile_failures_from_summary(summary_path: Path) -> dict[str, dict[str, Any]]:
    summary = _json_read(summary_path)
    selected: dict[str, dict[str, Any]] = {}
    for item in summary.get("evas", {}).get("fail_tasks", []):
        status = item.get("status")
        if status not in COMPILE_STATUSES:
            continue
        notes = [str(note) for note in item.get("notes", [])]
        if status == "FAIL_INFRA" and not any(
            marker in " ".join(notes).lower()
            for marker in ("missing_generated_files", "missing_staged_tb", "compile", "preflight")
        ):
            continue
        task_id = item.get("task_id")
        if task_id:
            selected[str(task_id)] = {"status": status, "notes": notes}
    return selected


def _task_sample_dir(root: Path, model: str, task_id: str, sample_idx: int) -> Path:
    return root / model / task_id / f"sample_{sample_idx}"


def _existing_result(result_root: Path, task_id: str) -> dict[str, Any] | None:
    for name in ("evas_result.json", "result.json"):
        path = result_root / task_id / name
        if path.exists():
            return _json_read(path)
    return None


def _result_path(result_root: Path, task_id: str) -> Path | None:
    for name in ("evas_result.json", "result.json"):
        path = result_root / task_id / name
        if path.exists():
            return path
    return None


def _result_notes(result: dict[str, Any] | None, fallback_notes: list[str]) -> list[str]:
    if not result:
        return fallback_notes
    notes = result.get("evas_notes") or result.get("notes") or []
    return [str(note) for note in notes]


def _scores(result: dict[str, Any] | None) -> dict[str, float]:
    raw = (result or {}).get("scores") or {}
    out: dict[str, float] = {}
    for key in ("dut_compile", "tb_compile", "sim_correct", "weighted_total"):
        try:
            out[key] = float(raw.get(key, 0.0) or 0.0)
        except (TypeError, ValueError):
            out[key] = 0.0
    return out


def _score_candidate(
    *,
    task_id: str,
    task_dir: Path,
    sample_dir: Path,
    output_root: Path,
    model: str,
    sample_idx: int,
    timeout_s: int,
) -> dict[str, Any]:
    return score_one_task(
        task_id,
        task_dir,
        sample_dir,
        output_root,
        model=model,
        sample_idx=sample_idx,
        temperature=0.0,
        top_p=1.0,
        timeout_s=timeout_s,
    )


def _count_sourced_port_conflicts(notes: list[str]) -> int:
    count = 0
    for note in notes:
        if "sourced_port_voltage_drive=" not in note:
            continue
        payload = note.split("sourced_port_voltage_drive=", 1)[1]
        count += sum(1 for item in payload.split(",") if item.strip())
    return count


def _failure_families(notes: list[str], *, task_form: str, sim_correct_required: bool) -> list[str]:
    joined = " ".join(notes).lower()
    families: list[str] = []
    if "pwl wave must contain at least one time/value pair" in joined:
        families.append("empty_pwl")
    if "nonincreasing_pwl_time=" in joined:
        families.append("nonincreasing_pwl")
    sourced_count = _count_sourced_port_conflicts(notes)
    if sourced_count == 1:
        families.append("single_sourced_port")
    elif sourced_count > 1:
        families.append("multi_sourced_port")
    if task_form in {"dut-generation", "spec-to-va", "bugfix"} and sourced_count and "generated_dut_staged_as=" in joined:
        families.append("dut_header_or_port_order")
    if "undefined_module=" in joined:
        families.append("undefined_module")
    if "instance_port_count_mismatch=" in joined:
        families.append("port_count_mismatch")
    if "conditional_transition" in joined:
        families.append("conditional_transition")
    if "dynamic_analog_vector_index=" in joined or "modulo_array_index=" in joined:
        families.append("dynamic_vector_index")
    if "missing_generated_files" in joined or "missing_staged_tb" in joined:
        families.append("missing_artifact")
    if "gold_dut_include=" in joined and sourced_count:
        families.append("tb_public_instance_wiring")
    if "pwl wave must contain at least one time/value pair" in joined and not sim_correct_required:
        families.append("tb_compile_only_empty_pwl")
    return families or ["unknown_compile_failure"]


def _extract_state(
    *,
    task_id: str,
    task_meta: dict[str, Any],
    result: dict[str, Any] | None,
    fallback_notes: list[str],
) -> RepairState:
    notes = _result_notes(result, fallback_notes)
    joined = " ".join(notes).lower()
    required_axes = task_meta.get("scoring") or task_meta.get("required_axes") or []
    task_form = str(task_meta.get("task_form") or task_meta.get("family") or "")
    sim_correct_required = "sim_correct" in required_axes
    return RepairState(
        task_id=task_id,
        status=str((result or {}).get("status") or ""),
        task_form=task_form,
        core_function=str(task_meta.get("core_function") or task_meta.get("category") or ""),
        required_axes=[str(axis) for axis in required_axes],
        failure_families=_failure_families(notes, task_form=task_form, sim_correct_required=sim_correct_required),
        has_empty_pwl="pwl wave must contain at least one time/value pair" in joined,
        has_gold_dut_include="gold_dut_include=" in joined,
        sourced_port_conflicts=_count_sourced_port_conflicts(notes),
        has_undefined_module="undefined_module=" in joined,
        has_conditional_transition="conditional_transition" in joined,
        sim_correct_required=sim_correct_required,
        scores=_scores(result),
        notes=notes,
    )


def _fallback_decision(state: RepairState, policy: str, *, max_projected_tokens: int) -> ToolDecision:
    if policy == "never":
        return ToolDecision("cached_llm_ce_fallback", False, "policy_never", "none", 0, 0, "none")
    if policy == "all-compile":
        return ToolDecision("cached_llm_ce_fallback", True, "policy_all_compile", "compile_coverage", 1, max_projected_tokens, "high_cost")

    if policy == "pass-efficient":
        if state.has_empty_pwl and not state.sim_correct_required:
            return ToolDecision(
                "cached_llm_ce_fallback",
                True,
                "empty_pwl_tb_compile_only",
                "likely_pass",
                1,
                max_projected_tokens,
                "low",
            )
        if state.has_gold_dut_include and state.sourced_port_conflicts == 1:
            return ToolDecision(
                "cached_llm_ce_fallback",
                True,
                "single_gold_dut_sourced_port",
                "likely_pass",
                1,
                max_projected_tokens,
                "medium",
            )
        return ToolDecision("cached_llm_ce_fallback", False, "not_pass_efficient_family", "none", 0, 0, "none")

    if policy == "compile-coverage":
        if state.has_empty_pwl:
            return ToolDecision(
                "cached_llm_ce_fallback",
                True,
                "empty_pwl_compile_coverage",
                "compile_gate_clear",
                1,
                max_projected_tokens,
                "medium",
            )
        if state.has_gold_dut_include and state.sourced_port_conflicts == 1:
            return ToolDecision(
                "cached_llm_ce_fallback",
                True,
                "single_gold_dut_sourced_port",
                "compile_gate_clear",
                1,
                max_projected_tokens,
                "medium",
            )
        return ToolDecision("cached_llm_ce_fallback", False, "not_compile_coverage_family", "none", 0, 0, "none")

    raise ValueError(f"unknown fallback policy: {policy}")


def _select_fallback_decision(
    *,
    initial_decision: ToolDecision,
    current_decision: ToolDecision,
    fallback_routing_state: str,
    current_status: str,
) -> tuple[ToolDecision, str]:
    """Select the routing view for candidate arbitration.

    The controller evaluates tools as competing candidates.  A local compile
    tool can move a task from compile failure to behavior failure, but that
    should not suppress a CE fallback that the initial strict-EVAS signal already
    identified as a useful candidate.
    """
    if current_status == "PASS":
        return (
            ToolDecision(
                initial_decision.tool,
                False,
                "current_pass_stop",
                "none",
                0,
                0,
                "none",
            ),
            "current",
        )
    if fallback_routing_state == "initial":
        return initial_decision, "initial"
    if fallback_routing_state == "current":
        return current_decision, "current"
    if fallback_routing_state == "either":
        if current_decision.route:
            return current_decision, "current"
        if initial_decision.route:
            chosen = ToolDecision(
                initial_decision.tool,
                initial_decision.route,
                f"initial:{initial_decision.reason}",
                initial_decision.expected_effect,
                initial_decision.max_projected_calls,
                initial_decision.max_projected_tokens,
                initial_decision.risk,
            )
            return chosen, "initial"
        return current_decision, "current"
    raise ValueError(f"unknown fallback routing state: {fallback_routing_state}")


def _cached_usage_meta(cached_sample: Path) -> dict[str, Any]:
    meta_path = cached_sample / "generation_meta.json"
    if not meta_path.exists():
        return {}
    meta = _json_read(meta_path)
    selected = meta.get("selected_sample")
    if selected:
        selected_meta_path = Path(str(selected)) / "generation_meta.json"
        if selected_meta_path.exists():
            meta = _json_read(selected_meta_path)
            meta["selected_generation_meta"] = str(selected_meta_path)
    return meta


def _usage_projection(meta: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "input_tokens",
        "output_tokens",
        "reasoning_tokens",
        "cached_input_tokens",
        "api_elapsed_s",
        "local_eval_elapsed_s",
        "api_call_count",
        "finish_reason",
        "provider",
        "reasoning_mode",
        "mimo_thinking_type",
        "mimo_reasoning_effort",
        "mimo_extra_body_keys",
    )
    return {key: meta[key] for key in keys if key in meta}


def _cached_artifact_audit(
    *,
    cached_sample: Path,
    cached_result_path: Path | None,
    cached_result: dict[str, Any] | None,
    cached_meta: dict[str, Any],
    model: str,
    task_id: str,
    sample_idx: int,
) -> dict[str, Any]:
    issues: list[str] = []
    if not cached_sample.exists():
        issues.append("missing_cached_sample")
    if cached_result_path is None or not cached_result_path.exists():
        issues.append("missing_cached_result")
    if cached_result and cached_result.get("task_id") not in (None, task_id):
        issues.append(f"cached_result_task_mismatch:{cached_result.get('task_id')}")
    if cached_meta:
        if cached_meta.get("task_id") not in (None, task_id):
            issues.append(f"cached_meta_task_mismatch:{cached_meta.get('task_id')}")
        if cached_meta.get("model") not in (None, "", model):
            issues.append(f"cached_meta_model_mismatch:{cached_meta.get('model')}")
    if cached_sample.name != f"sample_{sample_idx}":
        issues.append(f"cached_sample_idx_mismatch:{cached_sample.name}")
    return {
        "ok": not issues,
        "issues": issues,
        "cached_sample": str(cached_sample),
        "cached_result_path": str(cached_result_path) if cached_result_path else "",
        "cached_generation_meta": str(cached_sample / "generation_meta.json"),
    }


def _merge_usage_sum(base: dict[str, Any], addition: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key in ("input_tokens", "output_tokens", "reasoning_tokens", "cached_input_tokens", "api_call_count"):
        out[key] = int(out.get(key, 0) or 0) + int(addition.get(key, 0) or 0)
    out["api_elapsed_s"] = round(float(out.get("api_elapsed_s", 0) or 0) + float(addition.get("api_elapsed_s", 0) or 0), 3)
    for key in ("provider", "reasoning_mode", "mimo_thinking_type", "mimo_reasoning_effort", "finish_reason"):
        if key not in out and addition.get(key):
            out[key] = addition[key]
    if "mimo_extra_body_keys" not in out and addition.get("mimo_extra_body_keys"):
        out["mimo_extra_body_keys"] = addition["mimo_extra_body_keys"]
    return out


def _merge_local_runtime(base: dict[str, Any], elapsed_s: float) -> dict[str, Any]:
    out = dict(base)
    out["local_eval_elapsed_s"] = round(float(out.get("local_eval_elapsed_s", 0) or 0) + elapsed_s, 3)
    return out


def _status_domain(status: str) -> str:
    if status == "PASS":
        return "pass"
    if status in {"FAIL_DUT_COMPILE", "FAIL_TB_COMPILE", "FAIL_INFRA"}:
        return "compile"
    if status == "FAIL_SIM_CORRECTNESS":
        return "behavior"
    return "other"


def _controller_reward(
    before_result: dict[str, Any] | None,
    after_result: dict[str, Any] | None,
    usage: dict[str, Any],
    config: RewardConfig,
) -> dict[str, float]:
    before_scores = _scores(before_result)
    after_scores = _scores(after_result)
    pass_gain = 1.0 if (after_result or {}).get("status") == "PASS" and (before_result or {}).get("status") != "PASS" else 0.0
    compile_gain = (
        after_scores.get("dut_compile", 0.0)
        + after_scores.get("tb_compile", 0.0)
        - before_scores.get("dut_compile", 0.0)
        - before_scores.get("tb_compile", 0.0)
    )
    behavior_gain = after_scores.get("sim_correct", 0.0) - before_scores.get("sim_correct", 0.0)
    total_tokens = int(usage.get("input_tokens", 0) or 0) + int(usage.get("output_tokens", 0) or 0)
    api_elapsed = float(usage.get("api_elapsed_s", 0) or 0)
    local_eval_elapsed = float(usage.get("local_eval_elapsed_s", 0) or 0)
    reward = (
        config.pass_weight * pass_gain
        + config.compile_weight * compile_gain
        + config.behavior_weight * behavior_gain
        - config.token_weight_per_1k * (total_tokens / 1000.0)
        - config.api_second_weight * (api_elapsed + local_eval_elapsed)
    )
    return {
        "reward": round(reward, 6),
        "pass_gain": pass_gain,
        "compile_gain": round(compile_gain, 6),
        "behavior_gain": round(behavior_gain, 6),
        "total_tokens": float(total_tokens),
        "api_elapsed_s": round(api_elapsed, 3),
        "local_eval_elapsed_s": round(local_eval_elapsed, 3),
    }


def _write_trace_files(output_root: Path, rows: list[dict[str, Any]]) -> None:
    jsonl_path = output_root / "tool_controller_trace.jsonl"
    csv_path = output_root / "tool_controller_trace.csv"
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    fields = [
        "task_id",
        "policy",
        "tool",
        "decision",
        "route_reason",
        "source_status",
        "final_status",
        "selected_source",
        "reward",
        "pass_gain",
        "compile_gain",
        "behavior_gain",
        "input_tokens",
        "output_tokens",
        "api_elapsed_s",
        "local_eval_elapsed_s",
        "failure_families",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            flat = {key: row.get(key, "") for key in fields}
            if isinstance(flat.get("failure_families"), list):
                flat["failure_families"] = ";".join(flat["failure_families"])
            writer.writerow(flat)


def _build_summary(manifest_tasks: dict[str, Any], trace_rows: list[dict[str, Any]]) -> dict[str, Any]:
    selected_sources = Counter(str(item.get("selected_source", "")) for item in manifest_tasks.values())
    final_statuses = Counter(str(item.get("final_status", "")) for item in manifest_tasks.values())
    families = Counter(
        family
        for item in manifest_tasks.values()
        for family in item.get("state", {}).get("failure_families", [])
    )
    total_input = sum(int((item.get("projected_usage") or {}).get("input_tokens", 0) or 0) for item in manifest_tasks.values())
    total_output = sum(int((item.get("projected_usage") or {}).get("output_tokens", 0) or 0) for item in manifest_tasks.values())
    total_reasoning = sum(int((item.get("projected_usage") or {}).get("reasoning_tokens", 0) or 0) for item in manifest_tasks.values())
    total_api = sum(float((item.get("projected_usage") or {}).get("api_elapsed_s", 0) or 0) for item in manifest_tasks.values())
    total_local_eval = sum(float((item.get("projected_usage") or {}).get("local_eval_elapsed_s", 0) or 0) for item in manifest_tasks.values())
    total_calls = sum(int((item.get("projected_usage") or {}).get("api_call_count", 0) or 0) for item in manifest_tasks.values())
    rewards = [float(row.get("reward", 0.0) or 0.0) for row in trace_rows]
    return {
        "tasks": len(manifest_tasks),
        "final_status_counts": dict(sorted(final_statuses.items())),
        "selected_source_counts": dict(sorted(selected_sources.items())),
        "failure_family_counts": dict(sorted(families.items())),
        "projected_cost": {
            "api_call_count": total_calls,
            "input_tokens": total_input,
            "output_tokens": total_output,
            "reasoning_tokens": total_reasoning,
            "total_tokens": total_input + total_output,
            "api_elapsed_s": round(total_api, 3),
            "local_eval_elapsed_s": round(total_local_eval, 3),
            "avg_tokens_per_task": round((total_input + total_output) / max(len(manifest_tasks), 1), 3),
            "avg_api_elapsed_s_per_task": round(total_api / max(len(manifest_tasks), 1), 3),
            "avg_local_eval_elapsed_s_per_task": round(total_local_eval / max(len(manifest_tasks), 1), 3),
        },
        "reward": {
            "total": round(sum(rewards), 6),
            "avg_per_task": round(sum(rewards) / max(len(rewards), 1), 6),
        },
    }


def _update_final_meta(
    sample_dir: Path,
    *,
    model: str,
    task_id: str,
    actions: list[dict[str, Any]],
    state: RepairState,
    reward: dict[str, float],
    usage: dict[str, Any],
    selected_source: str,
    elapsed_s: float,
) -> None:
    try:
        meta = _json_read(sample_dir / "generation_meta.json")
    except Exception:
        meta = {}
    for key in (
        "input_tokens",
        "output_tokens",
        "reasoning_tokens",
        "cached_input_tokens",
        "api_elapsed_s",
        "api_call_count",
        "finish_reason",
        "provider",
        "reasoning_mode",
        "mimo_thinking_type",
        "mimo_reasoning_effort",
        "mimo_extra_body_keys",
    ):
        meta.pop(key, None)
    meta.update(
        {
            "model": model,
            "model_slug": model,
            "task_id": task_id,
            "mode": "tool-controller-v0",
            "status": "generated" if usage.get("api_call_count", 0) else "local_or_source_selected",
            "tool_controller": {
                "version": "0.3",
                "selected_source": selected_source,
                "state": asdict(state),
                "actions": actions,
                "reward": reward,
                "elapsed_s": round(elapsed_s, 3),
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "input_tokens": int(usage.get("input_tokens", 0) or 0),
            "output_tokens": int(usage.get("output_tokens", 0) or 0),
            "reasoning_tokens": int(usage.get("reasoning_tokens", 0) or 0),
            "cached_input_tokens": int(usage.get("cached_input_tokens", 0) or 0),
            "api_elapsed_s": round(float(usage.get("api_elapsed_s", 0) or 0), 3),
            "local_eval_elapsed_s": round(float(usage.get("local_eval_elapsed_s", 0) or 0), 3),
            "api_call_count": int(usage.get("api_call_count", 0) or 0),
            **usage,
        }
    )
    _json_write(sample_dir / "generation_meta.json", meta)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bench-dir", required=True, type=Path)
    parser.add_argument("--source-generated-dir", required=True, type=Path)
    parser.add_argument("--source-result-root", required=True, type=Path)
    parser.add_argument("--source-summary", required=True, type=Path)
    parser.add_argument("--cached-fallback-generated-dir", type=Path, default=None)
    parser.add_argument("--cached-fallback-result-root", type=Path, default=None)
    parser.add_argument("--output-generated-dir", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--model", default="kimi-k2.5")
    parser.add_argument("--sample-idx", type=int, default=0)
    parser.add_argument("--timeout-s", type=int, default=240)
    parser.add_argument(
        "--selected-only",
        action="store_true",
        help="Materialize only tasks selected by --source-summary instead of copying the full generated root.",
    )
    parser.add_argument(
        "--fallback-policy",
        choices=["never", "pass-efficient", "compile-coverage", "all-compile"],
        default="pass-efficient",
    )
    parser.add_argument(
        "--fallback-routing-state",
        choices=["initial", "current", "either"],
        default="either",
        help=(
            "Which repair-state view can route CE/LLM fallback.  'either' treats "
            "fallback as an independent candidate if either the initial or "
            "post-local-tool state routes it."
        ),
    )
    parser.add_argument(
        "--max-fallback-tokens",
        type=int,
        default=8192,
        help="Projected token budget used in tool-decision manifests for one CE/LLM fallback call.",
    )
    parser.add_argument("--reward-pass-weight", type=float, default=RewardConfig.pass_weight)
    parser.add_argument("--reward-compile-weight", type=float, default=RewardConfig.compile_weight)
    parser.add_argument("--reward-behavior-weight", type=float, default=RewardConfig.behavior_weight)
    parser.add_argument("--reward-token-weight-per-1k", type=float, default=RewardConfig.token_weight_per_1k)
    parser.add_argument("--reward-api-second-weight", type=float, default=RewardConfig.api_second_weight)
    parser.add_argument("--disable-local-tools", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source_generated_dir.resolve()
    output_root = args.output_generated_dir.resolve()
    selected = _compile_failures_from_summary(args.source_summary)
    if args.selected_only:
        _copy_selected_samples(
            source_root,
            output_root,
            model=args.model,
            sample_idx=args.sample_idx,
            task_ids=set(selected),
        )
    else:
        if output_root.exists():
            shutil.rmtree(output_root)
        shutil.copytree(source_root, output_root)
    if args.output_root.exists():
        shutil.rmtree(args.output_root)
    args.output_root.mkdir(parents=True, exist_ok=True)

    task_dirs = {
        task_id: task_dir
        for task_id, task_dir in list_bench_task_dirs(args.bench_dir, selected=set(selected))
    }
    reward_config = RewardConfig(
        pass_weight=args.reward_pass_weight,
        compile_weight=args.reward_compile_weight,
        behavior_weight=args.reward_behavior_weight,
        token_weight_per_1k=args.reward_token_weight_per_1k,
        api_second_weight=args.reward_api_second_weight,
    )
    trace_rows: list[dict[str, Any]] = []
    manifest: dict[str, Any] = {
        "mode": "tool-controller-v0",
        "controller_version": "0.3",
        "source_generated_dir": str(source_root),
        "source_result_root": str(args.source_result_root.resolve()),
        "source_summary": str(args.source_summary.resolve()),
        "cached_fallback_generated_dir": str(args.cached_fallback_generated_dir.resolve()) if args.cached_fallback_generated_dir else "",
        "cached_fallback_result_root": str(args.cached_fallback_result_root.resolve()) if args.cached_fallback_result_root else "",
        "output_generated_dir": str(output_root),
        "output_root": str(args.output_root.resolve()),
        "model": args.model,
        "sample_idx": args.sample_idx,
        "fallback_policy": args.fallback_policy,
        "fallback_routing_state": args.fallback_routing_state,
        "selected_only": bool(args.selected_only),
        "disable_local_tools": bool(args.disable_local_tools),
        "reward_config": asdict(reward_config),
        "selected_tasks": len(selected),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tasks": {},
    }

    for task_id, info in sorted(selected.items()):
        task_start = time.perf_counter()
        sample_dir = _task_sample_dir(output_root, args.model, task_id, args.sample_idx)
        task_dir = task_dirs.get(task_id)
        actions: list[dict[str, Any]] = []
        projected_usage: dict[str, Any] = {}
        selected_source = "source"
        if task_dir is None or not sample_dir.exists():
            manifest["tasks"][task_id] = {"error": "missing_task_or_sample", "actions": actions}
            continue

        task_meta = _json_read(task_dir / "meta.json") if (task_dir / "meta.json").exists() else {}
        current_result = _existing_result(args.source_result_root, task_id) or {
            "status": info["status"],
            "scores": {},
            "evas_notes": info["notes"],
        }
        source_result = current_result
        current_rank = _compile_closure_rank(task_id, current_result)
        current_notes = _result_notes(current_result, info["notes"])
        initial_state = _extract_state(
            task_id=task_id,
            task_meta=task_meta,
            result=current_result,
            fallback_notes=info["notes"],
        )
        initial_fallback_decision = _fallback_decision(
            initial_state,
            args.fallback_policy,
            max_projected_tokens=args.max_fallback_tokens,
        )

        if not args.disable_local_tools:
            candidate_dir = args.output_root / "_candidates" / task_id / "local_batch"
            _copy_sample(sample_dir, candidate_dir)
            local_manifest = apply_compile_skill_actions(candidate_dir, notes=current_notes)
            edits = [str(edit) for edit in local_manifest.get("edits", [])]
            action: dict[str, Any] = {
                "tool": "local_compile_skill_batch",
                "tool_type": "deterministic_local",
                "selected_skills": local_manifest.get("selected_skills", []),
                "edits": edits,
                "before_status": current_result.get("status"),
                "before_rank": list(current_rank),
                "decision": "no_edit",
            }
            if edits:
                local_eval_start = time.perf_counter()
                scored = _score_candidate(
                    task_id=task_id,
                    task_dir=task_dir,
                    sample_dir=candidate_dir,
                    output_root=args.output_root / "quick" / task_id / "local_batch",
                    model=args.model,
                    sample_idx=args.sample_idx,
                    timeout_s=args.timeout_s,
                )
                local_eval_elapsed_s = time.perf_counter() - local_eval_start
                projected_usage = _merge_local_runtime(projected_usage, local_eval_elapsed_s)
                next_rank = _compile_closure_rank(task_id, scored)
                improved = next_rank > current_rank
                action.update({
                    "after_status": scored.get("status"),
                    "after_rank": list(next_rank),
                    "improved": improved,
                    "local_eval_elapsed_s": round(local_eval_elapsed_s, 3),
                })
                if improved:
                    _copy_sample(candidate_dir, sample_dir)
                    current_result = scored
                    current_rank = next_rank
                    current_notes = _result_notes(scored, current_notes)
                    selected_source = "local_compile_skill_batch"
                    action["decision"] = "accepted"
                else:
                    action["decision"] = "rejected"
            actions.append(action)

        current_state = _extract_state(
            task_id=task_id,
            task_meta=task_meta,
            result=current_result,
            fallback_notes=current_notes,
        )
        current_fallback_decision = _fallback_decision(
            current_state,
            args.fallback_policy,
            max_projected_tokens=args.max_fallback_tokens,
        )
        fallback_decision, selected_routing_state = _select_fallback_decision(
            initial_decision=initial_fallback_decision,
            current_decision=current_fallback_decision,
            fallback_routing_state=args.fallback_routing_state,
            current_status=str(current_result.get("status", "")),
        )
        action = {
            "tool": "cached_llm_ce_fallback",
            "tool_type": "llm_cached_fallback",
            "route": fallback_decision.route,
            "route_reason": fallback_decision.reason,
            "fallback_routing_state": selected_routing_state,
            "fallback_routing_policy": args.fallback_routing_state,
            "expected_effect": fallback_decision.expected_effect,
            "max_projected_calls": fallback_decision.max_projected_calls,
            "max_projected_tokens": fallback_decision.max_projected_tokens,
            "risk": fallback_decision.risk,
            "before_status": current_result.get("status"),
            "before_rank": list(current_rank),
            "initial_tool_decision": asdict(initial_fallback_decision),
            "current_tool_decision": asdict(current_fallback_decision),
            "initial_routing_state": asdict(initial_state),
            "routing_state": asdict(current_state),
            "decision": "not_routed",
        }
        if fallback_decision.route and args.cached_fallback_generated_dir and args.cached_fallback_result_root:
            cached_sample = _task_sample_dir(
                args.cached_fallback_generated_dir,
                args.model,
                task_id,
                args.sample_idx,
            )
            cached_result_path = _result_path(args.cached_fallback_result_root, task_id)
            cached_result = _json_read(cached_result_path) if cached_result_path else None
            cached_meta = _cached_usage_meta(cached_sample) if cached_sample.exists() else {}
            cached_audit = _cached_artifact_audit(
                cached_sample=cached_sample,
                cached_result_path=cached_result_path,
                cached_result=cached_result,
                cached_meta=cached_meta,
                model=args.model,
                task_id=task_id,
                sample_idx=args.sample_idx,
            )
            action["cached_artifact_audit"] = cached_audit
            if cached_audit["ok"] and cached_result:
                cached_eval_start = time.perf_counter()
                verified_result = _score_candidate(
                    task_id=task_id,
                    task_dir=task_dir,
                    sample_dir=cached_sample,
                    output_root=args.output_root / "quick" / task_id / "cached_fallback",
                    model=args.model,
                    sample_idx=args.sample_idx,
                    timeout_s=args.timeout_s,
                )
                cached_eval_elapsed_s = time.perf_counter() - cached_eval_start
                usage = _usage_projection(cached_meta)
                usage = _merge_local_runtime(usage, cached_eval_elapsed_s)
                projected_usage = _merge_usage_sum(projected_usage, usage)
                projected_usage = _merge_local_runtime(projected_usage, cached_eval_elapsed_s)
                cached_rank = _compile_closure_rank(task_id, verified_result)
                improved = cached_rank > current_rank
                action.update({
                    "cached_declared_status": cached_result.get("status"),
                    "cached_status": verified_result.get("status"),
                    "cached_verified": True,
                    "cached_verification_elapsed_s": round(cached_eval_elapsed_s, 3),
                    "cached_rank": list(cached_rank),
                    "projected_usage": usage,
                    "improved": improved,
                    "decision": "accepted" if improved else "rejected",
                })
                if improved:
                    _copy_sample(cached_sample, sample_dir)
                    current_result = verified_result
                    current_rank = cached_rank
                    current_notes = _result_notes(verified_result, current_notes)
                    selected_source = "cached_llm_ce_fallback"
            else:
                action.update({
                    "decision": "cached_artifact_rejected",
                    "cached_sample_exists": cached_sample.exists(),
                    "cached_result_exists": bool(cached_result),
                })
        actions.append(action)

        reward = _controller_reward(source_result, current_result, projected_usage, reward_config)
        trace_row = {
            "task_id": task_id,
            "policy": args.fallback_policy,
            "source_status": source_result.get("status"),
            "source_domain": _status_domain(str(source_result.get("status", ""))),
            "final_status": current_result.get("status"),
            "final_domain": _status_domain(str(current_result.get("status", ""))),
            "selected_source": selected_source,
            "tool": selected_source,
            "decision": actions[-1].get("decision", ""),
            "route_reason": actions[-1].get("route_reason", ""),
            "state": asdict(initial_state),
            "failure_families": initial_state.failure_families,
            "reward": reward["reward"],
            "pass_gain": reward["pass_gain"],
            "compile_gain": reward["compile_gain"],
            "behavior_gain": reward["behavior_gain"],
            "input_tokens": int(projected_usage.get("input_tokens", 0) or 0),
            "output_tokens": int(projected_usage.get("output_tokens", 0) or 0),
            "api_elapsed_s": float(projected_usage.get("api_elapsed_s", 0) or 0),
            "actions": actions,
        }
        trace_rows.append(trace_row)

        _update_final_meta(
            sample_dir,
            model=args.model,
            task_id=task_id,
            actions=actions,
            state=initial_state,
            reward=reward,
            usage=projected_usage,
            selected_source=selected_source,
            elapsed_s=time.perf_counter() - task_start,
        )
        _json_write(args.output_root / "best" / task_id / "result.json", current_result)
        manifest["tasks"][task_id] = {
            "source_status": info["status"],
            "final_status": current_result.get("status"),
            "final_rank": list(current_rank),
            "state": asdict(initial_state),
            "selected_source": selected_source,
            "actions": actions,
            "reward": reward,
            "projected_usage": projected_usage,
        }

    manifest["summary"] = _build_summary(manifest["tasks"], trace_rows)
    _json_write(output_root / "tool_controller_manifest.json", manifest)
    _write_trace_files(output_root, trace_rows)
    print(json.dumps({"output_generated_dir": str(output_root), "selected_tasks": len(selected)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
