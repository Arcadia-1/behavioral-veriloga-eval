#!/usr/bin/env python3
"""Run v3 pure-Rust skeleton waveform and Spectre parity on selected gold rows."""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import statistics
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

import simulate_evas  # noqa: E402
from run_gold_dual_suite import (  # noqa: E402
    compare_waveforms,
    default_bridge_repo,
    normalize_spectre_backend,
    normalize_spectre_mode,
    run_spectre_case,
)
from run_v3_spectre_audit import (  # noqa: E402
    choose_case_testbench,
    effective_task_form,
    load_v3_checks_config,
    read_task_toml,
    resolve_checker_id,
    resolve_include_paths,
)


DEFAULT_TASKS = [
    "149-offset-gain-amplifier",
    "279-safe-analog-divider",
    "306-case-mode-gain-selector",
    "316-final-step-edge-counter-file",
    "320-file-io-sampled-metric-writer",
    "379-file-fgets-config-loader",
    "385-table-model-linear-gain",
    "397-hierarchy-gain-child",
    "404-vector-part-select-window",
    "413-while-loop-array-sum",
    "435-ddt-voltage-derivative-source",
    "437-laplace-nd-lowpass-filter",
    "441-zi-nd-discrete-filter",
    "461-vt-thermal-voltage-source",
    "466-temperature-environment-metric",
    "469-current-contribution-conductance",
    "493-continuous-laplace-nd-filter",
    "494-continuous-zi-nd-filter",
    "505-fractional-n-divider-accumulator-flow",
]

DEFAULT_SPECTRE_REUSE_ROOTS = [
    ROOT / "results/v3_spectre_audit_reviewed_hidden",
    ROOT / "results/v3_spectre_audit",
]

DEFAULT_VISIBLE_EVAS_REUSE_ROOTS = [
    Path("/private/tmp/evas_rust_visible_probe_all_with_assets"),
    Path("/private/tmp/evas_rust_visible_probe_all"),
]


def task_number(task_dir: Path) -> int | None:
    try:
        return int(task_dir.name[:3])
    except ValueError:
        return None


def read_task_artifact_targets(task_dir: Path) -> list[str]:
    return simulate_evas.read_task_artifact_targets(task_dir)


def read_task_index_id(task_dir: Path) -> str | None:
    return simulate_evas.read_task_index_id(task_dir)


def resolve_task_case(task_dir: Path, split: str, force_harness_tb: bool) -> dict[str, Any]:
    meta = read_task_toml(task_dir)
    form = effective_task_form(task_dir, meta)
    targets = read_task_artifact_targets(task_dir)
    candidate_root = task_dir / "solution"
    checks_config = load_v3_checks_config(task_dir)
    checker_id = resolve_checker_id(task_dir, meta, checks_config)
    tb_path = choose_case_testbench(
        task_dir=task_dir,
        candidate_root=candidate_root,
        targets=targets,
        form=form,
        split=split,
        force_harness_tb=force_harness_tb,
    )
    include_paths: list[Path] = []
    missing_includes: list[str] = []
    if tb_path is not None:
        include_paths, missing_includes = resolve_include_paths(task_dir, candidate_root, tb_path)
    dut = candidate_root / targets[0] if targets else None
    if dut is not None and not dut.exists():
        va_candidates = sorted(candidate_root.glob("*.va"))
        dut = va_candidates[0] if len(va_candidates) == 1 else dut
    return {
        "task": task_dir.name,
        "task_id": read_task_index_id(task_dir) or str(meta.get("id") or task_dir.name),
        "checker_id": checker_id,
        "checks_config": checks_config,
        "targets": targets,
        "candidate_root": candidate_root,
        "dut": dut,
        "tb": tb_path,
        "include_paths": include_paths,
        "missing_includes": missing_includes,
    }


def eligible_tasks(root: Path) -> list[Path]:
    tasks = []
    for task_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        if task_number(task_dir) is None:
            continue
        try:
            case = resolve_task_case(task_dir, "hidden", False)
        except Exception:
            continue
        dut = case.get("dut")
        tb = case.get("tb")
        if isinstance(dut, Path) and dut.exists() and isinstance(tb, Path) and tb.exists():
            tasks.append(task_dir)
    return tasks


def select_tasks(root: Path, args: argparse.Namespace) -> list[Path]:
    all_tasks = {path.name: path for path in sorted(root.iterdir()) if path.is_dir()}
    if args.task:
        selected = []
        for name in args.task:
            if name not in all_tasks:
                raise SystemExit(f"unknown task: {name}")
            selected.append(all_tasks[name])
        return selected
    if args.random_count:
        pool = eligible_tasks(root)
        if args.random_count > len(pool):
            raise SystemExit(f"requested {args.random_count} tasks but only {len(pool)} eligible tasks exist")
        return sorted(random.Random(args.seed).sample(pool, args.random_count), key=lambda path: task_number(path) or 0)
    return [all_tasks[name] for name in DEFAULT_TASKS if name in all_tasks]


def set_engine_env(label: str, main_repo: Path, skeleton_repo: Path) -> None:
    if label == "python_rust":
        os.environ["VAEVAS_EVAS_REPO"] = str(main_repo)
        os.environ["VAEVAS_DEFAULT_EVAS_ENGINE"] = "evas2"
        os.environ["EVAS_ENGINE"] = "evas2"
    elif label == "pure_rust_skeleton":
        os.environ["VAEVAS_EVAS_REPO"] = str(skeleton_repo)
        os.environ["VAEVAS_DEFAULT_EVAS_ENGINE"] = "evas2"
        os.environ["EVAS_ENGINE"] = "evas2"
    else:
        raise ValueError(label)


def copy_artifact_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if src.resolve() == dst.resolve():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        elif item.is_file():
            shutil.copy2(item, target)


def lane_cache_dir(cache_root: Path, split: str, task_name: str, label: str) -> Path:
    return cache_root / split / task_name / label


def score_cached_evas_lane(label: str, case: dict[str, Any], out_dir: Path, timeout_s: int, source: Path) -> dict[str, Any]:
    csv_path = out_dir / "tran.csv"
    score = 0.0
    notes: list[str] = []
    if csv_path.exists():
        score, notes = simulate_evas.evaluate_behavior_with_timeout(
            case["checker_id"],
            csv_path,
            timeout_s=timeout_s,
            checks_config=case["checks_config"],
        )
        side = simulate_evas.validate_behavior_side_outputs(case["checker_id"], out_dir, csv_path)
        if side is not None:
            side_ok, side_note = side
            notes.append(side_note)
            if not side_ok:
                score = 0.0
    else:
        notes.append("cached tran.csv missing")
    return {
        "label": label,
        "status": "PASS" if score == 1.0 else "FAIL",
        "checker_id": case["checker_id"],
        "engine": "cached",
        "csv_path": str(csv_path),
        "csv_exists": csv_path.exists(),
        "wall_s": 0.0,
        "sim_wall_s": 0.0,
        "checker_wall_s": 0.0,
        "scores": {case["checker_id"]: score},
        "notes": notes,
        "cache_hit": True,
        "cache_source": str(source),
    }


def find_evas_cache_source(
    *,
    label: str,
    task_dir: Path,
    split: str,
    cache_root: Path,
    reuse_roots: list[Path],
) -> Path | None:
    own = lane_cache_dir(cache_root, split, task_dir.name, label)
    if (own / "tran.csv").exists():
        return own
    if label != "pure_rust_skeleton":
        return None
    for root in reuse_roots:
        candidate = root / task_dir.name
        if (candidate / "tran.csv").exists():
            return candidate
    return None


def run_or_reuse_evas_lane(
    *,
    label: str,
    case: dict[str, Any],
    task_dir: Path,
    out_dir: Path,
    timeout_s: int,
    main_repo: Path,
    skeleton_repo: Path,
    cache_root: Path,
    split: str,
    reuse_roots: list[Path],
    no_reuse_cache: bool,
) -> dict[str, Any]:
    cache_dst = lane_cache_dir(cache_root, split, task_dir.name, label)
    if not no_reuse_cache:
        cache_source = find_evas_cache_source(
            label=label,
            task_dir=task_dir,
            split=split,
            cache_root=cache_root,
            reuse_roots=reuse_roots,
        )
        if cache_source is not None:
            copy_artifact_dir(cache_source, out_dir)
            copy_artifact_dir(cache_source, cache_dst)
            return score_cached_evas_lane(label, case, out_dir, timeout_s, cache_source)
    result = run_evas_lane(
        label=label,
        case=case,
        task_dir=task_dir,
        out_dir=out_dir,
        timeout_s=timeout_s,
        main_repo=main_repo,
        skeleton_repo=skeleton_repo,
    )
    result["cache_hit"] = False
    copy_artifact_dir(out_dir, cache_dst)
    result["cache_dest"] = str(cache_dst)
    return result


def run_evas_lane(
    *,
    label: str,
    case: dict[str, Any],
    task_dir: Path,
    out_dir: Path,
    timeout_s: int,
    main_repo: Path,
    skeleton_repo: Path,
) -> dict[str, Any]:
    set_engine_env(label, main_repo, skeleton_repo)
    simulate_evas._close_persistent_evas_worker()
    started = time.perf_counter()
    result = simulate_evas.run_case(
        task_dir,
        case["dut"],
        case["tb"],
        output_root=out_dir,
        keep_run_dir=True,
        timeout_s=timeout_s,
        task_id_override=case["task_id"],
        checker_task_id_override=case["checker_id"],
    )
    wall_s = time.perf_counter() - started
    simulate_evas._close_persistent_evas_worker()
    csv_path = out_dir / "tran.csv"
    return {
        "label": label,
        "status": result.get("status"),
        "checker_id": result.get("checker_task_id"),
        "engine": result.get("evas_engine_used"),
        "csv_path": str(csv_path),
        "csv_exists": csv_path.exists(),
        "wall_s": wall_s,
        "sim_wall_s": (result.get("timing_split") or {}).get("evas_subprocess_wall_s"),
        "checker_wall_s": (result.get("timing_split") or {}).get("behavior_checker_s"),
        "scores": result.get("scores") or {},
        "notes": result.get("notes") or [],
    }


def run_spectre_lane(
    *,
    case: dict[str, Any],
    out_dir: Path,
    args: argparse.Namespace,
    spectre_backend: str,
    spectre_mode: str,
) -> dict[str, Any]:
    started = time.perf_counter()
    result = run_spectre_case(
        task_id=case["task"],
        tb_path=case["tb"],
        include_paths=case["include_paths"],
        output_dir=out_dir,
        bridge_repo=Path(args.bridge_repo).resolve() if args.bridge_repo else default_bridge_repo(),
        cadence_cshrc=args.cadence_cshrc,
        timeout_s=args.spectre_timeout_s,
        side_output_files=simulate_evas.behavior_side_output_names(case["checker_id"]),
        spectre_backend=spectre_backend,
        sui_host=args.sui_host,
        sui_work_root=args.sui_work_root,
        spectre_mode=spectre_mode,
    )
    wall_s = time.perf_counter() - started
    csv_path = Path(str(result.get("csv_path") or out_dir / "tran_spectre.csv"))
    behavior_score = 0.0
    behavior_notes: list[str] = []
    if result.get("ok") and csv_path.exists():
        behavior_score, behavior_notes = simulate_evas.evaluate_behavior_with_timeout(
            case["checker_id"],
            csv_path,
            timeout_s=args.spectre_timeout_s,
            checks_config=case["checks_config"],
        )
        side = simulate_evas.validate_behavior_side_outputs(case["checker_id"], out_dir, csv_path)
        if side is not None:
            side_ok, side_note = side
            behavior_notes.append(side_note)
            if not side_ok:
                behavior_score = 0.0
    else:
        behavior_notes.append("spectre csv missing or run failed")
    return {
        "ok": bool(result.get("ok")),
        "status": result.get("status"),
        "backend": result.get("spectre_backend"),
        "mode": result.get("spectre_mode"),
        "csv_path": str(csv_path),
        "csv_exists": csv_path.exists(),
        "wall_s": wall_s,
        "behavior_score": behavior_score,
        "behavior_notes": behavior_notes,
        "errors": result.get("errors") or [],
        "warnings": result.get("warnings") or [],
        "remote_run_dir": result.get("remote_run_dir"),
    }


def find_spectre_cache_source(*, task_dir: Path, split: str, cache_root: Path, reuse_roots: list[Path]) -> Path | None:
    own = lane_cache_dir(cache_root, split, task_dir.name, "spectre")
    if (own / "tran_spectre.csv").exists():
        return own
    cache_name = f"{task_dir.name}__{split}__gold"
    for root in reuse_roots:
        candidate = root / cache_name
        if (candidate / "tran_spectre.csv").exists():
            return candidate
    return None


def score_cached_spectre_lane(case: dict[str, Any], out_dir: Path, timeout_s: int, source: Path) -> dict[str, Any]:
    csv_path = out_dir / "tran_spectre.csv"
    behavior_score = 0.0
    behavior_notes: list[str] = []
    if csv_path.exists():
        behavior_score, behavior_notes = simulate_evas.evaluate_behavior_with_timeout(
            case["checker_id"],
            csv_path,
            timeout_s=timeout_s,
            checks_config=case["checks_config"],
        )
        side = simulate_evas.validate_behavior_side_outputs(case["checker_id"], out_dir, csv_path)
        if side is not None:
            side_ok, side_note = side
            behavior_notes.append(side_note)
            if not side_ok:
                behavior_score = 0.0
    else:
        behavior_notes.append("cached tran_spectre.csv missing")
    return {
        "ok": csv_path.exists(),
        "status": "cached",
        "backend": "cached",
        "mode": "cached",
        "csv_path": str(csv_path),
        "csv_exists": csv_path.exists(),
        "wall_s": 0.0,
        "behavior_score": behavior_score,
        "behavior_notes": behavior_notes,
        "errors": [],
        "warnings": [],
        "remote_run_dir": None,
        "cache_hit": True,
        "cache_source": str(source),
    }


def run_or_reuse_spectre_lane(
    *,
    case: dict[str, Any],
    task_dir: Path,
    out_dir: Path,
    args: argparse.Namespace,
    spectre_backend: str,
    spectre_mode: str,
    cache_root: Path,
    reuse_roots: list[Path],
    no_reuse_cache: bool,
) -> dict[str, Any]:
    cache_dst = lane_cache_dir(cache_root, args.split, task_dir.name, "spectre")
    if not no_reuse_cache:
        cache_source = find_spectre_cache_source(
            task_dir=task_dir,
            split=args.split,
            cache_root=cache_root,
            reuse_roots=reuse_roots,
        )
        if cache_source is not None:
            copy_artifact_dir(cache_source, out_dir)
            copy_artifact_dir(cache_source, cache_dst)
            return score_cached_spectre_lane(case, out_dir, args.spectre_timeout_s, cache_source)
    if args.spectre_cache_only:
        return {
            "ok": False,
            "status": "blocked_no_cache",
            "backend": spectre_backend,
            "mode": spectre_mode,
            "csv_path": str(out_dir / "tran_spectre.csv"),
            "csv_exists": False,
            "wall_s": 0.0,
            "behavior_score": None,
            "behavior_notes": ["spectre cache missing; --spectre-cache-only prevented rerun"],
            "errors": [],
            "warnings": [],
            "remote_run_dir": None,
            "cache_hit": False,
        }
    result = run_spectre_lane(
        case=case,
        out_dir=out_dir,
        args=args,
        spectre_backend=spectre_backend,
        spectre_mode=spectre_mode,
    )
    result["cache_hit"] = False
    copy_artifact_dir(out_dir, cache_dst)
    result["cache_dest"] = str(cache_dst)
    return result


def parity_or_blocked(task_id: str, left_csv: str, right_csv: str, sample_n: int) -> dict[str, Any]:
    left = Path(left_csv)
    right = Path(right_csv)
    if not left.exists() or not right.exists():
        return {
            "status": "blocked",
            "reason": f"missing csv left={left.exists()} right={right.exists()}",
        }
    return compare_waveforms(task_id, left, right, sample_n=sample_n)


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    spectre_rows = [row for row in rows if row.get("spectre", {}).get("ok")]
    skel_pass = [row for row in rows if row.get("skeleton", {}).get("status") == "PASS"]
    rust_pass = [row for row in rows if row.get("python_rust", {}).get("status") == "PASS"]
    wave_pass = [row for row in rows if row.get("waveform_parity", {}).get("status") == "passed"]
    spectre_pass = [
        row
        for row in rows
        if row.get("spectre", {}).get("behavior_score") == 1.0
        and row.get("spectre_parity", {}).get("status") == "passed"
    ]
    walls = [float(row.get("wall_s", 0.0)) for row in rows]
    return {
        "rows": len(rows),
        "skeleton_checker_pass": len(skel_pass),
        "python_rust_checker_pass": len(rust_pass),
        "spectre_ok": len(spectre_rows),
        "waveform_parity_pass": len(wave_pass),
        "spectre_behavior_and_parity_pass": len(spectre_pass),
        "total_wall_s": sum(walls),
        "median_row_wall_s": statistics.median(walls) if walls else 0.0,
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# v3 Skeleton Dual Parity",
        "",
        f"- split: `{report['split']}`",
        f"- spectre_backend: `{report['spectre_backend']}`",
        f"- spectre_mode: `{report['spectre_mode']}`",
        f"- artifact_cache_root: `{report['artifact_cache_root']}`",
        f"- sample_n: `{report['sample_n']}`",
        "",
        "## Summary",
        "",
        "| metric | value |",
        "| --- | ---: |",
    ]
    for key, value in report["summary"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| task | skeleton checker | py+rust checker | EVAS waveform parity | Spectre behavior | Spectre parity | cache | wall s |",
            "| --- | --- | --- | --- | --- | --- | --- | ---: |",
        ]
    )
    for row in report["rows"]:
        lines.append(
            "| {task} | {skel} | {rust} | {wave} | {spbeh} | {sppar} | {cache} | {wall:.2f} |".format(
                task=row["task"],
                skel=row.get("skeleton", {}).get("status"),
                rust=row.get("python_rust", {}).get("status"),
                wave=row.get("waveform_parity", {}).get("status"),
                spbeh=row.get("spectre", {}).get("behavior_score"),
                sppar=row.get("spectre_parity", {}).get("status"),
                cache="/".join(
                    [
                        "S" if row.get("skeleton", {}).get("cache_hit") else "-",
                        "R" if row.get("python_rust", {}).get("cache_hit") else "-",
                        "P" if row.get("spectre", {}).get("cache_hit") else "-",
                    ]
                ),
                wall=float(row.get("wall_s", 0.0)),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="benchmark-vabench-release-v3/tasks")
    parser.add_argument("--task", action="append")
    parser.add_argument("--random-count", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260709)
    parser.add_argument("--split", choices=("hidden", "visible"), default="hidden")
    parser.add_argument("--force-harness-tb", action="store_true")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--main-evas-repo", type=Path, default=ROOT.parent / "EVAS")
    parser.add_argument("--skeleton-repo", type=Path, default=ROOT.parent / "_worktrees/evas-pure-rust-skeleton")
    parser.add_argument("--evas-timeout-s", type=int, default=120)
    parser.add_argument("--spectre-timeout-s", type=int, default=300)
    parser.add_argument("--sample-n", type=int, default=1200)
    parser.add_argument("--bridge-repo", default=None)
    parser.add_argument("--cadence-cshrc", default=None)
    parser.add_argument("--spectre-backend", default=os.environ.get("VAEVAS_SPECTRE_BACKEND", "labctl"))
    parser.add_argument("--spectre-mode", default="ax")
    parser.add_argument("--sui-host", "--labctl-host", dest="sui_host", default=None)
    parser.add_argument("--sui-work-root", "--labctl-work-root", dest="sui_work_root", default=None)
    parser.add_argument("--artifact-cache-root", type=Path, default=ROOT / "results/_local/v3_skeleton_dual_parity_cache")
    parser.add_argument("--reuse-evas-root", action="append", type=Path, default=[])
    parser.add_argument("--reuse-spectre-root", action="append", type=Path, default=[])
    parser.add_argument("--no-default-reuse-roots", action="store_true")
    parser.add_argument("--no-reuse-cache", action="store_true")
    parser.add_argument("--spectre-cache-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    spectre_backend = normalize_spectre_backend(args.spectre_backend)
    spectre_mode = normalize_spectre_mode(args.spectre_mode)
    cache_root = args.artifact_cache_root
    cache_root.mkdir(parents=True, exist_ok=True)
    reuse_evas_roots = list(args.reuse_evas_root)
    reuse_spectre_roots = list(args.reuse_spectre_root)
    if not args.no_default_reuse_roots:
        reuse_spectre_roots.extend(root for root in DEFAULT_SPECTRE_REUSE_ROOTS if root.exists())
        if args.split == "visible":
            reuse_evas_roots.extend(root for root in DEFAULT_VISIBLE_EVAS_REUSE_ROOTS if root.exists())
    rows: list[dict[str, Any]] = []
    tasks = select_tasks(root, args)

    for index, task_dir in enumerate(tasks, start=1):
        row_start = time.perf_counter()
        case = resolve_task_case(task_dir, args.split, args.force_harness_tb)
        row: dict[str, Any] = {
            "task": task_dir.name,
            "task_id": case["task_id"],
            "checker_id": case["checker_id"],
            "notes": [],
        }
        if not isinstance(case.get("dut"), Path) or not case["dut"].exists() or not isinstance(case.get("tb"), Path) or not case["tb"].exists():
            row["status"] = "FAIL_NO_CASE"
            row["notes"].append("missing DUT or TB")
            rows.append(row)
            continue
        if case["missing_includes"]:
            row["status"] = "FAIL_MISSING_INCLUDE"
            row["notes"].extend(case["missing_includes"])
            rows.append(row)
            continue

        case_out = out_dir / task_dir.name
        skeleton = run_or_reuse_evas_lane(
            label="pure_rust_skeleton",
            case=case,
            task_dir=task_dir,
            out_dir=case_out / "skeleton",
            timeout_s=args.evas_timeout_s,
            main_repo=args.main_evas_repo,
            skeleton_repo=args.skeleton_repo,
            cache_root=cache_root,
            split=args.split,
            reuse_roots=reuse_evas_roots,
            no_reuse_cache=args.no_reuse_cache,
        )
        python_rust = run_or_reuse_evas_lane(
            label="python_rust",
            case=case,
            task_dir=task_dir,
            out_dir=case_out / "python_rust",
            timeout_s=args.evas_timeout_s,
            main_repo=args.main_evas_repo,
            skeleton_repo=args.skeleton_repo,
            cache_root=cache_root,
            split=args.split,
            reuse_roots=[],
            no_reuse_cache=args.no_reuse_cache,
        )
        waveform_parity = parity_or_blocked(
            case["checker_id"],
            skeleton["csv_path"],
            python_rust["csv_path"],
            args.sample_n,
        )
        spectre = run_or_reuse_spectre_lane(
            case=case,
            task_dir=task_dir,
            out_dir=case_out / "spectre",
            args=args,
            spectre_backend=spectre_backend,
            spectre_mode=spectre_mode,
            cache_root=cache_root,
            reuse_roots=reuse_spectre_roots,
            no_reuse_cache=args.no_reuse_cache,
        )
        spectre_parity = parity_or_blocked(
            case["checker_id"],
            skeleton["csv_path"],
            spectre["csv_path"],
            args.sample_n,
        )
        row.update(
            {
                "skeleton": skeleton,
                "python_rust": python_rust,
                "waveform_parity": waveform_parity,
                "spectre": spectre,
                "spectre_parity": spectre_parity,
                "wall_s": time.perf_counter() - row_start,
            }
        )
        rows.append(row)
        print(
            "[{}/{}] {} skel={} py_rust={} wave={} spectre_beh={} spectre_parity={} {:.2f}s".format(
                index,
                len(tasks),
                task_dir.name,
                skeleton.get("status"),
                python_rust.get("status"),
                waveform_parity.get("status"),
                spectre.get("behavior_score"),
                spectre_parity.get("status"),
                row["wall_s"],
            ),
            flush=True,
        )

    report = {
        "root": str(root),
        "split": args.split,
        "spectre_backend": spectre_backend,
        "spectre_mode": spectre_mode,
        "artifact_cache_root": str(cache_root),
        "reuse_evas_roots": [str(path) for path in reuse_evas_roots],
        "reuse_spectre_roots": [str(path) for path in reuse_spectre_roots],
        "sample_n": args.sample_n,
        "tasks": [path.name for path in tasks],
        "summary": summarize(rows),
        "rows": rows,
    }
    json_path = out_dir / "v3_skeleton_dual_parity.json"
    md_path = out_dir / "v3_skeleton_dual_parity.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report, md_path)
    print(f"JSON {json_path}", flush=True)
    print(f"MARKDOWN {md_path}", flush=True)
    failures = [
        row
        for row in rows
        if row.get("skeleton", {}).get("status") != "PASS"
        or row.get("python_rust", {}).get("status") != "PASS"
        or row.get("waveform_parity", {}).get("status") != "passed"
        or row.get("spectre", {}).get("behavior_score") != 1.0
        or row.get("spectre_parity", {}).get("status") != "passed"
    ]
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
