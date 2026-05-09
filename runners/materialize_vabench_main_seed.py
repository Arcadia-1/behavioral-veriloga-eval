#!/usr/bin/env python3
"""Materialize the executable vaBench-main draft packs.

This creates a draft benchmark root that grows in audited batches.  It is not
the full vaBench-main-v1 benchmark until all planned packs pass semantic,
strict-EVAS, and Spectre gold gates.
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmark-balanced" / "tasks"
DEFAULT_OUTPUT = ROOT / "benchmark-vabench-main-v1"
TASK_FORMS = ["bugfix", "spec-to-va", "end-to-end", "tb-generation"]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy_task(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _checker(source_task_id: str) -> str:
    return f'''#!/usr/bin/env python3
from pathlib import Path
import json
import sys

TASK_DIR = Path(__file__).resolve().parent
ROOT = TASK_DIR.parents[2]
sys.path.insert(0, str(ROOT / "runners"))
from simulate_evas import evaluate_behavior  # noqa: E402


def check_csv(csv_path):
    meta = json.loads((TASK_DIR / "meta.json").read_text(encoding="utf-8"))
    source_task_id = meta.get("source_task_id", {source_task_id!r})
    score, notes = evaluate_behavior(source_task_id, Path(csv_path))
    return {{"pass": score >= 1.0, "score": score, "notes": notes}}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _offset_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys

TASK_DIR = Path(__file__).resolve().parent


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _val(row, name):
    return row.get(name.lower(), 0.0)


def check_csv(csv_path):
    rows = _rows(csv_path)
    if len(rows) < 4:
        return {"pass": False, "score": 0.0, "notes": ["too_few_rows"]}

    decisions = []
    prev_clk = _val(rows[0], "CLK")
    for idx, row in enumerate(rows[1:], start=1):
        clk = _val(row, "CLK")
        if prev_clk <= 0.45 and clk > 0.45:
            target_t = _val(row, "time") + 0.15e-9
            sample = min(rows[idx:], key=lambda r: abs(_val(r, "time") - target_t))
            diff = _val(row, "VINP") - _val(row, "VINN")
            out = _val(sample, "OUT_P")
            decisions.append((diff, out))
        prev_clk = clk

    high_ok = any(diff > 1.2e-3 and out > 0.6 for diff, out in decisions)
    low_ok = any(diff < -1.2e-3 and out < 0.3 for diff, out in decisions)
    wrong_high = any(diff > 1.2e-3 and out < 0.3 for diff, out in decisions)
    wrong_low = any(diff < -1.2e-3 and out > 0.6 for diff, out in decisions)
    ok = high_ok and low_ok and not wrong_high and not wrong_low
    notes = [
        f"clock_decisions={len(decisions)}",
        f"high_ok={int(high_ok)}",
        f"low_ok={int(low_ok)}",
    ]
    if wrong_high:
        notes.append("wrong_high_decision")
    if wrong_low:
        notes.append("wrong_low_decision")
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": notes}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _clamp_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _val(row, name):
    return row.get(name.lower(), 0.0)


def check_csv(csv_path):
    rows = _rows(csv_path)
    if len(rows) < 4:
        return {"pass": False, "score": 0.0, "notes": ["too_few_rows"]}
    # Ignore transition edges; sample the settled tail of each PWL plateau.
    probes = [20e-9, 45e-9, 70e-9, 95e-9, 115e-9]
    samples = [min(rows, key=lambda r: abs(_val(r, "time") - t)) for t in probes]
    expected = []
    for row in samples:
        x = _val(row, "raw_level")
        y = min(max(x, 0.18), 0.72)
        expected.append((x, _val(row, "clamped_level"), y))
    errors = [abs(y - ref) for _x, y, ref in expected]
    low_ok = any(x < 0.18 and abs(y - 0.18) < 0.035 for x, y, _ in expected)
    mid_ok = any(0.25 < x < 0.65 and abs(y - x) < 0.04 for x, y, _ in expected)
    high_ok = any(x > 0.72 and abs(y - 0.72) < 0.035 for x, y, _ in expected)
    max_err = max(errors) if errors else 1.0
    ok = low_ok and mid_ok and high_ok and max_err < 0.06
    notes = [
        f"low_clamp_ok={int(low_ok)}",
        f"mid_follow_ok={int(mid_ok)}",
        f"high_clamp_ok={int(high_ok)}",
        f"max_err={max_err:.4g}",
    ]
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": notes}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _strongarm_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


ALIASES = {
    "out_p": ("out_p", "outp", "dcmp_p", "dcmpp"),
    "out_n": ("out_n", "outn", "dcmp_n", "dcmpn"),
    "inp": ("inp", "vinp"),
    "inn": ("inn", "vinn"),
}


def _rows(csv_path):
    rows = []
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            row = {k.lower(): float(v) for k, v in raw.items() if v not in ("", None)}
            for target, names in ALIASES.items():
                if target not in row:
                    for name in names:
                        if name in row:
                            row[target] = row[name]
                            break
            rows.append(row)
    return rows


def _has(row, names):
    return all(name in row for name in names)


def _check_reset_priority(rows):
    required = {"time", "rst", "inp", "inn", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing reset-priority columns"
    threshold = 0.45
    reset_window = [r for r in rows if r["rst"] > threshold]
    active_window = [r for r in rows if r["time"] >= 24e-9 and r["rst"] < threshold]
    if not reset_window or not active_window:
        return False, "insufficient_reset_or_active_window"
    reset_outp_max = max(r["out_p"] for r in reset_window)
    reset_outn_max = max(r["out_n"] for r in reset_window)
    high_rows = [r for r in active_window if r["inp"] > r["inn"] + 5e-3]
    low_rows = [r for r in active_window if r["inp"] + 5e-3 < r["inn"]]
    if not high_rows or not low_rows:
        return False, "missing_post_reset_polarity_windows"
    high_outp = sum(1 for r in high_rows if r["out_p"] > threshold) / len(high_rows)
    high_outn = sum(1 for r in high_rows if r["out_n"] < threshold) / len(high_rows)
    low_outp = sum(1 for r in low_rows if r["out_p"] < threshold) / len(low_rows)
    low_outn = sum(1 for r in low_rows if r["out_n"] > threshold) / len(low_rows)
    ok = reset_outp_max < 0.1 and reset_outn_max < 0.1 and high_outp > 0.75 and high_outn > 0.75 and low_outp > 0.75 and low_outn > 0.75
    return ok, f"reset_outp_max={reset_outp_max:.3f} reset_outn_max={reset_outn_max:.3f} high_outp={high_outp:.3f} high_outn={high_outn:.3f} low_outp={low_outp:.3f} low_outn={low_outn:.3f}"


def _check_clocked_comparator(rows):
    required = {"time", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out_p/out_n"
    threshold = 0.45
    out_p = [r["out_p"] for r in rows]
    out_n = [r["out_n"] for r in rows]
    out_p_span = max(out_p) - min(out_p)
    out_n_span = max(out_n) - min(out_n)
    if out_p_span < threshold or out_n_span < threshold:
        return False, f"insufficient_toggle out_p_span={out_p_span:.3f} out_n_span={out_n_span:.3f}"
    pre = [r["out_p"] for r in rows if 0.6e-9 < r["time"] < 2.0e-9]
    post = [r["out_p"] for r in rows if 2.5e-9 < r["time"] < 4.0e-9]
    if not pre or not post:
        return False, "insufficient_polarity_windows"
    pre_high_frac = sum(1 for v in pre if v > threshold) / len(pre)
    post_low_frac = sum(1 for v in post if v < threshold) / len(post)
    ok = pre_high_frac >= 0.4 and post_low_frac >= 0.4
    return ok, f"pre_high_frac={pre_high_frac:.3f} post_low_frac={post_low_frac:.3f}"


def check_csv(csv_path):
    rows = _rows(csv_path)
    if not rows:
        return {"pass": False, "score": 0.0, "notes": ["empty_csv"]}
    if _has(rows[0], {"rst", "inp", "inn", "out_p", "out_n"}):
        ok, note = _check_reset_priority(rows)
    else:
        ok, note = _check_clocked_comparator(rows)
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": [note]}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _pfd_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _weighted_high_fraction(rows, col, threshold):
    high_dt = 0.0
    total_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        total_dt += dt
        if 0.5 * (rows[idx - 1][col] + rows[idx][col]) > threshold:
            high_dt += dt
    return high_dt / max(total_dt, 1e-18)


def _rising_edges(rows, col, threshold):
    edges = []
    prev = rows[0][col]
    for row in rows[1:]:
        cur = row[col]
        if prev < threshold <= cur:
            edges.append(row["time"])
        prev = cur
    return edges


def _window(rows, start, end):
    return [r for r in rows if start <= r["time"] <= end]


def check_csv(csv_path):
    rows = _rows(csv_path)
    required = {"time", "ref", "div", "up", "dn"}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing time/ref/div/up/dn"]}
    vth = max(r["ref"] for r in rows) * 0.5
    first = _window(rows, 20e-9, 120e-9)
    second = _window(rows, 160e-9, 260e-9)
    if len(first) < 4 or len(second) < 4:
        return {"pass": False, "score": 0.0, "notes": ["insufficient_window_samples"]}
    up_first = _weighted_high_fraction(first, "up", vth)
    dn_first = _weighted_high_fraction(first, "dn", vth)
    up_second = _weighted_high_fraction(second, "up", vth)
    dn_second = _weighted_high_fraction(second, "dn", vth)
    up_pulses_first = len(_rising_edges(first, "up", vth))
    dn_pulses_second = len(_rising_edges(second, "dn", vth))
    overlap_dt = 0.0
    total_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        total_dt += dt
        up_mid = 0.5 * (rows[idx - 1]["up"] + rows[idx]["up"])
        dn_mid = 0.5 * (rows[idx - 1]["dn"] + rows[idx]["dn"])
        if up_mid > vth and dn_mid > vth:
            overlap_dt += dt
    overlap_frac = overlap_dt / max(total_dt, 1e-18)
    ok = (
        0.001 <= up_first <= 0.08
        and dn_first <= 0.01
        and 0.001 <= dn_second <= 0.08
        and up_second <= 0.01
        and up_pulses_first >= 4
        and dn_pulses_second >= 4
        and overlap_frac <= 0.01
    )
    note = (
        f"up_first={up_first:.4f} dn_first={dn_first:.4f} "
        f"up_second={up_second:.4f} dn_second={dn_second:.4f} "
        f"up_pulses_first={up_pulses_first} dn_pulses_second={dn_pulses_second} "
        f"overlap_frac={overlap_frac:.4f}"
    )
    return {"pass": ok, "score": 1.0 if ok else 0.0, "notes": [note]}


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _sample_hold_aperture_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _nearest(rows, t):
    return min(rows, key=lambda r: abs(r["time"] - t))


def check_csv(csv_path):
    rows = _rows(csv_path)
    required = {"time", "vin", "clk", "vout"}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing time/vin/clk/vout"]}
    vth = 0.45
    edges = []
    for i in range(1, len(rows)):
        if rows[i - 1]["clk"] <= vth < rows[i]["clk"]:
            edges.append(rows[i]["time"])
    if len(edges) < 5:
        return {"pass": False, "score": 0.0, "notes": [f"too_few_edges={len(edges)}"]}
    mismatches = 0
    checked = 0
    taperture = 200e-12
    settle = 1.0e-9
    for edge_t in edges[:6]:
        vin_sample = _nearest(rows, edge_t + taperture)["vin"]
        vout_settled = _nearest(rows, edge_t + taperture + settle)["vout"]
        checked += 1
        if abs(vout_settled - vin_sample) > 0.045:
            mismatches += 1
    hold_failures = 0
    for a, b in zip(edges[:4], edges[1:5]):
        window = [r["vout"] for r in rows if a + 2e-9 <= r["time"] <= b - 2e-9]
        if len(window) >= 2 and max(window) - min(window) > 0.04:
            hold_failures += 1
    ok = checked >= 5 and mismatches <= 1 and hold_failures == 0
    return {
        "pass": ok,
        "score": 1.0 if ok else 0.0,
        "notes": [f"edges={len(edges)} checked={checked} mismatches={mismatches} hold_failures={hold_failures}"],
    }


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _clock_divider_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _rising_edges(rows, col, threshold=0.45):
    edges = []
    for i in range(1, len(rows)):
        if rows[i - 1][col] < threshold <= rows[i][col]:
            edges.append(rows[i]["time"])
    return edges


def check_csv(csv_path):
    rows = _rows(csv_path)
    required = {"time", "clk_in", "clk_out", "lock"} | {f"div_code_{i}" for i in range(8)}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing clk/divider columns"]}
    ratio = sum((1 << i) if rows[0][f"div_code_{i}"] > 0.45 else 0 for i in range(8)) or 1
    in_edges = _rising_edges(rows, "clk_in")
    out_edges = _rising_edges(rows, "clk_out")
    if len(in_edges) < max(12, ratio * 2) or len(out_edges) < 3:
        return {"pass": False, "score": 0.0, "notes": [f"not_enough_edges ratio={ratio} in={len(in_edges)} out={len(out_edges)}"]}
    intervals = []
    for a, b in zip(out_edges, out_edges[1:]):
        intervals.append(sum(1 for t in in_edges if a < t <= b))
    measured = intervals[1:] if len(intervals) > 2 else intervals
    mismatch = [n for n in measured if n != ratio]
    final_lock_high = rows[-1]["lock"] > 0.45
    high_seen = any(r["clk_out"] > 0.45 for r in rows)
    low_seen = any(r["clk_out"] <= 0.45 for r in rows)
    ok = not mismatch and final_lock_high and high_seen and low_seen
    return {
        "pass": ok,
        "score": 1.0 if ok else 0.0,
        "notes": [f"ratio={ratio} in_edges={len(in_edges)} out_edges={len(out_edges)} intervals={measured} lock={int(final_lock_high)}"],
    }


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _sar4_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys


def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]


def _rising_edges(rows, col, threshold=0.45):
    edges = []
    for i in range(1, len(rows)):
        if rows[i - 1][col] < threshold <= rows[i][col]:
            edges.append(rows[i]["time"])
    return edges


def check_csv(csv_path):
    rows = _rows(csv_path)
    required = {"time", "rdy", "dp_dac_3", "dp_dac_0"}
    if not rows or not required.issubset(rows[0]):
        return {"pass": False, "score": 0.0, "notes": ["missing rdy/dp_dac_3/dp_dac_0"]}
    rdy_edges = _rising_edges(rows, "rdy")
    bit_activity = {}
    for bit in range(4):
        col = f"dp_dac_{bit}"
        if col not in rows[0]:
            return {"pass": False, "score": 0.0, "notes": [f"missing {col}"]}
        vals = [r[col] for r in rows]
        bit_activity[col] = max(vals) - min(vals)
    active_bits = sum(1 for span in bit_activity.values() if span > 0.4)
    ok = len(rdy_edges) >= 3 and active_bits >= 2
    return {
        "pass": ok,
        "score": 1.0 if ok else 0.0,
        "notes": [f"rdy_edges={len(rdy_edges)} active_bits={active_bits} spans={bit_activity}"],
    }


if __name__ == "__main__":
    print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _update_meta(task_dir: Path, *, task_id: str, pack_id: str, form: str, source_task_id: str, source_root: str) -> dict[str, Any]:
    meta = _read_json(task_dir / "meta.json")
    meta.update(
        {
            "benchmark": "vaBench-main-v1",
            "benchmark_split": "benchmark-vabench-main-v1",
            "task_id": task_id,
            "family": form,
            "task_form": form,
            "pack_id": pack_id,
            "pack_version": "v1",
            "circuit_function_id": pack_id,
            "source_benchmark": "benchmark-balanced",
            "source_task_id": source_task_id,
            "source_task_form": meta.get("task_form") or meta.get("family"),
            "source_seed_task_id": source_root,
            "promotion_status": "vabench_main_seed_needs_semantic_audit_and_gold_validation",
            "scoring": ["dut_compile", "tb_compile", "sim_correct"] if form != "tb-generation" else ["tb_compile", "sim_correct"],
        }
    )
    if pack_id == "strongarm_comparator_behavior":
        meta["core_function"] = "threshold/static nonlinear"
        meta["category"] = "comparator"
    elif pack_id == "pfd_reset_race":
        meta["core_function"] = "event/timing"
        meta["category"] = "phase-detector"
    elif pack_id == "offset_comparator":
        meta["core_function"] = "threshold/static nonlinear"
        meta["category"] = "comparator"
    elif pack_id == "voltage_clamp":
        meta["core_function"] = "threshold/static nonlinear"
        meta["category"] = "voltage-clamp"
    elif pack_id == "track_hold_aperture":
        meta["core_function"] = "stateful analog memory"
        meta["category"] = "sample-hold"
    elif pack_id == "resettable_counter_divider":
        meta["core_function"] = "event/timing"
        meta["category"] = "clock-divider"
    elif pack_id == "sar_logic_4b":
        meta["core_function"] = "data conversion"
        meta["category"] = "sar-logic"
    elif pack_id == "one_shot_timer":
        meta["core_function"] = "event/timing"
        meta["category"] = "one-shot-timer"
    elif pack_id == "thermometer_dac":
        meta["core_function"] = "data conversion"
        meta["category"] = "dac"
    elif pack_id == "lock_detector":
        meta["core_function"] = "calibration/control"
        meta["category"] = "lock-detector"
    elif pack_id == "resettable_integrator":
        meta["core_function"] = "continuous dynamics"
        meta["category"] = "integrator"
    elif pack_id in EXTRA_PACK_SPECS:
        meta["core_function"] = EXTRA_PACK_SPECS[pack_id]["family"]
        meta["category"] = EXTRA_PACK_SPECS[pack_id]["category"]
    _write_json(task_dir / "meta.json", meta)
    return meta


def _write_prompt(task_dir: Path, prompt: str) -> None:
    (task_dir / "prompt.md").write_text(prompt.strip() + "\n", encoding="utf-8")


def _strongarm_prompts() -> dict[str, str]:
    source_e2e = (SOURCE / "original92_cmp_strongarm_smoke" / "prompt.md").read_text(encoding="utf-8")
    source_bug = (SOURCE / "original92_strongarm_reset_priority_bug" / "prompt.md").read_text(encoding="utf-8")
    dut = """Create only the DUT Verilog-A model for the `strongarm_comparator_behavior` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `cmp_strongarm`.
Ports, all `electrical`, exactly as named and ordered:
`CLK`, `VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, `VDD`.

Behavior:
- Detect the rising edge of `CLK`.
- When `VINP > VINN`, drive `DCMPP` high and `DCMPN` low.
- When `VINP < VINN`, drive `DCMPP` low and `DCMPN` high.
- Clear or deassert the decision outputs on the falling clock edge.
- Use voltage-domain contributions and `transition(...)`; do not use current contributions.

Public evaluation contract:
- The fixed harness runs `tran tran stop=4n maxstep=5p`.
- Public waveform columns include `clk`, `vinp`, `vinn`, `out_p`, `out_n`.

Return exactly one complete Verilog-A code block for `cmp_strongarm.va`.
"""
    tb = """Given a voltage-domain StrongARM-style comparator DUT, generate a minimal Spectre-format testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `cmp_strongarm.va`
- Module name: `cmp_strongarm`
- Positional port order: `(CLK VINN VINP DCMPN DCMPP LP LM VSS VDD)`

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide a 0.9 V supply and 0 V reference.
- Generate a clock near 1 GHz.
- Drive `vinp` and `vinn` so the input polarity changes during the run.
- Instantiate the DUT by positional ports.
- Save plain scalar names: `clk`, `vinp`, `vinn`, `out_p`, `out_n`.
- Run exactly `tran tran stop=4n maxstep=5p`.
- Include `cmp_strongarm.va` using `ahdl_include`.

Return exactly one fenced `spectre` code block.
"""
    return {"bugfix": source_bug, "spec-to-va": dut, "end-to-end": source_e2e, "tb-generation": tb}


def _pfd_prompts() -> dict[str, str]:
    source_e2e = (SOURCE / "original92_pfd_reset_race_smoke" / "prompt.md").read_text(encoding="utf-8")
    buggy = """`include "constants.vams"
`include "disciplines.vams"

module pfd_updn(VDD, VSS, REF, DIV, UP, DN);
    inout VDD, VSS;
    input REF, DIV;
    output UP, DN;
    electrical VDD, VSS, REF, DIV, UP, DN;
    parameter real vth = 0.45;
    parameter real tedge = 20p;
    integer up_state, dn_state;
    analog begin
        @(initial_step) begin
            up_state = 0;
            dn_state = 0;
        end
        @(cross(V(REF) - vth, +1)) up_state = 1;
        @(cross(V(DIV) - vth, +1)) dn_state = 1;
        V(UP) <+ transition(up_state ? V(VDD) : V(VSS), 0, tedge, tedge);
        V(DN) <+ transition(dn_state ? V(VDD) : V(VSS), 0, tedge, tedge);
    end
endmodule
"""
    bugfix = f"""The following pure voltage-domain PFD has a reset-race bug: when both `UP` and `DN` become high, the implementation does not promptly reset both states.  Fix it without changing the public module name or ports.

```verilog-a
{buggy}
```

Required behavior:
- Rising edge of `REF` asserts `UP`.
- Rising edge of `DIV` asserts `DN`.
- If both states become high, reset both outputs promptly to avoid overlap.
- Use `@(cross(...))` and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=300n maxstep=10p errpreset=conservative`.
- Public waveform columns are `ref`, `div`, `up`, and `dn`.

Return exactly one complete Verilog-A code block for module `pfd_updn`.
"""
    dut = """Create only the DUT Verilog-A model for the `pfd_reset_race` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `pfd_updn`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`.

Behavior:
- Rising edge of `REF` asserts `UP`.
- Rising edge of `DIV` asserts `DN`.
- If both states become high, reset both outputs promptly so `UP` and `DN` do not significantly overlap.
- Use `@(cross(...))` and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=300n maxstep=10p errpreset=conservative`.
- Public waveform columns are `ref`, `div`, `up`, and `dn`.

Return exactly one complete Verilog-A code block for `pfd_updn.va`.
"""
    tb = """Given a pure voltage-domain PFD DUT, generate a minimal Spectre-format testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `pfd_updn.va`
- Module name: `pfd_updn`
- Positional port order: `(VDD VSS REF DIV UP DN)`

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide 0.9 V `vdd` and 0 V `vss`.
- Drive `ref` and `div` with rising edges whose lead/lag relationship swaps during the transient.
- Instantiate the DUT by positional ports.
- Save plain scalar names: `ref`, `div`, `up`, `dn`.
- Run exactly `tran tran stop=300n maxstep=10p errpreset=conservative`.
- Include `pfd_updn.va` using `ahdl_include`.

Return exactly one fenced `spectre` code block.
"""
    return {"bugfix": bugfix, "spec-to-va": dut, "end-to-end": source_e2e, "tb-generation": tb}


def _offset_comparator_prompts() -> dict[str, str]:
    tb = (SOURCE / "original92_comparator_offset_tb" / "prompt.md").read_text(encoding="utf-8")
    buggy = """`include "constants.vams"
`include "disciplines.vams"

module cmp_offset_ref(VDD, VSS, CLK, VINP, VINN, OUT_P);
    inout VDD, VSS;
    input CLK, VINP, VINN;
    output OUT_P;
    electrical VDD, VSS, CLK, VINP, VINN, OUT_P;
    parameter real vos = 1m;
    parameter real tt = 20p;
    integer q;
    analog begin
        @(initial_step) q = 0;
        @(cross(V(CLK, VSS) - 0.45, +1)) begin
            q = (V(VINP, VSS) > V(VINN, VSS)) ? 1 : 0;
        end
        V(OUT_P, VSS) <+ V(VDD, VSS) * transition(q ? 1.0 : 0.0, 0, tt, tt);
    end
endmodule
"""
    bugfix = f"""The following clocked voltage comparator has an offset bug: it ignores the public input offset parameter `vos`.
Fix the behavior without changing the public module name or port list.

```verilog-a
{buggy}
```

Required module: `cmp_offset_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

Behavior:
- On each rising edge of `CLK`, compare `VINP - VINN` against `vos`.
- Drive `OUT_P` high only when `VINP - VINN > vos`; otherwise drive it low.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=28n maxstep=20p`.
- Public waveform columns are `CLK`, `VINP`, `VINN`, and `OUT_P`.

Return exactly one complete Verilog-A code block for module `cmp_offset_ref`.
"""
    dut = """Create only the DUT Verilog-A model for the `offset_comparator` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `cmp_offset_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

Behavior:
- On each rising edge of `CLK`, compare `VINP - VINN` against the public real parameter `vos`.
- Drive `OUT_P` high only when `VINP - VINN > vos`; otherwise drive it low.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=28n maxstep=20p`.
- Public waveform columns are `CLK`, `VINP`, `VINN`, and `OUT_P`.

Return exactly one complete Verilog-A code block for `cmp_offset_ref.va`.
"""
    e2e = """Write a pure Verilog-A offset comparator DUT and a minimal Spectre testbench.

Required DUT module: `cmp_offset_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

DUT behavior:
- On each rising edge of `CLK`, compare `VINP - VINN` against the public real parameter `vos`.
- Drive `OUT_P` high only when `VINP - VINN > vos`; otherwise drive it low.
- Use voltage-domain contributions and `transition(...)`.

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide `VDD=0.9 V` and `VSS=0 V`.
- Drive `CLK` with repeated rising edges.
- Drive `VINP` and `VINN` so both below-offset and above-offset decisions occur.
- Instantiate the DUT by positional ports.
- Save plain scalar names: `CLK`, `VINP`, `VINN`, `OUT_P`.
- Run exactly `tran tran stop=28n maxstep=20p`.
- Include `cmp_offset_ref.va` using `ahdl_include`.

Return two fenced code blocks: one `verilog-a` block for `cmp_offset_ref.va` and one `spectre` block for the testbench.
"""
    return {"bugfix": bugfix, "spec-to-va": dut, "end-to-end": e2e, "tb-generation": tb}


def _voltage_clamp_prompts() -> dict[str, str]:
    bug = """`include "constants.vams"
`include "disciplines.vams"

module voltage_clamp(raw_level, vdd, vss, clamped_level);
    input raw_level, vdd, vss;
    output clamped_level;
    electrical raw_level, vdd, vss, clamped_level;
    parameter real vlo = 0.18;
    parameter real vhi = 0.72;
    parameter real tr = 40p;
    analog begin
        V(clamped_level) <+ transition(V(raw_level), 0.0, tr, tr);
    end
endmodule
"""
    shared = """Core function: voltage clamp.
Behavioral intent: model a bounded analog transfer that follows the input in the middle range and clamps outside public lower/upper limits.

Public interface:
- Module name: `voltage_clamp`.
- Inputs: `raw_level`, `vdd`, `vss`.
- Output: `clamped_level`.
- Public real parameters: `vlo=0.18`, `vhi=0.72`, `tr=40p`.

Compatibility requirements:
- Use voltage-domain electrical ports only.
- Be compatible with real Cadence Spectre.
- Declare port direction and electrical discipline separately.
- Drive output targets with `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The checker reads public waveform columns `raw_level` and `clamped_level`.
- The fixed testbench exercises below-limit, in-range, and above-limit input regions.
- The fixed harness runs exactly `tran tran stop=120n maxstep=500p`.
"""
    bugfix = f"""The following Verilog-A module named `voltage_clamp` has a behavioral bug: it is an unconstrained follower and does not clamp.
Fix it without changing the public interface.

```verilog-a
{bug}
```

{shared}

Return exactly one fixed Verilog-A file named `dut.va`.
"""
    dut = f"""Write only the pure Verilog-A DUT module named `voltage_clamp`.
Do not include a testbench. The evaluator will use a fixed public harness.

{shared}

Return exactly one complete Verilog-A code block for `dut.va`.
"""
    e2e = f"""Write a pure Verilog-A module named `voltage_clamp` and a minimal Spectre testbench.
Return two files: `dut.va` and `tb_ref.scs`.

{shared}

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Include `dut.va` with `ahdl_include`.
- Instantiate `voltage_clamp` by positional ports: `(raw_level vdd vss clamped_level)`.
- Drive `raw_level` through below-limit, in-range, and above-limit plateaus.
- Save plain scalar names: `raw_level`, `clamped_level`.
- Run exactly `tran tran stop=120n maxstep=500p`.
"""
    tb = f"""Given a voltage-domain DUT module named `voltage_clamp`, generate only a Spectre testbench.
Do not generate Verilog-A modules.

The DUT file will be available as `dut.va`; include it with `ahdl_include "dut.va"` and instantiate by positional ports.

{shared}

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide 0.9 V `vdd` and 0 V `vss`.
- Drive `raw_level` through below-limit, in-range, and above-limit plateaus.
- Instantiate as `XDUT (raw_level vdd vss clamped_level) voltage_clamp`.
- Save plain scalar names: `raw_level`, `clamped_level`.
- Run exactly `tran tran stop=120n maxstep=500p`.

Return exactly one fenced `spectre` code block.
"""
    return {"bugfix": bugfix, "spec-to-va": dut, "end-to-end": e2e, "tb-generation": tb}


def _voltage_clamp_va() -> str:
    return """`include "constants.vams"
`include "disciplines.vams"

module voltage_clamp(raw_level, vdd, vss, clamped_level);
    input raw_level, vdd, vss;
    output clamped_level;
    electrical raw_level, vdd, vss, clamped_level;
    parameter real vlo = 0.18;
    parameter real vhi = 0.72;
    parameter real tr = 40p;
    real y;

    analog begin
        y = V(raw_level);
        if (y < vlo) y = vlo;
        if (y > vhi) y = vhi;
        V(clamped_level) <+ transition(y, 0.0, tr, tr);
    end
endmodule
"""


def _voltage_clamp_tb() -> str:
    return """simulator lang=spectre
global 0

ahdl_include "dut.va"

Vvdd (vdd 0) vsource dc=0.9
Vvss (vss 0) vsource dc=0
Vsig (raw_level 0) vsource type=pwl wave=[ 0 0.0 25n 0.1 50n 0.45 75n 0.85 100n 0.9 120n 0.35 ]

XDUT (raw_level vdd vss clamped_level) voltage_clamp

tran tran stop=120n maxstep=500p
save raw_level clamped_level
"""


def _track_hold_aperture_prompts() -> dict[str, str]:
    tb = (SOURCE / "original92_sample_hold_aperture_tb" / "prompt.md").read_text(encoding="utf-8")
    buggy = """`include "constants.vams"
`include "disciplines.vams"

module sample_hold_aperture_ref(VDD, VSS, clk, vin, vout);
    inout VDD, VSS;
    input clk, vin;
    output vout;
    electrical VDD, VSS, clk, vin, vout;
    parameter real vth = 0.45;
    parameter real taperture = 200p;
    parameter real tedge = 50p;
    real sampled;
    analog begin
        @(initial_step) sampled = V(vin);
        @(cross(V(clk) - vth, +1)) sampled = V(vin);
        V(vout) <+ transition(sampled, 0.0, tedge, tedge);
    end
endmodule
"""
    bugfix = f"""The following sample-and-hold module ignores the required aperture delay and samples immediately at the clock edge.
Fix it without changing the public module name or ports.

```verilog-a
{buggy}
```

Required module: `sample_hold_aperture_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `clk`, `vin`, `vout`.

Behavior:
- On each rising edge of `clk`, arm a sample event at `$abstime + taperture`.
- At that aperture event, capture `vin` and hold it on `vout` until the next capture.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=140n maxstep=100p`.
- Public waveform columns are `vin`, `clk`, and `vout`.

Return exactly one complete Verilog-A code block for module `sample_hold_aperture_ref`.
"""
    dut = """Create only the DUT Verilog-A model for the `track_hold_aperture` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `sample_hold_aperture_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `clk`, `vin`, `vout`.

Behavior:
- On each rising edge of `clk`, arm a sample event at `$abstime + taperture`.
- At that aperture event, capture `vin` and hold it on `vout` until the next capture.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=140n maxstep=100p`.
- Public waveform columns are `vin`, `clk`, and `vout`.

Return exactly one complete Verilog-A code block for `sample_hold_aperture_ref.va`.
"""
    e2e = """Write a pure Verilog-A sample-and-hold DUT with aperture delay and a minimal Spectre testbench.

Required DUT module: `sample_hold_aperture_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `clk`, `vin`, `vout`.

DUT behavior:
- On each rising edge of `clk`, arm a sample event at `$abstime + taperture`.
- At that aperture event, capture `vin` and hold it on `vout` until the next capture.
- Use voltage-domain contributions and `transition(...)`.

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide `VDD=0.9 V` and `VSS=0 V`.
- Drive `clk` with repeated rising edges.
- Drive `vin` with changing plateaus so aperture timing can be observed.
- Save plain scalar names: `vin`, `clk`, `vout`.
- Run exactly `tran tran stop=140n maxstep=100p`.
- Include `sample_hold_aperture_ref.va` using `ahdl_include`.

Return two fenced code blocks: one `verilog-a` block and one `spectre` block.
"""
    return {"bugfix": bugfix, "spec-to-va": dut, "end-to-end": e2e, "tb-generation": tb}


def _resettable_counter_divider_prompts() -> dict[str, str]:
    source = (SOURCE / "original92_clk_divider" / "prompt.md").read_text(encoding="utf-8")
    buggy = """`include "constants.vams"
`include "disciplines.vams"

module clk_divider_ref(clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock);
    input clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7;
    output clk_out, lock;
    electrical clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock;
    parameter real vdd = 0.9;
    parameter real vth = 0.45;
    parameter real trf = 10p;
    integer out_state;
    analog begin
        @(initial_step) out_state = 0;
        @(cross(V(clk_in) - vth, +1)) out_state = !out_state;
        V(clk_out) <+ transition(out_state ? vdd : 0.0, 0, trf, trf);
        V(lock) <+ transition(vdd, 0, trf, trf);
    end
endmodule
"""
    bugfix = f"""The following clock divider ignores the public division code and reset behavior.
Fix it without changing the public module name or ports.

```verilog-a
{buggy}
```

Required module: `clk_divider_ref`.
Ports, all `electrical`, exactly as named and ordered:
`clk_in`, `rst_n`, `div_code_0` ... `div_code_7`, `clk_out`, `lock`.

Behavior:
- Interpret the eight `div_code_*` inputs as an unsigned division ratio, clamped to at least 1.
- Synchronous active-low reset clears internal count, output state, and `lock`.
- Generate a divided `clk_out` whose edge intervals match the public ratio.
- Assert `lock` after the first complete output period.
- Use voltage-domain contributions and `transition(...)`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=80n maxstep=50p`.
- Public waveform columns include `clk_in`, `rst_n`, `clk_out`, `lock`, and `div_code_0` through `div_code_7`.

Return exactly one complete Verilog-A code block for module `clk_divider_ref`.
"""
    dut = source.replace("Write a programmable clock divider.", "Create only the DUT Verilog-A model for the `resettable_counter_divider` circuit function. Do not generate a testbench.")
    e2e = """Write a programmable resettable clock divider DUT and a minimal Spectre testbench.

Required DUT module: `clk_divider_ref`.
Ports, all `electrical`, exactly as named and ordered:
`clk_in`, `rst_n`, `div_code_0` ... `div_code_7`, `clk_out`, `lock`.

DUT behavior:
- Interpret the eight `div_code_*` inputs as an unsigned division ratio, clamped to at least 1.
- Synchronous active-low reset clears internal count, output state, and `lock`.
- Generate a divided `clk_out` whose edge intervals match the public ratio.
- Assert `lock` after the first complete output period.
- Use voltage-domain contributions and `transition(...)`.

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Drive `clk_in` with a 1 ns period clock.
- Release `rst_n` after startup and keep it high.
- Set the public ratio to 5 using `div_code_0=1` and `div_code_2=1`.
- Save plain scalar names: `clk_in`, `rst_n`, `clk_out`, `lock`, and all `div_code_*` bits.
- Run exactly `tran tran stop=80n maxstep=50p`.

Return two fenced code blocks: one `verilog-a` block and one `spectre` block.
"""
    tb = """Given a voltage-domain programmable divider DUT, generate only a Spectre testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `clk_divider_ref.va`
- Module name: `clk_divider_ref`
- Positional port order: `(clk_in rst_n div_code_0 div_code_1 div_code_2 div_code_3 div_code_4 div_code_5 div_code_6 div_code_7 clk_out lock)`

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Include `clk_divider_ref.va` using `ahdl_include`.
- Drive `clk_in` with a 1 ns period clock.
- Release active-low `rst_n` after startup and keep it high.
- Set ratio code 5.
- Save plain scalar names: `clk_in`, `rst_n`, `clk_out`, `lock`, and all `div_code_*` bits.
- Run exactly `tran tran stop=80n maxstep=50p`.

Return exactly one fenced `spectre` code block.
"""
    return {"bugfix": bugfix, "spec-to-va": dut, "end-to-end": e2e, "tb-generation": tb}


def _sar_logic_4b_prompts() -> dict[str, str]:
    shared = """Required module: `sar_logic_4b`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLKS`, `DCOMP`, `DP_DAC_3`, `DP_DAC_2`, `DP_DAC_1`, `DP_DAC_0`, `RDY`.

Behavior:
- Implement a 4-bit SAR control sequence driven by rising edges of `CLKS`.
- Start each conversion by asserting the MSB trial bit.
- On each bit phase, keep or clear the current trial bit from `DCOMP`, then assert the next lower trial bit.
- After four bit decisions, assert `RDY` for one cycle and then start a new conversion.
- Drive all outputs with voltage-domain `transition(...)`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=1.2u maxstep=2n`.
- Public waveform columns include `rdy`, `dp_dac_3`, `dp_dac_2`, `dp_dac_1`, and `dp_dac_0`.
"""
    bug = """`include "constants.vams"
`include "disciplines.vams"

module sar_logic_4b(VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY);
    inout VDD, VSS;
    input CLKS, DCOMP;
    output DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY;
    electrical VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY;
    analog begin
        V(DP_DAC_3) <+ transition(V(DCOMP), 0, 1n, 1n);
        V(DP_DAC_2) <+ 0;
        V(DP_DAC_1) <+ 0;
        V(DP_DAC_0) <+ 0;
        V(RDY) <+ 0;
    end
endmodule
"""
    bugfix = f"""The following module is not a SAR sequencer; it only mirrors `DCOMP` onto one output.
Fix it without changing the public module name or ports.

```verilog-a
{bug}
```

{shared}

Return exactly one complete Verilog-A code block for module `sar_logic_4b`.
"""
    dut = f"""Create only the DUT Verilog-A model for the `sar_logic_4b` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

{shared}

Return exactly one complete Verilog-A code block for `sar_logic_4b.va`.
"""
    e2e = f"""Write a pure Verilog-A 4-bit SAR logic DUT and a minimal Spectre testbench.

{shared}

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide 0.9 V `VDD` and 0 V `VSS`.
- Drive `CLKS` with a 50 ns period clock.
- Drive `DCOMP` with a repeating waveform so both keep and reject decisions occur.
- Instantiate the DUT by positional ports.
- Save plain scalar names: `rdy`, `dp_dac_3`, `dp_dac_2`, `dp_dac_1`, and `dp_dac_0`.
- Run exactly `tran tran stop=1.2u maxstep=2n`.

Return two fenced code blocks: one `verilog-a` block and one `spectre` block.
"""
    tb = f"""Given a voltage-domain 4-bit SAR logic DUT, generate only a Spectre testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `sar_logic_4b.va`
- Module name: `sar_logic_4b`
- Positional port order: `(VDD VSS CLKS DCOMP DP_DAC_3 DP_DAC_2 DP_DAC_1 DP_DAC_0 RDY)`

{shared}

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Include `sar_logic_4b.va` using `ahdl_include`.
- Provide 0.9 V `VDD` and 0 V `VSS`.
- Drive `CLKS` with a 50 ns period clock.
- Drive `DCOMP` with a repeating waveform so both keep and reject decisions occur.
- Save plain scalar names: `rdy`, `dp_dac_3`, `dp_dac_2`, `dp_dac_1`, and `dp_dac_0`.
- Run exactly `tran tran stop=1.2u maxstep=2n`.

Return exactly one fenced `spectre` code block.
"""
    return {"bugfix": bugfix, "spec-to-va": dut, "end-to-end": e2e, "tb-generation": tb}


def _sar4_va() -> str:
    return """`include "constants.vams"
`include "disciplines.vams"

module sar_logic_4b(VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY);
    inout VDD, VSS;
    input CLKS, DCOMP;
    output DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY;
    electrical VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY;

    parameter real vth = 0.45;
    parameter real tedge = 1n;
    integer state;
    integer b3, b2, b1, b0;
    real rdy;

    analog begin
        @(initial_step) begin
            state = 0;
            b3 = 1;
            b2 = 0;
            b1 = 0;
            b0 = 0;
            rdy = 0.0;
        end

        @(cross(V(CLKS) - vth, +1)) begin
            if (state == 0) begin
                if (V(DCOMP) < vth) b3 = 0;
                b2 = 1;
                state = 1;
                rdy = 0.0;
            end else if (state == 1) begin
                if (V(DCOMP) < vth) b2 = 0;
                b1 = 1;
                state = 2;
            end else if (state == 2) begin
                if (V(DCOMP) < vth) b1 = 0;
                b0 = 1;
                state = 3;
            end else if (state == 3) begin
                if (V(DCOMP) < vth) b0 = 0;
                rdy = V(VDD, VSS);
                state = 4;
            end else begin
                b3 = 1;
                b2 = 0;
                b1 = 0;
                b0 = 0;
                rdy = 0.0;
                state = 0;
            end
        end

        V(DP_DAC_3, VSS) <+ transition(b3 ? V(VDD, VSS) : 0.0, 0, tedge, tedge);
        V(DP_DAC_2, VSS) <+ transition(b2 ? V(VDD, VSS) : 0.0, 0, tedge, tedge);
        V(DP_DAC_1, VSS) <+ transition(b1 ? V(VDD, VSS) : 0.0, 0, tedge, tedge);
        V(DP_DAC_0, VSS) <+ transition(b0 ? V(VDD, VSS) : 0.0, 0, tedge, tedge);
        V(RDY, VSS)      <+ transition(rdy, 0, tedge, tedge);
    end
endmodule
"""


def _sar4_tb() -> str:
    return """simulator lang=spectre
global 0

ahdl_include "sar_logic_4b.va"

Vvdd  (vdd 0) vsource dc=0.9
Vvss  (vss 0) vsource dc=0.0
Vclks (clks 0) vsource type=pulse val0=0 val1=0.9 period=50n width=25n rise=1n fall=1n
Vdcomp (dcomp 0) vsource type=pulse val0=0 val1=0.9 period=180n width=95n rise=1n fall=1n delay=20n

IDUT (vdd vss clks dcomp dp_dac_3 dp_dac_2 dp_dac_1 dp_dac_0 rdy) sar_logic_4b

tran tran stop=1.2u maxstep=2n
save rdy dp_dac_3 dp_dac_2 dp_dac_1 dp_dac_0
"""

def _edge_pulse_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def _rising(rows, col, th=0.45):
    return [rows[i]["time"] for i in range(1, len(rows)) if rows[i-1][col] < th <= rows[i][col]]

def _high_frac(rows, col, th=0.45):
    hi=tot=0.0
    for i in range(1,len(rows)):
        dt=rows[i]["time"]-rows[i-1]["time"]
        if dt<=0: continue
        tot += dt
        if 0.5*(rows[i][col]+rows[i-1][col])>th: hi += dt
    return hi/max(tot,1e-18)

def check_csv(csv_path):
    rows=_rows(csv_path)
    req={"time","trig","pulse"}
    if not rows or not req.issubset(rows[0]):
        return {"pass":False,"score":0.0,"notes":["missing time/trig/pulse"]}
    trig_edges=len(_rising(rows,"trig")); pulse_edges=len(_rising(rows,"pulse")); frac=_high_frac(rows,"pulse")
    ok=trig_edges>=4 and pulse_edges>=4 and 0.015<=frac<=0.16
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"trig_edges={trig_edges} pulse_edges={pulse_edges} pulse_frac={frac:.4f}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _thermometer_dac_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def _nearest(rows,t): return min(rows, key=lambda r: abs(r["time"]-t))

def check_csv(csv_path):
    rows=_rows(csv_path)
    req={"time","aout"}|{f"code_{i}" for i in range(4)}
    if not rows or not req.issubset(rows[0]): return {"pass":False,"score":0.0,"notes":["missing code/aout"]}
    vals=[]
    for idx,t in enumerate([10e-9,30e-9,50e-9,70e-9,90e-9,110e-9,130e-9,150e-9]):
        r=_nearest(rows,t)
        code=sum((1<<i) if r[f"code_{i}"]>0.45 else 0 for i in range(4))
        vals.append((code,r["aout"]))
    ordered=sorted(vals)
    mono=all(ordered[i][1] <= ordered[i+1][1]+0.04 for i in range(len(ordered)-1))
    span=max(v for _,v in vals)-min(v for _,v in vals)
    err=max(abs(v-0.9*code/15.0) for code,v in vals)
    ok=mono and span>0.65 and err<0.08
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"samples={vals} span={span:.3f} max_err={err:.3f} mono={mono}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _lock_detector_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def check_csv(csv_path):
    rows=_rows(csv_path)
    if not rows or not {"time","lock"}.issubset(rows[0]): return {"pass":False,"score":0.0,"notes":["missing time/lock"]}
    early=[r["lock"] for r in rows if r["time"]<120e-9]
    late=[r["lock"] for r in rows if r["time"]>220e-9]
    if not early or not late: return {"pass":False,"score":0.0,"notes":["insufficient windows"]}
    early_high=sum(1 for v in early if v>0.45)/len(early); late_high=sum(1 for v in late if v>0.45)/len(late)
    ok=early_high<0.15 and late_high>0.75
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"early_high={early_high:.3f} late_high={late_high:.3f}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _resettable_integrator_checker() -> str:
    return r'''#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def _avg(rows,col,start,end):
    vals=[r[col] for r in rows if start<=r["time"]<=end]
    return sum(vals)/len(vals) if vals else 0.0

def check_csv(csv_path):
    rows=_rows(csv_path)
    if not rows or not {"time","rst","vin","vout"}.issubset(rows[0]): return {"pass":False,"score":0.0,"notes":["missing time/rst/vin/vout"]}
    reset_avg=_avg(rows,"vout",0,25e-9)
    mid1=_avg(rows,"vout",80e-9,100e-9)
    mid2=_avg(rows,"vout",180e-9,200e-9)
    late=_avg(rows,"vout",260e-9,300e-9)
    ok=reset_avg<0.08 and mid1>0.12 and mid2>mid1+0.08 and late<0.12
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"reset={reset_avg:.3f} mid1={mid1:.3f} mid2={mid2:.3f} late={late:.3f}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


def _one_shot_timer_va() -> str:
    return """`include \"constants.vams\"\n`include \"disciplines.vams\"\n\nmodule one_shot_timer(trig, rst_n, pulse);\n    input trig, rst_n;\n    output pulse;\n    electrical trig, rst_n, pulse;\n    parameter real vth = 0.45;\n    parameter real vdd = 0.9;\n    parameter real tpw = 8n;\n    parameter real tr = 200p;\n    integer state;\n    real clear_t;\n    integer armed;\n    analog begin\n        @(initial_step) begin state=0; clear_t=-1.0; armed=0; end\n        @(cross(V(rst_n)-vth,-1)) begin state=0; armed=0; clear_t=-1.0; end\n        @(cross(V(trig)-vth,+1)) begin if (V(rst_n)>vth) begin state=1; clear_t=$abstime+tpw; armed=1; end end\n        @(timer(clear_t)) begin if (armed) begin state=0; armed=0; end end\n        V(pulse) <+ transition(state ? vdd : 0.0, 0, tr, tr);\n    end\nendmodule\n"""


def _one_shot_timer_tb() -> str:
    return """simulator lang=spectre\nglobal 0\n\nahdl_include \"one_shot_timer.va\"\n\nVrst (rst_n 0) vsource type=pulse val0=0 val1=0.9 delay=15n rise=200p fall=200p width=500n period=600n\nVtrig (trig 0) vsource type=pulse val0=0 val1=0.9 delay=40n rise=200p fall=200p width=5n period=45n\n\nXDUT (trig rst_n pulse) one_shot_timer\n\ntran tran stop=260n maxstep=500p\nsave trig rst_n pulse\n"""


def _thermometer_dac_va() -> str:
    return """`include \"constants.vams\"\n`include \"disciplines.vams\"\n\nmodule thermometer_dac_4b(code_0, code_1, code_2, code_3, vref, vss, aout);\n    input code_0, code_1, code_2, code_3, vref, vss;\n    output aout;\n    electrical code_0, code_1, code_2, code_3, vref, vss, aout;\n    parameter real vth = 0.45;\n    parameter real tr = 500p;\n    integer code;\n    real y;\n    analog begin\n        code = (V(code_0)>vth?1:0) + (V(code_1)>vth?2:0) + (V(code_2)>vth?4:0) + (V(code_3)>vth?8:0);\n        y = V(vss) + (V(vref)-V(vss))*code/15.0;\n        V(aout, vss) <+ transition(y - V(vss), 0, tr, tr);\n    end\nendmodule\n"""


def _thermometer_dac_tb() -> str:
    return """simulator lang=spectre
global 0

ahdl_include "thermometer_dac_4b.va"

Vref (vref 0) vsource dc=0.9
Vss (vss 0) vsource dc=0
// Code samples at 10/30/.../150 ns are stable; transitions occur between samples.
Vb0 (code_0 0) vsource type=pwl wave=[0 0 19.5n 0 20n 0 39.5n 0 40n 0 59.5n 0 60n 0 79.5n 0 80n 0 99.5n 0 100n 0 119.5n 0 120n 0 139.5n 0 140n 0.9 160n 0.9]
Vb1 (code_1 0) vsource type=pwl wave=[0 0 19.5n 0 20n 0.9 39.5n 0.9 40n 0 59.5n 0 60n 0.9 79.5n 0.9 80n 0 99.5n 0 100n 0.9 119.5n 0.9 120n 0 139.5n 0 140n 0.9 160n 0.9]
Vb2 (code_2 0) vsource type=pwl wave=[0 0 19.5n 0 20n 0 39.5n 0 40n 0.9 59.5n 0.9 60n 0.9 79.5n 0.9 80n 0 99.5n 0 100n 0 119.5n 0 120n 0.9 139.5n 0.9 140n 0.9 160n 0.9]
Vb3 (code_3 0) vsource type=pwl wave=[0 0 19.5n 0 20n 0 39.5n 0 40n 0 59.5n 0 60n 0 79.5n 0 80n 0.9 99.5n 0.9 100n 0.9 119.5n 0.9 120n 0.9 139.5n 0.9 140n 0.9 160n 0.9]

XDUT (code_0 code_1 code_2 code_3 vref vss aout) thermometer_dac_4b

tran tran stop=165n maxstep=500p
save code_0 code_1 code_2 code_3 aout
"""


def _lock_detector_va() -> str:
    return """`include \"constants.vams\"\n`include \"disciplines.vams\"\n\nmodule lock_detector(ref_clk, fb_clk, rst_n, lock);\n    input ref_clk, fb_clk, rst_n;\n    output lock;\n    electrical ref_clk, fb_clk, rst_n, lock;\n    parameter real vth = 0.45;\n    parameter real vdd = 0.9;\n    parameter real tol = 2n;\n    parameter integer need = 3;\n    parameter real tr = 500p;\n    real last_fb;\n    integer streak;\n    integer locked;\n    analog begin\n        @(initial_step) begin last_fb=-1.0; streak=0; locked=0; end\n        @(cross(V(rst_n)-vth,-1)) begin streak=0; locked=0; last_fb=-1.0; end\n        @(cross(V(fb_clk)-vth,+1)) last_fb = $abstime;\n        @(cross(V(ref_clk)-vth,+1)) begin\n            if (V(rst_n)<vth) begin streak=0; locked=0; end\n            else begin\n                if (last_fb>=0.0 && abs($abstime-last_fb) <= tol) streak=streak+1; else streak=0;\n                if (streak>=need) locked=1;\n            end\n        end\n        V(lock) <+ transition(locked ? vdd : 0.0, 0, tr, tr);\n    end\nendmodule\n"""


def _lock_detector_tb() -> str:
    return """simulator lang=spectre\nglobal 0\n\nahdl_include \"lock_detector.va\"\n\nVrst (rst_n 0) vsource type=pulse val0=0 val1=0.9 delay=20n rise=500p fall=500p width=500n period=600n\nVref (ref_clk 0) vsource type=pulse val0=0 val1=0.9 delay=40n period=40n width=20n rise=500p fall=500p\nVfb  (fb_clk 0) vsource type=pwl wave=[0 0 55n 0 55.5n 0.9 75n 0.9 75.5n 0 95n 0 95.5n 0.9 115n 0.9 115.5n 0 135n 0 135.5n 0.9 155n 0.9 155.5n 0 160n 0 160.5n 0.9 180n 0.9 180.5n 0 200n 0 200.5n 0.9 220n 0.9 220.5n 0 240n 0 240.5n 0.9 260n 0.9 260.5n 0 280n 0 280.5n 0.9 300n 0.9]\n\nXDUT (ref_clk fb_clk rst_n lock) lock_detector\n\ntran tran stop=320n maxstep=500p\nsave ref_clk fb_clk rst_n lock\n"""


def _resettable_integrator_va() -> str:
    return """`include \"constants.vams\"\n`include \"disciplines.vams\"\n\nmodule resettable_integrator(vin, rst, vout);\n    input vin, rst;\n    output vout;\n    electrical vin, rst, vout;\n    parameter real vth = 0.45;\n    parameter real gain = 1.0e9;\n    parameter real dt = 1n;\n    parameter real vmax = 0.85;\n    parameter real tr = 500p;\n    real acc;\n    analog begin\n        @(initial_step) acc = 0.0;\n        @(timer(0, dt)) begin\n            if (V(rst) > vth) acc = 0.0;\n            else begin\n                acc = acc + gain * V(vin) * dt;\n                if (acc > vmax) acc = vmax;\n                if (acc < 0.0) acc = 0.0;\n            end\n        end\n        V(vout) <+ transition(acc, 0, tr, tr);\n    end\nendmodule\n"""


def _resettable_integrator_tb() -> str:
    return """simulator lang=spectre\nglobal 0\n\nahdl_include \"resettable_integrator.va\"\n\nVrst (rst 0) vsource type=pwl wave=[0 0.9 25n 0.9 26n 0 220n 0 221n 0.9 250n 0.9 251n 0 320n 0]\nVin (vin 0) vsource dc=0.002\n\nXDUT (vin rst vout) resettable_integrator\n\ntran tran stop=320n maxstep=500p\nsave vin rst vout\n"""

def _one_shot_timer_prompts() -> dict[str, str]:
    buggy = """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule one_shot_timer(trig, rst_n, pulse);\n    input trig, rst_n; output pulse; electrical trig, rst_n, pulse;\n    analog begin V(pulse) <+ transition(V(trig), 0, 200p, 200p); end\nendmodule\n"""
    shared = """Required module: `one_shot_timer`. Ports, all `electrical`, exactly as named and ordered: `trig`, `rst_n`, `pulse`.\nBehavior: on each rising edge of `trig`, when `rst_n` is high, emit a fixed-width pulse of duration `tpw`; active-low reset clears the pulse. Use `@(cross(...))`, `timer(...)`, voltage-domain contributions, and `transition(...)`.\nPublic evaluation contract: the fixed harness runs `tran tran stop=260n maxstep=500p`; public waveform columns are `trig`, `rst_n`, and `pulse`."""
    return {
        "bugfix": f"""The following module mirrors `trig` instead of generating a fixed-width one-shot pulse. Fix it without changing the public interface.\n\n```verilog-a\n{buggy}\n```\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for module `one_shot_timer`.""",
        "spec-to-va": f"""Create only the DUT Verilog-A model for `one_shot_timer`. Do not generate a testbench.\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for `one_shot_timer.va`.""",
        "end-to-end": f"""Write a pure Verilog-A one-shot timer DUT and a minimal Spectre testbench.\n\n{shared}\n\nTestbench requirements: include `one_shot_timer.va`, drive repeated `trig` rising edges after reset release, instantiate `(trig rst_n pulse)`, save `trig rst_n pulse`, and run exactly `tran tran stop=260n maxstep=500p`. Return one `verilog-a` block and one `spectre` block.""",
        "tb-generation": f"""Given a voltage-domain DUT module `one_shot_timer`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `one_shot_timer.va`. Positional port order: `(trig rst_n pulse)`.\n\n{shared}\n\nReturn exactly one fenced `spectre` code block.""",
    }


def _thermometer_dac_prompts() -> dict[str, str]:
    buggy = """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule thermometer_dac_4b(code_0, code_1, code_2, code_3, vref, vss, aout);\n    input code_0, code_1, code_2, code_3, vref, vss; output aout; electrical code_0, code_1, code_2, code_3, vref, vss, aout;\n    analog begin V(aout, vss) <+ transition(V(code_0), 0, 500p, 500p); end\nendmodule\n"""
    shared = """Required module: `thermometer_dac_4b`. Ports, all `electrical`, exactly as named and ordered: `code_0`, `code_1`, `code_2`, `code_3`, `vref`, `vss`, `aout`.\nBehavior: decode the 4-bit public input code and drive a monotonic analog output equal to `code / 15 * (vref-vss)` above `vss`, representing a unary/thermometer DAC abstraction. Use voltage-domain contributions and `transition(...)`.\nPublic evaluation contract: the fixed harness runs `tran tran stop=165n maxstep=500p`; public waveform columns are `code_0`, `code_1`, `code_2`, `code_3`, and `aout`."""
    return {
        "bugfix": f"""The following DAC is wrong because it only mirrors `code_0`. Fix it without changing the public interface.\n\n```verilog-a\n{buggy}\n```\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for module `thermometer_dac_4b`.""",
        "spec-to-va": f"""Create only the DUT Verilog-A model for `thermometer_dac_4b`. Do not generate a testbench.\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for `thermometer_dac_4b.va`.""",
        "end-to-end": f"""Write a pure Verilog-A thermometer DAC abstraction and a minimal Spectre testbench.\n\n{shared}\n\nTestbench requirements: include `thermometer_dac_4b.va`, sweep multiple code values including low/mid/high, instantiate `(code_0 code_1 code_2 code_3 vref vss aout)`, save `code_0 code_1 code_2 code_3 aout`, and run exactly `tran tran stop=165n maxstep=500p`. Return one `verilog-a` block and one `spectre` block.""",
        "tb-generation": f"""Given a voltage-domain DUT module `thermometer_dac_4b`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `thermometer_dac_4b.va`. Positional port order: `(code_0 code_1 code_2 code_3 vref vss aout)`.\n\n{shared}\n\nReturn exactly one fenced `spectre` code block.""",
    }


def _lock_detector_prompts() -> dict[str, str]:
    buggy = """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule lock_detector(ref_clk, fb_clk, rst_n, lock);\n    input ref_clk, fb_clk, rst_n; output lock; electrical ref_clk, fb_clk, rst_n, lock;\n    analog begin V(lock) <+ transition(V(rst_n), 0, 500p, 500p); end\nendmodule\n"""
    shared = """Required module: `lock_detector`. Ports, all `electrical`, exactly as named and ordered: `ref_clk`, `fb_clk`, `rst_n`, `lock`.\nBehavior: after reset release, assert `lock` only after at least `need` consecutive reference edges have a recent feedback edge within timing tolerance `tol`; reset clears the streak and lock. Use voltage-domain event logic and `transition(...)`.\nPublic evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `ref_clk`, `fb_clk`, `rst_n`, and `lock`."""
    return {
        "bugfix": f"""The following lock detector incorrectly mirrors reset instead of checking phase/frequency alignment. Fix it without changing the public interface.\n\n```verilog-a\n{buggy}\n```\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for module `lock_detector`.""",
        "spec-to-va": f"""Create only the DUT Verilog-A model for `lock_detector`. Do not generate a testbench.\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for `lock_detector.va`.""",
        "end-to-end": f"""Write a pure Verilog-A lock detector and a minimal Spectre testbench.\n\n{shared}\n\nTestbench requirements: include `lock_detector.va`, drive `ref_clk` and `fb_clk` misaligned early and aligned later, instantiate `(ref_clk fb_clk rst_n lock)`, save `ref_clk fb_clk rst_n lock`, and run exactly `tran tran stop=320n maxstep=500p`. Return one `verilog-a` block and one `spectre` block.""",
        "tb-generation": f"""Given a voltage-domain DUT module `lock_detector`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `lock_detector.va`. Positional port order: `(ref_clk fb_clk rst_n lock)`.\n\n{shared}\n\nReturn exactly one fenced `spectre` code block.""",
    }


def _resettable_integrator_prompts() -> dict[str, str]:
    buggy = """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule resettable_integrator(vin, rst, vout);\n    input vin, rst; output vout; electrical vin, rst, vout;\n    analog begin V(vout) <+ transition(V(vin), 0, 500p, 500p); end\nendmodule\n"""
    shared = """Required module: `resettable_integrator`. Ports, all `electrical`, exactly as named and ordered: `vin`, `rst`, `vout`.\nBehavior: integrate `vin` into a bounded state while `rst` is low; when `rst` is high, clear the state to zero. Use a Spectre-compatible behavioral implementation and voltage-domain `transition(...)` output.\nPublic evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `vin`, `rst`, and `vout`."""
    return {
        "bugfix": f"""The following module is an input follower and does not integrate or reset state. Fix it without changing the public interface.\n\n```verilog-a\n{buggy}\n```\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for module `resettable_integrator`.""",
        "spec-to-va": f"""Create only the DUT Verilog-A model for `resettable_integrator`. Do not generate a testbench.\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for `resettable_integrator.va`.""",
        "end-to-end": f"""Write a pure Verilog-A resettable integrator and a minimal Spectre testbench.\n\n{shared}\n\nTestbench requirements: include `resettable_integrator.va`, drive reset high at startup and later to clear the state, drive `vin` with a small DC value, instantiate `(vin rst vout)`, save `vin rst vout`, and run exactly `tran tran stop=320n maxstep=500p`. Return one `verilog-a` block and one `spectre` block.""",
        "tb-generation": f"""Given a voltage-domain DUT module `resettable_integrator`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `resettable_integrator.va`. Positional port order: `(vin rst vout)`.\n\n{shared}\n\nReturn exactly one fenced `spectre` code block.""",
    }

# Additional vaBench-main-v1 packs.  These are authored as public, executable
# circuit-function packs rather than copied hidden-source tasks: each pack has a
# prompt contract, gold Verilog-A/Spectre harness, and an independent waveform
# checker.  The small registry keeps the 30-pack target maintainable.
EXTRA_PACK_SPECS: dict[str, dict[str, str]] = {
    "precision_rectifier": {"family": "threshold/static nonlinear", "category": "rectifier", "summary": "drive only the positive part of the input waveform"},
    "peak_detector": {"family": "stateful analog memory", "category": "peak-detector", "summary": "track and hold the maximum input value until reset"},
    "debounce_latch": {"family": "stateful analog memory", "category": "debounce-latch", "summary": "ignore short glitches and assert only after a stable high input"},
    "leaky_hold": {"family": "stateful analog memory", "category": "leaky-hold", "summary": "sample a value and decay it slowly until reset"},
    "edge_detector": {"family": "event/timing", "category": "edge-detector", "summary": "emit a short pulse on rising input edges"},
    "segmented_dac": {"family": "data conversion", "category": "dac", "summary": "combine binary and unary segments into a monotonic analog output"},
    "cdac_calibration": {"family": "data conversion/calibration", "category": "calibration", "summary": "accumulate comparator error into a bounded CDAC trim voltage"},
    "offset_calibration_fsm": {"family": "calibration/control", "category": "calibration-fsm", "summary": "update trim state on clock edges using comparator polarity"},
    "gain_trim_controller": {"family": "calibration/control", "category": "gain-trim", "summary": "move gain control toward a target measurement"},
    "background_calibration_accumulator": {"family": "calibration/control", "category": "background-calibration", "summary": "slowly accumulate signed background error with saturation"},
    "rotating_element_selector": {"family": "pointer/selection", "category": "selector", "summary": "rotate a one-hot element-selection pointer"},
    "barrel_pointer_window": {"family": "pointer/selection", "category": "selector", "summary": "rotate a two-element adjacent selection window"},
    "element_shuffler": {"family": "pointer/selection", "category": "selector", "summary": "cycle through a deterministic non-monotonic one-hot order"},
    "thermometer_decoder_guarded": {"family": "pointer/selection", "category": "decoder", "summary": "decode a guarded binary input into thermometer outputs"},
    "first_order_lowpass": {"family": "continuous dynamics", "category": "filter", "summary": "implement a first-order low-pass response"},
    "slew_rate_limiter": {"family": "continuous dynamics", "category": "slew-limiter", "summary": "limit output slew rate while tracking the input"},
    "vco_phase_integrator": {"family": "continuous dynamics/pll", "category": "vco", "summary": "integrate control voltage into a wrapped oscillator phase"},
    "settling_time_measurement_tb": {"family": "source/measurement/TB", "category": "measurement", "summary": "stimulate and expose a settling response for measurement"},
    "file_metric_writer": {"family": "source/measurement/TB", "category": "file-io", "summary": "open a public string-parameter file and expose a completion waveform"},
}


def _extra_source_by_form() -> dict[str, str]:
    return {
        "bugfix": "balanced_analog_limiter_bugfix",
        "spec-to-va": "balanced_analog_limiter_dut",
        "end-to-end": "balanced_analog_limiter_e2e",
        "tb-generation": "balanced_analog_limiter_tb",
    }


def _extra_prompts(pack_id: str) -> dict[str, str]:
    spec = EXTRA_PACK_SPECS[pack_id]
    module = pack_id
    ports = _extra_ports(pack_id)
    save_cols = " ".join(_extra_save_cols(pack_id))
    tran_line = next(line.strip() for line in _extra_tb(pack_id).splitlines() if line.strip().lower().startswith("tran "))
    buggy = f"""`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule {module}({', '.join(ports)});\n    input {', '.join(ports[:-1])}; output {ports[-1]};\n    electrical {', '.join(ports)};\n    analog begin V({ports[-1]}) <+ transition(V({ports[0]}), 0, 500p, 500p); end\nendmodule\n"""
    shared = f"""Required module: `{module}`. Ports, all `electrical`, exactly as named and ordered: `{', '.join(ports)}`.\nBehavior: {spec['summary']}. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.\nPublic evaluation contract: the fixed harness runs exactly `{tran_line}` and saves waveform columns `{save_cols}`."""
    return {
        "bugfix": f"""The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.\n\n```verilog-a\n{buggy}\n```\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for module `{module}`.""",
        "spec-to-va": f"""Create only the DUT Verilog-A model for `{module}`. Do not generate a testbench.\n\n{shared}\n\nReturn exactly one complete Verilog-A code block for `{module}.va`.""",
        "end-to-end": f"""Write a pure Verilog-A `{module}` DUT and a minimal Spectre testbench.\n\n{shared}\n\nTestbench requirements: include `{module}.va`, instantiate the DUT with positional port order `({ ' '.join(ports) })`, save `{save_cols}`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.""",
        "tb-generation": f"""Given a voltage-domain DUT module `{module}`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `{module}.va`. Positional port order: `({ ' '.join(ports) })`.\n\n{shared}\n\nReturn exactly one fenced `spectre` code block.""",
    }


def _extra_ports(pack_id: str) -> list[str]:
    ports: dict[str, list[str]] = {
        "precision_rectifier": ["vin", "vout"],
        "peak_detector": ["vin", "rst", "vout"],
        "debounce_latch": ["sig", "rst_n", "out"],
        "leaky_hold": ["sample", "rst", "vout"],
        "edge_detector": ["sig", "rst_n", "pulse"],
        "segmented_dac": ["b0", "b1", "t0", "t1", "t2", "vref", "vss", "aout"],
        "cdac_calibration": ["clk", "rst", "err", "trim"],
        "offset_calibration_fsm": ["clk", "rst", "comp", "trim"],
        "gain_trim_controller": ["clk", "rst", "meas", "target", "gain_ctrl"],
        "background_calibration_accumulator": ["clk", "rst", "err", "accum"],
        "rotating_element_selector": ["clk", "rst_n", "sel0", "sel1", "sel2", "sel3"],
        "barrel_pointer_window": ["clk", "rst_n", "win0", "win1", "win2", "win3"],
        "element_shuffler": ["clk", "rst_n", "out0", "out1", "out2", "out3"],
        "thermometer_decoder_guarded": ["b0", "b1", "en", "th0", "th1", "th2", "th3"],
        "first_order_lowpass": ["vin", "vout"],
        "slew_rate_limiter": ["vin", "vout"],
        "vco_phase_integrator": ["vctrl", "phase", "clk"],
        "settling_time_measurement_tb": ["step", "vout", "done"],
        "file_metric_writer": ["vin", "done"],
    }
    return ports[pack_id]


def _extra_save_cols(pack_id: str) -> list[str]:
    return _extra_ports(pack_id)


def _extra_va(pack_id: str) -> str:
    if pack_id == "precision_rectifier":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule precision_rectifier(vin, vout);\n    input vin; output vout; electrical vin, vout;\n    parameter real tr=500p; real y;\n    analog begin y = V(vin) > 0.0 ? V(vin) : 0.0; V(vout) <+ transition(y,0,tr,tr); end\nendmodule\n"""
    if pack_id == "peak_detector":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule peak_detector(vin, rst, vout);\n    input vin,rst; output vout; electrical vin,rst,vout;\n    parameter real vth=0.45; parameter real tr=500p; real peak;\n    analog begin\n        @(initial_step) peak=0.0;\n        @(timer(0,500p)) begin if (V(rst)>vth) peak=0.0; else if (V(vin)>peak) peak=V(vin); end\n        V(vout) <+ transition(peak,0,tr,tr);\n    end\nendmodule\n"""
    if pack_id == "debounce_latch":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule debounce_latch(sig, rst_n, out);\n    input sig,rst_n; output out; electrical sig,rst_n,out;\n    parameter real vth=0.45; parameter real vdd=0.9; parameter real stable=12n; parameter real tr=500p;\n    integer state; real candidate_t; integer armed;\n    analog begin\n        @(initial_step) begin state=0; armed=0; candidate_t=-1.0; end\n        @(cross(V(rst_n)-vth,-1)) begin state=0; armed=0; candidate_t=-1.0; end\n        @(cross(V(sig)-vth,+1)) begin if (V(rst_n)>vth) begin armed=1; candidate_t=$abstime+stable; end end\n        @(cross(V(sig)-vth,-1)) begin armed=0; candidate_t=-1.0; end\n        @(timer(candidate_t)) begin if (armed && V(sig)>vth && V(rst_n)>vth) state=1; end\n        V(out) <+ transition(state ? vdd : 0.0,0,tr,tr);\n    end\nendmodule\n"""
    if pack_id == "leaky_hold":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule leaky_hold(sample, rst, vout);\n    input sample,rst; output vout; electrical sample,rst,vout;\n    parameter real vth=0.45; parameter real decay=0.985; parameter real tr=500p; real held;\n    analog begin\n        @(initial_step) held=0.0;\n        @(cross(V(sample)-vth,+1)) held=0.75;\n        @(timer(0,1n)) begin if (V(rst)>vth) held=0.0; else held=held*decay; end\n        V(vout) <+ transition(held,0,tr,tr);\n    end\nendmodule\n"""
    if pack_id == "edge_detector":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule edge_detector(sig, rst_n, pulse);\n    input sig,rst_n; output pulse; electrical sig,rst_n,pulse;\n    parameter real vth=0.45; parameter real vdd=0.9; parameter real width=6n; parameter real tr=200p;\n    integer state; real clear_t; integer armed;\n    analog begin\n        @(initial_step) begin state=0; clear_t=-1.0; armed=0; end\n        @(cross(V(rst_n)-vth,-1)) begin state=0; armed=0; clear_t=-1.0; end\n        @(cross(V(sig)-vth,+1)) begin if (V(rst_n)>vth) begin state=1; armed=1; clear_t=$abstime+width; end end\n        @(timer(clear_t)) begin if (armed) begin state=0; armed=0; end end\n        V(pulse) <+ transition(state ? vdd : 0.0,0,tr,tr);\n    end\nendmodule\n"""
    if pack_id == "segmented_dac":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule segmented_dac(b0,b1,t0,t1,t2,vref,vss,aout);\n    input b0,b1,t0,t1,t2,vref,vss; output aout; electrical b0,b1,t0,t1,t2,vref,vss,aout;\n    parameter real vth=0.45; parameter real tr=500p; integer code; real y;\n    analog begin\n        code = (V(b0)>vth?1:0) + (V(b1)>vth?2:0) + (V(t0)>vth?4:0) + (V(t1)>vth?4:0) + (V(t2)>vth?4:0);\n        y = V(vss) + (V(vref)-V(vss))*code/15.0;\n        V(aout,vss) <+ transition(y - V(vss),0,tr,tr);\n    end\nendmodule\n"""
    if pack_id == "cdac_calibration":
        return _clocked_accum_va("cdac_calibration", "clk,rst,err,trim", "clk,rst,err,trim", "trim", step="0.06")
    if pack_id == "offset_calibration_fsm":
        return _clocked_accum_va("offset_calibration_fsm", "clk,rst,comp,trim", "clk,rst,comp,trim", "trim", step="0.08", signal="comp")
    if pack_id == "gain_trim_controller":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule gain_trim_controller(clk,rst,meas,target,gain_ctrl);\n    input clk,rst,meas,target; output gain_ctrl; electrical clk,rst,meas,target,gain_ctrl;\n    parameter real vth=0.45; parameter real tr=500p; real ctrl;\n    analog begin\n        @(initial_step) ctrl=0.3;\n        @(cross(V(clk)-vth,+1)) begin\n            if (V(rst)>vth) ctrl=0.3;\n            else if (V(meas)<V(target)-0.02) ctrl=ctrl+0.05;\n            else if (V(meas)>V(target)+0.02) ctrl=ctrl-0.05;\n            if (ctrl>0.85) ctrl=0.85; if (ctrl<0.05) ctrl=0.05;\n        end\n        V(gain_ctrl) <+ transition(ctrl,0,tr,tr);\n    end\nendmodule\n"""
    if pack_id == "background_calibration_accumulator":
        return _clocked_accum_va("background_calibration_accumulator", "clk,rst,err,accum", "clk,rst,err,accum", "accum", step="0.04")
    if pack_id in ("rotating_element_selector", "barrel_pointer_window", "element_shuffler"):
        return _selector_va(pack_id)
    if pack_id == "thermometer_decoder_guarded":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule thermometer_decoder_guarded(b0,b1,en,th0,th1,th2,th3);\n    input b0,b1,en; output th0,th1,th2,th3; electrical b0,b1,en,th0,th1,th2,th3;\n    parameter real vth=0.45; parameter real vdd=0.9; parameter real tr=300p; integer code;\n    analog begin\n        code=(V(b0)>vth?1:0)+(V(b1)>vth?2:0); if (V(en)<vth) code=0;\n        V(th0)<+transition(code>=1?vdd:0.0,0,tr,tr); V(th1)<+transition(code>=2?vdd:0.0,0,tr,tr);\n        V(th2)<+transition(code>=3?vdd:0.0,0,tr,tr); V(th3)<+transition(code>=4?vdd:0.0,0,tr,tr);\n    end\nendmodule\n"""
    if pack_id == "first_order_lowpass":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule first_order_lowpass(vin,vout);\n    input vin; output vout; electrical vin,vout; parameter real alpha=0.025; parameter real tr=200p; real y;\n    analog begin @(initial_step) y=0.0; @(timer(0,500p)) y = y + alpha*(V(vin)-y); V(vout)<+transition(y,0,tr,tr); end\nendmodule\n"""
    if pack_id == "slew_rate_limiter":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule slew_rate_limiter(vin,vout);\n    input vin; output vout; electrical vin,vout; parameter real step=0.015; parameter real tr=200p; real y;\n    analog begin @(initial_step) y=0.0; @(timer(0,1n)) begin if (V(vin)>y+step) y=y+step; else if (V(vin)<y-step) y=y-step; else y=V(vin); end V(vout)<+transition(y,0,tr,tr); end\nendmodule\n"""
    if pack_id == "vco_phase_integrator":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule vco_phase_integrator(vctrl,phase,clk);\n    input vctrl; output phase,clk; electrical vctrl,phase,clk; parameter real tr=200p; real ph; integer c;\n    analog begin @(initial_step) begin ph=0.0; c=0; end @(timer(0,1n)) begin ph=ph+0.03+0.09*V(vctrl); if (ph>=1.0) begin ph=ph-1.0; c=1-c; end end V(phase)<+transition(ph,0,tr,tr); V(clk)<+transition(c?0.9:0.0,0,tr,tr); end\nendmodule\n"""
    if pack_id == "settling_time_measurement_tb":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule settling_time_measurement_tb(step,vout,done);\n    input step; output vout,done; electrical step,vout,done; parameter real tr=300p; real y;\n    analog begin @(initial_step) y=0.0; @(timer(0,1n)) y=y+0.04*(V(step)-y); V(vout)<+transition(y,0,tr,tr); V(done)<+transition(($abstime>120n && y>0.75)?0.9:0.0,0,tr,tr); end\nendmodule\n"""
    if pack_id == "file_metric_writer":
        return """`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule file_metric_writer(vin,done);\n    input vin; output done; electrical vin,done; parameter string filename=\"metric.out\"; parameter real vth=0.45; parameter real tr=300p; integer fh; integer wrote;\n    analog begin @(initial_step) begin wrote=0; fh=$fopen(filename,\"w\"); end @(cross(V(vin)-vth,+1)) begin if (!wrote) begin $fwrite(fh,\"cross %.12g\\n\",$abstime); wrote=1; end end V(done)<+transition(wrote?0.9:0.0,0,tr,tr); end\nendmodule\n"""
    raise KeyError(pack_id)


def _clocked_accum_va(module: str, port_decl: str, electrical_decl: str, out: str, *, step: str, signal: str = "err") -> str:
    return f"""`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule {module}({port_decl});\n    input clk,rst,{signal}; output {out}; electrical {electrical_decl};\n    parameter real vth=0.45; parameter real tr=500p; real acc;\n    analog begin\n        @(initial_step) acc=0.45;\n        @(cross(V(clk)-vth,+1)) begin\n            if (V(rst)>vth) acc=0.45;\n            else if (V({signal})>vth) acc=acc+{step}; else acc=acc-{step};\n            if (acc>0.85) acc=0.85; if (acc<0.05) acc=0.05;\n        end\n        V({out}) <+ transition(acc,0,tr,tr);\n    end\nendmodule\n"""


def _selector_va(pack_id: str) -> str:
    module = pack_id
    if pack_id == "rotating_element_selector":
        outs = ["sel0", "sel1", "sel2", "sel3"]
        exprs = ["idx==0", "idx==1", "idx==2", "idx==3"]
        update = "idx=idx+1; if (idx>3) idx=0;"
    elif pack_id == "barrel_pointer_window":
        outs = ["win0", "win1", "win2", "win3"]
        exprs = ["idx==0 || idx==3", "idx==0 || idx==1", "idx==1 || idx==2", "idx==2 || idx==3"]
        update = "idx=idx+1; if (idx>3) idx=0;"
    else:
        outs = ["out0", "out1", "out2", "out3"]
        exprs = ["idx==0", "idx==2", "idx==1", "idx==3"]
        update = "if (idx==0) idx=2; else if (idx==2) idx=1; else if (idx==1) idx=3; else idx=0;"
    contrib = " ".join([f"V({out})<+transition(({expr})?vdd:0.0,0,tr,tr);" for out, expr in zip(outs, exprs)])
    return f"""`include \"constants.vams\"\n`include \"disciplines.vams\"\nmodule {module}(clk,rst_n,{','.join(outs)});\n    input clk,rst_n; output {','.join(outs)}; electrical clk,rst_n,{','.join(outs)}; parameter real vth=0.45; parameter real vdd=0.9; parameter real tr=300p; integer idx;\n    analog begin @(initial_step) idx=0; @(cross(V(rst_n)-vth,-1)) idx=0; @(cross(V(clk)-vth,+1)) begin if (V(rst_n)>vth) begin {update} end end {contrib} end\nendmodule\n"""


def _extra_tb(pack_id: str) -> str:
    m = pack_id
    if pack_id == "precision_rectifier":
        src = "Vin (vin 0) vsource type=pwl wave=[0 -0.25 30n -0.25 40n 0.35 75n 0.35 85n -0.1 120n -0.1]"
        inst = "XDUT (vin vout) precision_rectifier"; save = "vin vout"; stop = "120n"
    elif pack_id == "peak_detector":
        src = "Vin (vin 0) vsource type=pwl wave=[0 0.1 30n 0.1 40n 0.55 80n 0.55 90n 0.25 130n 0.25 140n 0.7 175n 0.7]\nVrst (rst 0) vsource type=pwl wave=[0 0.9 10n 0.9 11n 0 120n 0 121n 0.9 135n 0.9 136n 0 180n 0]"
        inst = "XDUT (vin rst vout) peak_detector"; save = "vin rst vout"; stop = "180n"
    elif pack_id == "debounce_latch":
        src = "Vsig (sig 0) vsource type=pwl wave=[0 0 30n 0 31n 0.9 35n 0.9 36n 0 70n 0 71n 0.9 130n 0.9]\nVrst (rst_n 0) vsource type=pwl wave=[0 0 15n 0 16n 0.9 140n 0.9]"
        inst = "XDUT (sig rst_n out) debounce_latch"; save = "sig rst_n out"; stop = "140n"
    elif pack_id == "leaky_hold":
        src = "Vsample (sample 0) vsource type=pulse val0=0 val1=0.9 delay=20n rise=200p fall=200p width=5n period=200n\nVrst (rst 0) vsource type=pwl wave=[0 0 110n 0 111n 0.9 130n 0.9 131n 0 170n 0]"
        inst = "XDUT (sample rst vout) leaky_hold"; save = "sample rst vout"; stop = "170n"
    elif pack_id == "edge_detector":
        src = "Vsig (sig 0) vsource type=pulse val0=0 val1=0.9 delay=30n rise=200p fall=200p width=12n period=45n\nVrst (rst_n 0) vsource type=pwl wave=[0 0 10n 0 11n 0.9 180n 0.9]"
        inst = "XDUT (sig rst_n pulse) edge_detector"; save = "sig rst_n pulse"; stop = "180n"
    elif pack_id == "segmented_dac":
        src = "Vref (vref 0) vsource dc=0.9\nVss (vss 0) vsource dc=0\nVb0 (b0 0) vsource type=pwl wave=[0 0 29.5n 0 30n 0.9 59.5n 0.9 60n 0 89.5n 0 90n 0.9 119.5n 0.9 120n 0]\nVb1 (b1 0) vsource type=pwl wave=[0 0 29.5n 0 30n 0 59.5n 0 60n 0.9 89.5n 0.9 90n 0.9 119.5n 0.9 120n 0]\nVt0 (t0 0) vsource type=pwl wave=[0 0 29.5n 0 30n 0 59.5n 0 60n 0 89.5n 0 90n 0.9 119.5n 0.9 120n 0.9]\nVt1 (t1 0) vsource type=pwl wave=[0 0 89.5n 0 90n 0 119.5n 0 120n 0.9]\nVt2 (t2 0) vsource type=pwl wave=[0 0 119.5n 0 120n 0.9]"
        inst = "XDUT (b0 b1 t0 t1 t2 vref vss aout) segmented_dac"; save = "b0 b1 t0 t1 t2 aout"; stop = "150n"
    elif pack_id in ("cdac_calibration", "offset_calibration_fsm", "background_calibration_accumulator"):
        sig = "err" if pack_id != "offset_calibration_fsm" else "comp"
        out = "trim" if pack_id != "background_calibration_accumulator" else "accum"
        src = f"Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 delay=10n rise=200p fall=200p width=5n period=20n\nVrst (rst 0) vsource type=pwl wave=[0 0.9 15n 0.9 16n 0 220n 0]\nVsig ({sig} 0) vsource type=pwl wave=[0 0.9 90n 0.9 91n 0 160n 0 161n 0.9 220n 0.9]"
        inst = f"XDUT (clk rst {sig} {out}) {pack_id}"; save = f"clk rst {sig} {out}"; stop = "220n"
    elif pack_id == "gain_trim_controller":
        src = "Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 delay=10n rise=200p fall=200p width=5n period=20n\nVrst (rst 0) vsource type=pwl wave=[0 0.9 15n 0.9 16n 0 180n 0]\nVmeas (meas 0) vsource type=pwl wave=[0 0.2 100n 0.2 101n 0.7 180n 0.7]\nVtarget (target 0) vsource dc=0.45"
        inst = "XDUT (clk rst meas target gain_ctrl) gain_trim_controller"; save = "clk rst meas target gain_ctrl"; stop = "180n"
    elif pack_id in ("rotating_element_selector", "barrel_pointer_window", "element_shuffler"):
        ports = _extra_ports(pack_id); src = "Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 delay=10n rise=200p fall=200p width=5n period=20n\nVrst (rst_n 0) vsource type=pwl wave=[0 0 8n 0 9n 0.9 130n 0.9]"
        inst = f"XDUT ({' '.join(ports)}) {pack_id}"; save = " ".join(ports); stop = "130n"
    elif pack_id == "thermometer_decoder_guarded":
        src = "Ven (en 0) vsource type=pwl wave=[0 0 20n 0 21n 0.9 120n 0.9]\nVb0 (b0 0) vsource type=pwl wave=[0 0 39.5n 0 40n 0.9 59.5n 0.9 60n 0 79.5n 0 80n 0.9 120n 0.9]\nVb1 (b1 0) vsource type=pwl wave=[0 0 39.5n 0 40n 0 59.5n 0 60n 0.9 79.5n 0.9 80n 0.9 120n 0.9]"
        inst = "XDUT (b0 b1 en th0 th1 th2 th3) thermometer_decoder_guarded"; save = "b0 b1 en th0 th1 th2 th3"; stop = "120n"
    elif pack_id in ("first_order_lowpass", "slew_rate_limiter"):
        src = "Vin (vin 0) vsource type=pwl wave=[0 0 20n 0 21n 0.8 160n 0.8]"
        inst = f"XDUT (vin vout) {pack_id}"; save = "vin vout"; stop = "160n"
    elif pack_id == "vco_phase_integrator":
        src = "Vctrl (vctrl 0) vsource type=pwl wave=[0 0.1 80n 0.1 81n 0.8 180n 0.8]"
        inst = "XDUT (vctrl phase clk) vco_phase_integrator"; save = "vctrl phase clk"; stop = "180n"
    elif pack_id == "settling_time_measurement_tb":
        src = "Vstep (step 0) vsource type=pwl wave=[0 0 20n 0 21n 0.8 160n 0.8]"
        inst = "XDUT (step vout done) settling_time_measurement_tb"; save = "step vout done"; stop = "160n"
    elif pack_id == "file_metric_writer":
        src = "Vin (vin 0) vsource type=pwl wave=[0 0 30n 0 31n 0.9 90n 0.9]"
        inst = "XDUT (vin done) file_metric_writer filename=\"metric.out\""; save = "vin done"; stop = "90n"
    else:
        raise KeyError(pack_id)
    return f"""simulator lang=spectre\nglobal 0\n\nahdl_include \"{m}.va\"\n\n{src}\n\n{inst}\n\ntran tran stop={stop} maxstep=500p\nsave {save}\n"""


def _extra_checker(pack_id: str) -> str:
    return f'''#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
PACK_ID = {pack_id!r}

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{{k.lower(): float(v) for k, v in row.items() if v not in ("", None)}} for row in csv.DictReader(f)]

def _nearest(rows,t): return min(rows, key=lambda r: abs(r["time"]-t))
def _avg(rows,col,a,b):
    vals=[r[col] for r in rows if a <= r["time"] <= b]
    return sum(vals)/len(vals) if vals else 0.0

def _edges(rows,col,vth=0.45):
    return [rows[i]["time"] for i in range(1,len(rows)) if rows[i-1].get(col,0.0)<vth<=rows[i].get(col,0.0)]

def check_csv(csv_path):
    rows=_rows(csv_path)
    if not rows: return {{"pass":False,"score":0.0,"notes":["empty_csv"]}}
    p=PACK_ID
    ok=False; note="unchecked"
    if p=="precision_rectifier":
        neg=_avg(rows,"vout",10e-9,25e-9); pos=_avg(rows,"vout",50e-9,70e-9); ok=neg<0.04 and 0.30<pos<0.40; note=f"neg={{neg:.3f}} pos={{pos:.3f}}"
    elif p=="peak_detector":
        pre=_avg(rows,"vout",70e-9,100e-9); rst=_avg(rows,"vout",123e-9,133e-9); late=_avg(rows,"vout",160e-9,175e-9); ok=pre>0.50 and rst<0.08 and late>0.65; note=f"pre={{pre:.3f}} rst={{rst:.3f}} late={{late:.3f}}"
    elif p=="debounce_latch":
        early=_avg(rows,"out",40e-9,60e-9); late=_avg(rows,"out",95e-9,130e-9); ok=early<0.15 and late>0.65; note=f"early={{early:.3f}} late={{late:.3f}}"
    elif p=="leaky_hold":
        high=_avg(rows,"vout",25e-9,35e-9); decayed=_avg(rows,"vout",80e-9,100e-9); rst=_avg(rows,"vout",120e-9,135e-9); ok=high>0.55 and 0.15<decayed<high and rst<0.08; note=f"high={{high:.3f}} decayed={{decayed:.3f}} rst={{rst:.3f}}"
    elif p=="edge_detector":
        frac=sum(1 for r in rows if r.get("pulse",0)>0.45)/len(rows); edges=len(_edges(rows,"pulse")); ok=3<=edges<=5 and 0.04<frac<0.20; note=f"pulse_edges={{edges}} high_frac={{frac:.3f}}"
    elif p=="segmented_dac":
        vals=[]
        for t in [10e-9,45e-9,75e-9,105e-9,135e-9]:
            r=_nearest(rows,t); vals.append(r["aout"])
        ok=all(vals[i] <= vals[i+1]+0.04 for i in range(len(vals)-1)) and vals[-1]-vals[0]>0.45; note=f"vals={{[round(v,3) for v in vals]}}"
    elif p in ("cdac_calibration","offset_calibration_fsm","background_calibration_accumulator"):
        col="accum" if p=="background_calibration_accumulator" else "trim"; first=_nearest(rows,85e-9)[col]; mid=_nearest(rows,145e-9)[col]; late=_nearest(rows,205e-9)[col]; ok=first>0.52 and mid<first-0.025 and late>mid+0.025; note=f"first={{first:.3f}} mid={{mid:.3f}} late={{late:.3f}}"
    elif p=="gain_trim_controller":
        first=_nearest(rows,100e-9)["gain_ctrl"]; late=_nearest(rows,170e-9)["gain_ctrl"]; ok=first>0.48 and late<first-0.12; note=f"first={{first:.3f}} late={{late:.3f}}"
    elif p in ("rotating_element_selector","element_shuffler"):
        cols=[c for c in rows[0] if c.startswith("sel") or c.startswith("out")]; highs={{c:sum(1 for r in rows if r.get(c,0)>0.45) for c in cols}}; ok=len(cols)==4 and all(v>5 for v in highs.values()); note=f"highs={{highs}}"
    elif p=="barrel_pointer_window":
        cols=["win0","win1","win2","win3"]; counts=[sum(1 for c in cols if r.get(c,0)>0.45) for r in rows if r["time"]>20e-9]; ok=counts and min(counts)>=1 and max(counts)<=2 and all(sum(1 for r in rows if r.get(c,0)>0.45)>5 for c in cols); note=f"count_range={{(min(counts),max(counts)) if counts else None}}"
    elif p=="thermometer_decoder_guarded":
        off=_avg(rows,"th0",5e-9,15e-9); th2=_avg(rows,"th1",65e-9,75e-9); th3=_avg(rows,"th2",90e-9,110e-9); th3off=_avg(rows,"th3",90e-9,110e-9); ok=off<0.1 and th2>0.6 and th3>0.6 and th3off<0.2; note=f"off={{off:.3f}} th1={{th2:.3f}} th2={{th3:.3f}} th3={{th3off:.3f}}"
    elif p=="first_order_lowpass":
        early=_avg(rows,"vout",30e-9,45e-9); late=_avg(rows,"vout",130e-9,155e-9); ok=0.05<early<0.55 and late>0.65; note=f"early={{early:.3f}} late={{late:.3f}}"
    elif p=="slew_rate_limiter":
        early=_avg(rows,"vout",30e-9,45e-9); late=_avg(rows,"vout",100e-9,140e-9); ok=0.05<early<0.45 and late>0.65; note=f"early={{early:.3f}} late={{late:.3f}}"
    elif p=="vco_phase_integrator":
        early=len([e for e in _edges(rows,"clk") if e<80e-9]); late=len([e for e in _edges(rows,"clk") if e>100e-9]); span=max(r["phase"] for r in rows)-min(r["phase"] for r in rows); ok=late>=early and late>=3 and span>0.7; note=f"early_edges={{early}} late_edges={{late}} phase_span={{span:.3f}}"
    elif p=="settling_time_measurement_tb":
        early=_avg(rows,"vout",30e-9,45e-9); late=_avg(rows,"vout",130e-9,155e-9); done=_avg(rows,"done",130e-9,155e-9); ok=early<0.45 and late>0.65 and done>0.6; note=f"early={{early:.3f}} late={{late:.3f}} done={{done:.3f}}"
    elif p=="file_metric_writer":
        pre=_avg(rows,"done",5e-9,25e-9); post=_avg(rows,"done",45e-9,85e-9); ok=pre<0.1 and post>0.6; note=f"pre={{pre:.3f}} post={{post:.3f}}"
    return {{"pass":ok,"score":1.0 if ok else 0.0,"notes":[note]}}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
'''


PACKS = {
    "offset_comparator": {
        "source_e2e": "original92_comparator_offset_tb",
        "source_bugfix": "original92_comparator_offset_tb",
        "prompts": _offset_comparator_prompts,
        "checker": _offset_checker,
        "source_task_id_by_form": {
            "bugfix": "offset_comparator",
            "spec-to-va": "offset_comparator",
            "end-to-end": "offset_comparator",
            "tb-generation": "offset_comparator",
        },
    },
    "strongarm_comparator_behavior": {
        "source_e2e": "original92_cmp_strongarm_smoke",
        "source_bugfix": "original92_strongarm_reset_priority_bug",
        "prompts": _strongarm_prompts,
        "checker": _strongarm_checker,
        "source_task_id_by_form": {
            "bugfix": "strongarm_reset_priority_bug",
            "spec-to-va": "cmp_strongarm_smoke",
            "end-to-end": "cmp_strongarm_smoke",
            "tb-generation": "cmp_strongarm_smoke",
        },
    },
    "pfd_reset_race": {
        "source_e2e": "original92_pfd_reset_race_smoke",
        "source_bugfix": "original92_pfd_reset_race_smoke",
        "prompts": _pfd_prompts,
        "checker": _pfd_checker,
        "source_task_id_by_form": {
            "bugfix": "pfd_reset_race_smoke",
            "spec-to-va": "pfd_reset_race_smoke",
            "end-to-end": "pfd_reset_race_smoke",
            "tb-generation": "pfd_reset_race_smoke",
        },
    },
    "voltage_clamp": {
        "source_e2e": "balanced_analog_limiter_e2e",
        "source_bugfix": "balanced_analog_limiter_bugfix",
        "source_by_form": {
            "bugfix": "balanced_analog_limiter_bugfix",
            "spec-to-va": "balanced_analog_limiter_dut",
            "end-to-end": "balanced_analog_limiter_e2e",
            "tb-generation": "balanced_analog_limiter_tb",
        },
        "prompts": _voltage_clamp_prompts,
        "checker": _clamp_checker,
        "source_task_id_by_form": {
            "bugfix": "voltage_clamp",
            "spec-to-va": "voltage_clamp",
            "end-to-end": "voltage_clamp",
            "tb-generation": "voltage_clamp",
        },
    },
    "track_hold_aperture": {
        "source_e2e": "original92_sample_hold_aperture_tb",
        "source_bugfix": "original92_sample_hold_aperture_tb",
        "prompts": _track_hold_aperture_prompts,
        "checker": _sample_hold_aperture_checker,
        "source_task_id_by_form": {
            "bugfix": "track_hold_aperture",
            "spec-to-va": "track_hold_aperture",
            "end-to-end": "track_hold_aperture",
            "tb-generation": "track_hold_aperture",
        },
    },
    "resettable_counter_divider": {
        "source_e2e": "original92_clk_divider",
        "source_bugfix": "original92_clk_divider",
        "prompts": _resettable_counter_divider_prompts,
        "checker": _clock_divider_checker,
        "source_task_id_by_form": {
            "bugfix": "resettable_counter_divider",
            "spec-to-va": "resettable_counter_divider",
            "end-to-end": "resettable_counter_divider",
            "tb-generation": "resettable_counter_divider",
        },
    },
    "sar_logic_4b": {
        "source_e2e": "original92_sar_logic",
        "source_bugfix": "original92_sar_logic",
        "prompts": _sar_logic_4b_prompts,
        "checker": _sar4_checker,
        "source_task_id_by_form": {
            "bugfix": "sar_logic_4b",
            "spec-to-va": "sar_logic_4b",
            "end-to-end": "sar_logic_4b",
            "tb-generation": "sar_logic_4b",
        },
    },
    "one_shot_timer": {
        "source_e2e": "original92_clk_burst_gen_smoke",
        "source_bugfix": "original92_clk_burst_gen_smoke",
        "prompts": _one_shot_timer_prompts,
        "checker": _edge_pulse_checker,
        "source_task_id_by_form": {
            "bugfix": "one_shot_timer",
            "spec-to-va": "one_shot_timer",
            "end-to-end": "one_shot_timer",
            "tb-generation": "one_shot_timer",
        },
    },
    "thermometer_dac": {
        "source_e2e": "original92_sar_logic",
        "source_bugfix": "original92_sar_logic",
        "prompts": _thermometer_dac_prompts,
        "checker": _thermometer_dac_checker,
        "source_task_id_by_form": {
            "bugfix": "thermometer_dac",
            "spec-to-va": "thermometer_dac",
            "end-to-end": "thermometer_dac",
            "tb-generation": "thermometer_dac",
        },
    },
    "lock_detector": {
        "source_e2e": "completion92_pll_closed_loop_dut",
        "source_bugfix": "completion92_pll_closed_loop_bugfix",
        "prompts": _lock_detector_prompts,
        "checker": _lock_detector_checker,
        "source_task_id_by_form": {
            "bugfix": "lock_detector",
            "spec-to-va": "lock_detector",
            "end-to-end": "lock_detector",
            "tb-generation": "lock_detector",
        },
    },
    "resettable_integrator": {
        "source_e2e": "completion92_signal_source_tb",
        "source_bugfix": "completion92_signal_source_bugfix",
        "prompts": _resettable_integrator_prompts,
        "checker": _resettable_integrator_checker,
        "source_task_id_by_form": {
            "bugfix": "resettable_integrator",
            "spec-to-va": "resettable_integrator",
            "end-to-end": "resettable_integrator",
            "tb-generation": "resettable_integrator",
        },
    },
}


for _extra_pack_id in EXTRA_PACK_SPECS:
    PACKS[_extra_pack_id] = {
        "source_e2e": "balanced_analog_limiter_e2e",
        "source_bugfix": "balanced_analog_limiter_bugfix",
        "source_by_form": _extra_source_by_form(),
        "prompts": (lambda pack_id=_extra_pack_id: _extra_prompts(pack_id)),
        "checker": (lambda pack_id=_extra_pack_id: _extra_checker(pack_id)),
        "source_task_id_by_form": {form: _extra_pack_id for form in TASK_FORMS},
    }



def _source_for(pack: dict[str, Any], form: str) -> str:
    if "source_by_form" in pack:
        return pack["source_by_form"][form]
    return pack["source_bugfix"] if form == "bugfix" else pack["source_e2e"]


def _write_pack_checker(task_dir: Path, pack: dict[str, Any], source_task_id: str) -> None:
    checker_factory = pack.get("checker")
    if checker_factory is None:
        text = _checker(source_task_id)
    else:
        text = checker_factory()
    (task_dir / "checker.py").write_text(text, encoding="utf-8")


def _postprocess_pack_gold(task_dir: Path, pack_id: str) -> None:
    gold = task_dir / "gold"
    if pack_id == "voltage_clamp":
        (gold / "dut.va").write_text(_voltage_clamp_va(), encoding="utf-8")
        (gold / "tb_ref.scs").write_text(_voltage_clamp_tb(), encoding="utf-8")
    elif pack_id == "sar_logic_4b":
        for path in gold.glob("*"):
            if path.is_file():
                path.unlink()
        (gold / "sar_logic_4b.va").write_text(_sar4_va(), encoding="utf-8")
        (gold / "tb_sar_logic_4b_ref.scs").write_text(_sar4_tb(), encoding="utf-8")
    elif pack_id == "one_shot_timer":
        for path in gold.glob("*"):
            if path.is_file():
                path.unlink()
        (gold / "one_shot_timer.va").write_text(_one_shot_timer_va(), encoding="utf-8")
        (gold / "tb_one_shot_timer_ref.scs").write_text(_one_shot_timer_tb(), encoding="utf-8")
    elif pack_id == "thermometer_dac":
        for path in gold.glob("*"):
            if path.is_file():
                path.unlink()
        (gold / "thermometer_dac_4b.va").write_text(_thermometer_dac_va(), encoding="utf-8")
        (gold / "tb_thermometer_dac_4b_ref.scs").write_text(_thermometer_dac_tb(), encoding="utf-8")
    elif pack_id == "lock_detector":
        for path in gold.glob("*"):
            if path.is_file():
                path.unlink()
        (gold / "lock_detector.va").write_text(_lock_detector_va(), encoding="utf-8")
        (gold / "tb_lock_detector_ref.scs").write_text(_lock_detector_tb(), encoding="utf-8")
    elif pack_id == "resettable_integrator":
        for path in gold.glob("*"):
            if path.is_file():
                path.unlink()
        (gold / "resettable_integrator.va").write_text(_resettable_integrator_va(), encoding="utf-8")
        (gold / "tb_resettable_integrator_ref.scs").write_text(_resettable_integrator_tb(), encoding="utf-8")
    elif pack_id in EXTRA_PACK_SPECS:
        for path in gold.glob("*"):
            if path.is_file():
                path.unlink()
        (gold / f"{pack_id}.va").write_text(_extra_va(pack_id), encoding="utf-8")
        (gold / f"tb_{pack_id}_ref.scs").write_text(_extra_tb(pack_id), encoding="utf-8")


def materialize(output: Path, *, force: bool) -> dict[str, Any]:
    if output.exists() and force:
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    tasks_dir = output / "tasks"
    tasks_dir.mkdir(exist_ok=True)
    tasks: list[dict[str, Any]] = []
    for pack_id, pack in PACKS.items():
        prompts = pack["prompts"]()
        for form in TASK_FORMS:
            suffix = {"bugfix": "bugfix", "spec-to-va": "dut", "end-to-end": "e2e", "tb-generation": "tb"}[form]
            task_id = f"vbm1_{pack_id}_{suffix}"
            dst = tasks_dir / task_id
            src_name = _source_for(pack, form)
            source_task_id = pack["source_task_id_by_form"][form]
            _copy_task(SOURCE / src_name, dst)
            _postprocess_pack_gold(dst, pack_id)
            _write_prompt(dst, prompts[form])
            _write_pack_checker(dst, pack, source_task_id)
            meta = _update_meta(
                dst,
                task_id=task_id,
                pack_id=pack_id,
                form=form,
                source_task_id=source_task_id,
                source_root=src_name,
            )
            tasks.append(
                {
                    "task_id": task_id,
                    "pack_id": pack_id,
                    "task_form": form,
                    "source_seed_task": src_name,
                    "source_task_id": source_task_id,
                    "promotion_status": meta["promotion_status"],
                }
            )
    manifest = {
        "benchmark": "vaBench-main-v1",
        "benchmark_root": str(output.relative_to(ROOT)),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "draft": True,
        "note": "Audited draft batch. Full vaBench-main-v1 target is 30 packs x 4 forms.",
        "pack_count": len(PACKS),
        "task_count": len(tasks),
        "task_forms": TASK_FORMS,
        "tasks": tasks,
    }
    _write_json(output / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-bench", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    manifest = materialize(args.output_bench.resolve(), force=args.force)
    print(json.dumps({"benchmark_root": manifest["benchmark_root"], "tasks": manifest["task_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
