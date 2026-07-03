#!/usr/bin/env python3
"""Run Spectre evidence for selected vaBench release-v3 tasks."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from run_gold_dual_suite import (  # noqa: E402
    default_bridge_repo,
    normalize_spectre_backend,
    normalize_spectre_mode,
    run_spectre_case,
)
from run_gold_suite import ahdl_includes  # noqa: E402
from simulate_evas import (  # noqa: E402
    CHECKS,
    behavior_side_output_names,
    evaluate_behavior_with_timeout,
    read_task_artifact_targets,
    read_task_index_id,
    validate_behavior_side_outputs,
)


REVIEWED_TASKS = (
    "006-element-shuffler",
    "007-first-order-lowpass",
    "049-window-comparator-detector",
    "081-aperture-delay-track-and-hold",
    "097-cppll-tracking-reacquire-timer",
    "099-dither-adder",
    "101-fixed-gain-amplifier",
    "107-reference-step-clock",
    "111-clocked-sine-source",
    "146-smooth-comparator-tanh",
    "148-absolute-value",
    "274-weighted-decoder-6bit",
    "282-pfd-timer-reset",
    "284-window-comparator-testbench",
    "285-aperture-delay-sample-hold",
    "286-first-order-lowpass-bugfix",
    "287-gain-extraction-flow",
    "288-absolute-value",
    "292-smooth-tanh-comparator",
    "294-subradix-dac10",
    "300-pfd-active-low-reset",
)


def task_number(task_dir: Path) -> int | None:
    try:
        return int(task_dir.name[:3])
    except ValueError:
        return None


def read_task_toml(task_dir: Path) -> dict[str, Any]:
    task_toml = task_dir / "task.toml"
    if not task_toml.exists():
        return {}
    try:
        import tomllib

        return tomllib.loads(task_toml.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        text = task_toml.read_text(encoding="utf-8", errors="ignore")
        parsed: dict[str, Any] = {}
        for key in ("id", "name", "form"):
            match = re.search(rf"(?m)^\s*{key}\s*=\s*(\".*?\"|'.*?')\s*$", text)
            if match:
                try:
                    parsed[key] = ast.literal_eval(match.group(1))
                except (SyntaxError, ValueError):
                    pass
        return parsed


def read_task_index_entry(task_dir: Path) -> dict[str, Any]:
    if task_dir.parent.name != "tasks":
        return {}
    index_path = task_dir.parent.parent / "TASKS.json"
    if not index_path.exists():
        return {}
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    tasks = data.get("tasks", {})
    if not isinstance(tasks, dict):
        return {}
    entry = tasks.get(task_dir.name, {})
    if not isinstance(entry, dict):
        return {}
    defaults = data.get("defaults", {})
    if isinstance(defaults, dict):
        return {**defaults, **entry}
    return entry


def effective_task_form(task_dir: Path, meta: dict[str, Any]) -> str:
    task_toml_form = str(meta.get("form") or "").strip()
    if task_toml_form:
        return task_toml_form
    return str(read_task_index_entry(task_dir).get("form") or "").strip()


def load_v3_checks_config(task_dir: Path) -> dict[str, Any]:
    for checks_path in (
        task_dir / "test_harness" / "checks.yaml",
        task_dir / "checks.yaml",
        task_dir / "private" / "invisible_checker_config.yaml",
        task_dir / "private" / "checks.yaml",
    ):
        if not checks_path.exists():
            continue
        data = yaml.safe_load(checks_path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            continue
        checker = data.get("checker") if isinstance(data.get("checker"), dict) else {}
        syntax = data.get("syntax") if isinstance(data.get("syntax"), dict) else {}
        parameters = data.get("checker_parameters")
        if not isinstance(parameters, dict):
            parameters = {}
        return {
            "path": checks_path,
            "task_id": data.get("task_id"),
            "checker_task_id": checker.get("task_id"),
            "checker_parameters": parameters,
            "syntax_must_include": syntax.get("must_include") or data.get("must_include") or [],
            "syntax_must_not_include": syntax.get("must_not_include") or data.get("must_not_include") or [],
        }
    return {}


def checker_candidates(task_dir: Path, meta: dict[str, Any], checks_config: dict[str, Any]) -> list[str]:
    values = [
        checks_config.get("checker_task_id"),
        meta.get("id"),
        read_task_index_id(task_dir),
        task_dir.name,
        checks_config.get("task_id"),
        f"{checks_config.get('task_id')}:{meta.get('form')}" if checks_config.get("task_id") and meta.get("form") else None,
    ]
    candidates: list[str] = []
    for value in values:
        if not value:
            continue
        text = str(value)
        if text not in candidates:
            candidates.append(text)
    return candidates


def resolve_checker_id(task_dir: Path, meta: dict[str, Any], checks_config: dict[str, Any]) -> str:
    candidates = checker_candidates(task_dir, meta, checks_config)
    for candidate in candidates:
        if candidate in CHECKS:
            return candidate
    return candidates[0] if candidates else str(meta.get("id") or task_dir.name)


def select_testbench(task_dir: Path, split: str) -> Path | None:
    split_dir = task_dir / f"test_{split}"
    direct = split_dir / f"{split}.scs"
    if direct.exists():
        return direct
    candidates = sorted((split_dir / "tests").glob("*.scs"))
    if len(candidates) == 1:
        return candidates[0]
    preferred = [path for path in candidates if "ref" in path.name or split in path.name]
    if len(preferred) == 1:
        return preferred[0]
    return None


def target_testbench(candidate_root: Path, targets: list[str], form: str) -> Path | None:
    target_scs = [candidate_root / target for target in targets if target.endswith(".scs")]
    existing = [path for path in target_scs if path.exists()]
    if existing and form in {"tb", "e2e"}:
        return existing[0]
    scs_candidates = sorted(candidate_root.glob("*.scs"))
    if len(scs_candidates) == 1 and form in {"tb", "e2e"}:
        return scs_candidates[0]
    return None


def choose_case_testbench(
    *,
    task_dir: Path,
    candidate_root: Path,
    targets: list[str],
    form: str,
    split: str,
    force_harness_tb: bool,
) -> Path | None:
    if not force_harness_tb:
        candidate_tb = target_testbench(candidate_root, targets, form)
        if candidate_tb is not None:
            return candidate_tb
    return select_testbench(task_dir, split)


def variant_has_target(variant_dir: Path, targets: list[str], form: str) -> bool:
    if any((variant_dir / target).exists() for target in targets):
        return True
    if form in {"tb", "e2e"} and list(variant_dir.glob("*.scs")):
        return True
    return False


def candidate_roots(
    task_dir: Path,
    variants: list[str],
    *,
    targets: list[str],
    form: str,
    all_negative_variants: bool,
) -> list[tuple[str, Path, bool]]:
    if all_negative_variants:
        neg_root = task_dir / "negative_variants"
        if not neg_root.exists():
            return []
        roots = []
        for variant_dir in sorted(path for path in neg_root.iterdir() if path.is_dir()):
            if variant_has_target(variant_dir, targets, form):
                roots.append((variant_dir.name, variant_dir, False))
        return roots
    if not variants:
        return [("gold", task_dir / "solution", True)]
    roots: list[tuple[str, Path, bool]] = []
    for variant in variants:
        root = task_dir / "negative_variants" / variant
        roots.append((variant, root, False))
    return roots


def include_search_dirs(task_dir: Path, candidate_root: Path) -> list[Path]:
    dirs: list[Path] = []
    for path in (candidate_root, task_dir / "solution", task_dir / "starter"):
        if path.exists() and path not in dirs:
            dirs.append(path)
    return dirs


def resolve_include_paths(task_dir: Path, candidate_root: Path, tb_path: Path) -> tuple[list[Path], list[str]]:
    include_paths: list[Path] = []
    missing: list[str] = []
    search_dirs = include_search_dirs(task_dir, candidate_root)
    for include in ahdl_includes(tb_path):
        include_name = Path(include.replace("\\", "/")).name
        found = None
        for search_dir in search_dirs:
            candidate = search_dir / include_name
            if candidate.exists():
                found = candidate
                break
        if found is None:
            local_candidate = (tb_path.parent / include).resolve()
            if local_candidate.exists():
                found = local_candidate
        if found is None:
            missing.append(include)
            continue
        if found not in include_paths:
            include_paths.append(found)
    return include_paths, missing


def syntax_failures(checks_config: dict[str, Any], candidate_root: Path, include_paths: list[Path], tb_path: Path) -> list[str]:
    source_paths = [tb_path, *include_paths, *sorted(candidate_root.glob("*.va")), *sorted(candidate_root.glob("*.scs"))]
    seen: set[Path] = set()
    texts: list[str] = []
    for path in source_paths:
        if path in seen or not path.exists():
            continue
        seen.add(path)
        texts.append(path.read_text(encoding="utf-8", errors="ignore"))
    source_text = "\n".join(texts)
    failures: list[str] = []
    for phrase in checks_config.get("syntax_must_include", []):
        if str(phrase) and str(phrase) not in source_text:
            failures.append(f"checker_config_must_include_missing={phrase}")
    for phrase in checks_config.get("syntax_must_not_include", []):
        if str(phrase) and str(phrase) in source_text:
            failures.append(f"checker_config_must_not_include_present={phrase}")
    return failures


def run_audit_case(
    *,
    task_dir: Path,
    split: str,
    variant_label: str,
    candidate_root: Path,
    expected_pass: bool,
    output_root: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    spectre_backend: str,
    sui_host: str | None,
    sui_work_root: str | None,
    spectre_mode: str,
    force_harness_tb: bool,
) -> dict[str, Any]:
    meta = read_task_toml(task_dir)
    task_index_id = read_task_index_id(task_dir)
    form = effective_task_form(task_dir, meta)
    targets = read_task_artifact_targets(task_dir)
    checks_config = load_v3_checks_config(task_dir)
    checker_id = resolve_checker_id(task_dir, meta, checks_config)
    row: dict[str, Any] = {
        "task": task_dir.name,
        "task_id": meta.get("id") or task_index_id or task_dir.name,
        "form": form,
        "split": split,
        "variant": variant_label,
        "expected_pass": expected_pass,
        "checker_task_id": checker_id,
        "checks_path": str(checks_config.get("path") or ""),
        "targets": targets,
        "notes": [],
    }
    if not targets:
        row["status"] = "FAIL_NO_TARGET"
        row["notes"].append("missing task.toml artifacts.target")
        return row
    if not candidate_root.exists():
        row["status"] = "FAIL_NO_CANDIDATE_ROOT"
        row["notes"].append(f"missing candidate root {candidate_root}")
        return row
    tb_path = choose_case_testbench(
        task_dir=task_dir,
        candidate_root=candidate_root,
        targets=targets,
        form=form,
        split=split,
        force_harness_tb=force_harness_tb,
    )
    if tb_path is None:
        row["status"] = "FAIL_NO_TB"
        row["notes"].append(f"missing unique {split} testbench")
        return row
    include_paths, missing_includes = resolve_include_paths(task_dir, candidate_root, tb_path)
    row["tb_path"] = str(tb_path)
    row["include_paths"] = [str(path) for path in include_paths]
    if missing_includes:
        row["status"] = "FAIL_MISSING_INCLUDE"
        row["notes"].extend(f"missing ahdl_include={include}" for include in missing_includes)
        return row
    row["syntax_failures"] = syntax_failures(checks_config, candidate_root, include_paths, tb_path)

    case_name = f"{task_dir.name}__{split}__{variant_label}"
    case_out = output_root / case_name
    side_outputs = behavior_side_output_names(checker_id)
    started = time.perf_counter()
    spectre = run_spectre_case(
        task_id=f"{task_dir.name}:{split}:{variant_label}",
        tb_path=tb_path,
        include_paths=include_paths,
        output_dir=case_out,
        bridge_repo=bridge_repo,
        cadence_cshrc=cadence_cshrc,
        timeout_s=timeout_s,
        side_output_files=side_outputs,
        spectre_backend=spectre_backend,
        sui_host=sui_host,
        sui_work_root=sui_work_root,
        spectre_mode=spectre_mode,
    )
    row["wall_s"] = time.perf_counter() - started
    row["spectre"] = {
        "ok": bool(spectre.get("ok")),
        "status": spectre.get("status"),
        "errors": spectre.get("errors") or [],
        "warnings": spectre.get("warnings") or [],
        "signals": spectre.get("signals") or [],
        "rows": spectre.get("rows"),
        "csv_path": spectre.get("csv_path"),
        "result_json": str(case_out / "spectre_result.json"),
        "stdout_tail": (spectre.get("stdout_tail") or "")[-1200:],
    }
    if not spectre.get("ok"):
        row["status"] = "FAIL_SPECTRE"
        return row

    csv_path = Path(str(spectre.get("csv_path") or case_out / "tran_spectre.csv"))
    if not csv_path.exists():
        row["status"] = "FAIL_NO_CSV"
        row["notes"].append(f"missing Spectre CSV {csv_path}")
        return row
    behavior_score, behavior_notes = evaluate_behavior_with_timeout(
        checker_id,
        csv_path,
        timeout_s=timeout_s,
        checks_config=checks_config,
    )
    row["behavior_score"] = behavior_score
    row["behavior_notes"] = behavior_notes
    side_validation = validate_behavior_side_outputs(checker_id, case_out, csv_path)
    if side_validation is not None:
        row["side_output_ok"], row["side_output_note"] = side_validation
    passed = behavior_score == 1.0 and not row["syntax_failures"] and (
        side_validation is None or bool(side_validation[0])
    )
    if expected_pass:
        row["status"] = "PASS" if passed else "FAIL_BEHAVIOR"
    else:
        row["status"] = "NEGATIVE_REJECTED" if not passed else "NEGATIVE_UNEXPECTED_PASS"
    return row


def select_tasks(root: Path, args: argparse.Namespace) -> list[Path]:
    all_tasks = sorted(path for path in root.iterdir() if path.is_dir())
    selected_names: set[str] = set(args.task or [])
    if args.reviewed:
        selected_names.update(REVIEWED_TASKS)
    tasks: list[Path] = []
    for task_dir in all_tasks:
        number = task_number(task_dir)
        meta = read_task_toml(task_dir)
        ids = {task_dir.name, str(meta.get("id") or "")}
        if selected_names and not (ids & selected_names):
            continue
        if args.start is not None and (number is None or number < args.start):
            continue
        if args.end is not None and (number is None or number > args.end):
            continue
        tasks.append(task_dir)
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="benchmark-vabench-release-v3/tasks")
    parser.add_argument("--task", action="append", help="Task directory name or task.toml id. Repeatable.")
    parser.add_argument("--reviewed", action="store_true", help="Run the manually reviewed v3 rows.")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--split", choices=("hidden", "visible"), default="hidden")
    parser.add_argument("--variant", action="append", default=[], help="negative_variants subdir. Repeatable.")
    parser.add_argument("--all-negative-variants", action="store_true")
    parser.add_argument("--force-harness-tb", action="store_true")
    parser.add_argument("--timeout-s", type=int, default=300)
    parser.add_argument("--out", required=True)
    parser.add_argument("--work-root", default="results/v3_spectre_audit")
    parser.add_argument("--bridge-repo", default=None)
    parser.add_argument("--cadence-cshrc", default=None)
    parser.add_argument("--spectre-backend", default="bridge")
    parser.add_argument("--spectre-mode", default="ax")
    parser.add_argument("--sui-host", default=None)
    parser.add_argument("--sui-work-root", default=None)
    args = parser.parse_args()

    root = Path(args.root)
    output_root = Path(args.work_root)
    output_root.mkdir(parents=True, exist_ok=True)
    bridge_repo = Path(args.bridge_repo) if args.bridge_repo else default_bridge_repo()
    backend = normalize_spectre_backend(args.spectre_backend)
    mode = normalize_spectre_mode(args.spectre_mode)
    rows: list[dict[str, Any]] = []
    tasks = select_tasks(root, args)
    for task_dir in tasks:
        meta = read_task_toml(task_dir)
        targets = read_task_artifact_targets(task_dir)
        form = effective_task_form(task_dir, meta)
        variants = candidate_roots(
            task_dir,
            args.variant,
            targets=targets,
            form=form,
            all_negative_variants=args.all_negative_variants,
        )
        for variant_label, candidate_root, expected_pass in variants:
            row = run_audit_case(
                task_dir=task_dir,
                split=args.split,
                variant_label=variant_label,
                candidate_root=candidate_root,
                expected_pass=expected_pass,
                output_root=output_root,
                bridge_repo=bridge_repo,
                cadence_cshrc=args.cadence_cshrc,
                timeout_s=args.timeout_s,
                spectre_backend=backend,
                sui_host=args.sui_host,
                sui_work_root=args.sui_work_root,
                spectre_mode=mode,
                force_harness_tb=args.force_harness_tb,
            )
            rows.append(row)
            print(
                task_dir.name,
                args.split,
                variant_label,
                row.get("status"),
                row.get("checker_task_id"),
                f"{row.get('wall_s', 0.0):.2f}s",
                (row.get("behavior_notes") or row.get("notes") or [])[:4],
                flush=True,
            )

    report = {
        "root": str(root),
        "split": args.split,
        "variant": args.variant,
        "all_negative_variants": args.all_negative_variants,
        "tasks": len(tasks),
        "rows": len(rows),
        "pass": sum(1 for row in rows if row.get("status") == "PASS"),
        "negative_rejected": sum(1 for row in rows if row.get("status") == "NEGATIVE_REJECTED"),
        "fail": sum(1 for row in rows if row.get("status") not in {"PASS", "NEGATIVE_REJECTED"}),
        "rows_data": rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("REPORT", out, flush=True)
    return 0 if report["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
