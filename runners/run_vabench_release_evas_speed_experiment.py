#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import platform
import shutil
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from run_gold_dual_suite import compare_waveforms
from run_gold_suite import ahdl_includes, checker_task_id, choose_gold_tb, read_meta
from simulate_evas import run_case
from vabench_release_paths import release_form_dir


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
SPEED_OPT_ROOT = ROOT / "speed-optimization"
REPORTS_ROOT = SPEED_OPT_ROOT / "reports"
SPEED_ARTIFACT_JSON = REPORTS_ROOT / "speed_debug_artifact.json"
REPORT_JSON = REPORTS_ROOT / "evas_speed_experiment_p0_p3.json"
REPORT_MD = REPORTS_ROOT / "evas_speed_experiment_p0_p3.md"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / f"evas-speed-p0-p3-{date.today().isoformat().replace('-', '')}"
SCHEMA_VERSION = "evas-speed-p0p3-artifact.v1"
ARTIFACT_KIND = "candidate_evas_speed_experiment"
NO_CLAIM_REASON = "EVAS-only speed experiments are candidate evidence; paper-facing speed claims require same-slice EVAS/Spectre timing."


@dataclass(frozen=True)
class Mode:
    mode_id: str
    phase: str
    label: str
    simulator_options: tuple[str, ...] = ()
    default_off_fast_path: bool = False


MODES: dict[str, Mode] = {
    "strict_current": Mode(
        mode_id="strict_current",
        phase="P1",
        label="Current EVAS settings from the benchmark testbench",
    ),
    "profile_balanced": Mode(
        mode_id="profile_balanced",
        phase="P2",
        label="EVAS built-in balanced profile",
        simulator_options=("evas_profile=balanced",),
    ),
    "profile_fast": Mode(
        mode_id="profile_fast",
        phase="P2",
        label="EVAS built-in fast profile",
        simulator_options=("evas_profile=fast",),
    ),
    "skip_source_error_control": Mode(
        mode_id="skip_source_error_control",
        phase="P3",
        label="Default-off fast path: skip source nodes in dynamic voltage error-control",
        simulator_options=("evas_skip_source_error_control=yes",),
        default_off_fast_path=True,
    ),
    "profile_fast_skip_source_error_control": Mode(
        mode_id="profile_fast_skip_source_error_control",
        phase="P3",
        label="Fast profile plus default-off source-error-control ablation",
        simulator_options=("evas_profile=fast", "evas_skip_source_error_control=yes"),
        default_off_fast_path=True,
    ),
    "profile_fast_state_local": Mode(
        mode_id="profile_fast_state_local",
        phase="P4",
        label="Fast profile plus state-local generated evaluate fast path",
        simulator_options=(
            "evas_profile=fast",
            "evas_skip_source_error_control=yes",
            "evas_state_local_fastpath=yes",
        ),
        default_off_fast_path=True,
    ),
    "profile_fast_static_branch": Mode(
        mode_id="profile_fast_static_branch",
        phase="P4",
        label="Fast profile plus static branch read/write generated helpers",
        simulator_options=(
            "evas_profile=fast",
            "evas_skip_source_error_control=yes",
            "evas_static_branch_fastpath=yes",
        ),
        default_off_fast_path=True,
    ),
}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def float_or_none(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = round((len(ordered) - 1) * p)
    return ordered[int(idx)]


def geomean(values: list[float]) -> float | None:
    import math

    positives = [value for value in values if value > 0]
    if not positives:
        return None
    return math.exp(sum(math.log(value) for value in positives) / len(positives))


def task_dir_for(row: dict[str, object]) -> Path:
    return release_form_dir(PACKAGE_ROOT / "tasks", str(row["entry_id"]), str(row["form"]))


def load_speed_rows(path: Path) -> list[dict[str, object]]:
    artifact = read_json(path)
    rows = artifact.get("rows", [])
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def select_rows(
    rows: list[dict[str, object]],
    *,
    suite: str,
    entries: set[str] | None,
    forms: set[str] | None,
    limit: int | None,
) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        key = (str(row.get("entry_id", "")), str(row.get("form", "")), str(row.get("variant", "")))
        if key in seen:
            continue
        seen.add(key)
        if entries and key[0] not in entries:
            continue
        if forms and key[1] not in forms:
            continue
        if suite == "slow-outliers" and (float_or_none(row.get("wrapper_spectre_over_evas_speedup")) or 0.0) >= 1.0:
            continue
        if suite == "top-wall" and float_or_none(row.get("evas_wall_time_s")) is None:
            continue
        if not task_dir_for(row).exists():
            continue
        selected.append(row)
    selected.sort(
        key=lambda row: (
            -(float_or_none(row.get("evas_wall_time_s")) or 0.0),
            str(row.get("entry_id", "")),
            str(row.get("form", "")),
            str(row.get("variant", "")),
        )
    )
    if limit is not None:
        selected = selected[:limit]
    return selected


def inject_simulator_options(tb_text: str, options: tuple[str, ...]) -> str:
    if not options:
        return tb_text
    option_text = " ".join(options)
    lines = tb_text.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("simulatorOptions options"):
            missing = [opt for opt in options if opt.split("=", 1)[0] not in line]
            if missing:
                lines[idx] = line.rstrip() + " " + " ".join(missing)
            return "\n".join(lines) + ("\n" if tb_text.endswith("\n") else "")
    for idx, line in enumerate(lines):
        if line.strip().startswith("tran "):
            lines.insert(idx, f"simulatorOptions options {option_text}")
            return "\n".join(lines) + ("\n" if tb_text.endswith("\n") else "")
    lines.append(f"simulatorOptions options {option_text}")
    return "\n".join(lines) + "\n"


def stage_mode_task(task_dir: Path, mode: Mode, stage_root: Path) -> tuple[Path, Path, Path]:
    stage_task = stage_root / mode.mode_id
    if stage_task.exists():
        shutil.rmtree(stage_task)
    stage_gold = stage_task / "gold"
    stage_gold.mkdir(parents=True, exist_ok=True)
    shutil.copy2(task_dir / "meta.json", stage_task / "meta.json")
    checks_yaml = task_dir / "checks.yaml"
    if checks_yaml.exists():
        shutil.copy2(checks_yaml, stage_task / "checks.yaml")
    for item in sorted((task_dir / "gold").iterdir()):
        if item.is_file():
            shutil.copy2(item, stage_gold / item.name)
    tb_path = choose_gold_tb(stage_gold)
    if tb_path is None:
        raise FileNotFoundError(f"no gold testbench found in {task_dir}")
    if mode.simulator_options:
        tb_path.write_text(
            inject_simulator_options(tb_path.read_text(encoding="utf-8"), mode.simulator_options),
            encoding="utf-8",
        )
    includes = ahdl_includes(tb_path)
    if not includes:
        raise FileNotFoundError(f"no ahdl_include found in {tb_path}")
    primary_dut = stage_gold / includes[0]
    missing = [name for name in includes if not (stage_gold / name).exists()]
    if missing:
        raise FileNotFoundError(f"missing included files for {task_dir}: {', '.join(missing)}")
    return stage_task, primary_dut, tb_path


def parse_perf_counters(stdout_tail: str) -> dict[str, float]:
    counters: dict[str, float] = {}
    for line in stdout_tail.splitlines():
        text = line.strip()
        if " = " not in text:
            continue
        key, value = text.split(" = ", 1)
        if key.startswith("model["):
            continue
        if key in {
            "bound_step_clamps",
            "cross_event_steps",
            "cross_refine_triggers",
            "dynamic_step_grows",
            "dynamic_step_shrinks",
            "err_ratio_skipped_outputs",
            "err_ratio_skipped_sources",
            "min_step_clamps",
            "model_breakpoint_clamps",
            "output_step_clamps",
            "source_breakpoint_clamps",
            "steps_total",
        }:
            parsed = float_or_none(value)
            if parsed is not None:
                counters[key] = parsed
    return counters


def result_csv(raw: dict[str, object]) -> Path | None:
    artifacts = raw.get("artifacts", [])
    if not isinstance(artifacts, list) or len(artifacts) < 3:
        return None
    path = Path(str(artifacts[2]))
    return path if path.exists() else None


def run_one(
    row: dict[str, object],
    mode: Mode,
    *,
    output_root: Path,
    timeout_s: int,
) -> dict[str, object]:
    entry_id = str(row["entry_id"])
    form = str(row["form"])
    variant = str(row.get("variant", "gold"))
    task_dir = task_dir_for(row)
    stage_root = output_root / "_staged" / entry_id / form / variant
    stage_task, primary_dut, tb_path = stage_mode_task(task_dir, mode, stage_root)
    meta = read_meta(stage_task)
    task_id = str(meta.get("task_id") or meta.get("id") or stage_task.name)
    checker_id = checker_task_id(meta, task_id)
    result_root = output_root / "runs" / entry_id / form / variant / mode.mode_id
    result_root.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now().isoformat(timespec="seconds")
    t0 = time.perf_counter()
    raw = run_case(
        stage_task,
        primary_dut,
        tb_path,
        output_root=result_root / task_id,
        timeout_s=timeout_s,
        task_id_override=task_id,
        checker_task_id_override=checker_id,
    )
    if isinstance(raw, dict):
        raw.setdefault("backend_used", "evas")
    wall_time_s = time.perf_counter() - t0
    timing = raw.get("timing", {})
    if not isinstance(timing, dict):
        timing = {}
    return {
        "entry_id": entry_id,
        "form": form,
        "variant": variant,
        "mode_id": mode.mode_id,
        "phase": mode.phase,
        "default_off_fast_path": mode.default_off_fast_path,
        "task_id": task_id,
        "checker_task_id": checker_id,
        "status": raw.get("status", "UNKNOWN"),
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "execution": {
            "kind": "executed",
            "timeout_s": timeout_s,
            "run_dir_isolated": True,
            "counted_in_timing": True,
        },
        "input_hashes": {
            "meta_json": sha256_file(stage_task / "meta.json"),
            "gold_tb": sha256_file(tb_path),
            "primary_dut": sha256_file(primary_dut),
        },
        "evas_wall_time_s": wall_time_s,
        "evas_reported_total_elapsed_s": timing.get("total_elapsed_s"),
        "evas_reported_tran_elapsed_s": timing.get("tran_elapsed_s"),
        "evas_accepted_tran_steps": timing.get("accepted_tran_steps"),
        "perf_counters": parse_perf_counters(str(raw.get("stdout_tail", ""))),
        "source_speed_row": {
            "evas_wall_time_s": row.get("evas_wall_time_s"),
            "spectre_wall_time_s": row.get("spectre_wall_time_s"),
            "wrapper_spectre_over_evas_speedup": row.get("wrapper_spectre_over_evas_speedup"),
            "summary_source": row.get("summary_source"),
        },
        "staged_task_dir": rel(stage_task),
        "result_root": rel(result_root),
        "raw_result": raw,
    }


def attach_strict_comparisons(results: list[dict[str, object]]) -> None:
    strict_by_case: dict[tuple[str, str, str], dict[str, object]] = {}
    for result in results:
        key = (str(result["entry_id"]), str(result["form"]), str(result["variant"]))
        if result["mode_id"] == "strict_current":
            strict_by_case[key] = result
    for result in results:
        key = (str(result["entry_id"]), str(result["form"]), str(result["variant"]))
        strict = strict_by_case.get(key)
        if strict is None or result["mode_id"] == "strict_current":
            result["strict_comparison"] = {
                "status": "baseline" if result["mode_id"] == "strict_current" else "missing_strict",
            }
            result["safety"] = {
                "equivalence_status": "baseline" if result["mode_id"] == "strict_current" else "blocked",
                "requires_dual_rerun": bool(result.get("default_off_fast_path")),
                "parity_claim_eligible": False,
                "blockers": [] if result["mode_id"] == "strict_current" else ["missing strict_current baseline"],
            }
            continue
        strict_wall = float_or_none(strict.get("evas_wall_time_s"))
        mode_wall = float_or_none(result.get("evas_wall_time_s"))
        speedup = strict_wall / mode_wall if strict_wall and mode_wall and mode_wall > 0 else None
        strict_csv = result_csv(strict.get("raw_result", {}) if isinstance(strict.get("raw_result"), dict) else {})
        mode_csv = result_csv(result.get("raw_result", {}) if isinstance(result.get("raw_result"), dict) else {})
        parity = {"status": "blocked", "reason": "missing waveform csv"}
        if strict_csv is not None and mode_csv is not None:
            parity = compare_waveforms(str(result["checker_task_id"]), mode_csv, strict_csv)
        safe_vs_strict = (
            strict.get("status") == result.get("status") == "PASS"
            and parity.get("status") in {"passed", "not_required"}
        )
        result["strict_comparison"] = {
            "status": "checked",
            "strict_status": strict.get("status"),
            "mode_status": result.get("status"),
            "status_matches_strict": strict.get("status") == result.get("status"),
            "speedup_vs_strict": speedup,
            "waveform_parity_vs_strict": parity,
            "safe_vs_strict": safe_vs_strict,
        }
        blockers = []
        if strict.get("status") != result.get("status"):
            blockers.append("status differs from strict_current")
        if result.get("status") != "PASS":
            blockers.append("candidate did not pass the release behavior checker")
        if parity.get("status") not in {"passed", "not_required"}:
            blockers.append("waveform parity against strict_current failed or was blocked")
        result["safety"] = {
            "equivalence_status": "pass" if safe_vs_strict else "fail",
            "requires_dual_rerun": bool(result.get("default_off_fast_path")),
            "parity_claim_eligible": False,
            "blockers": blockers,
        }


def summarize(results: list[dict[str, object]]) -> dict[str, object]:
    by_mode: dict[str, list[dict[str, object]]] = defaultdict(list)
    for result in results:
        by_mode[str(result["mode_id"])].append(result)
    mode_summaries: dict[str, object] = {}
    for mode_id, rows in sorted(by_mode.items()):
        comparisons = [
            row.get("strict_comparison", {})
            for row in rows
            if isinstance(row.get("strict_comparison"), dict)
            and row.get("mode_id") != "strict_current"
        ]
        speedups = [
            float(value)
            for value in (
                comp.get("speedup_vs_strict") for comp in comparisons if isinstance(comp, dict)
            )
            if value is not None
        ]
        mode_summaries[mode_id] = {
            "run_count": len(rows),
            "pass_count": sum(1 for row in rows if row.get("status") == "PASS"),
            "nonpass_count": sum(1 for row in rows if row.get("status") != "PASS"),
            "status_counts": dict(sorted(Counter(str(row.get("status")) for row in rows).items())),
            "total_evas_wall_time_s": sum(float(row["evas_wall_time_s"]) for row in rows),
            "median_speedup_vs_strict": percentile(speedups, 0.5),
            "geomean_speedup_vs_strict": geomean(speedups),
            "safe_vs_strict_count": sum(
                1 for comp in comparisons if isinstance(comp, dict) and comp.get("safe_vs_strict")
            ),
            "unsafe_vs_strict_count": sum(
                1
                for comp in comparisons
                if isinstance(comp, dict)
                and comp.get("status") == "checked"
                and not comp.get("safe_vs_strict")
            ),
        }
    return mode_summaries


def summarize_phases(results: list[dict[str, object]]) -> dict[str, object]:
    by_phase: dict[str, list[dict[str, object]]] = defaultdict(list)
    for result in results:
        by_phase[str(result.get("phase", "unknown"))].append(result)
    return {
        phase: {
            "run_count": len(rows),
            "pass_count": sum(1 for row in rows if row.get("status") == "PASS"),
            "unsafe_vs_strict_count": sum(
                1
                for row in rows
                if isinstance(row.get("safety"), dict)
                and row["safety"].get("equivalence_status") == "fail"
            ),
            "total_evas_wall_time_s": sum(float(row["evas_wall_time_s"]) for row in rows),
        }
        for phase, rows in sorted(by_phase.items())
    }


def timing_totals(results: list[dict[str, object]]) -> dict[str, object]:
    strict_rows = [row for row in results if row.get("mode_id") == "strict_current"]
    candidate_rows = [row for row in results if row.get("mode_id") != "strict_current"]
    strict_total = sum(float(row["evas_wall_time_s"]) for row in strict_rows)
    candidate_total = sum(float(row["evas_wall_time_s"]) for row in candidate_rows)
    return {
        "strict_baseline_evas_wall_time_s": strict_total,
        "candidate_evas_wall_time_s": candidate_total,
        "candidate_over_strict_wall_ratio": candidate_total / strict_total if strict_total > 0 else None,
        "timed_rows": len(results),
        "excluded_cached_rows": 0,
        "excluded_dry_run_rows": 0,
        "excluded_early_stopped_rows": 0,
    }


def p0_existing_summary(speed_artifact_path: Path) -> dict[str, object]:
    artifact = read_json(speed_artifact_path)
    scope = artifact.get("measurement_scope", {})
    totals = artifact.get("timing_totals", {})
    distribution = artifact.get("timing_distribution", {})
    if not isinstance(scope, dict):
        scope = {}
    if not isinstance(totals, dict):
        totals = {}
    if not isinstance(distribution, dict):
        distribution = {}
    return {
        "status": artifact.get("status", "missing"),
        "claim_allowed": artifact.get("claim_allowed", False),
        "reason": artifact.get("reason", ""),
        "source": rel(speed_artifact_path),
        "hardware_caveat": "existing artifact compares local EVAS wrapper timing with remote Spectre wrapper timing",
        "timed_rows": scope.get("timed_rows"),
        "timed_scored_forms": scope.get("timed_scored_form_count"),
        "scored_forms": scope.get("scored_form_count"),
        "timing_totals": totals,
        "wrapper_ratio": distribution.get("wrapper_ratio", {}),
        "reported_total_ratio": distribution.get("reported_total_ratio", {}),
        "tran_ratio": distribution.get("tran_ratio", {}),
    }


def write_markdown(report: dict[str, object], path: Path) -> None:
    mode_summary = report["mode_summary"]
    lines = [
        "# EVAS Speed Experiment P0-P3",
        "",
        f"Date: {report['date']}",
        f"Claim allowed: `{report['claim_allowed']}`",
        f"Reason: {report['reason']}",
        "",
        "This artifact evaluates EVAS speed optimization candidates while keeping",
        "the current EVAS path as the strict baseline. Default-off fast paths are",
        "not claimable unless they pass strict-EVAS waveform parity and behavior checks.",
        "",
        "## P0 Existing Baseline",
        "",
        f"- Source: `{report['p0_existing_baseline']['source']}`",
        f"- Caveat: {report['p0_existing_baseline']['hardware_caveat']}",
        f"- Existing status: `{report['p0_existing_baseline']['status']}`",
        f"- Existing speed claim allowed: `{report['p0_existing_baseline']['claim_allowed']}`",
        "",
        "## Scope",
        "",
        f"- Selected rows: {report['selected_row_count']}",
        f"- Modes: `{', '.join(report['mode_ids'])}`",
        f"- Output root: `{report['output_root']}`",
        "",
        "## Mode Summary",
        "",
        "| Mode | Runs | PASS | Non-PASS | Wall s | Median speedup vs strict | Safe vs strict | Unsafe vs strict |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for mode_id, summary in mode_summary.items():
        lines.append(
            "| {mode} | {runs} | {passes} | {nonpass} | {wall:.3f} | {median} | {safe} | {unsafe} |".format(
                mode=mode_id,
                runs=summary["run_count"],
                passes=summary["pass_count"],
                nonpass=summary["nonpass_count"],
                wall=summary["total_evas_wall_time_s"],
                median=summary["median_speedup_vs_strict"],
                safe=summary["safe_vs_strict_count"],
                unsafe=summary["unsafe_vs_strict_count"],
            )
        )
    lines.extend(
        [
            "",
            "## Safety Policy",
            "",
            "- `strict_current` remains the certification baseline.",
            "- P2 profiles are parameter ablations, not default behavior.",
            "- P3 fast paths are default-off and must pass behavior and strict-EVAS waveform parity before promotion.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run EVAS-only speed P0-P3 experiments on vaBench release rows.")
    ap.add_argument("--speed-artifact", default=str(SPEED_ARTIFACT_JSON))
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    ap.add_argument("--report-json", default=str(REPORT_JSON))
    ap.add_argument("--report-md", default=str(REPORT_MD))
    ap.add_argument("--suite", choices=("slow-outliers", "all", "top-wall"), default="slow-outliers")
    ap.add_argument("--entry", action="append", default=[])
    ap.add_argument("--form", action="append", default=[])
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument(
        "--mode",
        action="append",
        choices=tuple(MODES),
        default=[],
        help="Mode to run. Defaults to strict_current, profile_fast, and profile_fast_skip_source_error_control.",
    )
    ap.add_argument("--timeout-s", type=int, default=240)
    ap.add_argument("--jobs", type=int, default=1)
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    speed_artifact = Path(args.speed_artifact).resolve()
    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    output_root.mkdir(parents=True, exist_ok=True)
    report_json = Path(args.report_json)
    if not report_json.is_absolute():
        report_json = ROOT / report_json
    report_md = Path(args.report_md)
    if not report_md.is_absolute():
        report_md = ROOT / report_md

    rows = select_rows(
        load_speed_rows(speed_artifact),
        suite=args.suite,
        entries=set(args.entry) if args.entry else None,
        forms=set(args.form) if args.form else None,
        limit=args.limit,
    )
    mode_ids = args.mode or [
        "strict_current",
        "profile_fast",
        "profile_fast_skip_source_error_control",
    ]
    modes = [MODES[mode_id] for mode_id in mode_ids]

    jobs: list[tuple[dict[str, object], Mode]] = [
        (row, mode)
        for row in rows
        for mode in modes
    ]
    results: list[dict[str, object]] = []
    if args.jobs <= 1:
        for row, mode in jobs:
            results.append(run_one(row, mode, output_root=output_root, timeout_s=args.timeout_s))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
            future_map = {
                executor.submit(run_one, row, mode, output_root=output_root, timeout_s=args.timeout_s): (row, mode)
                for row, mode in jobs
            }
            for future in concurrent.futures.as_completed(future_map):
                results.append(future.result())
    results.sort(
        key=lambda row: (
            str(row["entry_id"]),
            str(row["form"]),
            str(row["variant"]),
            mode_ids.index(str(row["mode_id"])),
        )
    )
    attach_strict_comparisons(results)
    mode_summary = summarize(results)
    unsafe_profiles = [
        mode_id
        for mode_id, summary in mode_summary.items()
        if mode_id != "strict_current" and summary["unsafe_vs_strict_count"] > 0
    ]

    report = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": ARTIFACT_KIND,
        "date": date.today().isoformat(),
        "status": "complete_with_unsafe_profiles" if unsafe_profiles else "complete",
        "claim_allowed": False,
        "reason": NO_CLAIM_REASON,
        "release": "vabench-release-v1",
        "runner": {
            "name": Path(__file__).name,
            "argv": sys.argv,
            "python_version": platform.python_version(),
            "cwd": str(Path.cwd()),
            "source_hashes": {
                "run_vabench_release_evas_speed_experiment.py": sha256_file(Path(__file__).resolve()),
                "simulate_evas.py": sha256_file(ROOT / "runners" / "simulate_evas.py"),
                "run_gold_suite.py": sha256_file(ROOT / "runners" / "run_gold_suite.py"),
                "run_gold_dual_suite.py": sha256_file(ROOT / "runners" / "run_gold_dual_suite.py"),
            },
        },
        "output_root": rel(output_root),
        "p0_existing_baseline": p0_existing_summary(speed_artifact),
        "parity_safety": {
            "speed_claim_effect": "no_claim",
            "requires_dual_rerun_before_claim": True,
            "violations": unsafe_profiles,
        },
        "selected_row_count": len(rows),
        "selected_rows": [
            {
                "entry_id": row.get("entry_id"),
                "form": row.get("form"),
                "variant": row.get("variant"),
                "source_evas_wall_time_s": row.get("evas_wall_time_s"),
                "source_spectre_wall_time_s": row.get("spectre_wall_time_s"),
                "source_wrapper_spectre_over_evas_speedup": row.get("wrapper_spectre_over_evas_speedup"),
            }
            for row in rows
        ],
        "mode_ids": mode_ids,
        "modes": {
            mode.mode_id: {
                "phase": mode.phase,
                "label": mode.label,
                "simulator_options": list(mode.simulator_options),
                "default_off_fast_path": mode.default_off_fast_path,
            }
            for mode in modes
        },
        "mode_summary": mode_summary,
        "phase_summary": summarize_phases(results),
        "timing_totals": timing_totals(results),
        "safety_requirements": [
            "strict_current remains the certification path",
            "P2/P3 candidates must keep behavior status equal to strict_current",
            "P2/P3 candidates must pass waveform parity against strict_current before promotion",
            "default-off fast paths require Spectre revalidation before any paper claim",
        ],
        "results": results,
    }
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, report_md)
    print(
        "wrote EVAS speed experiment: rows={rows}; modes={modes}; report={report}".format(
            rows=len(rows),
            modes=",".join(mode_ids),
            report=rel(report_json),
        )
    )


if __name__ == "__main__":
    main()
