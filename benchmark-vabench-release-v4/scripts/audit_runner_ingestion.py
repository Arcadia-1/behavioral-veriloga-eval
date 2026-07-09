#!/usr/bin/env python3
"""Audit v4 runner dry-run jobs against the source experiment records."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = SCRIPT_DIR.parents[0]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
        if not isinstance(row, dict):
            raise SystemExit(f"{path}:{line_no}: expected JSON object")
        rows.append(row)
    return rows


def require(condition: bool, problems: list[str], message: str) -> None:
    if not condition:
        problems.append(message)


def rel_to_package(path: Path) -> str:
    return path.relative_to(PACKAGE_ROOT).as_posix()


def expected_dispatch(record: dict[str, Any]) -> str:
    if record.get("runner_family") == "llms" and record.get("process_type") == "direct_llm":
        return "direct_llm_completion"
    if record.get("runner_family") == "agents" and record.get("process_type") == "agentic":
        return "agentic_feedback_oracle_session"
    return "invalid_dispatch"


def prompt_hash_from_path(record: dict[str, Any]) -> str | None:
    prompt_path = PACKAGE_ROOT / str(record.get("prompt_path") or "")
    if not prompt_path.exists():
        return None
    return sha256_text(prompt_path.read_text(encoding="utf-8"))


def audit_pair(record: dict[str, Any], job: dict[str, Any], index: int, records_path: Path, records_sha: str, problems: list[str]) -> None:
    key = f"{record.get('task_slug')}/{record.get('mode')}"
    require(job.get("record_key") == key, problems, f"{key}: job record_key mismatch")
    require(job.get("record_index") == index, problems, f"{key}: job record_index mismatch")
    require(job.get("record_source_path") == rel_to_package(records_path), problems, f"{key}: job source path mismatch")
    require(job.get("record_source_sha256") == records_sha, problems, f"{key}: job source sha mismatch")
    require(job.get("record_fingerprint") == sha256_text(canonical_json(record)), problems, f"{key}: record fingerprint mismatch")
    require(job.get("runner_family") == record.get("runner_family"), problems, f"{key}: runner_family changed")
    require(job.get("process_type") == record.get("process_type"), problems, f"{key}: process_type changed")
    require(job.get("dispatch_kind") == expected_dispatch(record), problems, f"{key}: dispatch kind mismatch")
    require(job.get("mode_label") == record.get("mode_label"), problems, f"{key}: mode_label changed")
    require(job.get("skills") == (record.get("skills") or []), problems, f"{key}: skills changed")
    require(job.get("skill_files") == (record.get("skill_files") or []), problems, f"{key}: skill_files changed")
    require(job.get("target_artifacts") == (record.get("target_artifacts") or []), problems, f"{key}: target_artifacts changed")
    require(job.get("access_policy") == (record.get("access_policy") or {}), problems, f"{key}: access_policy changed")
    prompt = job.get("prompt") if isinstance(job.get("prompt"), dict) else {}
    require(prompt.get("path") == record.get("prompt_path"), problems, f"{key}: prompt path changed")
    require(prompt.get("sha256") == record.get("prompt_sha256"), problems, f"{key}: prompt sha changed")
    actual_prompt_sha = prompt_hash_from_path(record)
    require(actual_prompt_sha == record.get("prompt_sha256"), problems, f"{key}: rendered prompt no longer matches record sha")
    guards = job.get("runner_guards") if isinstance(job.get("runner_guards"), dict) else {}
    require(guards.get("consumed_from_record") is True, problems, f"{key}: missing consumed_from_record guard")
    require(guards.get("prompt_hash_verified") is True, problems, f"{key}: missing prompt hash guard")
    require(guards.get("hidden_access_blocked") is True, problems, f"{key}: hidden access guard not true")
    require(guards.get("private_score_access_blocked") is True, problems, f"{key}: private score access guard not true")

    access = record.get("access_policy") or {}
    mode = str(record.get("mode") or "")
    if mode in {"G0", "G1"}:
        require(record.get("runner_family") == "llms", problems, f"{key}: clean direct must use llms")
        require(not access.get("shell"), problems, f"{key}: clean direct exposes shell")
        require(access.get("file_browsing") == "none", problems, f"{key}: clean direct exposes file browsing")
        require(access.get("public_feedback_access") == "none", problems, f"{key}: clean direct exposes feedback")
        require(not access.get("feedback_files"), problems, f"{key}: clean direct exposes feedback files")
        require(not access.get("embedded_feedback_files"), problems, f"{key}: clean direct embeds feedback files")
        require(not access.get("allowed_commands"), problems, f"{key}: clean direct exposes commands")
    elif mode in {"G2", "G3", "G4", "G5"}:
        require(record.get("runner_family") == "agents", problems, f"{key}: agentic must use agents")
        require(access.get("shell") is True, problems, f"{key}: agentic does not expose shell")
        require(access.get("file_browsing") == "feedback_surface_only", problems, f"{key}: agentic file browsing mismatch")
        require(access.get("public_feedback_access") == "runnable_oracle", problems, f"{key}: agentic feedback access mismatch")
        require(bool(access.get("feedback_runner")), problems, f"{key}: agentic missing feedback runner")
        require(bool(access.get("feedback_files")), problems, f"{key}: agentic missing feedback files")
        require(not access.get("embedded_feedback_files"), problems, f"{key}: agentic embeds feedback files in prompt")
        require(bool(access.get("allowed_commands")), problems, f"{key}: agentic missing allowed command")


def summarize(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    mode_counts: dict[str, int] = {}
    runner_counts: dict[str, int] = {}
    for row in rows:
        mode = str(row.get("mode"))
        runner = str(row.get("runner_family"))
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
        runner_counts[runner] = runner_counts.get(runner, 0) + 1
    return {
        "mode_counts": dict(sorted(mode_counts.items())),
        "runner_family_counts": dict(sorted(runner_counts.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--records-jsonl",
        default="reports/experiment_specs/records.jsonl",
        help="records JSONL path relative to the v4 package",
    )
    parser.add_argument(
        "--jobs-jsonl",
        default="reports/runner_ingestion/jobs.jsonl",
        help="runner jobs JSONL path relative to the v4 package",
    )
    args = parser.parse_args()

    records_path = Path(args.records_jsonl)
    if not records_path.is_absolute():
        records_path = PACKAGE_ROOT / records_path
    jobs_path = Path(args.jobs_jsonl)
    if not jobs_path.is_absolute():
        jobs_path = PACKAGE_ROOT / jobs_path

    records = read_jsonl(records_path)
    jobs = read_jsonl(jobs_path)
    records_sha = sha256_bytes(records_path.read_bytes())
    problems: list[str] = []
    require(len(jobs) == len(records), problems, f"job count {len(jobs)} != record count {len(records)}")
    seen_jobs: set[str] = set()
    jobs_by_key = {}
    for job in jobs:
        key = str(job.get("record_key") or "")
        if key in seen_jobs:
            problems.append(f"{key}: duplicate job")
        seen_jobs.add(key)
        jobs_by_key[key] = job
    for index, record in enumerate(records):
        key = f"{record.get('task_slug')}/{record.get('mode')}"
        job = jobs_by_key.get(key)
        if job is None:
            problems.append(f"{key}: missing job")
            continue
        audit_pair(record, job, index, records_path, records_sha, problems)

    summary = {
        "benchmark": "benchmark-vabench-release-v4",
        "records_path": rel_to_package(records_path),
        "jobs_path": rel_to_package(jobs_path),
        "record_count": len(records),
        "job_count": len(jobs),
        "status": "PASS" if not problems else "FAIL",
        "problem_count": len(problems),
        "problems": problems,
        **summarize(jobs),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
