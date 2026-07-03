#!/usr/bin/env python3
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


def main() -> int:
    tests_dir = Path(__file__).resolve().parent
    task_dir = tests_dir.parents[1]
    starter_dir = task_dir / "starter"
    tb_src = tests_dir / "tb_visible_smoke.scs"
    starter_files = sorted(starter_dir.glob("*.va"))
    if len(starter_files) != 1:
        raise SystemExit(f"expected one starter .va under {starter_dir}, found {len(starter_files)}")
    if not tb_src.exists():
        raise SystemExit(f"missing visible smoke testbench: {tb_src}")

    repo_root = find_repo_root(tests_dir)
    sys.path.insert(0, str(repo_root / "runners"))
    from simulate_evas import run_evas, spectre_aligned_veriloga_preflight

    with tempfile.TemporaryDirectory(prefix="visible_smoke_") as td:
        run_dir = Path(td)
        starter_dst = run_dir / starter_files[0].name
        tb_dst = run_dir / "tb_visible_smoke.scs"
        shutil.copy2(starter_files[0], starter_dst)
        shutil.copy2(tb_src, tb_dst)

        preflight = spectre_aligned_veriloga_preflight(run_dir)
        if preflight:
            print("VISIBLE_SMOKE_PREFLIGHT_FAIL")
            for item in preflight:
                print(item)
            return 1

        output_dir = run_dir / "out"
        old_worker = os.environ.get("VAEVAS_EVAS_PERSISTENT_WORKER")
        old_engine = os.environ.get("EVAS_ENGINE")
        os.environ["VAEVAS_EVAS_PERSISTENT_WORKER"] = "0"
        try:
            result = run_evas(run_dir, tb_dst, output_dir, timeout_s=30)
            combined = (result.stdout or "") + "\n" + (result.stderr or "")
            if result.returncode != 0 and "no supported whole-segment Rust runtime" in combined:
                os.environ["EVAS_ENGINE"] = "python"
                result = run_evas(run_dir, tb_dst, output_dir, timeout_s=30)
        finally:
            if old_worker is None:
                os.environ.pop("VAEVAS_EVAS_PERSISTENT_WORKER", None)
            else:
                os.environ["VAEVAS_EVAS_PERSISTENT_WORKER"] = old_worker
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
        print("VISIBLE_SMOKE_PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
