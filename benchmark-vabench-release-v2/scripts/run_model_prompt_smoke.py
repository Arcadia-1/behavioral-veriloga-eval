#!/usr/bin/env python3
"""Run a minimal OpenAI-compatible model smoke test on vaBench v2 prompts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time
from typing import Any
import urllib.error
import urllib.request


DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_SYSTEM_PROMPT = (
    "You are solving a vaBench behavioral Verilog-A task. Return only the "
    "requested target artifact contents using the requested filenames."
)
SECRET_ENV_CANDIDATES = ("DEEPSEEK_API_KEY", "OPENAI_API_KEY")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_renderer(script_dir: Path):
    renderer_path = script_dir / "render_agent_prompt.py"
    spec = importlib.util.spec_from_file_location("render_agent_prompt", renderer_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load renderer from {renderer_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def model_slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


def default_output_root(model: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path("/private/tmp") / f"vabench-v2-model-smoke-{model_slug(model)}-{stamp}"


def task_card_paths(root: Path) -> list[Path]:
    return sorted(root.glob("tasks/**/task_release_card.json"))


def select_task_cards(root: Path, task_ids: set[str] | None, limit: int | None) -> list[Path]:
    selected: list[Path] = []
    for card_path in task_card_paths(root):
        card = load_json(card_path)
        task_id = str(card.get("id") or "")
        release_entry_id = str(card.get("release_entry_id") or "")
        if task_ids and task_id not in task_ids and release_entry_id not in task_ids:
            continue
        selected.append(card_path)
    if limit is not None:
        selected = selected[:limit]
    return selected


def manifest_path_for_card(card_path: Path) -> Path:
    card = load_json(card_path)
    artifacts = card.get("artifacts", {})
    manifest_name = artifacts.get("agent_visible_files", "agent_visible_files.json")
    return card_path.parent / manifest_name


def chat_endpoint(base_url: str) -> str:
    stripped = base_url.rstrip("/")
    if stripped.endswith("/chat/completions"):
        return stripped
    if stripped.endswith("/v1"):
        return stripped + "/chat/completions"
    return stripped + "/chat/completions"


def api_key_from_env(env_name: str | None) -> tuple[str, str]:
    env_names = [env_name] if env_name else list(SECRET_ENV_CANDIDATES)
    for candidate in env_names:
        if not candidate:
            continue
        value = os.environ.get(candidate, "").strip()
        if value:
            return value, f"env:{candidate}"
    expected = ", ".join(env_names)
    raise SystemExit(f"API key not found in environment: {expected}")


def load_api_key(api_key_file: str, api_key_env: str | None) -> tuple[str, str]:
    if api_key_file:
        path = Path(api_key_file).expanduser()
        key = path.read_text(encoding="utf-8").strip()
        if not key:
            raise SystemExit(f"empty API key file: {path}")
        return key, f"file:{path}"
    return api_key_from_env(api_key_env)


def request_payload(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
    thinking: str,
    reasoning_effort: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if thinking != "omit":
        payload["thinking"] = {"type": thinking}
    if thinking == "enabled":
        payload["reasoning_effort"] = reasoning_effort
    return payload


def call_openai_compatible(
    *,
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
    thinking: str,
    reasoning_effort: str,
    timeout_s: int,
) -> tuple[str, dict[str, Any]]:
    payload = request_payload(
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        thinking=thinking,
        reasoning_effort=reasoning_effort,
    )
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        chat_endpoint(base_url),
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            response_body = response.read().decode("utf-8", errors="replace")
            status_code = response.status
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"http_{exc.code}: {error_body[:1200]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"url_error: {exc}") from exc

    elapsed_s = time.perf_counter() - started
    try:
        data = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"bad_json_response: {response_body[:1200]}") from exc
    if "error" in data:
        raise RuntimeError(f"api_error: {json.dumps(data['error'], ensure_ascii=False)[:1200]}")
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"no_choices: {json.dumps(data, ensure_ascii=False)[:1200]}")
    choice = choices[0]
    message = choice.get("message") or {}
    text = message.get("content") or ""
    if not text.strip():
        raise RuntimeError(
            "empty_response_content: "
            f"finish_reason={choice.get('finish_reason')}; "
            f"usage={json.dumps(data.get('usage', {}), ensure_ascii=False)[:800]}"
        )
    return text, {
        "status_code": status_code,
        "elapsed_s": round(elapsed_s, 3),
        "usage": data.get("usage", {}),
        "finish_reason": choice.get("finish_reason"),
        "thinking": thinking,
        "reasoning_effort": reasoning_effort if thinking == "enabled" else "",
        "response_id": data.get("id", ""),
    }


def row_for_card(
    *,
    card_path: Path,
    root: Path,
    renderer,
    output_root: Path,
    dry_run: bool,
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str,
    max_tokens: int,
    temperature: float,
    thinking: str,
    reasoning_effort: str,
    timeout_s: int,
) -> dict[str, Any]:
    card = load_json(card_path)
    manifest_path = manifest_path_for_card(card_path)
    prompt = renderer.render_agent_prompt(manifest_path)
    prompt_sha256 = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    task_id = str(card.get("id") or manifest_path.parent.name)
    task_dir = output_root / task_id.replace(":", "__")
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    row: dict[str, Any] = {
        "task_id": task_id,
        "release_entry_id": card.get("release_entry_id"),
        "manifest": manifest_path.relative_to(root).as_posix(),
        "prompt_path": str(task_dir / "prompt.md"),
        "prompt_chars": len(prompt),
        "prompt_sha256": prompt_sha256,
        "renderer_version": getattr(renderer, "RENDERER_VERSION", ""),
        "status": "DRY_RUN" if dry_run else "PENDING",
    }
    if dry_run:
        return row

    try:
        response_text, metadata = call_openai_compatible(
            api_key=api_key,
            base_url=base_url,
            model=model,
            system_prompt=system_prompt,
            user_prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            thinking=thinking,
            reasoning_effort=reasoning_effort,
            timeout_s=timeout_s,
        )
    except Exception as exc:  # noqa: BLE001 - smoke runner should record model/API failures.
        row.update({"status": "FAIL", "error": str(exc)[:2000]})
        return row

    response_path = task_dir / "response.txt"
    response_path.write_text(response_text, encoding="utf-8")
    write_json(task_dir / "response_metadata.json", metadata)
    row.update(
        {
            "status": "PASS",
            "response_path": str(response_path),
            "response_chars": len(response_text),
            "metadata_path": str(task_dir / "response_metadata.json"),
            "usage": metadata.get("usage", {}),
        }
    )
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="benchmark-vabench-release-v2 root directory",
    )
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key-env", default="DEEPSEEK_API_KEY")
    parser.add_argument("--api-key-file", default="")
    parser.add_argument("--system-prompt", default=DEFAULT_SYSTEM_PROMPT)
    parser.add_argument("--task-id", action="append", default=[])
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--thinking", choices=["omit", "enabled", "disabled"], default="disabled")
    parser.add_argument("--reasoning-effort", choices=["high", "max"], default="high")
    parser.add_argument("--timeout-s", type=int, default=120)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.root
    output_root = args.output_root or default_output_root(args.model)
    output_root.mkdir(parents=True, exist_ok=True)
    renderer = load_renderer(root / "scripts")
    selected = select_task_cards(root, set(args.task_id) if args.task_id else None, args.limit)
    if not selected:
        raise SystemExit("no v2 task cards selected")

    api_key = ""
    api_key_source = "not_used_dry_run"
    if not args.dry_run:
        api_key, api_key_source = load_api_key(args.api_key_file, args.api_key_env)

    rows = [
        row_for_card(
            card_path=card_path,
            root=root,
            renderer=renderer,
            output_root=output_root,
            dry_run=args.dry_run,
            api_key=api_key,
            base_url=args.base_url,
            model=args.model,
            system_prompt=args.system_prompt,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            thinking=args.thinking,
            reasoning_effort=args.reasoning_effort,
            timeout_s=args.timeout_s,
        )
        for card_path in selected
    ]
    summary = {
        "date": datetime.now(timezone.utc).isoformat(),
        "release": "vabench-release-v2",
        "status": "PASS" if all(row["status"] in {"PASS", "DRY_RUN"} for row in rows) else "FAIL",
        "dry_run": args.dry_run,
        "model": args.model,
        "base_url": args.base_url,
        "temperature": args.temperature,
        "thinking": args.thinking,
        "reasoning_effort": args.reasoning_effort if args.thinking == "enabled" else "",
        "api_key_source": api_key_source,
        "selected_count": len(rows),
        "pass_count": sum(1 for row in rows if row["status"] == "PASS"),
        "output_root": str(output_root),
        "rows": rows,
    }
    write_json(output_root / "summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
