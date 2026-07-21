#!/usr/bin/env python3
"""Materialize the immutable r45 experiment-result protocol."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any


SCHEMA_VERSION = "vabench-experiment-result-v1"
REPLAY_STATUSES = {
    "passed",
    "compile_failure",
    "runtime_failure",
    "behavior_failure",
    "infrastructure_failure",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def raw_model_final_output(messages: list[dict[str, Any]]) -> dict[str, Any]:
    message = next(
        (item for item in reversed(messages) if item.get("role") == "assistant"),
        None,
    )
    if message is None:
        return {"available": False, "sha256": None, "message": None}
    preserved = dict(message)
    return {
        "available": True,
        "sha256": canonical_sha256(preserved),
        "message": preserved,
    }


def snapshot_submission(runtime: Path, artifact_gate: dict[str, Any]) -> dict[str, Any]:
    expected = list(artifact_gate.get("expected_artifacts") or [])
    if not artifact_gate.get("passed"):
        return {
            "status": "no_submission",
            "artifacts": [],
            "tree_sha256": None,
            "diagnostics": list(artifact_gate.get("diagnostics") or []),
        }

    source_root = runtime / "public" / "submission"
    snapshot_root = runtime / "evidence" / "final_submission"
    if snapshot_root.exists():
        shutil.rmtree(snapshot_root)
    artifacts: list[dict[str, Any]] = []
    for relative in expected:
        source = source_root / relative
        data = source.read_bytes()
        target = snapshot_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        artifacts.append({
            "path": relative,
            "snapshot_path": f"evidence/final_submission/{relative}",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    return {
        "status": "available",
        "artifacts": artifacts,
        "tree_sha256": canonical_sha256(
            [{"path": row["path"], "sha256": row["sha256"]} for row in artifacts]
        ),
        "diagnostics": [],
    }


def hash_test_tree(evaluator_dir: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    if evaluator_dir.is_dir():
        for path in sorted(evaluator_dir.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(evaluator_dir).as_posix()
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            data = path.read_bytes()
            files.append({
                "path": relative,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            })
    return {
        "file_count": len(files),
        "tree_sha256": canonical_sha256(
            [{"path": row["path"], "sha256": row["sha256"]} for row in files]
        ),
        "files": files,
    }


def evas_identity(command: list[str], timeout_s: int = 10) -> dict[str, Any]:
    resolved = shutil.which(command[0]) if command else None
    executable_sha256 = None
    if resolved:
        try:
            executable_sha256 = hashlib.sha256(Path(resolved).read_bytes()).hexdigest()
        except OSError:
            executable_sha256 = None
    try:
        completed = subprocess.run(
            [*command, "--version"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_s,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "available": False,
            "command": command,
            "resolved_executable": resolved,
            "executable_sha256": executable_sha256,
            "version_output": None,
            "sha256": None,
            "error_type": type(exc).__name__,
            "error": str(exc)[:1000],
        }
    version_output = (completed.stdout or completed.stderr).strip()
    available = completed.returncode == 0 and bool(version_output)
    return {
        "available": available,
        "command": command,
        "resolved_executable": resolved,
        "executable_sha256": executable_sha256,
        "returncode": completed.returncode,
        "version_output": version_output or None,
        "sha256": (
            hashlib.sha256(version_output.encode("utf-8")).hexdigest()
            if version_output else None
        ),
    }


def trusted_replay(
    command: dict[str, Any] | None,
    adapter_result: dict[str, Any] | None,
    test_manifest: dict[str, Any],
    identity: dict[str, Any],
    submission_tree_sha256: str | None = None,
) -> dict[str, Any]:
    if command is None:
        status = "not_run"
        diagnostics: list[str] = []
    elif command.get("execution_status") == "timeout":
        status = "runtime_failure"
        diagnostics = ["trusted_replay_timeout"]
    elif command.get("execution_status") != "completed":
        status = "infrastructure_failure"
        diagnostics = ["trusted_replay_did_not_execute"]
    elif adapter_result is not None:
        status = str(adapter_result.get("status") or "")
        if status not in REPLAY_STATUSES:
            status = "infrastructure_failure"
            diagnostics = ["invalid_trusted_replay_status"]
        else:
            diagnostics = list(adapter_result.get("diagnostics") or [])
    elif command.get("returncode") == 0:
        status = "passed"
        diagnostics = ["legacy_adapter_without_structured_result"]
    else:
        status = "infrastructure_failure"
        diagnostics = ["missing_structured_trusted_replay_result"]
    return {
        "status": status,
        "executed": command is not None,
        "test_manifest": test_manifest,
        "submission_tree_sha256": submission_tree_sha256,
        "evas_identity": identity,
        "command": command,
        "adapter_result": adapter_result,
        "diagnostics": diagnostics,
    }


def terminal_outcome(
    model_status: str,
    submission: dict[str, Any],
    replay: dict[str, Any],
) -> str:
    if model_status == "agent_resource_exhausted":
        return "agent_resource_exhausted"
    if model_status in {"provider_failure", "runner_failure"}:
        return "infrastructure_failure"
    if model_status == "agent_timeout" and submission.get("status") != "available":
        return "agent_timeout"
    if submission.get("status") != "available":
        return "no_submission"
    replay_status = str(replay.get("status") or "not_run")
    if replay_status in REPLAY_STATUSES:
        return replay_status
    return "not_scored"


def build_experiment_result(
    *,
    cell: dict[str, Any],
    model_status: str,
    messages: list[dict[str, Any]],
    artifact_gate: dict[str, Any],
    runtime: Path,
    replay: dict[str, Any],
    final_submission: dict[str, Any] | None = None,
) -> dict[str, Any]:
    submission = final_submission or snapshot_submission(runtime, artifact_gate)
    outcome = terminal_outcome(model_status, submission, replay)
    scored = outcome in {"passed", "compile_failure", "runtime_failure", "behavior_failure"}
    score = 1.0 if outcome == "passed" else 0.0 if scored else None
    return {
        "schema_version": SCHEMA_VERSION,
        "recorded_at": now(),
        "cell_id": str(cell.get("cell_id") or ""),
        "task_id": str(cell.get("task_id") or ""),
        "mode": str(cell.get("mode") or ""),
        "model_execution": {
            "status": model_status,
            "raw_final_output": raw_model_final_output(messages),
        },
        "final_submission": submission,
        "final_trusted_replay": replay,
        "outcome": outcome,
        "score_eligible": scored,
        "score": score,
    }
