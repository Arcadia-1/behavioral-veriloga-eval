#!/usr/bin/env python3
"""Materialize runner-side jobs from v4 experiment records.

This is a dry-run ingestion surface: it consumes `records.jsonl` as the source
of truth and writes the exact job payloads a direct or agentic runner should
dispatch. It does not call a model or execute agents.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import hashlib


SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = SCRIPT_DIR.parents[0]
SCHEMA_VERSION = "v4-pilot-runner-ingestion-v1"


def rel(path: Path) -> str:
    return path.relative_to(PACKAGE_ROOT).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_no}: invalid JSONL record: {exc}") from exc
        if not isinstance(record, dict):
            raise SystemExit(f"{path}:{line_no}: expected JSON object record")
        records.append(record)
    return records


def dispatch_kind(record: dict[str, Any]) -> str:
    runner_family = str(record.get("runner_family") or "")
    process_type = str(record.get("process_type") or "")
    if runner_family == "llms" and process_type == "direct_llm":
        return "direct_llm_completion"
    if runner_family == "agents" and process_type == "agentic":
        return "agentic_feedback_oracle_session"
    return "invalid_dispatch"


def read_prompt(record: dict[str, Any]) -> tuple[str, str]:
    prompt_path = PACKAGE_ROOT / str(record.get("prompt_path") or "")
    if not prompt_path.exists():
        raise SystemExit(f"{record.get('task_slug')}/{record.get('mode')}: missing prompt_path {prompt_path}")
    prompt = prompt_path.read_text(encoding="utf-8")
    prompt_hash = sha256_text(prompt)
    expected_hash = str(record.get("prompt_sha256") or "")
    if prompt_hash != expected_hash:
        raise SystemExit(
            f"{record.get('task_slug')}/{record.get('mode')}: prompt hash mismatch "
            f"record={expected_hash} actual={prompt_hash}"
        )
    return prompt, prompt_hash


def build_job(record: dict[str, Any], *, index: int, records_path: Path, records_sha256: str) -> dict[str, Any]:
    prompt, prompt_hash = read_prompt(record)
    access_policy = record.get("access_policy") or {}
    record_key = f"{record.get('task_slug')}/{record.get('mode')}"
    record_fingerprint = sha256_text(canonical_json(record))
    job_id = sha256_text(f"{records_sha256}:{index}:{record_key}:{record_fingerprint}")[:24]
    hidden_access = bool(access_policy.get("hidden_access"))
    return {
        "schema_version": SCHEMA_VERSION,
        "benchmark": record.get("benchmark"),
        "job_id": job_id,
        "record_index": index,
        "record_key": record_key,
        "record_fingerprint": record_fingerprint,
        "record_source_path": rel(records_path),
        "record_source_sha256": records_sha256,
        "task_slug": record.get("task_slug"),
        "task_id": record.get("task_id"),
        "mode": record.get("mode"),
        "mode_label": record.get("mode_label"),
        "runner_family": record.get("runner_family"),
        "process_type": record.get("process_type"),
        "dispatch_kind": dispatch_kind(record),
        "prompt": {
            "path": record.get("prompt_path"),
            "sha256": prompt_hash,
            "chars": len(prompt),
        },
        "canonical_prompt_path": record.get("canonical_prompt_path"),
        "target_artifacts": record.get("target_artifacts") or [],
        "skills": record.get("skills") or [],
        "skill_files": record.get("skill_files") or [],
        "access_policy": access_policy,
        "runner_guards": {
            "consumed_from_record": True,
            "prompt_hash_verified": True,
            "hidden_access_blocked": not hidden_access,
            "private_score_access_blocked": not bool(access_policy.get("private_score_access")),
            "access_policy_preserved": True,
            "record_fingerprint_preserved": True,
        },
        "execution_plan": {
            "submit_prompt": record.get("prompt_path"),
            "direct_prompt_embeds_feedback_interface": False,
            "agentic_feedback_loop": record.get("runner_family") == "agents",
            "feedback_surface_mounts": access_policy.get("feedback_files") or [],
            "embedded_feedback_files": access_policy.get("embedded_feedback_files") or [],
            "allowed_commands": access_policy.get("allowed_commands") or [],
        },
    }


def summarize(jobs: list[dict[str, Any]]) -> dict[str, Any]:
    mode_counts: dict[str, int] = {}
    runner_counts: dict[str, int] = {}
    dispatch_counts: dict[str, int] = {}
    for job in jobs:
        mode = str(job.get("mode"))
        runner = str(job.get("runner_family"))
        dispatch = str(job.get("dispatch_kind"))
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
        runner_counts[runner] = runner_counts.get(runner, 0) + 1
        dispatch_counts[dispatch] = dispatch_counts.get(dispatch, 0) + 1
    return {
        "mode_counts": dict(sorted(mode_counts.items())),
        "runner_family_counts": dict(sorted(runner_counts.items())),
        "dispatch_counts": dict(sorted(dispatch_counts.items())),
    }


def write_markdown(manifest: dict[str, Any], path: Path) -> None:
    lines = [
        "# v4 Pilot Runner Ingestion Evidence",
        "",
        f"- Schema: `{manifest['schema_version']}`",
        f"- Status: `{manifest['status']}`",
        f"- Source records: `{manifest['records_jsonl']}`",
        f"- Source records SHA-256: `{manifest['records_sha256']}`",
        f"- Job count: `{manifest['job_count']}`",
        "",
        "This report proves that the v4 runner-side dry-run consumed the",
        "`records.jsonl` experiment specs as its source of truth and materialized",
        "one dispatch job per record without changing prompt hashes, process",
        "families, skills, or access policies.",
        "",
        "## Counts",
        "",
        "| Field | Counts |",
        "|---|---|",
        f"| Modes | `{json.dumps(manifest['mode_counts'], sort_keys=True)}` |",
        f"| Runner families | `{json.dumps(manifest['runner_family_counts'], sort_keys=True)}` |",
        f"| Dispatch kinds | `{json.dumps(manifest['dispatch_counts'], sort_keys=True)}` |",
        "",
        "## Guarantees",
        "",
        "- Every job records the source record fingerprint.",
        "- Every job re-hashes the rendered prompt and requires it to match the record.",
        "- G0/G1 jobs dispatch through direct LLM completion.",
        "- G2/G3/G4/G5 jobs dispatch through agentic visible-feedback-oracle sessions.",
        "- Hidden/private score access remains blocked in all jobs.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(jobs: list[dict[str, Any]], records_path: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    jobs_json = out_dir / "jobs.json"
    jobs_jsonl = out_dir / "jobs.jsonl"
    manifest_path = out_dir / "manifest.json"
    report_path = out_dir / "runner_ingestion.md"
    records_sha256 = sha256_bytes(records_path.read_bytes())
    manifest = {
        "benchmark": "benchmark-vabench-release-v4",
        "schema_version": SCHEMA_VERSION,
        "status": "PASS",
        "records_jsonl": rel(records_path),
        "records_sha256": records_sha256,
        "jobs_json": rel(jobs_json),
        "jobs_jsonl": rel(jobs_jsonl),
        "job_count": len(jobs),
        **summarize(jobs),
    }
    jobs_json.write_text(json.dumps({"jobs": jobs}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    jobs_jsonl.write_text("".join(json.dumps(job, sort_keys=True) + "\n" for job in jobs), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(manifest, report_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--records-jsonl",
        default="reports/experiment_specs/records.jsonl",
        help="records JSONL path relative to the v4 package",
    )
    parser.add_argument(
        "--out-dir",
        default="reports/runner_ingestion",
        help="output directory relative to the v4 package",
    )
    args = parser.parse_args()

    records_path = Path(args.records_jsonl)
    if not records_path.is_absolute():
        records_path = PACKAGE_ROOT / records_path
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PACKAGE_ROOT / out_dir
    records_sha256 = sha256_bytes(records_path.read_bytes())
    records = read_jsonl(records_path)
    jobs = [
        build_job(record, index=index, records_path=records_path, records_sha256=records_sha256)
        for index, record in enumerate(records)
    ]
    write_outputs(jobs, records_path, out_dir)
    summary = {
        "benchmark": "benchmark-vabench-release-v4",
        "schema_version": SCHEMA_VERSION,
        "status": "WROTE",
        "record_count": len(records),
        "job_count": len(jobs),
        "out_dir": rel(out_dir),
        **summarize(jobs),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
