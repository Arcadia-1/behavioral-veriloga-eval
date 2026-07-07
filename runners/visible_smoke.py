from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path


def find_repo_root(path: Path) -> Path:
    for parent in [path, *path.parents]:
        if (parent / "runners" / "simulate_evas.py").exists():
            return parent
    env_root = os.environ.get("VABENCH_ROOT")
    if env_root and (Path(env_root) / "runners" / "simulate_evas.py").exists():
        return Path(env_root)
    raise SystemExit("cannot find behavioral-veriloga-eval repo root; set VABENCH_ROOT")


def _candidate_source_dir(task_dir: Path) -> Path:
    override = os.environ.get("VABENCH_VISIBLE_SOURCE_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return task_dir / "starter"


def run_visible_smoke(
    script_file: str | Path,
    *,
    checker_task_id: str | None = None,
    timeout_s: int = 60,
    extra_trace_signals: set[str] | frozenset[str] | None = None,
    force_python_engine: bool = False,
) -> int:
    tests_dir = Path(script_file).resolve().parent
    task_dir = tests_dir.parents[1]
    source_dir = _candidate_source_dir(task_dir)
    tb_src = tests_dir / "tb_visible_smoke.scs"
    source_files = sorted(source_dir.glob("*.va"))
    if not source_files:
        raise SystemExit(f"expected at least one candidate .va under {source_dir}")
    if not tb_src.exists():
        raise SystemExit(f"missing visible smoke testbench: {tb_src}")

    repo_root = find_repo_root(tests_dir)
    runners_dir = str(repo_root / "runners")
    if runners_dir not in sys.path:
        sys.path.insert(0, runners_dir)
    from simulate_evas import (
        evaluate_behavior,
        required_trace_signals_for_checker,
        run_evas,
        spectre_aligned_veriloga_preflight,
    )

    with tempfile.TemporaryDirectory(prefix="visible_smoke_") as td:
        run_dir = Path(td)
        for source_file in source_files:
            shutil.copy2(source_file, run_dir / source_file.name)
        tb_dst = run_dir / "tb_visible_smoke.scs"
        shutil.copy2(tb_src, tb_dst)

        preflight = spectre_aligned_veriloga_preflight(run_dir)
        if preflight:
            print("VISIBLE_SMOKE_PREFLIGHT_FAIL")
            for item in preflight:
                print(item)
            return 1

        required_signals = set(extra_trace_signals or ())
        if checker_task_id:
            required_signals.update(required_trace_signals_for_checker(checker_task_id))

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
            print("VISIBLE_SMOKE_EVAS_FAIL")
            print(combined[-4000:])
            return 1
        if "Compiled Verilog-A module:" not in combined:
            print("VISIBLE_SMOKE_NO_COMPILE_MARKER")
            print(combined[-4000:])
            return 1
        if "Transient Analysis" not in combined:
            print("VISIBLE_SMOKE_NO_TRAN_MARKER")
            print(combined[-4000:])
            return 1

        if checker_task_id:
            csv_path = output_dir / "tran.csv"
            if not csv_path.exists():
                print("VISIBLE_BEHAVIOR_NO_TRACE")
                print(combined[-4000:])
                return 1
            score, notes = evaluate_behavior(checker_task_id, csv_path)
            if score < 1.0:
                print("VISIBLE_BEHAVIOR_FAIL")
                for note in notes:
                    print(note)
                return 1
            print("VISIBLE_BEHAVIOR_PASS")
            for note in notes:
                print(note)

        print("VISIBLE_SMOKE_PASS")
        return 0
