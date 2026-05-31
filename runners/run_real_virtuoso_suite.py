#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

from virtuoso_bridge.spectre.runner import SpectreSimulator, spectre_mode_args


CASES = [
    {
        "id": "clk_divider",
        "tb": "tasks/spec-to-va/voltage/digital-logic/clk_divider/gold/tb_clk_divider_ref.scs",
    },
    {
        "id": "prbs7",
        "tb": "tasks/spec-to-va/voltage/digital-logic/prbs7/gold/tb_prbs7_ref.scs",
    },
    {
        "id": "therm2bin",
        "tb": "tasks/spec-to-va/voltage/digital-logic/therm2bin/gold/tb_therm2bin_ref.scs",
    },
    {
        "id": "bbpd",
        "tb": "tasks/spec-to-va/voltage/pll-clock/bbpd/gold/tb_bbpd_ref.scs",
    },
    {
        "id": "multimod_divider",
        "tb": "tasks/spec-to-va/voltage/pll-clock/multimod_divider/gold/tb_multimod_divider_ref.scs",
    },
    {
        "id": "bad_bus_output_loop",
        "tb": "tasks/bugfix/voltage/bad_bus_output_loop/gold/tb_bad_bus_output_loop.scs",
    },
    {
        "id": "missing_transition_outputs",
        "tb": "tasks/bugfix/voltage/missing_transition_outputs/gold/tb_missing_transition_outputs.scs",
    },
]


def parse_ahdl_includes(tb_path: Path) -> list[Path]:
    text = tb_path.read_text(encoding="utf-8", errors="ignore")
    names = re.findall(r'^\s*ahdl_include\s+"([^"]+)"', text, flags=re.MULTILINE)
    return [tb_path.parent / name for name in names]


def main() -> int:
    if load_dotenv is not None:
        bridge_env = Path(__file__).resolve().parents[2] / "virtuoso-bridge-lite" / ".env"
        if bridge_env.exists():
            load_dotenv(bridge_env)

    repo = Path(__file__).resolve().parents[1]
    out_root = repo / "results" / "real-virtuoso-suite"
    out_root.mkdir(parents=True, exist_ok=True)

    sim = SpectreSimulator.from_env(
        spectre_cmd="spectre",
        spectre_args=spectre_mode_args("ax"),
        output_format="psfascii",
    )

    all_results: list[dict] = []
    t0 = time.time()

    for case in CASES:
        case_id = case["id"]
        tb = repo / case["tb"]
        includes = parse_ahdl_includes(tb)
        case_out = out_root / case_id
        case_out.mkdir(parents=True, exist_ok=True)

        rec: dict = {
            "case": case_id,
            "tb": str(tb),
            "includes": [str(p) for p in includes],
            "ok": False,
            "status": "NOT_RUN",
            "errors": [],
            "warnings": [],
            "execution_time": None,
            "points": 0,
            "output_dir": str(case_out),
        }

        missing = [str(p) for p in [tb, *includes] if not Path(p).exists()]
        if missing:
            rec["status"] = "MISSING_INPUT"
            rec["errors"] = [f"missing file: {m}" for m in missing]
            all_results.append(rec)
            print(f"[FAIL] {case_id}: missing input files")
            continue

        print(f"[RUN] {case_id}")
        st = time.time()
        try:
            result = sim.run_simulation(tb, {"include_files": includes, "work_dir": case_out})
            rec["ok"] = bool(getattr(result, "ok", False))
            rec["status"] = str(getattr(result, "status", "UNKNOWN"))
            rec["errors"] = list(getattr(result, "errors", []))
            rec["warnings"] = list(getattr(result, "warnings", []))
            rec["execution_time"] = float(getattr(result, "execution_time", 0.0))
            data = getattr(result, "data", {}) or {}
            rec["points"] = len(data.get("time", [])) if isinstance(data, dict) else 0
        except Exception as exc:
            rec["status"] = "EXCEPTION"
            rec["errors"] = [repr(exc)]

        if rec["ok"]:
            print(f"[PASS] {case_id} ({rec['execution_time']:.3f}s, points={rec['points']})")
        else:
            print(f"[FAIL] {case_id}: {rec['status']}")
            if rec["errors"]:
                print(f"       {rec['errors'][0]}")
        rec["wall_time_s"] = round(time.time() - st, 3)
        all_results.append(rec)

    summary = {
        "total": len(all_results),
        "pass": sum(1 for r in all_results if r["ok"]),
        "fail": sum(1 for r in all_results if not r["ok"]),
        "elapsed_s": round(time.time() - t0, 3),
        "results": all_results,
    }

    out_json = out_root / "summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSummary written: {out_json}")
    print(json.dumps({k: summary[k] for k in ("total", "pass", "fail", "elapsed_s")}, indent=2))
    return 0 if summary["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
