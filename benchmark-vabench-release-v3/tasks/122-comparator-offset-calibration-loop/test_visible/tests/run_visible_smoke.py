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
    starter_files = sorted((task_dir / "starter").glob("*.va"))
    if not starter_files:
        raise SystemExit("expected at least one starter .va under starter/")
    tb_src = tests_dir / "tb_visible_smoke.scs"
    repo_root = find_repo_root(tests_dir)
    sys.path.insert(0, str(repo_root / "runners"))
    from simulate_evas import run_evas, spectre_aligned_veriloga_preflight

    with tempfile.TemporaryDirectory(prefix="visible_smoke_") as td:
        run_dir = Path(td)
        for starter_file in starter_files:
            shutil.copy2(starter_file, run_dir / starter_file.name)
        shutil.copy2(tb_src, run_dir / "tb_visible_smoke.scs")
        preflight = spectre_aligned_veriloga_preflight(run_dir)
        if preflight:
            print("VISIBLE_SMOKE_PREFLIGHT_FAIL")
            for item in preflight:
                print(item)
            return 1
        old = os.environ.get("EVAS_ENGINE")
        os.environ["EVAS_ENGINE"] = "python"
        try:
            result = run_evas(run_dir, run_dir / "tb_visible_smoke.scs", run_dir / "out", timeout_s=30)
        finally:
            if old is None:
                os.environ.pop("EVAS_ENGINE", None)
            else:
                os.environ["EVAS_ENGINE"] = old
        combined = (result.stdout or "") + "\n" + (result.stderr or "")
        if result.returncode != 0:
            print("VISIBLE_SMOKE_EVAS_FAIL")
            print(combined[-4000:])
            return 1
        if "Compiled Verilog-A module:" not in combined:
            print("VISIBLE_SMOKE_NO_COMPILE_MARKER")
            print(combined[-4000:])
            return 1
        print("VISIBLE_SMOKE_PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
