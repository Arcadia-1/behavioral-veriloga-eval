#!/usr/bin/env python3
"""Run EVAS + Spectre dual judge on model-generated vaBench release candidates.

The prompt-only baseline runner first writes candidates and EVAS scores.  This
script re-stages those same candidates as temporary gold assets, then runs the
existing dual EVAS/Spectre judge so model capability and EVAS correctness can be
reported separately:

- Spectre final pass: Spectre compiles/runs and the public checker passes.
- EVAS/Spectre mismatch: especially EVAS PASS / Spectre FAIL, which is the
  conservative correctness invariant for EVAS-as-filter claims.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import time
from typing import Any

from run_gold_dual_suite import (
    REMOTE_SPECTRE_BACKENDS,
    default_bridge_repo,
    default_remote_cadence_cshrc,
    default_remote_host,
    default_remote_work_root,
    default_sui_cadence_cshrc,
    normalize_spectre_backend,
    run_dual_case,
)
from score import (
    all_save_signals,
    choose_gold_tb,
    find_tb_file,
    find_va_file_for_tb,
    read_meta,
    stage_candidate_case,
    _task_pass,
)
from run_vabench_release_minimax_baseline import (
    SCORE_DENOMINATOR,
    form_dir,
    model_slug,
    read_json,
    scored_form_rows,
    task_key,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
RESULTS_ROOT = ROOT / "results"


class CandidateStageSkip(RuntimeError):
    """Candidate cannot be staged into a complete DUT+TB pair for dual judge."""


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def output_root_for(model: str, tag: str | None) -> Path:
    stamp = tag or datetime.now().strftime("%Y%m%d-%H%M%S")
    return RESULTS_ROOT / f"vabench-release-v1-baseline-dual-{model_slug(model)}-{stamp}"


def load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_read_error": f"{type(exc).__name__}: {str(exc)[:300]}"}


def baseline_sample_dir(baseline_root: Path, model: str, task_id: str, sample_idx: int) -> Path:
    return baseline_root / "generated" / model_slug(model) / task_id / f"sample_{sample_idx}"


def baseline_evas_result_path(baseline_root: Path, task_id: str) -> Path:
    return baseline_root / "evas_results" / task_id / "result.json"


def has_candidate_files(sample_dir: Path) -> bool:
    return sample_dir.is_dir() and (any(sample_dir.glob("*.va")) or any(sample_dir.glob("*.scs")))


def generation_meta(sample_dir: Path) -> dict[str, Any]:
    return load_optional_json(sample_dir / "generation_meta.json")


def is_incomplete_generation(meta: dict[str, Any]) -> bool:
    return (
        meta.get("status") == "no_code_extracted"
        and str(meta.get("finish_reason", "")).lower() == "length"
    )


def copy_task_contract(task_dir: Path, staged_task_dir: Path) -> None:
    staged_task_dir.mkdir(parents=True, exist_ok=True)
    for name in ("meta.json", "checks.yaml", "release_task.json", "prompt.md"):
        src = task_dir / name
        if src.exists():
            shutil.copy2(src, staged_task_dir / name)


def stage_model_candidate(
    *,
    row: dict[str, Any],
    task_dir: Path,
    sample_dir: Path,
    staged_task_dir: Path,
) -> dict[str, Any]:
    if staged_task_dir.exists():
        shutil.rmtree(staged_task_dir)
    copy_task_contract(task_dir, staged_task_dir)
    staged_gold_dir = staged_task_dir / "gold"
    staged_gold_dir.mkdir(parents=True, exist_ok=True)

    meta = read_meta(task_dir)
    family = str(meta.get("family", "end-to-end"))
    required_axes: list[str] = list(meta.get("scoring", ["dut_compile", "tb_compile", "sim_correct"]))
    gold_dir = task_dir / "gold"
    generated_tb = find_tb_file(sample_dir)
    gold_tb = choose_gold_tb(gold_dir)
    generated_va = find_va_file_for_tb(sample_dir, gold_tb if family in ("spec-to-va", "bugfix") else generated_tb)
    contract_save_signals = all_save_signals(gold_tb) if gold_tb and gold_tb.exists() else None
    auxiliary_gold_vas: list[Path] = []

    if family in ("spec-to-va", "bugfix"):
        dut_path = generated_va
        tb_path = gold_tb
    elif family == "tb-generation":
        gold_vas = sorted(gold_dir.glob("*.va"))
        dut_path = gold_vas[0] if gold_vas else None
        tb_path = generated_tb
        auxiliary_gold_vas = gold_vas
    else:
        dut_path = generated_va
        tb_path = generated_tb

    missing = []
    if dut_path is None or not dut_path.exists():
        missing.append("dut.va")
    if tb_path is None or not tb_path.exists():
        missing.append("testbench.scs")
    if missing:
        raise CandidateStageSkip(f"missing_required_stage_files: {', '.join(missing)}")

    staged_dut, staged_tb, notes = stage_candidate_case(
        family=family,
        gold_dir=gold_dir,
        sample_dir=sample_dir,
        dut_path=dut_path,
        tb_path=tb_path,
        stage_dir=staged_gold_dir,
        auxiliary_gold_vas=auxiliary_gold_vas,
        save_policy="contract",
        required_axes=required_axes,
        contract_save_signals=contract_save_signals,
    )
    return {
        "staged_task_dir": rel(staged_task_dir),
        "staged_gold_dir": rel(staged_gold_dir),
        "staged_dut": rel(staged_dut),
        "staged_tb": rel(staged_tb),
        "stage_notes": notes,
        "family": family,
        "required_axes": required_axes,
        "release_entry_id": row.get("release_entry_id"),
        "form": row.get("form"),
        "category": row.get("category"),
        "difficulty": row.get("difficulty"),
    }


def spectre_checker_pass(raw_result: dict[str, Any]) -> bool:
    spectre = raw_result.get("spectre")
    if not isinstance(spectre, dict):
        return False
    if not spectre.get("ok"):
        return False
    try:
        behavior_score = float(spectre.get("behavior_score", 0.0))
    except (TypeError, ValueError):
        behavior_score = 0.0
    return behavior_score >= 1.0


def spectre_backend_inconclusive(raw_result: dict[str, Any]) -> bool:
    spectre = raw_result.get("spectre")
    if not isinstance(spectre, dict) or spectre.get("ok"):
        return False
    evidence = " | ".join(
        str(item)
        for item in [
            spectre.get("status", ""),
            *(spectre.get("errors") or []),
            *(spectre.get("notes") or []),
            spectre.get("stdout_tail", ""),
        ]
    )
    backend_markers = (
        "remote_workdir_create_failed",
        "remote_workdir_unresolved",
        "Connection timed out during banner exchange",
        "sui_direct_timeout_after_s",
        "connect to host",
        "Connection closed by UNKNOWN",
        "Failed to upload files",
        "spectre_result.json missing",
    )
    return any(marker in evidence for marker in backend_markers)


def classify_dual_result(raw_result: dict[str, Any]) -> dict[str, Any]:
    evas = raw_result.get("evas") if isinstance(raw_result, dict) else {}
    evas_status = evas.get("status") if isinstance(evas, dict) else "UNKNOWN"
    spectre_pass = spectre_checker_pass(raw_result)
    backend_inconclusive = spectre_backend_inconclusive(raw_result)
    status = str(raw_result.get("status", "UNKNOWN")) if isinstance(raw_result, dict) else "UNKNOWN"
    return {
        "evas_status": evas_status,
        "spectre_checker_pass": spectre_pass,
        "spectre_backend_inconclusive": backend_inconclusive,
        "dual_status": status,
        "evas_pass_spectre_fail": evas_status == "PASS" and not spectre_pass and not backend_inconclusive,
        "spectre_pass_evas_fail": spectre_pass and evas_status != "PASS",
        "dual_pass": status == "PASS",
    }


def run_one(
    *,
    index: int,
    row: dict[str, Any],
    baseline_root: Path,
    model: str,
    sample_idx: int,
    output_root: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    spectre_backend: str,
    sui_host: str | None,
    sui_work_root: str | None,
    selection: str,
    resume: bool,
) -> tuple[int, dict[str, Any]]:
    task_dir = form_dir(row)
    key = task_key(row, task_dir)
    result_path = output_root / "results" / key / "result.json"
    if resume and result_path.exists():
        return index, read_json(result_path)

    sample_dir = baseline_sample_dir(baseline_root, model, key, sample_idx)
    gen_meta = generation_meta(sample_dir)
    baseline_evas = load_optional_json(baseline_evas_result_path(baseline_root, key))
    baseline_evas_pass = _task_pass(baseline_evas) if baseline_evas else False

    base = {
        "task_id": key,
        "release_task_id": row.get("task_id"),
        "release_entry_id": row.get("release_entry_id"),
        "form": row.get("form"),
        "category": row.get("category"),
        "difficulty": row.get("difficulty"),
        "sample_idx": sample_idx,
        "sample_dir": rel(sample_dir),
        "baseline_evas_status": baseline_evas.get("status") if baseline_evas else "missing",
        "baseline_evas_pass": baseline_evas_pass,
        "generation_status": gen_meta.get("status", "missing"),
        "generation_finish_reason": gen_meta.get("finish_reason", ""),
        "selection": selection,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }

    skip_reason = ""
    if not has_candidate_files(sample_dir):
        skip_reason = "missing_candidate_files"
    elif selection == "evas-pass" and not baseline_evas_pass:
        skip_reason = "not_evas_pass"
    elif selection == "evas-fail" and baseline_evas_pass:
        skip_reason = "not_evas_fail"

    if skip_reason:
        status = "INCOMPLETE" if skip_reason == "missing_candidate_files" and is_incomplete_generation(gen_meta) else "SKIPPED"
        result = {
            **base,
            "status": status,
            "skip_reason": skip_reason,
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        if status == "INCOMPLETE":
            result["incomplete_reason"] = "model_output_budget_exhausted"
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return index, result

    staged_task_dir = output_root / "staged_tasks" / key
    case_output_root = output_root / "dual_cases"
    started = time.perf_counter()
    try:
        stage_meta = stage_model_candidate(
            row=row,
            task_dir=task_dir,
            sample_dir=sample_dir,
            staged_task_dir=staged_task_dir,
        )
        raw_result = run_dual_case(
            task_dir=staged_task_dir,
            output_root=case_output_root,
            bridge_repo=bridge_repo,
            cadence_cshrc=cadence_cshrc,
            timeout_s=timeout_s,
            spectre_backend=spectre_backend,
            sui_host=sui_host,
            sui_work_root=sui_work_root,
        )
        classification = classify_dual_result(raw_result)
        result = {
            **base,
            "status": "DONE",
            "wall_time_s": time.perf_counter() - started,
            "stage": stage_meta,
            "dual_result": raw_result,
            "classification": classification,
            "baseline_evas_status_matches_dual_evas": baseline_evas.get("status") == classification["evas_status"],
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
    except CandidateStageSkip as exc:
        result = {
            **base,
            "status": "SKIPPED",
            "skip_reason": str(exc),
            "wall_time_s": time.perf_counter() - started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        result = {
            **base,
            "status": "ERROR",
            "wall_time_s": time.perf_counter() - started,
            "error": f"{type(exc).__name__}: {str(exc)[:800]}",
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }

    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return index, result


def summarize(results: list[dict[str, Any]], *, rows_total: int, output_root: Path, model: str, selection: str) -> dict[str, Any]:
    completed = [item for item in results if item.get("status") == "DONE"]
    skipped = [item for item in results if item.get("status") == "SKIPPED"]
    incomplete = [item for item in results if item.get("status") == "INCOMPLETE"]
    errors = [item for item in results if item.get("status") == "ERROR"]
    classifications = [item.get("classification", {}) for item in completed]
    status_counts: dict[str, int] = {}
    dual_status_counts: dict[str, int] = {}
    by_form: dict[str, dict[str, int]] = {}
    for item in results:
        status = str(item.get("status", "UNKNOWN"))
        status_counts[status] = status_counts.get(status, 0) + 1
        form = str(item.get("form", "unknown"))
        stats = by_form.setdefault(form, {"total": 0, "spectre_pass": 0, "dual_pass": 0})
        stats["total"] += 1
        cls = item.get("classification", {})
        if isinstance(cls, dict):
            if cls.get("spectre_checker_pass"):
                stats["spectre_pass"] += 1
            if cls.get("dual_pass"):
                stats["dual_pass"] += 1
            dual_status = str(cls.get("dual_status", "missing"))
            dual_status_counts[dual_status] = dual_status_counts.get(dual_status, 0) + 1

    summary = {
        "date": datetime.now(timezone.utc).isoformat(),
        "benchmark": "vabench-release-v1",
        "model": model,
        "model_slug": model_slug(model),
        "selection": selection,
        "score_denominator": rel(SCORE_DENOMINATOR),
        "selected_scored_forms": rows_total,
        "results_total": len(results),
        "completed_dual_count": len(completed),
        "skipped_count": len(skipped),
        "incomplete_count": len(incomplete),
        "error_count": len(errors),
        "status_counts": status_counts,
        "dual_status_counts": dual_status_counts,
        "spectre_final_pass_count": sum(1 for cls in classifications if cls.get("spectre_checker_pass")),
        "dual_pass_count": sum(1 for cls in classifications if cls.get("dual_pass")),
        "evas_pass_spectre_fail_count": sum(1 for cls in classifications if cls.get("evas_pass_spectre_fail")),
        "spectre_pass_evas_fail_count": sum(1 for cls in classifications if cls.get("spectre_pass_evas_fail")),
        "spectre_backend_inconclusive_count": sum(
            1 for cls in classifications if cls.get("spectre_backend_inconclusive")
        ),
        "baseline_evas_status_mismatch_count": sum(
            1 for item in completed if item.get("baseline_evas_status_matches_dual_evas") is False
        ),
        "by_form": by_form,
        "paths": {
            "output_root": rel(output_root),
            "summary_json": rel(output_root / "summary.json"),
            "summary_md": rel(output_root / "summary.md"),
            "results_root": rel(output_root / "results"),
            "dual_cases_root": rel(output_root / "dual_cases"),
        },
    }
    return summary


def write_summary_files(summary: dict[str, Any], output_root: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# vaBench Model EVAS/Spectre Dual Judge",
        "",
        f"Date: {summary['date']}",
        f"Model: `{summary['model']}`",
        f"Selection: `{summary['selection']}`",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| selected scored forms | {summary['selected_scored_forms']} |",
        f"| completed dual rows | {summary['completed_dual_count']} |",
        f"| skipped rows | {summary['skipped_count']} |",
        f"| error rows | {summary['error_count']} |",
        f"| Spectre final pass | {summary['spectre_final_pass_count']} |",
        f"| dual pass | {summary['dual_pass_count']} |",
        f"| EVAS PASS / Spectre FAIL | {summary['evas_pass_spectre_fail_count']} |",
        f"| Spectre PASS / EVAS FAIL | {summary['spectre_pass_evas_fail_count']} |",
        f"| Spectre backend inconclusive | {summary['spectre_backend_inconclusive_count']} |",
        f"| baseline EVAS status mismatch | {summary['baseline_evas_status_mismatch_count']} |",
        "",
        "## Dual Status Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status, count in sorted(summary["dual_status_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## By Form", "", "| Form | Total | Spectre Pass | Dual Pass |", "| --- | ---: | ---: | ---: |"])
    for form, stats in sorted(summary["by_form"].items()):
        lines.append(f"| `{form}` | {stats['total']} | {stats['spectre_pass']} | {stats['dual_pass']} |")
    (output_root / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_rows(
    *,
    rows: list[dict[str, Any]],
    baseline_root: Path,
    model: str,
    sample_idx: int,
    output_root: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    spectre_backend: str,
    sui_host: str | None,
    sui_work_root: str | None,
    selection: str,
    workers: int,
    resume: bool,
) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    results_by_index: dict[int, dict[str, Any]] = {}
    partial_path = output_root / "summary.partial.json"

    def ordered_results() -> list[dict[str, Any]]:
        return [results_by_index[idx] for idx in sorted(results_by_index)]

    def write_partial() -> None:
        summary = summarize(
            ordered_results(),
            rows_total=len(rows),
            output_root=output_root,
            model=model,
            selection=selection,
        )
        summary["status"] = "running"
        summary["updated_at"] = datetime.now(timezone.utc).isoformat()
        partial_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    effective_workers = max(1, min(workers, len(rows) or 1))
    if effective_workers == 1:
        for idx, row in enumerate(rows, start=1):
            completed_idx, result = run_one(
                index=idx,
                row=row,
                baseline_root=baseline_root,
                model=model,
                sample_idx=sample_idx,
                output_root=output_root,
                bridge_repo=bridge_repo,
                cadence_cshrc=cadence_cshrc,
                timeout_s=timeout_s,
                spectre_backend=spectre_backend,
                sui_host=sui_host,
                sui_work_root=sui_work_root,
                selection=selection,
                resume=resume,
            )
            results_by_index[completed_idx] = result
            print(f"[dual] {idx}/{len(rows)} {row.get('task_id')} {result.get('status')}", flush=True)
            write_partial()
    else:
        with ThreadPoolExecutor(max_workers=effective_workers) as executor:
            futures = [
                executor.submit(
                    run_one,
                    index=idx,
                    row=row,
                    baseline_root=baseline_root,
                    model=model,
                    sample_idx=sample_idx,
                    output_root=output_root,
                    bridge_repo=bridge_repo,
                    cadence_cshrc=cadence_cshrc,
                    timeout_s=timeout_s,
                    spectre_backend=spectre_backend,
                    sui_host=sui_host,
                    sui_work_root=sui_work_root,
                    selection=selection,
                    resume=resume,
                )
                for idx, row in enumerate(rows, start=1)
            ]
            for future in as_completed(futures):
                completed_idx, result = future.result()
                results_by_index[completed_idx] = result
                print(
                    f"[dual] {len(results_by_index)}/{len(rows)} "
                    f"{result.get('task_id')} {result.get('status')}",
                    flush=True,
                )
                write_partial()

    final = summarize(
        ordered_results(),
        rows_total=len(rows),
        output_root=output_root,
        model=model,
        selection=selection,
    )
    final["status"] = "complete" if final["error_count"] == 0 else "errors_present"
    final["finished_at"] = datetime.now(timezone.utc).isoformat()
    final["workers"] = effective_workers
    final["spectre_backend"] = spectre_backend
    final["remote_host"] = sui_host or ""
    final["remote_work_root"] = sui_work_root or ""
    final["sui_host"] = sui_host or ""
    final["sui_work_root"] = sui_work_root or ""
    final["cadence_cshrc"] = cadence_cshrc or ""
    write_summary_files(final, output_root)
    if partial_path.exists():
        partial_path.unlink()
    return final


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline-root", required=True, help="Prompt-only baseline output root.")
    ap.add_argument("--model", required=True)
    ap.add_argument("--output-root", default="")
    ap.add_argument("--tag", default="")
    ap.add_argument("--sample-idx", type=int, default=0)
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
    ap.add_argument("--selection", choices=["all-generated", "evas-pass", "evas-fail"], default="all-generated")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout-s", type=int, default=240)
    ap.add_argument("--spectre-license-wait-s", type=int, default=None)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument(
        "--bridge-repo",
        default=os.environ.get("VAEVAS_BRIDGE_REPO", str(default_bridge_repo())),
    )
    ap.add_argument(
        "--spectre-backend",
        default=os.environ.get("VAEVAS_SPECTRE_BACKEND", "labctl"),
        help="Spectre execution backend: labctl, sui-direct, or bridge.",
    )
    ap.add_argument("--sui-host", "--labctl-host", dest="sui_host", default=None)
    ap.add_argument("--sui-work-root", "--labctl-work-root", dest="sui_work_root", default=None)
    ap.add_argument("--cadence-cshrc", default="")
    args = ap.parse_args()

    if args.spectre_license_wait_s is not None:
        os.environ["VAEVAS_SPECTRE_LQTIMEOUT_S"] = str(args.spectre_license_wait_s)

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

    baseline_root = Path(args.baseline_root)
    if not baseline_root.is_absolute():
        baseline_root = ROOT / baseline_root
    output_root = Path(args.output_root) if args.output_root else output_root_for(args.model, args.tag or None)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    spectre_backend = normalize_spectre_backend(args.spectre_backend)
    remote_backend = spectre_backend in REMOTE_SPECTRE_BACKENDS
    remote_host = (args.sui_host or default_remote_host(spectre_backend)) if remote_backend else ""
    remote_work_root = (args.sui_work_root or default_remote_work_root(spectre_backend)) if remote_backend else ""
    effective_cshrc = args.cadence_cshrc or default_remote_cadence_cshrc(spectre_backend) or default_sui_cadence_cshrc()
    bridge_repo = Path(args.bridge_repo).resolve()

    print(
        f"[model-dual] model={args.model} forms={len(rows)} selection={args.selection} "
        f"backend={spectre_backend} workers={args.workers} output={rel(output_root)}",
        flush=True,
    )
    summary = run_rows(
        rows=rows,
        baseline_root=baseline_root,
        model=args.model,
        sample_idx=args.sample_idx,
        output_root=output_root,
        bridge_repo=bridge_repo,
        cadence_cshrc=effective_cshrc or None,
        timeout_s=args.timeout_s,
        spectre_backend=spectre_backend,
        sui_host=remote_host if remote_backend else None,
        sui_work_root=remote_work_root if remote_backend else None,
        selection=args.selection,
        workers=args.workers,
        resume=args.resume,
    )
    summary["remote_host"] = remote_host
    summary["remote_work_root"] = remote_work_root
    summary["cadence_cshrc"] = effective_cshrc
    print(
        f"[model-dual] done status={summary['status']} "
        f"spectre_pass={summary['spectre_final_pass_count']}/{summary['completed_dual_count']} "
        f"evas_pass_spectre_fail={summary['evas_pass_spectre_fail_count']} "
        f"summary={summary['paths']['summary_json']}",
        flush=True,
    )
    return 0 if summary["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
