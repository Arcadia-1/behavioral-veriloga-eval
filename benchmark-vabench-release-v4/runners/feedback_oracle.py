from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


def find_repo_root(path: Path) -> Path:
    for parent in [path, *path.parents]:
        if (parent / "runners" / "simulate_evas.py").exists():
            return parent
    env_root = os.environ.get("VABENCH_ROOT")
    if env_root and (Path(env_root) / "runners" / "simulate_evas.py").exists():
        return Path(env_root)
    raise SystemExit("cannot find behavioral-veriloga-eval repo root; set VABENCH_ROOT")


def _candidate_source_dir(env_name: str) -> Path:
    override = os.environ.get(env_name)
    if override:
        return Path(override).expanduser().resolve()
    legacy = os.environ.get("VABENCH_VISIBLE_SOURCE_DIR")
    if legacy and env_name == "VABENCH_FEEDBACK_SOURCE_DIR":
        return Path(legacy).expanduser().resolve()
    raise SystemExit(
        f"missing candidate source directory; set {env_name}=<candidate-dir>. "
        "The v4 oracle runner does not fall back to starter files."
    )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _tb_path(task_dir: Path, profile_name: str) -> Path:
    if profile_name == "feedback":
        return task_dir / "test_feedback" / "public_tb.scs"
    if profile_name == "score":
        return task_dir / "evaluator" / "score_tb.scs"
    raise SystemExit(f"unsupported oracle profile name: {profile_name}")


def _load_tb_text(task_dir: Path, profile_name: str) -> str:
    path = _tb_path(task_dir, profile_name)
    if not path.exists():
        raise SystemExit(f"missing oracle testbench deck: {path}")
    return path.read_text(encoding="utf-8")


def _load_checker_profile(task_dir: Path) -> dict[str, Any]:
    profile_path = task_dir / "evaluator" / "checker_profile.json"
    if not profile_path.exists():
        raise SystemExit(f"missing checker profile: {profile_path}")
    return _read_json(profile_path)


def _copy_candidate_sources(source_dir: Path, run_dir: Path, expected_files: list[str]) -> None:
    source_files = sorted(source_dir.glob("*.va"))
    if not source_files:
        raise SystemExit(f"expected at least one candidate .va under {source_dir}")
    missing = [filename for filename in expected_files if not (source_dir / filename).exists()]
    if missing:
        raise SystemExit(f"candidate source directory is missing target artifact(s): {', '.join(missing)}")
    for source_file in source_files:
        shutil.copy2(source_file, run_dir / source_file.name)


def _run_oracle(
    script_file: str | Path,
    *,
    profile_name: str,
    source_env: str,
    result_prefix: str,
    checker_task_id: str | None = None,
    timeout_s: int = 60,
    extra_trace_signals: set[str] | frozenset[str] | None = None,
    force_python_engine: bool = False,
) -> int:
    script_path = Path(script_file).resolve()
    task_dir = script_path.parents[1] if script_path.parent.name == "test_feedback" else script_path.parents[1]
    contract = _read_json(task_dir / "public_contract.json")
    checker_profile = _load_checker_profile(task_dir)
    effective_checker_task_id = checker_task_id or str(checker_profile.get("checker_task_id") or "")
    source_dir = _candidate_source_dir(source_env)
    expected_files = [str(item) for item in contract.get("target_artifacts") or []]

    repo_root = find_repo_root(task_dir)
    runners_dir = str(repo_root / "runners")
    if runners_dir not in sys.path:
        sys.path.insert(0, runners_dir)
    from simulate_evas import (
        evaluate_behavior,
        required_trace_signals_for_checker,
        run_evas,
        spectre_aligned_veriloga_preflight,
    )

    with tempfile.TemporaryDirectory(prefix=f"v4_{profile_name}_oracle_") as td:
        run_dir = Path(td)
        _copy_candidate_sources(source_dir, run_dir, expected_files)
        tb_dst = run_dir / f"tb_{profile_name}.scs"
        tb_dst.write_text(_load_tb_text(task_dir, profile_name), encoding="utf-8")

        preflight = spectre_aligned_veriloga_preflight(run_dir)
        if preflight:
            print(f"{result_prefix}_PREFLIGHT_FAIL")
            for item in preflight:
                print(item)
            return 1

        required_signals = set(extra_trace_signals or ())
        trace_contract = checker_profile.get("trace_contract") or {}
        required_signals.update(str(signal) for signal in trace_contract.get("extra_trace_signals") or [])
        if effective_checker_task_id:
            required_signals.update(required_trace_signals_for_checker(effective_checker_task_id))

        output_dir = run_dir / "out"
        old_engine = os.environ.get("EVAS_ENGINE")
        if force_python_engine:
            os.environ["EVAS_ENGINE"] = "python"
        try:
            result = run_evas(
                run_dir,
                tb_dst,
                output_dir,
                timeout_s=timeout_s,
                required_trace_signals=required_signals or None,
            )
        finally:
            if force_python_engine:
                if old_engine is None:
                    os.environ.pop("EVAS_ENGINE", None)
                else:
                    os.environ["EVAS_ENGINE"] = old_engine

        combined = (result.stdout or "") + "\n" + (result.stderr or "")
        if result.returncode != 0:
            print(f"{result_prefix}_EVAS_FAIL")
            print(combined[-4000:])
            return 1
        if "Compiled Verilog-A module:" not in combined:
            print(f"{result_prefix}_NO_COMPILE_MARKER")
            print(combined[-4000:])
            return 1
        if "Transient Analysis" not in combined:
            print(f"{result_prefix}_NO_TRAN_MARKER")
            print(combined[-4000:])
            return 1

        if effective_checker_task_id:
            csv_path = output_dir / "tran.csv"
            if not csv_path.exists():
                print(f"{result_prefix}_BEHAVIOR_NO_TRACE")
                print(combined[-4000:])
                return 1
            score, notes = evaluate_behavior(effective_checker_task_id, csv_path)
            if score < 1.0:
                print(f"{result_prefix}_BEHAVIOR_FAIL")
                for note in notes:
                    print(note)
                return 1
            print(f"{result_prefix}_BEHAVIOR_PASS")
            for note in notes:
                print(note)

        print(f"{result_prefix}_PASS")
        return 0


def run_feedback(
    script_file: str | Path,
    *,
    checker_task_id: str | None = None,
    timeout_s: int = 60,
    extra_trace_signals: set[str] | frozenset[str] | None = None,
    force_python_engine: bool = False,
) -> int:
    return _run_oracle(
        script_file,
        profile_name="feedback",
        source_env="VABENCH_FEEDBACK_SOURCE_DIR",
        result_prefix="FEEDBACK",
        checker_task_id=checker_task_id,
        timeout_s=timeout_s,
        extra_trace_signals=extra_trace_signals,
        force_python_engine=force_python_engine,
    )


def run_score(
    script_file: str | Path,
    *,
    checker_task_id: str | None = None,
    timeout_s: int = 60,
    extra_trace_signals: set[str] | frozenset[str] | None = None,
    force_python_engine: bool = False,
) -> int:
    return _run_oracle(
        script_file,
        profile_name="score",
        source_env="VABENCH_SCORE_SOURCE_DIR",
        result_prefix="SCORE",
        checker_task_id=checker_task_id,
        timeout_s=timeout_s,
        extra_trace_signals=extra_trace_signals,
        force_python_engine=force_python_engine,
    )
