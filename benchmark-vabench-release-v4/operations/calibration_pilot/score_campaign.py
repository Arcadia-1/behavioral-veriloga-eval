#!/usr/bin/env python3
"""Evaluate completed calibration submissions and aggregate their telemetry."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import statistics
from typing import Any


HERE = Path(__file__).resolve().parent
RUNNER_PATH = HERE / "run_campaign.py"
SPEC = importlib.util.spec_from_file_location("v4_calibration_runner", RUNNER_PATH)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)

SUBMITTED = {"submitted", "submitted_at_budget"}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def provider_usage(events: list[dict[str, Any]]) -> dict[str, int]:
    totals: Counter[str] = Counter()
    for event in events:
        for key, value in (event.get("provider_usage") or {}).items():
            if isinstance(value, int):
                totals[key] += value
    return dict(sorted(totals.items()))


def event_telemetry(events: list[dict[str, Any]]) -> dict[str, Any]:
    tools = Counter(
        str(event["name"]) for event in events
        if event.get("type") == "tool" and event.get("name")
    )
    output_tokens = 0
    reasoning_tokens = 0
    visible_tokens = 0
    budget_hits = 0
    for event in events:
        if event.get("type") != "model":
            continue
        usage = event.get("provider_usage") or {}
        output = event.get("provider_output_tokens", usage.get("completion_tokens", 0))
        details = usage.get("completion_tokens_details") or {}
        reasoning = event.get(
            "provider_reasoning_tokens", details.get("reasoning_tokens", usage.get("reasoning_tokens", 0))
        )
        visible = event.get("provider_visible_tokens")
        output = int(output) if isinstance(output, int) else 0
        reasoning = int(reasoning) if isinstance(reasoning, int) else 0
        visible = int(visible) if isinstance(visible, int) else max(0, output - reasoning)
        output_tokens += output
        reasoning_tokens += reasoning
        visible_tokens += visible
        budget_hits += RUNNER.model_event_hit_limit(event)
    return {
        "model_calls": sum(event.get("type") == "model" for event in events),
        "model_elapsed_s": sum(
            float(event.get("elapsed_s", 0.0)) for event in events if event.get("type") == "model"
        ),
        "tool_calls": dict(sorted(tools.items())),
        "tool_calls_total": sum(tools.values()),
        "feedback_calls": tools.get("feedback", 0),
        "provider_output_tokens_total": output_tokens,
        "provider_reasoning_tokens_total": reasoning_tokens,
        "provider_visible_tokens_total": visible_tokens,
        "budget_hit_model_calls": budget_hits,
    }


def elapsed_seconds(result: dict[str, Any]) -> float | None:
    try:
        started = datetime.fromisoformat(str(result["started_at"]))
        finished = datetime.fromisoformat(str(result["finished_at"]))
    except (KeyError, TypeError, ValueError):
        return None
    return max(0.0, (finished - started).total_seconds())


def evaluate_cell(result_path: Path, command: str | None, timeout_s: int) -> dict[str, Any]:
    result = read_json(result_path)
    cell = result["cell"]
    runtime = result_path.parents[1]
    telemetry = event_telemetry(result.get("events") or [])
    output_tokens = result.get("output_tokens")
    if not isinstance(output_tokens, int):
        provider_total = telemetry["provider_output_tokens_total"]
        output_tokens = provider_total if provider_total > 0 else result.get("working_tokens", 0)
    row: dict[str, Any] = {
        "cell_id": cell["cell_id"],
        "family_id": cell["family_id"],
        "task_id": cell["task_id"],
        "form": cell["form"],
        "mode": cell["mode"],
        "submission_status": result["status"],
        "output_tokens": output_tokens,
        "working_tokens": result.get("working_tokens", result.get("output_tokens", 0)),
        "provider_usage": provider_usage(result.get("events") or []),
        "telemetry": telemetry,
        "episode_elapsed_s": elapsed_seconds(result),
    }
    if result["status"] not in SUBMITTED:
        row["judge_status"] = "not_submitted"
    elif not command:
        row["judge_status"] = "not_run"
    else:
        try:
            judged = RUNNER.command_result(command, runtime, timeout_s)
        except Exception as exc:
            row["judge_status"] = "judge_error"
            row["judge_error"] = {
                "error_type": type(exc).__name__,
                "error": str(exc)[:2000],
            }
        else:
            row["judge_status"] = "pass" if judged["returncode"] == 0 else "fail"
            row["judge"] = judged
    return row


def summarize(rows: list[dict[str, Any]], judge_kind: str) -> dict[str, Any]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[f"form:{row['form']}"][row["judge_status"]] += 1
        grouped[f"mode:{row['mode']}"][row["judge_status"]] += 1
    telemetry_by_mode = {}
    for mode in sorted({str(row["mode"]) for row in rows}):
        selected = [row for row in rows if row["mode"] == mode]
        output = [int(row.get("output_tokens", row.get("working_tokens", 0)) or 0) for row in selected]
        elapsed = [float(row["episode_elapsed_s"]) for row in selected if row.get("episode_elapsed_s") is not None]
        telemetry_by_mode[mode] = {
            "cell_count": len(selected),
            "output_tokens_total": sum(output),
            "output_tokens_median": statistics.median(output),
            "working_tokens_total": sum(output),
            "working_tokens_median": statistics.median(output),
            "episode_elapsed_s_median": statistics.median(elapsed) if elapsed else None,
            "model_calls_total": sum(int(row.get("telemetry", {}).get("model_calls", 0)) for row in selected),
            "tool_calls_total": sum(int(row.get("telemetry", {}).get("tool_calls_total", 0)) for row in selected),
            "feedback_calls_total": sum(int(row.get("telemetry", {}).get("feedback_calls", 0)) for row in selected),
            "provider_reasoning_tokens_total": sum(
                int(row.get("telemetry", {}).get("provider_reasoning_tokens_total", 0))
                for row in selected
            ),
            "budget_hit_model_calls": sum(
                int(row.get("telemetry", {}).get("budget_hit_model_calls", 0))
                for row in selected
            ),
        }
    return {
        "schema_version": "v4-calibration-score-report-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "judge_kind": judge_kind,
        "score_authority": "final" if judge_kind == "final_spectre" else "provisional_feedback_only",
        "cell_count": len(rows),
        "submission_statuses": dict(Counter(row["submission_status"] for row in rows)),
        "judge_statuses": dict(Counter(row["judge_status"] for row in rows)),
        "breakdown": {key: dict(value) for key, value in sorted(grouped.items())},
        "telemetry_by_mode": telemetry_by_mode,
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-output", type=Path, required=True)
    parser.add_argument("--judge-kind", choices=("feedback_evas", "final_spectre"), required=True)
    parser.add_argument("--judge-command")
    parser.add_argument("--timeout-s", type=int, default=120)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")
    result_paths = sorted(args.campaign_output.glob("v4-*/evidence/campaign_result.json"))
    if not result_paths:
        raise SystemExit(f"no campaign results under {args.campaign_output}")
    if args.workers == 1:
        rows = [evaluate_cell(path, args.judge_command, args.timeout_s) for path in result_paths]
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            rows = list(pool.map(
                lambda path: evaluate_cell(path, args.judge_command, args.timeout_s),
                result_paths,
            ))
    report = summarize(rows, args.judge_kind)
    output = args.output or args.campaign_output / f"SCORE_{args.judge_kind.upper()}.json"
    write_json(output, report)
    print(json.dumps({key: report[key] for key in (
        "judge_kind", "score_authority", "cell_count", "submission_statuses", "judge_statuses"
    )}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
