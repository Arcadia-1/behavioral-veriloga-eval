#!/usr/bin/env python3
"""Run prompt-only model evaluation on vaBench release-v3 tasks.

This runner is v3-native: it reads benchmark-vabench-release-v3/TASKS.json and
the v3 score-denominator manifest, presents public instruction.md contracts to
the model, stages public starter support artifacts, and scores generated DUTs
with the v3 hidden EVAS checker. The default selection is the current v3
candidate denominator, not counted_in_score, because the v3 formal score policy
is intentionally not frozen yet.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys
import time
from typing import Any

from generate import extract_code_blocks
from run_vabench_release_minimax_baseline import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    call_anthropic_compatible,
    call_minimax,
    is_quota_or_rate_error,
    load_api_key,
    model_slug,
    resolved_api_metadata,
)
from simulate_evas import (
    read_task_artifact_supports,
    read_task_artifact_targets,
    read_task_index_id,
    run_case,
)
from vabench_release_prompt_wrapper import (
    RELEASE_RUNNER_WRAPPER_VERSION,
    RELEASE_SYSTEM_PROMPT,
    build_release_generation_prompt,
    clean_artifact_text,
    extract_marked_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v3"
TASKS_JSON = PACKAGE_ROOT / "TASKS.json"
DEFAULT_SCORE_ROSTER = PACKAGE_ROOT / "reports" / "score_denominator_manifest.json"
RESULTS_ROOT = ROOT / "results"

CLAIM_BOUNDARY = (
    "v3 model runs are exploratory unless a future manifest marks "
    "counted_in_score=true. EVAS is the fast behavior gate; Spectre remains the "
    "final paper-facing judge."
)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def output_root_for(model: str, tag: str) -> Path:
    stamp = tag or datetime.now().strftime("%Y%m%d-%H%M%S")
    return RESULTS_ROOT / f"vabench-v3-model-eval-{model_slug(model)}-{stamp}"


def load_tasks() -> dict[str, dict[str, Any]]:
    payload = read_json(TASKS_JSON)
    defaults = payload.get("defaults", {})
    tasks: dict[str, dict[str, Any]] = {}
    for slug, entry in payload.get("tasks", {}).items():
        if not isinstance(entry, dict):
            continue
        merged = dict(defaults) if isinstance(defaults, dict) else {}
        merged.update(entry)
        tasks[str(slug)] = merged
    return tasks


def slug_number(slug: str) -> int:
    try:
        return int(slug.split("-", 1)[0])
    except ValueError:
        return 10**9


def task_dir(slug: str) -> Path:
    return PACKAGE_ROOT / "tasks" / slug


def task_tokens_from_args(args: argparse.Namespace) -> set[str]:
    tokens = {str(item).strip() for item in args.task if str(item).strip()}
    for raw_path in args.task_file:
        path = resolve_repo_path(raw_path)
        tokens.update(
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    return tokens


def task_matches(row: dict[str, Any], tokens: set[str]) -> bool:
    if not tokens:
        return True
    slug = str(row.get("release_entry_id") or "")
    task_id = str(row.get("task_id") or "")
    number = f"{slug_number(slug):03d}"
    return slug in tokens or task_id in tokens or number in tokens


def base_rows_from_denominator(score_roster: Path, tasks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if not score_roster.exists():
        rows: list[dict[str, Any]] = []
        for slug, task in tasks.items():
            rows.append({
                "release_entry_id": slug,
                "task_id": str(task.get("id") or slug),
                "form": str(task.get("form") or "dut"),
                "level": str(task.get("level") or ""),
                "track": "unknown",
                "difficulty": str(task.get("difficulty") or ""),
                "category": str(task.get("category") or ""),
                "base_function": str(task.get("title") or ""),
                "candidate_score_denominator": False,
                "counted_in_score": False,
                "spectre_recalibration_required": False,
            })
        return rows
    payload = read_json(score_roster)
    rows = payload.get("form_rows", [])
    return [dict(row) for row in rows if isinstance(row, dict)]


def selected_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    tasks = load_tasks()
    rows = base_rows_from_denominator(resolve_repo_path(args.score_roster), tasks)
    if args.selection_surface == "candidate":
        rows = [row for row in rows if row.get("candidate_score_denominator") is True]
    elif args.selection_surface == "counted":
        rows = [row for row in rows if row.get("counted_in_score") is True]
    elif args.selection_surface != "all":
        raise ValueError(f"unsupported selection surface: {args.selection_surface}")

    task_tokens = task_tokens_from_args(args)
    rows = [row for row in rows if task_matches(row, task_tokens)]
    if args.level:
        wanted = set(args.level)
        rows = [row for row in rows if str(row.get("level")) in wanted]
    if args.track:
        wanted = set(args.track)
        rows = [row for row in rows if str(row.get("track")) in wanted]
    if args.difficulty:
        wanted = set(args.difficulty)
        rows = [row for row in rows if str(row.get("difficulty")) in wanted]
    if args.category:
        wanted = set(args.category)
        rows = [row for row in rows if str(row.get("category")) in wanted]
    if args.exclude_spectre_divergent:
        rows = [row for row in rows if row.get("spectre_recalibration_required") is not True]

    rows.sort(key=lambda row: slug_number(str(row.get("release_entry_id") or "")))
    if args.limit is not None:
        rows = rows[: args.limit]
    return [augment_row(row, tasks) for row in rows]


def augment_row(row: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> dict[str, Any]:
    slug = str(row.get("release_entry_id") or "")
    task = tasks.get(slug, {})
    directory = task_dir(slug)
    targets = read_task_artifact_targets(directory)
    supports = read_task_artifact_supports(directory)
    augmented = dict(row)
    augmented.update({
        "task_dir": rel(directory),
        "instruction": rel(directory / "instruction.md"),
        "target_artifacts": targets,
        "support_artifacts": supports,
        "task_title": str(task.get("title") or row.get("base_function") or slug),
    })
    return augmented


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(key) or "unknown") for row in rows).items()))


def support_artifact_contents(directory: Path, support_names: list[str]) -> dict[str, str]:
    support: dict[str, str] = {}
    for name in support_names:
        path = directory / "starter" / name
        if path.exists() and path.is_file():
            support[name] = path.read_text(encoding="utf-8", errors="ignore")
    return support


def copy_public_support_artifacts(directory: Path, sample_dir: Path, support_names: list[str]) -> list[str]:
    copied: list[str] = []
    for name in support_names:
        src = directory / "starter" / name
        if not src.exists() or not src.is_file():
            continue
        dst = sample_dir / Path(name).name
        shutil.copyfile(src, dst)
        copied.append(str(dst.relative_to(sample_dir)))
    return copied


def fallback_code_blocks(response_text: str) -> dict[str, list[str]]:
    blocks = extract_code_blocks(response_text)
    if blocks["va"] or blocks["scs"]:
        return blocks
    stripped = response_text.strip()
    if not stripped:
        return {"va": [], "scs": []}
    if "simulator lang=spectre" in stripped.lower():
        return {"va": [], "scs": [stripped]}
    if "module " in stripped:
        return {"va": [stripped], "scs": []}
    return {"va": [], "scs": []}


def save_candidate_files(response_text: str, target_artifacts: list[str], sample_dir: Path) -> list[str]:
    saved: list[str] = []

    def write_file(filename: str, text: str) -> None:
        out = sample_dir / Path(filename).name
        out.write_text(clean_artifact_text(text) + "\n", encoding="utf-8")
        saved.append(str(out))

    marked = extract_marked_artifacts(response_text)
    for target in target_artifacts:
        if target in marked:
            write_file(target, marked[target])
    for name, text in marked.items():
        if name not in target_artifacts:
            write_file(name, text)
    if saved:
        return saved

    blocks = fallback_code_blocks(response_text)
    va_idx = 0
    scs_idx = 0
    for target in target_artifacts:
        if target.endswith((".va", ".vams")) and va_idx < len(blocks["va"]):
            write_file(target, blocks["va"][va_idx])
            va_idx += 1
        elif target.endswith(".scs") and scs_idx < len(blocks["scs"]):
            write_file(target, blocks["scs"][scs_idx])
            scs_idx += 1
    return saved


def call_model(
    *,
    api_format: str,
    api_key: str,
    base_url: str,
    model: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    timeout_s: int,
    network_mode: str,
    token_param: str,
    auth_header: str,
    extra_body: dict[str, Any] | None,
) -> tuple[str, dict[str, Any]]:
    if api_format == "anthropic":
        return call_anthropic_compatible(
            api_key=api_key,
            base_url=base_url,
            model=model,
            system_prompt=RELEASE_SYSTEM_PROMPT,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout_s=timeout_s,
            network_mode=network_mode,
            extra_body=extra_body,
        )
    return call_minimax(
        api_key=api_key,
        base_url=base_url,
        model=model,
        system_prompt=RELEASE_SYSTEM_PROMPT,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        timeout_s=timeout_s,
        network_mode=network_mode,
        token_param=token_param,
        auth_header=auth_header,
        extra_body=extra_body,
    )


def generate_one(
    *,
    row: dict[str, Any],
    api_key: str,
    args: argparse.Namespace,
    output_root: Path,
) -> dict[str, Any]:
    slug = str(row["release_entry_id"])
    directory = task_dir(slug)
    model_key = model_slug(args.model)
    sample_dir = output_root / "generated" / model_key / slug / f"sample_{args.sample_idx}"
    meta_path = sample_dir / "generation_meta.json"
    if args.resume and meta_path.exists():
        old = read_json(meta_path)
        if old.get("status") in {"generated", "no_code_extracted", "dry_run"}:
            return old

    sample_dir.mkdir(parents=True, exist_ok=True)
    targets = list(row.get("target_artifacts") or [])
    supports = list(row.get("support_artifacts") or [])
    copied_support = copy_public_support_artifacts(directory, sample_dir, supports)
    public_prompt_text = (directory / "instruction.md").read_text(encoding="utf-8")
    prompt_text = build_release_generation_prompt(
        public_prompt=public_prompt_text,
        target_artifacts=targets,
        form=str(row.get("form") or "dut"),
        support_artifacts=support_artifact_contents(directory, supports),
    )
    (sample_dir / "public_instruction.md").write_text(public_prompt_text, encoding="utf-8")
    (sample_dir / "prompt_sent.md").write_text(prompt_text, encoding="utf-8")

    resolved_token, resolved_auth = resolved_api_metadata(
        api_format=args.api_format,
        base_url=args.base_url,
        model=args.model,
        token_param=args.token_param,
        auth_header=args.auth_header,
    )
    base_meta = {
        "status": "pending",
        "benchmark": "benchmark-vabench-release-v3",
        "source": "api_prompt_only_v3_candidate_eval",
        "runner_wrapper_version": RELEASE_RUNNER_WRAPPER_VERSION,
        "model": args.model,
        "model_slug": model_key,
        "task_slug": slug,
        "task_id": row.get("task_id"),
        "form": row.get("form"),
        "level": row.get("level"),
        "difficulty": row.get("difficulty"),
        "category": row.get("category"),
        "selection_surface": args.selection_surface,
        "candidate_score_denominator": row.get("candidate_score_denominator"),
        "counted_in_score": row.get("counted_in_score"),
        "sample_idx": args.sample_idx,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "token_param": resolved_token,
        "auth_header": resolved_auth,
        "target_artifacts": targets,
        "support_artifacts": supports,
        "copied_support_artifacts": copied_support,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_base_url": args.base_url,
        "api_format": args.api_format,
        "claim_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if args.dry_run:
        meta = {**base_meta, "status": "dry_run", "saved_files": []}
        write_json(meta_path, meta)
        return meta

    extra_body = read_json(resolve_repo_path(args.extra_body_json)) if args.extra_body_json else None
    last_error = ""
    for attempt in range(1, args.api_attempts + 1):
        try:
            response_text, usage = call_model(
                api_format=args.api_format,
                api_key=api_key,
                base_url=args.base_url,
                model=args.model,
                prompt=prompt_text,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                timeout_s=args.request_timeout_s,
                network_mode=args.network_mode,
                token_param=resolved_token,
                auth_header=resolved_auth,
                extra_body=extra_body,
            )
            (sample_dir / "raw_response.txt").write_text(response_text, encoding="utf-8")
            saved = save_candidate_files(response_text, targets, sample_dir)
            meta = {
                **base_meta,
                "status": "generated" if saved else "no_code_extracted",
                "saved_files": [rel(Path(path)) for path in saved],
                "raw_response_length": len(response_text),
                "api_attempts_used": attempt,
                **usage,
            }
            write_json(meta_path, meta)
            return meta
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {str(exc)[:800]}"
            if attempt < args.api_attempts:
                delay_s = args.quota_retry_sleep_s if is_quota_or_rate_error(exc) else min(60, 5 * attempt)
                if delay_s > 0:
                    time.sleep(delay_s)
                continue

    meta = {**base_meta, "status": "api_error", "error": last_error, "saved_files": []}
    write_json(meta_path, meta)
    return meta


def run_generation(rows: list[dict[str, Any]], args: argparse.Namespace, output_root: Path) -> list[dict[str, Any]]:
    api_key = "" if args.dry_run else load_api_key(args.api_key_file, args.api_format)
    workers = max(1, min(args.gen_workers, len(rows) or 1))
    results: list[dict[str, Any]] = []
    if workers == 1:
        for index, row in enumerate(rows, start=1):
            print(f"[v3-generate] {index}/{len(rows)} {row['release_entry_id']} ...", flush=True)
            result = generate_one(row=row, api_key=api_key, args=args, output_root=output_root)
            print(f"[v3-generate] {row['release_entry_id']} {result.get('status')}", flush=True)
            results.append(result)
        return results
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(generate_one, row=row, api_key=api_key, args=args, output_root=output_root): row for row in rows}
        for future in as_completed(futures):
            row = futures[future]
            result = future.result()
            print(f"[v3-generate] {row['release_entry_id']} {result.get('status')}", flush=True)
            results.append(result)
    return results


def choose_hidden_tb(directory: Path) -> Path | None:
    direct = directory / "test_hidden" / "hidden.scs"
    if direct.exists():
        return direct
    candidates = sorted((directory / "test_hidden" / "tests").glob("*.scs"))
    return candidates[0] if len(candidates) == 1 else None


def fail_score(row: dict[str, Any], reason: str, output_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    result = {
        "benchmark": "benchmark-vabench-release-v3",
        "model": model_slug(args.model),
        "task_slug": row.get("release_entry_id"),
        "task_id": row.get("task_id"),
        "form": row.get("form"),
        "level": row.get("level"),
        "difficulty": row.get("difficulty"),
        "category": row.get("category"),
        "status": "FAIL_INFRA",
        "scores": {
            "dut_compile": 0.0,
            "tb_compile": 0.0,
            "sim_correct": 0.0,
            "weighted_total": 0.0,
        },
        "sample_idx": args.sample_idx,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "evas_notes": [reason],
        "claim_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    path = output_root / str(row.get("release_entry_id")) / "result.json"
    write_json(path, result)
    return result


def score_one(row: dict[str, Any], args: argparse.Namespace, output_root: Path) -> dict[str, Any]:
    slug = str(row["release_entry_id"])
    directory = task_dir(slug)
    model_key = model_slug(args.model)
    sample_dir = args.generated_root or output_root.parent / "generated"
    sample_path = sample_dir / model_key / slug / f"sample_{args.sample_idx}"
    result_path = output_root / slug / "result.json"
    if args.resume and result_path.exists():
        return read_json(result_path)
    if not sample_path.exists():
        return fail_score(row, "missing_generated_sample", output_root, args)
    targets = list(row.get("target_artifacts") or [])
    if not targets:
        return fail_score(row, "missing_target_artifacts", output_root, args)
    missing = [name for name in targets if not (sample_path / name).exists()]
    if missing:
        return fail_score(row, f"missing_generated_target_artifacts={','.join(missing)}", output_root, args)
    tb_path = choose_hidden_tb(directory)
    if tb_path is None:
        return fail_score(row, "missing_hidden_testbench", output_root, args)
    primary = sample_path / targets[0]
    try:
        raw = run_case(
            directory,
            primary,
            tb_path,
            output_root=output_root / slug / "evas_output",
            timeout_s=args.score_timeout_s,
            task_id_override=str(row.get("task_id") or slug),
        )
    except Exception as exc:
        return fail_score(row, f"{type(exc).__name__}: {str(exc)[:500]}", output_root, args)
    result = {
        "benchmark": "benchmark-vabench-release-v3",
        "model": model_key,
        "task_slug": slug,
        "task_id": row.get("task_id"),
        "form": row.get("form"),
        "level": row.get("level"),
        "difficulty": row.get("difficulty"),
        "category": row.get("category"),
        "selection_surface": args.selection_surface,
        "candidate_score_denominator": row.get("candidate_score_denominator"),
        "counted_in_score": row.get("counted_in_score"),
        "sample_idx": args.sample_idx,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "status": raw.get("status", "FAIL_UNKNOWN"),
        "checker_task_id": raw.get("checker_task_id"),
        "scores": raw.get("scores", {}),
        "evas_notes": raw.get("notes", []),
        "evas_timing": raw.get("timing", {}),
        "claim_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(result_path, result)
    return result


def run_scoring(rows: list[dict[str, Any]], args: argparse.Namespace, output_root: Path) -> list[dict[str, Any]]:
    workers = max(1, min(args.score_workers, len(rows) or 1))
    results: list[dict[str, Any]] = []
    if workers == 1:
        for index, row in enumerate(rows, start=1):
            print(f"[v3-score] {index}/{len(rows)} {row['release_entry_id']} ...", flush=True)
            result = score_one(row, args, output_root)
            print(f"[v3-score] {row['release_entry_id']} {result.get('status')}", flush=True)
            results.append(result)
        return results
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(score_one, row, args, output_root): row for row in rows}
        for future in as_completed(futures):
            row = futures[future]
            result = future.result()
            print(f"[v3-score] {row['release_entry_id']} {result.get('status')}", flush=True)
            results.append(result)
    return results


def pass_count(results: list[dict[str, Any]]) -> int:
    return sum(1 for item in results if item.get("status") == "PASS")


def status_counts(items: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(str(item.get("status") or "missing") for item in items).items()))


def write_summary(
    *,
    rows: list[dict[str, Any]],
    generation: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    output_root: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    summary = {
        "date": datetime.now(timezone.utc).isoformat(),
        "benchmark": "benchmark-vabench-release-v3",
        "model": args.model,
        "model_slug": model_slug(args.model),
        "runner_wrapper_version": RELEASE_RUNNER_WRAPPER_VERSION,
        "stage": args.stage,
        "selection_surface": args.selection_surface,
        "dry_run": args.dry_run,
        "status": "completed",
        "claim_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "score_roster": rel(resolve_repo_path(args.score_roster)),
        "selected_rows": len(rows),
        "selected_by_level": count_by(rows, "level"),
        "selected_by_track": count_by(rows, "track"),
        "selected_by_category": count_by(rows, "category"),
        "generation_status_counts": status_counts(generation),
        "scored_rows": len(scores),
        "evas_pass_count": pass_count(scores),
        "evas_pass_rate": round(pass_count(scores) / len(scores), 4) if scores else 0.0,
        "score_status_counts": status_counts(scores),
        "spectre_final_judge": {
            "status": "pending",
            "reason": "v3 model eval uses EVAS hidden behavior gate; run targeted Spectre before paper-facing model claims.",
        },
        "paths": {
            "output_root": rel(output_root),
            "generated_root": rel(output_root / "generated"),
            "evas_results_root": rel(output_root / "evas_results"),
            "summary": rel(output_root / "summary.json"),
        },
    }
    write_json(output_root / "summary.json", summary)
    return summary


def list_rows(args: argparse.Namespace) -> int:
    rows = selected_rows(args)
    payload = {
        "date": datetime.now(timezone.utc).isoformat(),
        "benchmark": "benchmark-vabench-release-v3",
        "score_roster": rel(resolve_repo_path(args.score_roster)),
        "selection_surface": args.selection_surface,
        "selected_rows": len(rows),
        "selected_by_level": count_by(rows, "level"),
        "selected_by_track": count_by(rows, "track"),
        "selected_by_category": count_by(rows, "category"),
        "claim_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "rows": rows,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"score_roster={payload['score_roster']}")
        print(f"selection_surface={payload['selection_surface']}")
        print(f"selected_rows={payload['selected_rows']}")
        print(f"by_level={payload['selected_by_level']}")
        print(f"by_track={payload['selected_by_track']}")
        print(f"by_category={payload['selected_by_category']}")
        for row in rows[: min(len(rows), 20)]:
            print(
                f"- {row['release_entry_id']} task_id={row.get('task_id')} "
                f"level={row.get('level')} category={row.get('category')} "
                f"targets={','.join(row.get('target_artifacts') or [])}"
            )
        if len(rows) > 20:
            print(f"... {len(rows) - 20} more rows")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="List selected v3 rows and exit.")
    ap.add_argument("--json", action="store_true", help="Print JSON for --list or final summary.")
    ap.add_argument("--score-roster", default=str(DEFAULT_SCORE_ROSTER))
    ap.add_argument(
        "--selection-surface",
        choices=["candidate", "all", "counted"],
        default="candidate",
        help="candidate uses candidate_score_denominator=true; counted uses counted_in_score=true.",
    )
    ap.add_argument("--exclude-spectre-divergent", action="store_true")
    ap.add_argument("--stage", choices=["generate", "score", "all"], default="all")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--api-format", choices=["openai", "anthropic"], default="openai")
    ap.add_argument("--api-key-file", default="")
    ap.add_argument("--output-root", default="")
    ap.add_argument("--tag", default="")
    ap.add_argument("--generated-root", type=Path, default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--task", action="append", default=[], help="Task slug, numeric id such as 001, or v3 task_id.")
    ap.add_argument("--task-file", action="append", default=[])
    ap.add_argument("--level", action="append", default=[])
    ap.add_argument("--track", action="append", default=[])
    ap.add_argument("--difficulty", action="append", default=[])
    ap.add_argument("--category", action="append", default=[])
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
    ap.add_argument("--token-param", choices=["auto", "max_tokens", "max_completion_tokens"], default="auto")
    ap.add_argument("--auth-header", choices=["auto", "authorization", "api-key", "both"], default="auto")
    ap.add_argument("--extra-body-json", default="")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.list:
        return list_rows(args)

    rows = selected_rows(args)
    if not rows:
        print("No v3 rows selected.", file=sys.stderr)
        return 1
    output_root = resolve_repo_path(args.output_root) if args.output_root else output_root_for(args.model, args.tag)
    generation: list[dict[str, Any]] = []
    scores: list[dict[str, Any]] = []
    if args.stage in {"generate", "all"}:
        generation = run_generation(rows, args, output_root)
    if args.stage in {"score", "all"} and not args.dry_run:
        scores = run_scoring(rows, args, output_root / "evas_results")
    summary = write_summary(rows=rows, generation=generation, scores=scores, output_root=output_root, args=args)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(
            f"[vabench-v3-model-eval] status={summary['status']} "
            f"rows={summary['selected_rows']} scored={summary['scored_rows']} "
            f"summary={summary['paths']['summary']}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
