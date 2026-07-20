#!/usr/bin/env python3
"""Build and run a benchmarkv4 model campaign with direct and agentic modes.

This is the operator-facing entry point for API experiments.  It builds a
campaign from ``release/benchmarkv4-r49`` and delegates execution to the v4
calibration runner:

* G0/G1 use direct one-shot artifact extraction.
* G2-G5 run in a pinned mini-SWE-agent scaffold with one bash tool. The public
  workspace exposes task/, submission/, and EVAS diagnostics; evaluator and
  trusted-replay assets stay outside the model shell.

The result is still an experiment runner, not the final Spectre scorer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parent
CALIBRATION = PACKAGE / "operations" / "calibration_pilot"
DEFAULT_RELEASE = PACKAGE / "release" / "benchmarkv4-r49"
DEFAULT_AGENT_TIMEOUT_S = 5400
DEFAULT_SETUP_TIMEOUT_S = 1800
DEFAULT_REQUEST_TIMEOUT_S = 1800
DEFAULT_TOOL_TIMEOUT_S = 1800
DEFAULT_JUDGE_TIMEOUT_S = 1800
MODES = tuple(f"G{i}" for i in range(6))

if str(CALIBRATION) not in sys.path:
    sys.path.insert(0, str(CALIBRATION))
from build_campaign import build_campaign  # noqa: E402


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def command_for_metadata(command: list[str]) -> list[str]:
    """Keep reproducible structure without persisting credential-adjacent paths."""
    redacted_values = {
        "--api-key-file": "<redacted-credential-file>",
        "--final-judge-command": "<redacted-operator-command>",
    }
    sanitized: list[str] = []
    redact_next: str | None = None
    for token in command:
        if redact_next is not None:
            sanitized.append(redact_next)
            redact_next = None
            continue
        sanitized.append(token)
        redact_next = redacted_values.get(token)
    return sanitized


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def filter_campaign(campaign: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    modes = set(args.mode or MODES)
    forms = set(args.form or ("dut", "testbench", "bugfix"))
    task_ids = set(args.task_id or [])
    cells = [
        cell
        for cell in campaign["cells"]
        if cell["mode"] in modes
        and cell["form"] in forms
        and (not task_ids or cell["task_id"] in task_ids)
    ]
    if args.limit is not None:
        cells = cells[: args.limit]
    if not cells:
        raise SystemExit("no campaign cells match the requested filters")
    campaign = dict(campaign)
    campaign["cells"] = cells
    campaign["cell_count"] = len(cells)
    campaign["mode_count"] = len({cell["mode"] for cell in cells})
    campaign["task_count"] = len({cell["task_id"] for cell in cells})
    campaign["family_count"] = len({cell["family_id"] for cell in cells})
    campaign["status"] = "planned_filtered"
    campaign["filters"] = {
        "modes": sorted(modes),
        "forms": sorted(forms),
        "task_ids": sorted(task_ids),
        "limit": args.limit,
    }
    return campaign


def family_ids_for_task_ids(release: Path, task_ids: list[str] | None) -> list[str] | None:
    if not task_ids:
        return None
    index = read_json(release / "TASK_INDEX.json")["tasks"]
    by_task = {str(row["task_id"]): str(row["family_id"]) for row in index}
    missing = [task_id for task_id in task_ids if task_id not in by_task]
    if missing:
        raise SystemExit(f"unknown task-id(s): {', '.join(missing)}")
    return sorted({by_task[task_id] for task_id in task_ids}, key=lambda value: int(value))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--sample-families", type=int)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--mode", action="append", choices=MODES)
    parser.add_argument("--form", action="append", choices=("dut", "testbench", "bugfix"))
    parser.add_argument("--task-id", action="append")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--model-provider", default="openai-compatible")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", default="https://api.deepseek.com/v1")
    parser.add_argument("--api-key-file")
    parser.add_argument("--api-key-env", default="DEEPSEEK_API_KEY")
    parser.add_argument(
        "--per-turn-max-tokens",
        "--max-output-tokens",
        "--max-working-tokens",
        dest="per_turn_max_tokens",
        type=int,
        default=65536,
        help="Provider per-call max_tokens cap. This is not a cumulative episode budget.",
    )
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--agent-scaffold",
        choices=("mini-swe", "native"),
        default="mini-swe",
        help="Use pinned mini-SWE-agent for G2-G5; native is a legacy sensitivity path.",
    )
    parser.add_argument(
        "--mini-swe-sandbox",
        choices=("auto", "sandbox-exec", "bubblewrap", "none"),
        default="auto",
        help="Use sandbox-exec on macOS or Bubblewrap on Linux/WSL2; 'none' is test-only.",
    )
    parser.add_argument("--agent-timeout-s", type=int, default=DEFAULT_AGENT_TIMEOUT_S)
    parser.add_argument("--setup-timeout-s", type=int, default=DEFAULT_SETUP_TIMEOUT_S)
    parser.add_argument("--request-timeout-s", type=int, default=DEFAULT_REQUEST_TIMEOUT_S)
    parser.add_argument("--tool-timeout-s", type=int, default=DEFAULT_TOOL_TIMEOUT_S)
    parser.add_argument("--judge-timeout-s", type=int, default=DEFAULT_JUDGE_TIMEOUT_S)
    parser.add_argument("--final-judge-command")
    parser.add_argument("--evas-command", default="evas")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.per_turn_max_tokens <= 0:
        raise SystemExit("--per-turn-max-tokens must be positive")
    if args.repetitions <= 0:
        raise SystemExit("--repetitions must be positive")
    if args.workers <= 0:
        raise SystemExit("--workers must be positive")
    if min(
        args.agent_timeout_s,
        args.setup_timeout_s,
        args.request_timeout_s,
        args.tool_timeout_s,
        args.judge_timeout_s,
    ) <= 0:
        raise SystemExit("all timeout values must be positive")
    if (
        args.agent_scaffold == "mini-swe"
        and args.mini_swe_sandbox == "none"
        and any(mode in {"G2", "G3", "G4", "G5"} for mode in (args.mode or MODES))
        and not args.dry_run
    ):
        raise SystemExit(
            "--mini-swe-sandbox none is test-only; use a supported secure sandbox "
            "for executable G2-G5 campaigns"
        )
    release = args.release.expanduser().resolve()
    output_root = args.output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    explicit_family_ids = None
    if args.task_id and args.selection is None and args.sample_families is None:
        explicit_family_ids = family_ids_for_task_ids(release, args.task_id)
    campaign = build_campaign(
        release,
        selection_path=args.selection.expanduser().resolve() if args.selection else None,
        sample_families=args.sample_families,
        family_ids=explicit_family_ids,
        seed=args.seed,
        model_provider=args.model_provider,
        model=args.model,
        per_turn_max_tokens=args.per_turn_max_tokens,
        repetitions=args.repetitions,
    )
    campaign = filter_campaign(campaign, args)
    campaign["execution_config"] = {
        "schema_version": "v4-campaign-execution-config-v1",
        "termination_policy": "wall_time",
        "agent_timeout_s": args.agent_timeout_s,
        "setup_timeout_s": args.setup_timeout_s,
        "request_timeout_s": args.request_timeout_s,
        "tool_timeout_s": args.tool_timeout_s,
        "judge_timeout_s": args.judge_timeout_s,
        "per_turn_max_tokens": args.per_turn_max_tokens,
        "token_accounting": "telemetry_only",
        "agent_scaffold": args.agent_scaffold,
        "mini_swe_sandbox": args.mini_swe_sandbox,
        "base_url_sha256": text_sha256(args.base_url.rstrip("/")),
        "temperature": args.temperature,
        "stream": args.stream,
        "evas_command_sha256": text_sha256(args.evas_command),
    }
    campaign_path = output_root / "campaign.json"
    write_json(campaign_path, campaign)
    command = [
        sys.executable,
        str(CALIBRATION / "run_campaign.py"),
        "--campaign",
        str(campaign_path),
        "--release",
        str(release),
        "--output",
        str(output_root / "run"),
        "--base-url",
        args.base_url,
        "--api-key-env",
        args.api_key_env,
        "--temperature",
        str(args.temperature),
        "--agent-scaffold",
        args.agent_scaffold,
        "--mini-swe-sandbox",
        args.mini_swe_sandbox,
        "--agent-timeout-s",
        str(args.agent_timeout_s),
        "--setup-timeout-s",
        str(args.setup_timeout_s),
        "--request-timeout-s",
        str(args.request_timeout_s),
        "--tool-timeout-s",
        str(args.tool_timeout_s),
        "--judge-timeout-s",
        str(args.judge_timeout_s),
        "--workers",
        str(args.workers),
        "--evas-command",
        args.evas_command,
    ]
    if args.api_key_file:
        command.extend(["--api-key-file", args.api_key_file])
    if args.final_judge_command:
        command.extend(["--final-judge-command", args.final_judge_command])
    if args.stream:
        command.append("--stream")
    if args.dry_run:
        command.append("--dry-run")
    if args.resume:
        command.append("--resume")
    metadata = {
        "schema_version": "v4-benchmarkv4-campaign-wrapper-v1",
        "campaign": str(campaign_path),
        "run_output": str(output_root / "run"),
        "release": str(release),
        "model": args.model,
        "base_url": args.base_url,
        "workers": args.workers,
        "dry_run": args.dry_run,
        "command": command_for_metadata(command),
    }
    write_json(output_root / "wrapper_summary.json", metadata)
    completed = subprocess.run(command, cwd=REPO, check=False)
    metadata["returncode"] = completed.returncode
    run_summary = output_root / "run" / "SUMMARY.json"
    if run_summary.is_file():
        metadata["run_summary"] = read_json(run_summary)
    write_json(output_root / "wrapper_summary.json", metadata)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
