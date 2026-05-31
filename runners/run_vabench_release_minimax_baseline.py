#!/usr/bin/env python3
"""Run a prompt-only MiniMax baseline on the scored vaBench release forms.

This runner is intentionally release-package native: it reads the frozen score
denominator, sends each public prompt to a MiniMax OpenAI-compatible endpoint,
saves candidate artifacts in the layout expected by score.py, and then runs the
existing EVAS scoring gate. Spectre remains a later final judge; this script's
summary is an EVAS-filter baseline, not a paper-ready final model claim.

API credentials are read from MINIMAX_API_KEY or --api-key-file. They are never
written to repo files, result metadata, or command-line arguments.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any

from generate import extract_code_blocks
from score import _fail_result, _task_pass, build_model_results, read_meta, score_one_task
from vabench_release_prompt_wrapper import (
    RELEASE_RUNNER_WRAPPER_VERSION,
    RELEASE_SYSTEM_PROMPT,
    build_release_generation_prompt,
    extract_marked_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
SCORE_DENOMINATOR = PACKAGE_ROOT / "reports" / "score_denominator_manifest.json"
RESULTS_ROOT = ROOT / "results"
DEFAULT_BASE_URL = "https://api.minimaxi.com/v1"
DEFAULT_MODEL = "MiniMax-M2.7"

_TARGET_RE = re.compile(r"^- Target artifact\(s\):\s*(.+)$", re.MULTILINE)
_BACKTICK_RE = re.compile(r"`([^`]+)`")
_MODULE_RE = re.compile(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)")
_TB_RE = re.compile(r"(tb_[A-Za-z0-9_]+)")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def model_slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


def load_api_key(api_key_file: str | None, api_format: str = "openai") -> str:
    env_names = ["MINIMAX_API_KEY"]
    if api_format == "anthropic":
        env_names = ["ANTHROPIC_API_KEY", "MINIMAX_API_KEY"]
    for env_name in env_names:
        key = os.environ.get(env_name, "").strip()
        if key:
            return key
    if api_key_file:
        path = Path(api_key_file).expanduser()
        key = path.read_text(encoding="utf-8").strip()
        if key:
            return key
    raise SystemExit("API key env var is not set and --api-key-file was not provided.")


def scored_form_rows(
    *,
    limit: int | None,
    entry: set[str] | None,
    form: set[str] | None,
    difficulty: set[str] | None,
    category: set[str] | None,
    task_id: set[str] | None = None,
) -> list[dict[str, Any]]:
    denominator = read_json(SCORE_DENOMINATOR)
    rows = [
        row
        for row in denominator.get("form_rows", [])
        if isinstance(row, dict) and row.get("counted_in_score") is True
    ]
    if entry:
        rows = [row for row in rows if str(row.get("release_entry_id")) in entry]
    if form:
        rows = [row for row in rows if str(row.get("form")) in form]
    if difficulty:
        rows = [row for row in rows if str(row.get("difficulty")) in difficulty]
    if category:
        rows = [row for row in rows if str(row.get("category")) in category]
    if task_id:
        rows = [row for row in rows if str(row.get("task_id")) in task_id]
    rows.sort(key=lambda row: (str(row.get("category")), str(row.get("release_entry_id")), str(row.get("form"))))
    if limit is not None:
        rows = rows[:limit]
    return rows


def form_dir(row: dict[str, Any]) -> Path:
    manifest = ROOT / str(row["manifest"])
    if not manifest.exists():
        raise FileNotFoundError(f"release_task manifest missing: {manifest}")
    return manifest.parent


def task_key(row: dict[str, Any], task_dir: Path) -> str:
    meta = read_meta(task_dir)
    return str(meta.get("task_id") or meta.get("id") or row.get("task_id"))


def output_root_for(model: str, tag: str | None) -> Path:
    stamp = tag or datetime.now().strftime("%Y%m%d-%H%M%S")
    return RESULTS_ROOT / f"vabench-release-v1-baseline-minimax-{model_slug(model)}-{stamp}"


def resolved_token_param(base_url: str, model: str, token_param: str) -> str:
    if token_param != "auto":
        return token_param
    lowered = f"{base_url} {model}".lower()
    if "mimo-v2.com" in lowered or "mimo-v2" in lowered:
        return "max_completion_tokens"
    return "max_tokens"


def resolved_auth_header(base_url: str, model: str, auth_header: str) -> str:
    if auth_header != "auto":
        return auth_header
    lowered = f"{base_url} {model}".lower()
    if "mimo-v2" in lowered:
        return "api-key"
    return "authorization"


def auth_header_lines(api_key: str, auth_header: str) -> list[str]:
    if auth_header == "api-key":
        return [f"api-key: {api_key}"]
    if auth_header == "authorization":
        return [f"Authorization: Bearer {api_key}"]
    if auth_header == "both":
        return [f"Authorization: Bearer {api_key}", f"api-key: {api_key}"]
    raise ValueError(f"unsupported auth header mode: {auth_header}")


def request_payload(
    *,
    model: str,
    system_prompt: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    token_param: str,
) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        token_param: max_tokens,
        "temperature": temperature,
    }


def anthropic_messages_endpoint(base_url: str) -> str:
    stripped = base_url.rstrip("/")
    if stripped.endswith("/v1/messages"):
        return stripped
    if stripped.endswith("/v1"):
        return stripped + "/messages"
    return stripped + "/v1/messages"


def resolved_api_metadata(
    *,
    api_format: str,
    base_url: str,
    model: str,
    token_param: str,
    auth_header: str,
) -> tuple[str, str]:
    if api_format == "anthropic":
        return "max_tokens", "x-api-key"
    return (
        resolved_token_param(base_url, model, token_param),
        resolved_auth_header(base_url, model, auth_header),
    )


def prompt_targets(prompt_text: str) -> list[str]:
    match = _TARGET_RE.search(prompt_text)
    if not match:
        return []
    return [item for item in _BACKTICK_RE.findall(match.group(1)) if item.endswith((".va", ".scs"))]


def release_targets(task_dir: Path) -> list[str]:
    release_task = read_json(task_dir / "release_task.json")
    artifacts = release_task.get("artifacts", {})
    explicit = artifacts.get("submission_artifacts")
    if isinstance(explicit, list) and explicit:
        return [str(item) for item in explicit]

    prompt_text = (task_dir / "prompt.md").read_text(encoding="utf-8", errors="ignore")
    targets = prompt_targets(prompt_text)
    if targets:
        return targets
    family = release_task.get("family") or read_meta(task_dir).get("family")
    gold_names = [Path(path).name for path in artifacts.get("gold", []) if isinstance(path, str)]
    if family == "tb-generation":
        return [name for name in gold_names if name.endswith(".scs")][:1]
    if family in {"spec-to-va", "bugfix"}:
        fixed = [name for name in gold_names if name.endswith(".va") and "fixed" in Path(name).stem]
        if fixed:
            return fixed[:1]
        return [name for name in gold_names if name.endswith(".va")][:1]
    if family == "end-to-end":
        vas = [name for name in gold_names if name.endswith(".va")]
        tbs = [name for name in gold_names if name.endswith(".scs")]
        return vas + tbs[:1]
    return []


def release_support_artifacts(task_dir: Path, target_artifacts: list[str]) -> dict[str, str]:
    """Load public read-only support artifacts declared by a release form.

    Bugfix forms declare `gold/dut_buggy.va` as a public input in meta.json.
    The fixed gold and checker assets stay hidden; only explicit public inputs
    are surfaced to the model invocation wrapper.
    """
    meta_path = task_dir / "meta.json"
    meta = read_json(meta_path) if meta_path.exists() else {}
    declared_inputs: list[str] = []
    for key in ("public_inputs", "inputs"):
        value = meta.get(key)
        if isinstance(value, list):
            declared_inputs.extend(str(item) for item in value)

    if (
        task_dir.name == "bugfix"
        and (task_dir / "gold" / "dut_buggy.va").exists()
        and "gold/dut_buggy.va" not in declared_inputs
    ):
        declared_inputs.append("gold/dut_buggy.va")

    target_names = {Path(name).name for name in target_artifacts}
    support: dict[str, str] = {}
    for item in declared_inputs:
        if item == "prompt.md":
            continue
        rel_path = Path(item)
        if rel_path.name in target_names:
            continue
        if rel_path.suffix not in {".va", ".scs"}:
            continue
        path = task_dir / rel_path
        if not path.exists():
            continue
        support[rel_path.name] = path.read_text(encoding="utf-8")
    return support


def infer_va_name(code: str) -> str:
    match = _MODULE_RE.search(code)
    return f"{match.group(1)}.va" if match else "generated_module.va"


def infer_scs_name(code: str) -> str:
    match = _TB_RE.search(code)
    return f"{match.group(1)}.scs" if match else "tb_generated.scs"


def fallback_code_blocks(response_text: str) -> dict[str, list[str]]:
    blocks = extract_code_blocks(response_text)
    if blocks["va"] or blocks["scs"]:
        return blocks
    stripped = response_text.strip()
    if not stripped:
        return {"va": [], "scs": []}
    if "simulator lang=spectre" in stripped.lower() or re.search(r"(?m)^\s*tran\s+", stripped):
        return {"va": [], "scs": [stripped]}
    if _MODULE_RE.search(stripped):
        return {"va": [stripped], "scs": []}
    return {"va": [], "scs": []}


def save_candidate_files(response_text: str, task_dir: Path, sample_dir: Path) -> list[str]:
    targets = release_targets(task_dir)
    saved: list[str] = []
    marked = extract_marked_artifacts(response_text)

    def clean_artifact_text(text: str) -> str:
        cleaned = text.strip()
        cleaned = re.sub(r"^\s*```[A-Za-z0-9_.+-]*\s*\n", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)
        return cleaned.strip()

    def write_file(name: str, text: str) -> None:
        out = sample_dir / Path(name).name
        out.write_text(clean_artifact_text(text) + "\n", encoding="utf-8")
        saved.append(str(out))

    for target in targets:
        if target in marked:
            write_file(target, marked[target])

    for name, text in marked.items():
        if name not in targets:
            write_file(name, text)

    if saved:
        return saved

    blocks = fallback_code_blocks(response_text)
    va_idx = 0
    scs_idx = 0

    for target in targets:
        if target.endswith(".va") and va_idx < len(blocks["va"]):
            write_file(target, blocks["va"][va_idx])
            va_idx += 1
        elif target.endswith(".scs") and scs_idx < len(blocks["scs"]):
            write_file(target, blocks["scs"][scs_idx])
            scs_idx += 1

    for code in blocks["va"][va_idx:]:
        write_file(infer_va_name(code), code)
    for code in blocks["scs"][scs_idx:]:
        write_file(infer_scs_name(code), code)
    return saved


def call_minimax(
    *,
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    timeout_s: int,
    network_mode: str,
    token_param: str,
    auth_header: str,
    extra_body: dict[str, Any] | None = None,
) -> tuple[str, dict[str, Any]]:
    payload = request_payload(
        model=model,
        system_prompt=system_prompt,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        token_param=token_param,
    )
    if extra_body:
        payload.update(extra_body)
    with tempfile.TemporaryDirectory(prefix="minimax_call_") as tmp:
        tmp_path = Path(tmp)
        payload_path = tmp_path / "payload.json"
        header_path = tmp_path / "auth.header"
        response_path = tmp_path / "response.json"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        header_path.write_text("\n".join(auth_header_lines(api_key, auth_header)) + "\n", encoding="utf-8")
        header_path.chmod(0o600)
        endpoint = base_url.rstrip("/") + "/chat/completions"

        def run_curl(*, use_direct: bool) -> subprocess.CompletedProcess[str]:
            cmd = [
                "curl",
                "-sS",
                "--ipv4",
                "--connect-timeout",
                "20",
                "--max-time",
                str(timeout_s),
                "-H",
                f"@{header_path}",
                "-H",
                "Content-Type: application/json",
                endpoint,
                "-d",
                f"@{payload_path}",
            ]
            if use_direct:
                cmd[1:1] = ["--noproxy", "*"]
            return subprocess.run(cmd, text=True, capture_output=True)

        if network_mode == "direct":
            proc = run_curl(use_direct=True)
        elif network_mode == "env":
            proc = run_curl(use_direct=False)
        else:
            proc = run_curl(use_direct=True)
            if proc.returncode != 0:
                proc = run_curl(use_direct=False)
        response_path.write_text(proc.stdout or "", encoding="utf-8")
        if proc.returncode != 0:
            raise RuntimeError(f"curl_returncode={proc.returncode}: {(proc.stderr or proc.stdout)[-600:]}")
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"bad_json_response: {proc.stdout[:600]}") from exc
    if "error" in data:
        error = data.get("error") or {}
        message = error.get("message") if isinstance(error, dict) else str(error)
        err_type = error.get("type") if isinstance(error, dict) else "api_error"
        code = error.get("http_code") if isinstance(error, dict) else ""
        raise RuntimeError(f"{err_type}: {message} ({code})")
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"no_choices_in_response: {str(data)[:600]}")
    message = choices[0].get("message") or {}
    text = message.get("content") or ""
    usage = data.get("usage") or {}
    return text, {
        "input_tokens": usage.get("prompt_tokens") or usage.get("input_tokens") or 0,
        "output_tokens": usage.get("completion_tokens") or usage.get("output_tokens") or 0,
        "total_tokens": usage.get("total_tokens") or 0,
        "finish_reason": choices[0].get("finish_reason", ""),
        "request_id": data.get("id", ""),
    }


def call_anthropic_compatible(
    *,
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    timeout_s: int,
    network_mode: str,
    extra_body: dict[str, Any] | None = None,
) -> tuple[str, dict[str, Any]]:
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system_prompt,
        "messages": [{"role": "user", "content": prompt}],
    }
    if extra_body:
        payload.update(extra_body)
    with tempfile.TemporaryDirectory(prefix="anthropic_call_") as tmp:
        tmp_path = Path(tmp)
        payload_path = tmp_path / "payload.json"
        header_path = tmp_path / "auth.header"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        header_path.write_text(
            f"x-api-key: {api_key}\n"
            "anthropic-version: 2023-06-01\n"
            "Content-Type: application/json\n",
            encoding="utf-8",
        )
        header_path.chmod(0o600)
        endpoint = anthropic_messages_endpoint(base_url)

        def run_curl(*, use_direct: bool) -> subprocess.CompletedProcess[str]:
            cmd = [
                "curl",
                "-sS",
                "--ipv4",
                "--connect-timeout",
                "20",
                "--max-time",
                str(timeout_s),
                "-H",
                f"@{header_path}",
                endpoint,
                "-d",
                f"@{payload_path}",
            ]
            if use_direct:
                cmd[1:1] = ["--noproxy", "*"]
            return subprocess.run(cmd, text=True, capture_output=True)

        if network_mode == "direct":
            proc = run_curl(use_direct=True)
        elif network_mode == "env":
            proc = run_curl(use_direct=False)
        else:
            proc = run_curl(use_direct=True)
            if proc.returncode != 0:
                proc = run_curl(use_direct=False)
        if proc.returncode != 0:
            raise RuntimeError(f"curl_returncode={proc.returncode}: {(proc.stderr or proc.stdout)[-600:]}")
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"bad_json_response: {proc.stdout[:600]}") from exc
    if "error" in data:
        error = data.get("error") or {}
        message = error.get("message") if isinstance(error, dict) else str(error)
        err_type = (error.get("type") or error.get("code") or "api_error") if isinstance(error, dict) else "api_error"
        raise RuntimeError(f"{err_type}: {message}")
    content = data.get("content") or []
    parts: list[str] = []
    for block in content:
        if isinstance(block, dict):
            if block.get("type") == "text" or "text" in block:
                parts.append(str(block.get("text", "")))
        elif isinstance(block, str):
            parts.append(block)
    text = "\n".join(part for part in parts if part)
    usage = data.get("usage") or {}
    return text, {
        "input_tokens": usage.get("input_tokens") or 0,
        "output_tokens": usage.get("output_tokens") or 0,
        "total_tokens": (usage.get("input_tokens") or 0) + (usage.get("output_tokens") or 0),
        "finish_reason": data.get("stop_reason", ""),
        "request_id": data.get("id", ""),
    }


def is_quota_or_rate_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return any(token in text for token in ("rate_limit", "usage limit", "quota", "429", "too many requests"))


def generate_one(
    *,
    row: dict[str, Any],
    api_key: str,
    base_url: str,
    model: str,
    output_root: Path,
    sample_idx: int,
    max_tokens: int,
    temperature: float,
    request_timeout_s: int,
    api_attempts: int,
    quota_retry_sleep_s: int,
    network_mode: str,
    api_format: str,
    token_param: str,
    auth_header: str,
    extra_body: dict[str, Any] | None,
    resume: bool,
    dry_run: bool,
) -> dict[str, Any]:
    task_dir = form_dir(row)
    key = task_key(row, task_dir)
    slug = model_slug(model)
    sample_dir = output_root / "generated" / slug / key / f"sample_{sample_idx}"
    meta_path = sample_dir / "generation_meta.json"
    if resume and meta_path.exists():
        old = read_json(meta_path)
        if old.get("status") in {"generated", "no_code_extracted"}:
            return old

    sample_dir.mkdir(parents=True, exist_ok=True)
    resolved_token, resolved_auth = resolved_api_metadata(
        api_format=api_format,
        base_url=base_url,
        model=model,
        token_param=token_param,
        auth_header=auth_header,
    )
    public_prompt_text = (task_dir / "prompt.md").read_text(encoding="utf-8")
    target_artifacts = release_targets(task_dir)
    support_artifacts = release_support_artifacts(task_dir, target_artifacts)
    prompt_text = build_release_generation_prompt(
        public_prompt=public_prompt_text,
        target_artifacts=target_artifacts,
        form=str(row.get("form") or ""),
        support_artifacts=support_artifacts,
    )
    (sample_dir / "public_prompt.md").write_text(public_prompt_text, encoding="utf-8")
    (sample_dir / "prompt_sent.md").write_text(prompt_text, encoding="utf-8")
    base_meta = {
        "status": "pending",
        "benchmark": "vabench-release-v1",
        "source": "api_prompt_only_release_baseline",
        "runner_wrapper_version": RELEASE_RUNNER_WRAPPER_VERSION,
        "model": model,
        "model_slug": slug,
        "task_id": key,
        "release_task_id": row.get("task_id"),
        "release_entry_id": row.get("release_entry_id"),
        "form": row.get("form"),
        "level": row.get("level"),
        "difficulty": row.get("difficulty"),
        "category": row.get("category"),
        "sample_idx": sample_idx,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "token_param": resolved_token,
        "auth_header": resolved_auth,
        "target_artifacts": target_artifacts,
        "support_artifacts": sorted(support_artifacts),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_base_url": base_url,
        "api_format": api_format,
        "api_key_source": "ANTHROPIC_API_KEY_or_MINIMAX_API_KEY_or_file"
        if api_format == "anthropic"
        else "MINIMAX_API_KEY_or_file",
    }
    if dry_run:
        meta = {**base_meta, "status": "dry_run", "saved_files": []}
        meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        return meta

    last_error = ""
    for attempt in range(1, api_attempts + 1):
        try:
            if api_format == "anthropic":
                response_text, usage = call_anthropic_compatible(
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    system_prompt=RELEASE_SYSTEM_PROMPT,
                    prompt=prompt_text,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    timeout_s=request_timeout_s,
                    network_mode=network_mode,
                    extra_body=extra_body,
                )
            else:
                response_text, usage = call_minimax(
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    system_prompt=RELEASE_SYSTEM_PROMPT,
                    prompt=prompt_text,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    timeout_s=request_timeout_s,
                    network_mode=network_mode,
                    token_param=resolved_token,
                    auth_header=resolved_auth,
                    extra_body=extra_body,
                )
            (sample_dir / "raw_response.txt").write_text(response_text, encoding="utf-8")
            saved = save_candidate_files(response_text, task_dir, sample_dir)
            status = "generated" if saved else "no_code_extracted"
            meta = {
                **base_meta,
                "status": status,
                "saved_files": [rel(Path(path)) for path in saved],
                "raw_response_length": len(response_text),
                "api_attempts_used": attempt,
                **usage,
            }
            meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
            return meta
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {str(exc)[:800]}"
            if attempt < api_attempts and is_quota_or_rate_error(exc) and quota_retry_sleep_s > 0:
                print(
                    f"[generate] {key} api_retry={attempt}/{api_attempts} "
                    f"quota_or_rate_error sleep={quota_retry_sleep_s}s",
                    flush=True,
                )
                time.sleep(quota_retry_sleep_s)
                continue
            if attempt < api_attempts and not is_quota_or_rate_error(exc):
                delay_s = min(60, 5 * attempt)
                print(
                    f"[generate] {key} api_retry={attempt}/{api_attempts} "
                    f"transient_error sleep={delay_s}s",
                    flush=True,
                )
                time.sleep(delay_s)
                continue
            break

    meta = {
        **base_meta,
        "status": "api_error",
        "error": last_error,
        "api_attempts_used": api_attempts,
        "saved_files": [],
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def run_generation(
    *,
    rows: list[dict[str, Any]],
    api_key: str,
    base_url: str,
    model: str,
    output_root: Path,
    sample_idx: int,
    max_tokens: int,
    temperature: float,
    request_timeout_s: int,
    api_attempts: int,
    quota_retry_sleep_s: int,
    network_mode: str,
    api_format: str,
    token_param: str,
    auth_header: str,
    extra_body: dict[str, Any] | None,
    workers: int,
    resume: bool,
    dry_run: bool,
) -> list[dict[str, Any]]:
    output_root.mkdir(parents=True, exist_ok=True)
    effective_workers = max(1, min(workers, len(rows) or 1))
    results: list[dict[str, Any]] = []
    if effective_workers == 1:
        for index, row in enumerate(rows, start=1):
            print(f"[generate] {index}/{len(rows)} {row['task_id']} ...", flush=True)
            meta = generate_one(
                row=row,
                api_key=api_key,
                base_url=base_url,
                model=model,
                output_root=output_root,
                sample_idx=sample_idx,
                max_tokens=max_tokens,
                temperature=temperature,
                request_timeout_s=request_timeout_s,
                api_attempts=api_attempts,
                quota_retry_sleep_s=quota_retry_sleep_s,
                network_mode=network_mode,
                api_format=api_format,
                token_param=token_param,
                auth_header=auth_header,
                extra_body=extra_body,
                resume=resume,
                dry_run=dry_run,
            )
            print(f"[generate] {row['task_id']} {meta['status']}", flush=True)
            results.append(meta)
        return results
    with ThreadPoolExecutor(max_workers=effective_workers) as executor:
        future_to_row = {
            executor.submit(
                generate_one,
                row=row,
                api_key=api_key,
                base_url=base_url,
                model=model,
                output_root=output_root,
                sample_idx=sample_idx,
                max_tokens=max_tokens,
                temperature=temperature,
                request_timeout_s=request_timeout_s,
                api_attempts=api_attempts,
                quota_retry_sleep_s=quota_retry_sleep_s,
                network_mode=network_mode,
                api_format=api_format,
                token_param=token_param,
                auth_header=auth_header,
                extra_body=extra_body,
                resume=resume,
                dry_run=dry_run,
            ): row
            for row in rows
        }
        for future in as_completed(future_to_row):
            row = future_to_row[future]
            meta = future.result()
            print(f"[generate] {row['task_id']} {meta['status']}", flush=True)
            results.append(meta)
    return results


def run_scoring(
    *,
    rows: list[dict[str, Any]],
    model: str,
    output_root: Path,
    sample_idx: int,
    temperature: float,
    top_p: float,
    timeout_s: int,
    workers: int,
    resume: bool,
) -> list[dict[str, Any]]:
    slug = model_slug(model)
    generated_root = output_root / "generated"
    score_root = output_root / "evas_results"
    score_root.mkdir(parents=True, exist_ok=True)

    def score_row(row: dict[str, Any]) -> dict[str, Any]:
        task_dir = form_dir(row)
        key = task_key(row, task_dir)
        sample_dir = generated_root / slug / key / f"sample_{sample_idx}"
        result_path = score_root / key / "result.json"
        if resume and result_path.exists():
            return read_json(result_path)
        meta = read_meta(task_dir)
        if not sample_dir.exists():
            result = _fail_result(
                key,
                slug,
                meta.get("family", "unknown"),
                meta.get("category", row.get("category", "unknown")),
                sample_idx,
                temperature,
                top_p,
                meta.get("scoring", ["dut_compile", "tb_compile", "sim_correct"]),
                "missing_generated_sample",
                None,
                None,
            )
        else:
            result = score_one_task(
                key,
                task_dir,
                sample_dir,
                score_root,
                model=slug,
                sample_idx=sample_idx,
                temperature=temperature,
                top_p=top_p,
                timeout_s=timeout_s,
            )
        result.update(
            {
                "benchmark": "vabench-release-v1",
                "release_task_id": row.get("task_id"),
                "release_entry_id": row.get("release_entry_id"),
                "form": row.get("form"),
                "level": row.get("level"),
                "difficulty": row.get("difficulty"),
                "track": row.get("track"),
                "counted_in_score": row.get("counted_in_score"),
            }
        )
        out = score_root / key / "result.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result

    results: list[dict[str, Any]] = []
    effective_workers = max(1, min(workers, len(rows) or 1))
    if effective_workers == 1:
        for index, row in enumerate(rows, start=1):
            print(f"[score] {index}/{len(rows)} {row['task_id']} ...", flush=True)
            result = score_row(row)
            print(f"[score] {row['task_id']} {result.get('status')}", flush=True)
            results.append(result)
        return results
    with ThreadPoolExecutor(max_workers=effective_workers) as executor:
        future_to_row = {executor.submit(score_row, row): row for row in rows}
        for future in as_completed(future_to_row):
            row = future_to_row[future]
            result = future.result()
            print(f"[score] {row['task_id']} {result.get('status')}", flush=True)
            results.append(result)
    return results


def rate_by_key(results: list[dict[str, Any]], key: str) -> dict[str, Any]:
    groups: dict[str, dict[str, int]] = {}
    for result in results:
        value = str(result.get(key, "unknown"))
        groups.setdefault(value, {"total": 0, "pass": 0})
        groups[value]["total"] += 1
        if _task_pass(result):
            groups[value]["pass"] += 1
    return {
        name: {
            "total": stats["total"],
            "pass": stats["pass"],
            "pass_rate": round(stats["pass"] / stats["total"], 4) if stats["total"] else 0.0,
        }
        for name, stats in sorted(groups.items())
    }


def write_summary(
    *,
    rows: list[dict[str, Any]],
    generation: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    model: str,
    output_root: Path,
    stage: str,
    temperature: float,
    top_p: float,
    dry_run: bool,
) -> dict[str, Any]:
    gen_status_counts: dict[str, int] = {}
    for item in generation:
        status = str(item.get("status", "missing"))
        gen_status_counts[status] = gen_status_counts.get(status, 0) + 1
    aggregate = build_model_results(model_slug(model), scores, temperature, top_p) if scores else {}
    pass_count = sum(1 for result in scores if _task_pass(result))
    summary = {
        "date": datetime.now(timezone.utc).isoformat(),
        "benchmark": "vabench-release-v1",
        "model": model,
        "model_slug": model_slug(model),
        "runner_wrapper_version": RELEASE_RUNNER_WRAPPER_VERSION,
        "stage": stage,
        "dry_run": dry_run,
        "status": "completed" if not any(item.get("status") == "api_error" for item in generation) else "api_errors_present",
        "claim_allowed": False,
        "claim_boundary": "EVAS filter baseline only; Spectre final judge is pending.",
        "score_denominator": rel(SCORE_DENOMINATOR),
        "selected_scored_forms": len(rows),
        "generation_status_counts": gen_status_counts,
        "scored_forms": len(scores),
        "evas_pass_count": pass_count,
        "evas_pass_rate": round(pass_count / len(scores), 4) if scores else 0.0,
        "aggregate": aggregate,
        "by_form": rate_by_key(scores, "form") if scores else {},
        "by_difficulty": rate_by_key(scores, "difficulty") if scores else {},
        "by_category": rate_by_key(scores, "category") if scores else {},
        "spectre_final_judge": {
            "status": "pending",
            "reason": "Run Spectre confirmation on EVAS PASS candidates before paper-facing model baseline claims.",
        },
        "prompt_layering": {
            "public_prompt_version": "public-contract-v3",
            "runner_wrapper_version": RELEASE_RUNNER_WRAPPER_VERSION,
            "boundary": "Question/Answer, file markers, and shared EVAS/Spectre rules are runner-side baseline protocol, not public benchmark prompt content.",
        },
        "paths": {
            "output_root": rel(output_root),
            "generated_root": rel(output_root / "generated"),
            "evas_results_root": rel(output_root / "evas_results"),
            "summary": rel(output_root / "summary.json"),
        },
    }
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# vaBench Release API Model Baseline",
        "",
        f"Date: {summary['date']}",
        f"Model: `{model}`",
        "",
        "This is a prompt-only EVAS-filter baseline. Spectre final judge is pending.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| selected scored forms | {summary['selected_scored_forms']} |",
        f"| generation status | `{summary['generation_status_counts']}` |",
        f"| EVAS scored forms | {summary['scored_forms']} |",
        f"| EVAS pass@1 | {summary['evas_pass_rate']} |",
        f"| EVAS pass count | {summary['evas_pass_count']} |",
        f"| claim allowed | `{summary['claim_allowed']}` |",
        "",
        "## By Form",
        "",
        "| Form | Pass | Total | Pass Rate |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, stats in summary["by_form"].items():
        lines.append(f"| `{name}` | {stats['pass']} | {stats['total']} | {stats['pass_rate']} |")
    lines.extend(["", "## By Difficulty", "", "| Difficulty | Pass | Total | Pass Rate |", "| --- | ---: | ---: | ---: |"])
    for name, stats in summary["by_difficulty"].items():
        lines.append(f"| `{name}` | {stats['pass']} | {stats['total']} | {stats['pass_rate']} |")
    (output_root / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--api-format", choices=["openai", "anthropic"], default="openai")
    ap.add_argument("--api-key-file", default="")
    ap.add_argument("--stage", choices=["generate", "score", "all"], default="all")
    ap.add_argument("--output-root", default="")
    ap.add_argument("--tag", default="")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--entry", action="append", default=[])
    ap.add_argument("--form", action="append", default=[])
    ap.add_argument("--difficulty", action="append", default=[])
    ap.add_argument("--category", action="append", default=[])
    ap.add_argument("--task-id", action="append", default=[])
    ap.add_argument(
        "--task-id-file",
        action="append",
        default=[],
        help="File with one release task id per line, e.g. vbr1_l1_example:tb.",
    )
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
    ap.add_argument(
        "--token-param",
        choices=["auto", "max_tokens", "max_completion_tokens"],
        default="auto",
        help="Chat-completions output token field. auto uses max_completion_tokens for MiMo v2 endpoints.",
    )
    ap.add_argument(
        "--auth-header",
        choices=["auto", "authorization", "api-key", "both"],
        default="auto",
        help="API authentication header. auto uses api-key for MiMo v2 endpoints and Authorization otherwise.",
    )
    ap.add_argument(
        "--extra-body-json",
        default=os.environ.get("VAEVAS_BASELINE_EXTRA_BODY_JSON", ""),
        help="Optional JSON object merged into each OpenAI-compatible chat completion payload.",
    )
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    task_ids = set(args.task_id)
    for task_id_file in args.task_id_file:
        task_ids.update(
            line.strip()
            for line in Path(task_id_file).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )

    rows = scored_form_rows(
        limit=args.limit,
        entry=set(args.entry) or None,
        form=set(args.form) or None,
        difficulty=set(args.difficulty) or None,
        category=set(args.category) or None,
        task_id=task_ids or None,
    )
    if not rows:
        print("No scored release forms selected.")
        return 1
    extra_body: dict[str, Any] | None = None
    if args.extra_body_json:
        parsed_extra = json.loads(args.extra_body_json)
        if not isinstance(parsed_extra, dict):
            raise SystemExit("--extra-body-json must decode to a JSON object")
        extra_body = parsed_extra
    output_root = Path(args.output_root) if args.output_root else output_root_for(args.model, args.tag or None)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    output_root.mkdir(parents=True, exist_ok=True)

    api_key = "" if args.stage == "score" or args.dry_run else load_api_key(args.api_key_file or None, args.api_format)
    print(
        f"[minimax-baseline] model={args.model} forms={len(rows)} stage={args.stage} "
        f"output={rel(output_root)}",
        flush=True,
    )
    generation: list[dict[str, Any]] = []
    scores: list[dict[str, Any]] = []
    if args.stage in {"generate", "all"}:
        generation = run_generation(
            rows=rows,
            api_key=api_key,
            base_url=args.base_url,
            model=args.model,
            output_root=output_root,
            sample_idx=args.sample_idx,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            request_timeout_s=args.request_timeout_s,
            api_attempts=args.api_attempts,
            quota_retry_sleep_s=args.quota_retry_sleep_s,
            network_mode=args.network_mode,
            api_format=args.api_format,
            token_param=args.token_param,
            auth_header=args.auth_header,
            extra_body=extra_body,
            workers=args.gen_workers,
            resume=args.resume,
            dry_run=args.dry_run,
        )
    else:
        generated_root = output_root / "generated" / model_slug(args.model)
        for row in rows:
            key = task_key(row, form_dir(row))
            meta_path = generated_root / key / f"sample_{args.sample_idx}" / "generation_meta.json"
            if meta_path.exists():
                generation.append(read_json(meta_path))

    if args.stage in {"score", "all"} and not args.dry_run:
        scores = run_scoring(
            rows=rows,
            model=args.model,
            output_root=output_root,
            sample_idx=args.sample_idx,
            temperature=args.temperature,
            top_p=args.top_p,
            timeout_s=args.score_timeout_s,
            workers=args.score_workers,
            resume=args.resume,
        )
    summary = write_summary(
        rows=rows,
        generation=generation,
        scores=scores,
        model=args.model,
        output_root=output_root,
        stage=args.stage,
        temperature=args.temperature,
        top_p=args.top_p,
        dry_run=args.dry_run,
    )
    print(
        "[minimax-baseline] done "
        f"status={summary['status']} evas_pass={summary['evas_pass_count']}/{summary['scored_forms']} "
        f"summary={summary['paths']['summary']}",
        flush=True,
    )
    return 0 if summary["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
