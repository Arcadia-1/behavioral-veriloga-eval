#!/usr/bin/env python3
"""Unified vaBench v4 API campaign entrypoint.

This is the one public runner for hosted-model API tests.  It delegates to the
current v4 tri-form campaign builder and OpenAI-compatible campaign runner:

1. build a v4 campaign manifest from the selected 10-family / 30-task pilot;
2. run selected cells through the provider endpoint;
3. keep a compact wrapper summary next to the campaign output.

The token budget is a provider *completion/working-token* ceiling.  It includes
provider-reported hidden reasoning tokens when the provider reports them.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v4"
OPERATIONS = PACKAGE / "operations"
CALIBRATION = OPERATIONS / "calibration_pilot"
DEFAULT_RELEASE = PACKAGE / "release" / "tri-form-v4-1200-final"
DEFAULT_SELECTION = OPERATIONS / "api_pilot_selection_10_20260714.json"
BUILD_CAMPAIGN = CALIBRATION / "build_campaign.py"
RUN_CAMPAIGN = CALIBRATION / "run_campaign.py"
FEEDBACK_ADAPTER = CALIBRATION / "feedback_adapter.py"
RESULTS_ROOT = ROOT / "results"

DEFAULT_MODEL = "qwen3.5-flash"
DEFAULT_BASE_URL = "https://www.cun.ai/v1"
DEFAULT_API_KEY_ENV = "VAEVAS_API_KEY"
DEFAULT_MAX_WORKING_TOKENS = 65_536
DEFAULT_REQUEST_TIMEOUT_S = 600
MODES = tuple(f"G{i}" for i in range(6))
FORM_ORDER = {"dut": 0, "testbench": 1, "bugfix": 2}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def resolve_repo_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    root_relative = ROOT / path
    if root_relative.exists() or str(path).startswith(("benchmark-", "runners/", "results/")):
        return root_relative
    cwd_relative = Path.cwd() / path
    if cwd_relative.exists():
        return cwd_relative
    return root_relative


def model_slug(model: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", model).strip("-._")
    return slug[:120] or "model"


def output_root_for(model: str, tag: str | None) -> Path:
    stamp = tag or datetime.now().strftime("%Y%m%d-%H%M%S")
    return RESULTS_ROOT / f"vabench-v4-api-eval-{model_slug(model)}-{stamp}"


def shell_join(cmd: list[str]) -> str:
    return shlex.join(str(part) for part in cmd)


def default_feedback_command() -> str:
    return shell_join([sys.executable, str(FEEDBACK_ADAPTER)])


def selected_tasks(release: Path, selection: Path) -> list[dict[str, Any]]:
    selection_payload = read_json(selection)
    family_ids = {str(row["family_id"]) for row in selection_payload["families"]}
    tasks = [
        row for row in read_json(release / "TASK_INDEX.json")["tasks"]
        if str(row.get("family_id")) in family_ids
    ]
    tasks.sort(key=lambda row: (str(row["family_id"]), FORM_ORDER.get(str(row["form"]), 99)))
    return tasks


def task_label(row: dict[str, Any]) -> str:
    path = str(row.get("path") or "")
    return str(row.get("task_slug") or row.get("slug") or Path(path).name or row.get("task_id"))


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def parse_filters(args: argparse.Namespace) -> dict[str, set[str]]:
    return {
        "mode": set(args.mode),
        "form": set(args.form),
        "family_id": set(args.family_id),
        "task_id": set(args.task_id),
    }


def filter_cells(cells: list[dict[str, Any]], filters: dict[str, set[str]]) -> list[dict[str, Any]]:
    selected = cells
    if filters["mode"]:
        selected = [row for row in selected if str(row.get("mode")) in filters["mode"]]
    if filters["form"]:
        selected = [row for row in selected if str(row.get("form")) in filters["form"]]
    if filters["family_id"]:
        selected = [row for row in selected if str(row.get("family_id")) in filters["family_id"]]
    if filters["task_id"]:
        selected = [row for row in selected if str(row.get("task_id")) in filters["task_id"]]
    return selected


def filtered_campaign_if_needed(campaign_path: Path, output_root: Path, filters: dict[str, set[str]]) -> Path:
    if not any(filters.values()):
        return campaign_path
    campaign = read_json(campaign_path)
    cells = filter_cells(list(campaign["cells"]), filters)
    if not cells:
        raise SystemExit("no campaign cells match the requested filters")
    filtered = dict(campaign)
    filtered["parent_campaign"] = str(campaign_path)
    filtered["filters"] = {key: sorted(value) for key, value in filters.items() if value}
    filtered["cells"] = cells
    filtered["family_count"] = len({str(row["family_id"]) for row in cells})
    filtered["task_count"] = len({str(row["task_id"]) for row in cells})
    filtered["mode_count"] = len({str(row["mode"]) for row in cells})
    filtered["cell_count"] = len(cells)
    filtered_path = output_root / "campaign.filtered.json"
    write_json(filtered_path, filtered)
    return filtered_path


def build_campaign_command(args: argparse.Namespace, campaign_path: Path) -> list[str]:
    return [
        sys.executable,
        str(BUILD_CAMPAIGN),
        "--release",
        str(args.release),
        "--selection",
        str(args.selection),
        "--output",
        str(campaign_path),
        "--model-provider",
        args.model_provider,
        "--model",
        args.model,
        "--max-working-tokens",
        str(args.max_working_tokens),
        "--repetitions",
        str(args.repetitions),
    ]


def run_campaign_command(
    args: argparse.Namespace,
    *,
    campaign_path: Path,
    run_output: Path,
    feedback_command: str | None,
) -> list[str]:
    cmd = [
        sys.executable,
        str(RUN_CAMPAIGN),
        "--campaign",
        str(campaign_path),
        "--release",
        str(args.release),
        "--output",
        str(run_output),
        "--base-url",
        args.base_url,
        "--api-key-env",
        args.api_key_env,
        "--temperature",
        str(args.temperature),
        "--request-timeout-s",
        str(args.request_timeout_s),
        "--tool-timeout-s",
        str(args.tool_timeout_s),
        "--judge-timeout-s",
        str(args.judge_timeout_s),
        "--workers",
        str(args.workers),
    ]
    if args.api_key_file:
        cmd.extend(["--api-key-file", str(args.api_key_file)])
    if args.cell:
        cmd.extend(["--cell", args.cell])
    if args.limit is not None:
        cmd.extend(["--limit", str(args.limit)])
    if feedback_command:
        cmd.extend(["--feedback-command", feedback_command])
    if args.final_judge_command:
        cmd.extend(["--final-judge-command", args.final_judge_command])
    if args.dry_run:
        cmd.append("--dry-run")
    if args.resume:
        cmd.append("--resume")
    return cmd


def run_command(cmd: list[str]) -> int:
    completed = subprocess.run(cmd, cwd=ROOT, check=False)
    return completed.returncode


def write_wrapper_summary(
    *,
    output_root: Path,
    model: str,
    base_url: str,
    api_key_env: str,
    campaign_path: Path,
    run_output: Path,
    build_cmd: list[str] | None,
    run_cmd: list[str],
    dry_run: bool,
    max_working_tokens: int,
    rc: int,
) -> dict[str, Any]:
    run_summary_path = run_output / "SUMMARY.json"
    run_summary = read_json(run_summary_path) if run_summary_path.is_file() else {}
    run_statuses = run_summary.get("statuses") or {}
    has_runner_error = bool(run_statuses.get("runner_error")) if isinstance(run_statuses, dict) else False
    payload: dict[str, Any] = {
        "schema_version": "vabench-v4-api-wrapper-summary-v1",
        "created_at": now_utc(),
        "status": "ok" if rc == 0 and not has_runner_error else "failed",
        "returncode": rc,
        "model": model,
        "base_url": base_url,
        "api_key_env": api_key_env,
        "dry_run": dry_run,
        "max_working_tokens": max_working_tokens,
        "campaign": str(campaign_path),
        "run_output": str(run_output),
        "build_command": shell_join(build_cmd) if build_cmd else None,
        "run_command": shell_join(run_cmd),
        "run_summary": run_summary,
    }
    write_json(output_root / "summary.json", payload)
    lines = [
        "# vaBench v4 API runner summary",
        "",
        f"- status: `{payload['status']}`",
        f"- model: `{model}`",
        f"- base URL: `{base_url}`",
        f"- dry run: `{dry_run}`",
        f"- max working tokens: `{max_working_tokens}`",
        f"- campaign: `{rel(campaign_path)}`",
        f"- output: `{rel(run_output)}`",
    ]
    if run_summary:
        lines.append(f"- run statuses: `{json.dumps(run_summary.get('statuses', {}), sort_keys=True)}`")
    (output_root / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def print_roster(args: argparse.Namespace) -> int:
    rows = selected_tasks(args.release, args.selection)
    filters = parse_filters(args)
    pseudo_cells = [
        {
            "family_id": str(task["family_id"]),
            "task_id": str(task["task_id"]),
            "form": str(task["form"]),
            "mode": mode,
        }
        for task in rows
        for mode in MODES
        for _ in range(args.repetitions)
    ]
    filtered_cells = filter_cells(pseudo_cells, filters)
    if args.limit is not None:
        filtered_cells = filtered_cells[: args.limit]
    payload = {
        "schema_version": "vabench-v4-api-runner-roster-v1",
        "runner": rel(Path(__file__)),
        "release": rel(args.release),
        "selection": rel(args.selection),
        "model_default": DEFAULT_MODEL,
        "base_url_default": DEFAULT_BASE_URL,
        "api_key_env_default": DEFAULT_API_KEY_ENV,
        "max_working_tokens_default": DEFAULT_MAX_WORKING_TOKENS,
        "family_count": len({str(row["family_id"]) for row in rows}),
        "task_count": len(rows),
        "mode_count": len(MODES),
        "cell_count": len(filtered_cells),
        "forms": count_by(rows, "form"),
        "modes": list(MODES),
        "tasks": [
            {
                "family_id": str(row["family_id"]),
                "task_id": str(row["task_id"]),
                "form": str(row["form"]),
                "label": task_label(row),
            }
            for row in rows
        ],
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    print(
        f"vaBench v4 API pilot: {payload['family_count']} families, "
        f"{payload['task_count']} tasks, {payload['cell_count']} selected cells"
    )
    print(f"release: {payload['release']}")
    print(f"selection: {payload['selection']}")
    print(f"default model/base_url: {DEFAULT_MODEL} @ {DEFAULT_BASE_URL}")
    print(f"default max working tokens: {DEFAULT_MAX_WORKING_TOKENS}")
    for row in payload["tasks"]:
        print(f"- {row['task_id']} [{row['form']}] family={row['family_id']} {row['label']}")
    return 0


def parser_for() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List the current 10-family / 30-task v4 API pilot roster.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable roster or wrapper summary.")
    parser.add_argument("--print-commands", action="store_true", help="Print build/run commands without executing them.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--model-provider", default="openai-compatible")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key-env", default=DEFAULT_API_KEY_ENV)
    parser.add_argument("--api-key-file", type=Path)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--campaign", type=Path, help="Use an existing campaign instead of building a new one.")
    parser.add_argument("--campaign-output", type=Path, help="Path for the generated campaign manifest.")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--tag")
    parser.add_argument(
        "--max-output-tokens",
        "--max-working-tokens",
        dest="max_working_tokens",
        type=int,
        default=DEFAULT_MAX_WORKING_TOKENS,
        help="Provider completion/working-token ceiling per episode.",
    )
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--mode", action="append", choices=MODES, default=[], help="Filter campaign cells by prompt mode.")
    parser.add_argument("--form", action="append", choices=sorted(FORM_ORDER), default=[], help="Filter cells by form.")
    parser.add_argument("--family-id", action="append", default=[], help="Filter cells by v4 family id, e.g. 342.")
    parser.add_argument("--task-id", action="append", default=[], help="Filter cells by v4 task id, e.g. v4-342.")
    parser.add_argument("--cell", help="Run exactly one campaign cell id after any campaign filtering.")
    parser.add_argument("--limit", type=int, help="Run only the first N selected cells.")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--request-timeout-s", type=int, default=DEFAULT_REQUEST_TIMEOUT_S)
    parser.add_argument("--tool-timeout-s", type=int, default=120)
    parser.add_argument("--judge-timeout-s", type=int, default=600)
    parser.add_argument("--feedback-command", help="Override the default repository EVAS feedback adapter command.")
    parser.add_argument("--no-feedback", action="store_true", help="Do not expose a feedback tool to G2-G5 cells.")
    parser.add_argument("--final-judge-command", help="Optional final judge adapter command.")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="Prepare runtimes without contacting the provider.")
    parser.add_argument("--resume", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = parser_for()
    args = parser.parse_args(argv)
    args.release = resolve_repo_path(args.release).resolve()
    args.selection = resolve_repo_path(args.selection).resolve()
    if args.api_key_file:
        args.api_key_file = args.api_key_file.expanduser().resolve()
    if args.max_working_tokens <= 0:
        parser.error("--max-working-tokens must be positive")
    if args.repetitions <= 0:
        parser.error("--repetitions must be positive")
    if args.workers <= 0:
        parser.error("--workers must be positive")
    if args.list:
        return print_roster(args)

    output_root = (args.output_root.resolve() if args.output_root else output_root_for(args.model, args.tag).resolve())
    output_root.mkdir(parents=True, exist_ok=True)
    campaign_path = (
        args.campaign.resolve()
        if args.campaign
        else (args.campaign_output.resolve() if args.campaign_output else output_root / "campaign.json")
    )
    run_output = output_root / "run"
    feedback_command = None if args.no_feedback else (args.feedback_command or default_feedback_command())

    build_cmd = None if args.campaign else build_campaign_command(args, campaign_path)
    if build_cmd and args.print_commands:
        print(shell_join(build_cmd))
    if build_cmd and not args.print_commands:
        rc = run_command(build_cmd)
        if rc != 0:
            return rc
    if not campaign_path.is_file() and not args.print_commands:
        raise SystemExit(f"campaign not found: {campaign_path}")

    filters = parse_filters(args)
    filtered_campaign = campaign_path
    if not args.print_commands:
        filtered_campaign = filtered_campaign_if_needed(campaign_path, output_root, filters)
    elif any(filters.values()):
        filtered_campaign = output_root / "campaign.filtered.json"
        print("# filters will materialize campaign.filtered.json before running")

    run_cmd = run_campaign_command(
        args,
        campaign_path=filtered_campaign,
        run_output=run_output,
        feedback_command=feedback_command,
    )
    if args.print_commands:
        print(shell_join(run_cmd))
        return 0

    rc = run_command(run_cmd)
    summary = write_wrapper_summary(
        output_root=output_root,
        model=args.model,
        base_url=args.base_url,
        api_key_env=args.api_key_env,
        campaign_path=filtered_campaign,
        run_output=run_output,
        build_cmd=build_cmd,
        run_cmd=run_cmd,
        dry_run=args.dry_run,
        max_working_tokens=args.max_working_tokens,
        rc=rc,
    )
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"[vabench-model-eval] status={summary['status']} output={rel(output_root)}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
