#!/usr/bin/env python3
"""Unified vaBench model-evaluation entrypoint.

This runner is a thin orchestration layer over the release-native model
baseline and Spectre dual-judge runners. It keeps one public command surface for
new models while preserving the existing evaluation split:

- generation + EVAS scoring is the fast model-development gate;
- Spectre + deterministic checker is the final reported model judge.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any

from export_vabench_eval_framework import MODEL_ROSTER_JSON
from run_vabench_release_minimax_baseline import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    model_slug,
    scored_form_rows,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results"
CLAIM_BOUNDARY = (
    "EVAS is a fast filter/debug gate. Spectre plus the deterministic behavior "
    "checker is the final model score."
)
REDACT_NEXT_ARG = {"--api-key-file", "--extra-body-json", "--proxy-url"}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"_read_error": f"{type(exc).__name__}: {str(exc)[:500]}"}
    return loaded if isinstance(loaded, dict) else {"_payload": loaded}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def output_root_for(model: str, tag: str | None) -> Path:
    stamp = tag or datetime.now().strftime("%Y%m%d-%H%M%S")
    return RESULTS_ROOT / f"vabench-model-eval-{model_slug(model)}-{stamp}"


def set_or_none(values: list[str]) -> set[str] | None:
    return set(values) or None


def task_ids_from_args(args: argparse.Namespace) -> set[str] | None:
    task_ids = set(args.task_id)
    for task_id_file in args.task_id_file:
        path = resolve_repo_path(task_id_file)
        task_ids.update(
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    return task_ids or None


def selected_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    return scored_form_rows(
        denominator_path=resolve_repo_path(args.score_roster),
        limit=args.limit,
        entry=set_or_none(args.entry),
        form=set_or_none(args.form),
        difficulty=set_or_none(args.difficulty),
        category=set_or_none(args.category),
        task_id=task_ids_from_args(args),
    )


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def append_repeated(cmd: list[str], flag: str, values: list[str]) -> None:
    for value in values:
        cmd.extend([flag, value])


def append_filters(cmd: list[str], args: argparse.Namespace) -> None:
    if args.limit is not None:
        cmd.extend(["--limit", str(args.limit)])
    append_repeated(cmd, "--entry", args.entry)
    append_repeated(cmd, "--form", args.form)
    append_repeated(cmd, "--difficulty", args.difficulty)
    append_repeated(cmd, "--category", args.category)
    append_repeated(cmd, "--task-id", args.task_id)
    append_repeated(cmd, "--task-id-file", args.task_id_file)


def build_generation_command(args: argparse.Namespace, output_root: Path) -> list[str]:
    cmd = [
        sys.executable,
        "runners/run_vabench_release_minimax_baseline.py",
        "--score-roster",
        str(resolve_repo_path(args.score_roster)),
        "--model",
        args.model,
        "--base-url",
        args.base_url,
        "--api-format",
        args.api_format,
        "--stage",
        args.stage,
        "--output-root",
        str(output_root),
        "--sample-idx",
        str(args.sample_idx),
        "--temperature",
        str(args.temperature),
        "--top-p",
        str(args.top_p),
        "--max-tokens",
        str(args.max_tokens),
        "--request-timeout-s",
        str(args.request_timeout_s),
        "--score-timeout-s",
        str(args.score_timeout_s),
        "--gen-workers",
        str(args.gen_workers),
        "--score-workers",
        str(args.score_workers),
        "--api-attempts",
        str(args.api_attempts),
        "--quota-retry-sleep-s",
        str(args.quota_retry_sleep_s),
        "--network-mode",
        args.network_mode,
        "--token-param",
        args.token_param,
        "--auth-header",
        args.auth_header,
    ]
    if args.api_key_file:
        cmd.extend(["--api-key-file", args.api_key_file])
    if args.extra_body_json:
        cmd.extend(["--extra-body-json", args.extra_body_json])
    if args.proxy_url:
        cmd.extend(["--proxy-url", args.proxy_url])
    if args.resume:
        cmd.append("--resume")
    if args.dry_run:
        cmd.append("--dry-run")
    append_filters(cmd, args)
    return cmd


def build_spectre_command(args: argparse.Namespace, baseline_root: Path, output_root: Path) -> list[str]:
    cmd = [
        sys.executable,
        "runners/run_vabench_release_model_dual_judge.py",
        "--score-roster",
        str(resolve_repo_path(args.score_roster)),
        "--baseline-root",
        str(baseline_root),
        "--model",
        args.model,
        "--output-root",
        str(output_root),
        "--sample-idx",
        str(args.sample_idx),
        "--selection",
        args.selection,
        "--workers",
        str(args.dual_workers),
        "--timeout-s",
        str(args.spectre_timeout_s),
        "--spectre-backend",
        args.spectre_backend,
    ]
    if args.spectre_license_wait_s is not None:
        cmd.extend(["--spectre-license-wait-s", str(args.spectre_license_wait_s)])
    if args.bridge_repo:
        cmd.extend(["--bridge-repo", args.bridge_repo])
    if args.sui_host:
        cmd.extend(["--sui-host", args.sui_host])
    if args.sui_work_root:
        cmd.extend(["--sui-work-root", args.sui_work_root])
    if args.cadence_cshrc:
        cmd.extend(["--cadence-cshrc", args.cadence_cshrc])
    if args.resume:
        cmd.append("--resume")
    append_filters(cmd, args)
    return cmd


def redact_command(cmd: list[str]) -> list[str]:
    redacted: list[str] = []
    skip_value = False
    for token in cmd:
        if skip_value:
            redacted.append("<redacted>")
            skip_value = False
            continue
        redacted.append(token)
        if token in REDACT_NEXT_ARG:
            skip_value = True
    return redacted


def command_record(stage: str, cmd: list[str]) -> dict[str, Any]:
    redacted = redact_command(cmd)
    display = list(redacted)
    if display and display[0] == sys.executable:
        display[0] = "python3"
    return {
        "stage": stage,
        "argv": redacted,
        "command": " ".join(shlex.quote(token) for token in display),
    }


def run_command(cmd: list[str]) -> int:
    completed = subprocess.run(cmd, cwd=ROOT)
    return int(completed.returncode)


def status_from_return_codes(generation_rc: int | None, spectre_rc: int | None, *, dry_run: bool) -> str:
    if generation_rc not in (None, 0):
        return "generation_evas_failed"
    if spectre_rc not in (None, 0):
        return "spectre_final_failed"
    if dry_run:
        return "complete_dry_run"
    return "complete"


def build_summary(
    *,
    args: argparse.Namespace,
    output_root: Path,
    generation_root: Path,
    spectre_root: Path,
    rows: list[dict[str, Any]],
    commands: list[dict[str, Any]],
    generation_rc: int | None,
    spectre_rc: int | None,
    status: str,
    spectre_skipped_reason: str | None = None,
) -> dict[str, Any]:
    generation_summary = read_json(generation_root / "summary.json")
    spectre_summary = read_json(spectre_root / "summary.json")
    spectre_claim_ready = (
        args.final_judge == "spectre"
        and status == "complete"
        and spectre_summary.get("status") == "complete"
        and spectre_summary.get("spectre_backend_inconclusive_count") == 0
    )
    return {
        "date": datetime.now(timezone.utc).isoformat(),
        "benchmark": "vabench-300",
        "score_roster": rel(resolve_repo_path(args.score_roster)),
        "model": args.model,
        "api_format": args.api_format,
        "base_url": args.base_url,
        "stage": args.stage,
        "final_judge": args.final_judge,
        "selection": args.selection,
        "proxy_url": "<redacted>" if args.proxy_url else "",
        "status": status,
        "dry_run": args.dry_run,
        "claim_allowed": spectre_claim_ready,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_scored_rows": len(rows),
        "selected_by_form": count_by(rows, "form"),
        "selected_by_category": count_by(rows, "category"),
        "return_codes": {
            "generation_evas": generation_rc,
            "spectre_final": spectre_rc,
        },
        "commands": commands,
        "generation_evas": {
            "status": generation_summary.get("status", "not_run" if generation_rc is None else "missing_summary"),
            "summary": rel(generation_root / "summary.json"),
            "selected_scored_forms": generation_summary.get("selected_scored_forms"),
            "scored_forms": generation_summary.get("scored_forms"),
            "evas_pass_count": generation_summary.get("evas_pass_count"),
            "evas_pass_rate": generation_summary.get("evas_pass_rate"),
            "generation_status_counts": generation_summary.get("generation_status_counts"),
        },
        "spectre_final": {
            "status": spectre_summary.get(
                "status",
                "skipped" if spectre_skipped_reason else ("not_run" if spectre_rc is None else "missing_summary"),
            ),
            "skipped_reason": spectre_skipped_reason,
            "summary": rel(spectre_root / "summary.json"),
            "selected_scored_forms": spectre_summary.get("selected_scored_forms"),
            "completed_dual_count": spectre_summary.get("completed_dual_count"),
            "spectre_final_pass_count": spectre_summary.get("spectre_final_pass_count"),
            "dual_pass_count": spectre_summary.get("dual_pass_count"),
            "evas_pass_spectre_fail_count": spectre_summary.get("evas_pass_spectre_fail_count"),
            "spectre_pass_evas_fail_count": spectre_summary.get("spectre_pass_evas_fail_count"),
            "spectre_backend_inconclusive_count": spectre_summary.get("spectre_backend_inconclusive_count"),
        },
        "paths": {
            "output_root": rel(output_root),
            "generation_evas_root": rel(generation_root),
            "spectre_final_root": rel(spectre_root),
            "summary_json": rel(output_root / "summary.json"),
            "summary_md": rel(output_root / "summary.md"),
        },
    }


def write_summary_md(path: Path, summary: dict[str, Any]) -> None:
    gen = summary["generation_evas"]
    spectre = summary["spectre_final"]
    lines = [
        "# vaBench Unified Model Evaluation",
        "",
        f"Date: {summary['date']}",
        f"Model: `{summary['model']}`",
        f"Status: `{summary['status']}`",
        "",
        summary["claim_boundary"],
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| selected scored rows | {summary['selected_scored_rows']} |",
        f"| generation/EVAS status | `{gen['status']}` |",
        f"| EVAS scored forms | {gen.get('scored_forms') or 0} |",
        f"| EVAS pass count | {gen.get('evas_pass_count') or 0} |",
        f"| EVAS pass rate | {gen.get('evas_pass_rate') or 0.0} |",
        f"| Spectre status | `{spectre['status']}` |",
        f"| Spectre final pass | {spectre.get('spectre_final_pass_count') or 0} |",
        f"| EVAS PASS / Spectre FAIL | {spectre.get('evas_pass_spectre_fail_count') or 0} |",
        f"| claim allowed | `{summary['claim_allowed']}` |",
        "",
        "## Commands",
        "",
    ]
    for record in summary["commands"]:
        lines.append(f"- `{record['stage']}`: `{record['command']}`")
    lines.extend(
        [
            "",
            "## Paths",
            "",
            f"- `generation_evas`: `{summary['paths']['generation_evas_root']}`",
            f"- `spectre_final`: `{summary['paths']['spectre_final_root']}`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_summary_files(output_root: Path, summary: dict[str, Any]) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    write_json(output_root / "summary.json", summary)
    write_summary_md(output_root / "summary.md", summary)


def list_rows(args: argparse.Namespace) -> int:
    rows = selected_rows(args)
    payload = {
        "date": datetime.now(timezone.utc).isoformat(),
        "benchmark": "vabench-300",
        "score_roster": rel(resolve_repo_path(args.score_roster)),
        "selected_scored_rows": len(rows),
        "selected_by_form": count_by(rows, "form"),
        "selected_by_category": count_by(rows, "category"),
        "rows": rows,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    print(f"score_roster={payload['score_roster']}")
    print(f"selected_scored_rows={payload['selected_scored_rows']}")
    print(f"by_form={payload['selected_by_form']}")
    print(f"by_category={payload['selected_by_category']}")
    for row in rows[: min(len(rows), 20)]:
        print(
            f"- {row.get('task_id')} form={row.get('form')} "
            f"category={row.get('category')} difficulty={row.get('difficulty')}"
        )
    if len(rows) > 20:
        print(f"... {len(rows) - 20} more rows")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="List selected scored rows and exit.")
    ap.add_argument("--json", action="store_true", help="Print JSON for --list or final summary.")
    ap.add_argument("--print-commands", action="store_true", help="Write a command preview summary without running.")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--api-format", choices=["openai", "anthropic"], default="openai")
    ap.add_argument("--api-key-file", default="")
    ap.add_argument("--score-roster", default=str(MODEL_ROSTER_JSON))
    ap.add_argument("--stage", choices=["generate", "score", "all"], default="all")
    ap.add_argument("--final-judge", choices=["none", "spectre"], default="none")
    ap.add_argument("--output-root", default="")
    ap.add_argument("--tag", default="")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--entry", action="append", default=[])
    ap.add_argument("--form", action="append", default=[])
    ap.add_argument("--difficulty", action="append", default=[])
    ap.add_argument("--category", action="append", default=[])
    ap.add_argument("--task-id", action="append", default=[])
    ap.add_argument("--task-id-file", action="append", default=[])
    ap.add_argument("--sample-idx", type=int, default=0)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--top-p", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--request-timeout-s", type=int, default=420)
    ap.add_argument("--score-timeout-s", type=int, default=180)
    ap.add_argument("--gen-workers", type=int, default=1)
    ap.add_argument("--score-workers", type=int, default=4)
    ap.add_argument("--api-attempts", type=int, default=2)
    ap.add_argument("--quota-retry-sleep-s", type=int, default=0)
    ap.add_argument("--network-mode", choices=["auto", "direct", "env"], default="auto")
    ap.add_argument("--proxy-url", default="")
    ap.add_argument("--token-param", choices=["auto", "max_tokens", "max_completion_tokens"], default="auto")
    ap.add_argument("--auth-header", choices=["auto", "authorization", "api-key", "both"], default="auto")
    ap.add_argument("--extra-body-json", default="")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selection", choices=["all-generated", "evas-pass", "evas-fail"], default="all-generated")
    ap.add_argument("--dual-workers", type=int, default=4)
    ap.add_argument("--spectre-timeout-s", type=int, default=240)
    ap.add_argument("--spectre-license-wait-s", type=int, default=None)
    ap.add_argument("--bridge-repo", default="")
    ap.add_argument(
        "--spectre-backend",
        choices=["labctl", "sui-direct", "bridge"],
        default=os.environ.get("VAEVAS_SPECTRE_BACKEND", "labctl"),
    )
    ap.add_argument("--sui-host", "--labctl-host", dest="sui_host", default="")
    ap.add_argument("--sui-work-root", "--labctl-work-root", dest="sui_work_root", default="")
    ap.add_argument("--cadence-cshrc", default="")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.list:
        return list_rows(args)

    rows = selected_rows(args)
    if not rows:
        print("No scored model rows selected.", file=sys.stderr)
        return 1

    output_root = resolve_repo_path(args.output_root) if args.output_root else output_root_for(args.model, args.tag or None)
    generation_root = output_root / "generation_evas"
    spectre_root = output_root / "spectre_final"
    generation_cmd = build_generation_command(args, generation_root)
    spectre_cmd = build_spectre_command(args, generation_root, spectre_root)
    commands = [command_record("generation_evas", generation_cmd)]
    if args.final_judge == "spectre":
        commands.append(command_record("spectre_final", spectre_cmd))

    if args.print_commands:
        summary = build_summary(
            args=args,
            output_root=output_root,
            generation_root=generation_root,
            spectre_root=spectre_root,
            rows=rows,
            commands=commands,
            generation_rc=None,
            spectre_rc=None,
            status="command_preview",
            spectre_skipped_reason="command_preview" if args.final_judge == "spectre" else "final_judge_none",
        )
        write_summary_files(output_root, summary)
        if args.json:
            print(json.dumps(summary, indent=2, sort_keys=True))
        else:
            for record in commands:
                print(f"{record['stage']}: {record['command']}")
            print(f"summary={summary['paths']['summary_json']}")
        return 0

    output_root.mkdir(parents=True, exist_ok=True)
    generation_rc = run_command(generation_cmd)
    spectre_rc: int | None = None
    spectre_skipped_reason: str | None = None
    if generation_rc == 0 and args.final_judge == "spectre":
        if args.dry_run:
            spectre_skipped_reason = "dry_run"
        else:
            spectre_rc = run_command(spectre_cmd)
    elif args.final_judge == "none":
        spectre_skipped_reason = "final_judge_none"

    status = status_from_return_codes(generation_rc, spectre_rc, dry_run=args.dry_run)
    summary = build_summary(
        args=args,
        output_root=output_root,
        generation_root=generation_root,
        spectre_root=spectre_root,
        rows=rows,
        commands=commands,
        generation_rc=generation_rc,
        spectre_rc=spectre_rc,
        status=status,
        spectre_skipped_reason=spectre_skipped_reason,
    )
    write_summary_files(output_root, summary)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(
            f"[vabench-model-eval] status={summary['status']} "
            f"rows={summary['selected_scored_rows']} summary={summary['paths']['summary_json']}",
            flush=True,
        )
    if generation_rc != 0:
        return generation_rc
    if spectre_rc not in (None, 0):
        return spectre_rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
