#!/usr/bin/env python3
"""Audit invariants for a materialized tool-controller run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sample_meta_path(root: Path, model: str, task_id: str, sample_idx: int) -> Path:
    return root / model / task_id / f"sample_{sample_idx}" / "generation_meta.json"


def _num(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _status_from_result_root(result_root: Path, task_id: str) -> str:
    for name in ("evas_result.json", "result.json"):
        path = result_root / task_id / name
        if path.exists():
            return str(_read_json(path).get("status", ""))
    return ""


def audit(args: argparse.Namespace) -> tuple[list[str], dict[str, Any]]:
    generated_root = args.generated_dir.resolve()
    manifest_path = generated_root / "tool_controller_manifest.json"
    manifest = _read_json(manifest_path)
    tasks = manifest.get("tasks", {})
    errors: list[str] = []

    trace_path = generated_root / "tool_controller_trace.jsonl"
    trace_rows = []
    if not trace_path.exists():
        errors.append("missing_trace_jsonl")
    else:
        for line_no, line in enumerate(trace_path.read_text(encoding="utf-8").splitlines(), start=1):
            try:
                trace_rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                errors.append(f"trace_json_decode_error:{line_no}:{exc}")

    if len(trace_rows) != len(tasks):
        errors.append(f"trace_task_count_mismatch:trace={len(trace_rows)}:tasks={len(tasks)}")

    summary = manifest.get("summary", {})
    projected = summary.get("projected_cost", {})
    sums = {
        "api_call_count": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "reasoning_tokens": 0,
        "total_tokens": 0,
        "api_elapsed_s": 0.0,
        "local_eval_elapsed_s": 0.0,
    }

    for task_id, info in sorted(tasks.items()):
        usage = info.get("projected_usage") or {}
        sample_meta_path = _sample_meta_path(generated_root, args.model, task_id, args.sample_idx)
        if not sample_meta_path.exists():
            errors.append(f"missing_generation_meta:{task_id}")
            continue
        meta = _read_json(sample_meta_path)
        for key in ("input_tokens", "output_tokens", "reasoning_tokens", "api_call_count"):
            if int(_num(meta.get(key))) != int(_num(usage.get(key))):
                errors.append(f"meta_usage_mismatch:{task_id}:{key}:meta={meta.get(key)}:manifest={usage.get(key)}")
        for key in ("api_elapsed_s", "local_eval_elapsed_s"):
            if abs(_num(meta.get(key)) - _num(usage.get(key))) > 1e-3:
                errors.append(f"meta_usage_mismatch:{task_id}:{key}:meta={meta.get(key)}:manifest={usage.get(key)}")

        selected_source = str(info.get("selected_source", ""))
        if selected_source == "source" and (
            int(_num(usage.get("input_tokens"))) or int(_num(usage.get("output_tokens"))) or int(_num(usage.get("api_call_count")))
        ):
            errors.append(f"source_selected_has_llm_cost:{task_id}")
        if selected_source == "cached_llm_ce_fallback":
            accepted = [
                action for action in info.get("actions", [])
                if action.get("tool") == "cached_llm_ce_fallback" and action.get("decision") == "accepted"
            ]
            if not accepted:
                errors.append(f"cached_selected_without_accepted_action:{task_id}")
            for action in accepted:
                audit_info = action.get("cached_artifact_audit") or {}
                if not audit_info.get("ok"):
                    errors.append(f"accepted_cached_audit_not_ok:{task_id}:{audit_info.get('issues')}")
        for action in info.get("actions", []):
            if action.get("tool") == "cached_llm_ce_fallback" and action.get("decision") == "accepted":
                if not (action.get("projected_usage") or {}).get("api_call_count"):
                    errors.append(f"accepted_cached_missing_usage:{task_id}")
                if not action.get("cached_verified"):
                    errors.append(f"accepted_cached_not_rescored:{task_id}")

        result_status = _status_from_result_root(args.result_root, task_id) if args.result_root else ""
        if result_status and result_status != info.get("final_status"):
            errors.append(f"result_status_mismatch:{task_id}:manifest={info.get('final_status')}:result={result_status}")

        sums["api_call_count"] += int(_num(usage.get("api_call_count")))
        sums["input_tokens"] += int(_num(usage.get("input_tokens")))
        sums["output_tokens"] += int(_num(usage.get("output_tokens")))
        sums["reasoning_tokens"] += int(_num(usage.get("reasoning_tokens")))
        sums["api_elapsed_s"] += _num(usage.get("api_elapsed_s"))
        sums["local_eval_elapsed_s"] += _num(usage.get("local_eval_elapsed_s"))
    sums["total_tokens"] = sums["input_tokens"] + sums["output_tokens"]
    sums["api_elapsed_s"] = round(sums["api_elapsed_s"], 3)
    sums["local_eval_elapsed_s"] = round(sums["local_eval_elapsed_s"], 3)

    for key, value in sums.items():
        expected = projected.get(key)
        if isinstance(value, float):
            if abs(_num(expected) - value) > 1e-3:
                errors.append(f"summary_cost_mismatch:{key}:summary={expected}:sum={value}")
        elif int(_num(expected)) != int(value):
            errors.append(f"summary_cost_mismatch:{key}:summary={expected}:sum={value}")

    sample_count = len(list(generated_root.glob(f"{args.model}/*/sample_{args.sample_idx}/generation_meta.json")))
    if sample_count != len(tasks):
        errors.append(f"sample_count_mismatch:samples={sample_count}:tasks={len(tasks)}")

    report = {
        "generated_dir": str(generated_root),
        "tasks": len(tasks),
        "trace_rows": len(trace_rows),
        "sample_count": sample_count,
        "computed_cost": sums,
        "summary_cost": projected,
        "errors": errors,
    }
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated-dir", required=True, type=Path)
    parser.add_argument("--result-root", type=Path, default=None)
    parser.add_argument("--model", default="mimo-v2.5-pro")
    parser.add_argument("--sample-idx", type=int, default=0)
    parser.add_argument("--output-json", type=Path, default=None)
    args = parser.parse_args()

    errors, report = audit(args)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
