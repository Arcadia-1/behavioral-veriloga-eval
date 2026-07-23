from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_303 import CHECKER as check_303
from checkers.v4.task_304 import CHECKER as check_304
from checkers.v4.task_305 import CHECKER as check_305
from checkers.v4.task_306 import CHECKER as check_306
from checkers.v4.task_307 import CHECKER as check_307
from checkers.v4.task_308 import CHECKER as check_308
from checkers.v4.task_309 import CHECKER as check_309
from checkers.v4.task_310 import CHECKER as check_310


def _clip01(value: float) -> float:
    return min(0.9, max(0.0, value))


def _gm_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    diffs = (0.05, -0.07, 0.18, -0.22)
    for index in range(100):
        enabled = 0.9 if 10 <= index < 80 else 0.0
        diff = diffs[index % len(diffs)]
        limited = diff / (1.0 + abs(diff) / 0.12)
        separation = 4.0 * limited if enabled else 0.0
        rows.append(
            {
                "time": index * 1e-10,
                "vinp": 0.45 + 0.5 * diff,
                "vinn": 0.45 - 0.5 * diff,
                "bias": 0.45,
                "enable": enabled,
                "voutp": 0.45 + 0.5 * separation,
                "voutn": 0.45 - 0.5 * separation,
                "gm_metric": 0.9 * 0.12 / (0.12 + abs(diff)) if enabled else 0.0,
                "limit_flag": 0.9 if enabled and abs(diff) > 0.12 else 0.0,
            }
        )
    return rows


def _tia_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(100):
        active = 10 <= index < 80
        bias = 0.28 if index % 4 < 2 else 0.62
        vin = (0.08, 0.38, 0.54, 0.86)[index % 4]
        gain_scale = _clip01((bias - 0.3) / 0.15)
        gain_scale = max(gain_scale, 0.35)
        gain = 3.0 * gain_scale
        raw = 0.45 + gain * (vin - 0.45)
        rows.append(
            {
                "time": index * 1e-10,
                "vin_proxy": vin,
                "bias": bias,
                "enable": 0.9 if active else 0.0,
                "rst": 0.0 if active else 0.9,
                "vout": _clip01(raw) if active else 0.45,
                "transimpedance_metric": _clip01(0.9 * gain / 3.0) if active else 0.0,
                "overload": 0.9 if active and (raw > 0.9 or raw < 0.0) else 0.0,
            }
        )
    return rows


def _clocked_rows(
    cycles: list[dict[str, float]],
    update,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state: dict[str, float] = {}
    for cycle_index, controls in enumerate(cycles):
        for phase in range(10):
            clk = 0.9 if 2 <= phase < 5 else 0.0
            if phase == 2:
                state = update(controls, state)
            row = {
                "time": (10 * cycle_index + phase) * 1e-10,
                "clk": clk,
                **controls,
                **state,
            }
            rows.append(row)
    return rows


def _cfa_rows() -> list[dict[str, float]]:
    cycles: list[dict[str, float]] = []
    cycles.extend(
        [
            {"vin": 0.32, "rst": 0.9, "enable": 0.0, "gain_1": 0.0, "gain_0": 0.0},
            {"vin": 0.32, "rst": 0.0, "enable": 0.0, "gain_1": 0.0, "gain_0": 0.0},
        ]
    )
    for code, vin in ((0, 0.22), (1, 0.62), (2, 0.30), (3, 0.58), (0, 0.50), (1, 0.40)):
        cycles.append(
            {
                "vin": vin,
                "rst": 0.0,
                "enable": 0.9,
                "gain_1": 0.9 if code & 2 else 0.0,
                "gain_0": 0.9 if code & 1 else 0.0,
            }
        )
    cycles.extend(
        [
            {"vin": 0.50, "rst": 0.0, "enable": 0.9, "gain_1": 0.0, "gain_0": 0.0}
            for _ in range(4)
        ]
    )

    def update(control: dict[str, float], state: dict[str, float]) -> dict[str, float]:
        if control["rst"] > 0.45 or control["enable"] < 0.45:
            return {"vout": 0.45, "sampled_metric": 0.0, "settled": 0.0}
        code = int(control["gain_0"] > 0.45) + 2 * int(control["gain_1"] > 0.45)
        target = _clip01(0.45 + (1.0 + 0.75 * code) * (control["vin"] - 0.45))
        repeated = abs(state.get("vout", -1.0) - target) < 1e-9
        count = int(state.get("settle_count", 0.0)) + 1 if repeated else 0
        return {
            "vout": target,
            "sampled_metric": control["vin"],
            "settled": 0.9 if count >= 2 else 0.0,
            "settle_count": float(count),
        }

    rows = _clocked_rows(cycles, update)
    for row in rows:
        row["gain_code"] = int(row["gain_0"] > 0.45) + 2 * int(row["gain_1"] > 0.45)
    return rows


def _cds_rows() -> list[dict[str, float]]:
    cycles = [
        {"vin": 0.45, "rst": 0.9, "sample_reset": 0.0, "sample_signal": 0.0},
        {"vin": 0.30, "rst": 0.0, "sample_reset": 0.9, "sample_signal": 0.0},
        {"vin": 0.70, "rst": 0.0, "sample_reset": 0.0, "sample_signal": 0.9},
        {"vin": 0.66, "rst": 0.0, "sample_reset": 0.9, "sample_signal": 0.0},
        {"vin": 0.18, "rst": 0.0, "sample_reset": 0.0, "sample_signal": 0.9},
        {"vin": 0.52, "rst": 0.0, "sample_reset": 0.0, "sample_signal": 0.0},
    ]

    def update(control: dict[str, float], state: dict[str, float]) -> dict[str, float]:
        state = dict(state or {"vout": 0.45, "offset_dbg": 0.0, "valid": 0.0, "reset_sample": 0.45})
        if control["rst"] > 0.45:
            state.update(vout=0.45, offset_dbg=0.0, valid=0.0, reset_sample=0.45)
        elif control["sample_reset"] > 0.45:
            state["reset_sample"] = control["vin"]
        elif control["sample_signal"] > 0.45:
            state.update(
                vout=_clip01(0.45 + control["vin"] - state["reset_sample"]),
                offset_dbg=_clip01(state["reset_sample"]),
                valid=0.9,
            )
        return state

    return _clocked_rows(cycles, update)


def _autozero_rows() -> list[dict[str, float]]:
    cycles = [
        {"vinp": 0.45, "vinn": 0.45, "rst": 0.9, "az_en": 0.0, "eval_en": 0.0},
        {"vinp": 0.50, "vinn": 0.44, "rst": 0.0, "az_en": 0.9, "eval_en": 0.0},
        {"vinp": 0.70, "vinn": 0.42, "rst": 0.0, "az_en": 0.0, "eval_en": 0.9},
        {"vinp": 0.38, "vinn": 0.62, "rst": 0.0, "az_en": 0.0, "eval_en": 0.9},
        {"vinp": 0.39, "vinn": 0.47, "rst": 0.0, "az_en": 0.9, "eval_en": 0.0},
        {"vinp": 0.60, "vinn": 0.44, "rst": 0.0, "az_en": 0.0, "eval_en": 0.9},
        {"vinp": 0.32, "vinn": 0.55, "rst": 0.0, "az_en": 0.0, "eval_en": 0.9},
        {"vinp": 0.50, "vinn": 0.45, "rst": 0.0, "az_en": 0.0, "eval_en": 0.0},
    ]

    def update(control: dict[str, float], state: dict[str, float]) -> dict[str, float]:
        state = dict(state or {"decision": 0.0, "offset_store": 0.45, "ready": 0.0})
        if control["rst"] > 0.45:
            state.update(decision=0.0, offset_store=0.45, ready=0.0)
        elif control["az_en"] > 0.45:
            state.update(
                offset_store=_clip01(0.45 + control["vinp"] - control["vinn"]),
                ready=0.9,
            )
        elif control["eval_en"] > 0.45 and state["ready"] > 0.45:
            corrected = control["vinp"] - control["vinn"] - (state["offset_store"] - 0.45)
            state["decision"] = 0.9 if corrected >= 0.0 else 0.0
        return state

    return _clocked_rows(cycles, update)


def _sampler_rows() -> list[dict[str, float]]:
    captures = (0.45, 0.82, 0.12, 0.48, 0.78, 0.16, 0.52, 0.84)
    cycles = [
        {"vin": 0.45, "rst": 0.9, "enable": 0.0},
        {"vin": 0.45, "rst": 0.0, "enable": 0.0},
        *({"vin": vin, "rst": 0.0, "enable": 0.9} for vin in captures),
    ]

    def update(control: dict[str, float], state: dict[str, float]) -> dict[str, float]:
        if control["rst"] > 0.45 or control["enable"] < 0.45:
            return {"vhold": 0.45, "boot_metric": 0.0, "droop_flag": 0.0, "age": 0.0}
        return {
            "vhold": control["vin"],
            "boot_metric": _clip01(2.0 * abs(control["vin"] - 0.45)),
            "droop_flag": 0.0,
            "age": 0.0,
        }

    rows: list[dict[str, float]] = []
    state: dict[str, float] = {}
    for cycle_index, controls in enumerate(cycles):
        for phase in range(20):
            clk = 0.9 if 2 <= phase < 8 else 0.0
            if phase == 2:
                state = update(controls, state)
            row = {
                "time": (20 * cycle_index + phase) * 5e-11,
                "clk": clk,
                **controls,
                **state,
            }
            if controls["enable"] > 0.45 and phase >= 17:
                row["droop_flag"] = 0.9
            rows.append(row)
    return rows


def test_task_303_rejects_mostly_wrong_disabled_window() -> None:
    rows = _gm_rows()
    assert check_303(rows)[0]
    bad = deepcopy(rows)
    for row in bad[88:-1]:
        row.update(voutp=0.9, voutn=0.0, gm_metric=0.9, limit_flag=0.9)
    assert not check_303(bad)[0]


def test_task_304_rejects_mostly_wrong_inactive_window() -> None:
    rows = _tia_rows()
    assert check_304(rows)[0]
    bad = deepcopy(rows)
    for row in bad[88:-1]:
        row.update(vout=0.9, transimpedance_metric=0.9, overload=0.9)
    assert not check_304(bad)[0]


def test_task_305_rejects_combinational_outputs_in_place_of_sample_and_hold() -> None:
    rows = _cfa_rows()
    assert check_305(rows)[0]
    bad = deepcopy(rows)
    for row in bad:
        code = int(row["gain_0"] > 0.45) + 2 * int(row["gain_1"] > 0.45)
        row["sampled_metric"] = row["vin"]
        row["vout"] = _clip01(0.45 + (1.0 + 0.75 * code) * (row["vin"] - 0.45))
        row["settled"] = 0.9
    assert not check_305(bad)[0]


def test_task_308_rejects_fabricated_offset_not_captured_from_reset_phase() -> None:
    rows = _cds_rows()
    assert check_308(rows)[0]
    bad = deepcopy(rows)
    for row in bad:
        if row.get("valid", 0.0) > 0.45:
            row["offset_dbg"] = 0.12
            row["vout"] = _clip01(0.45 + row["vin"] - 0.12)
    assert not check_308(bad)[0]


def test_task_309_rejects_self_consistent_but_uncaptured_offset() -> None:
    rows = _autozero_rows()
    assert check_309(rows)[0]
    bad = deepcopy(rows)
    for row in bad:
        if row.get("ready", 0.0) > 0.45:
            row["offset_store"] = 0.72
            corrected = row["vinp"] - row["vinn"] - (0.72 - 0.45)
            row["decision"] = 0.9 if corrected >= 0.0 else 0.0
    assert not check_309(bad)[0]


def test_task_310_rejects_combinational_tracking_and_immediate_droop_flag() -> None:
    rows = _sampler_rows()
    assert check_310(rows)[0]
    bad = deepcopy(rows)
    for row in bad:
        if row["enable"] > 0.45:
            row["vhold"] = row["vin"]
            row["boot_metric"] = _clip01(2.0 * abs(row["vin"] - 0.45))
            row["droop_flag"] = 0.9
    assert not check_310(bad)[0]


def test_task_310_rejects_even_one_reset_or_disable_clear_violation() -> None:
    rows = _sampler_rows()
    assert check_310(rows)[0]
    bad = deepcopy(rows)
    first_edge = next(
        index
        for index, (previous, row) in enumerate(zip(bad, bad[1:]), start=1)
        if previous["clk"] <= 0.45 < row["clk"]
    )
    for row in bad[first_edge + 3 : first_edge + 5]:
        row.update(vhold=0.9, boot_metric=0.9, droop_flag=0.9)
    assert not check_310(bad)[0]


def _trim_rows() -> list[dict[str, float]]:
    cycles = [
        {"rst": 0.9, "cal_en": 0.0},
        {"rst": 0.9, "cal_en": 0.0},
        *({"rst": 0.0, "cal_en": 0.9} for _ in range(10)),
        {"rst": 0.9, "cal_en": 0.0},
        {"rst": 0.9, "cal_en": 0.0},
        *({"rst": 0.0, "cal_en": 0.9} for _ in range(5)),
    ]
    rows: list[dict[str, float]] = []
    trim_adapt = 0.0
    active_corr = 0.0
    updates = 0
    for cycle_index, controls in enumerate(cycles):
        for phase in range(12):
            clk = 0.9 if 2 <= phase < 5 else 0.0
            vinp = 0.49
            vinn = 0.45
            if phase == 2:
                if controls["rst"] > 0.45:
                    trim_adapt = active_corr = 0.0
                    updates = 0
                elif controls["cal_en"] > 0.45:
                    error = vinp - vinn - trim_adapt
                    if error > 4e-3:
                        trim_adapt += 8e-3
                    elif error < -4e-3:
                        trim_adapt -= 8e-3
                    active_corr = trim_adapt
                    updates += 1
            if controls["rst"] > 0.45:
                vout = 0.45
                metric = 0.0
                ready = 0.0
            else:
                vout = _clip01(0.45 + 8.0 * (vinp - vinn - active_corr))
                metric = _clip01(0.45 + active_corr)
                ready = 0.9 if updates >= 3 else 0.0
            rows.append(
                {
                    "time": (12 * cycle_index + phase) * 1e-10,
                    "vinp": vinp,
                    "vinn": vinn,
                    "clk": clk,
                    "rst": controls["rst"],
                    "cal_en": controls["cal_en"],
                    "trim_2": 0.9,
                    "trim_1": 0.0,
                    "trim_0": 0.0,
                    "vout": vout,
                    "offset_metric": metric,
                    "ready": ready,
                }
            )
    return rows


def _phase_pair_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state = 0.45
    metric = 0.45
    valid = 0.0
    sample = 0.45
    step = 1e-10

    for index in range(20):
        rows.append(
            {
                "time": index * step,
                "vin": 0.45,
                "phi1": 0.0,
                "phi2": 0.0,
                "rst": 0.9,
                "enable": 0.0,
                "vout": 0.45,
                "phase_metric": 0.45,
                "valid": 0.0,
            }
        )

    for cycle_index, (vin, overlap) in enumerate(
        ((0.33, False), (0.74, False), (0.69, True), (0.22, False))
    ):
        base = 20 + cycle_index * 30
        for phase in range(30):
            phi1 = 0.9 if 2 <= phase < (14 if overlap else 6) else 0.0
            phi2 = 0.9 if 12 <= phase < 16 else 0.0
            if phase == 2:
                sample = vin
            if phase == 12:
                if overlap:
                    valid = 0.0
                else:
                    state = _clip01(state + 0.2 * (sample - 0.45))
                    metric = sample
                    valid = 0.9
            rows.append(
                {
                    "time": base * step + phase * step,
                    "vin": vin,
                    "phi1": phi1,
                    "phi2": phi2,
                    "rst": 0.0,
                    "enable": 0.9,
                    "vout": state,
                    "phase_metric": metric,
                    "valid": valid,
                }
            )
    return rows


def test_task_306_requires_every_settled_reset_sample_to_be_clear() -> None:
    rows = _trim_rows()
    assert check_306(rows)[0]

    bad = deepcopy(rows)
    reset_rows = [row for row in bad if row["rst"] > 0.45]
    for row in reset_rows[8:-1]:
        row.update(vout=0.9, offset_metric=0.9, ready=0.9)
    assert not check_306(bad)[0]


def test_task_307_accepts_phase_state_machine_and_rejects_combinational_tracking() -> None:
    rows = _phase_pair_rows()
    passed, note = check_307(rows)
    assert passed, note

    bad = deepcopy(rows)
    for row in bad:
        if row["enable"] > 0.45 and row["rst"] < 0.45:
            row["phase_metric"] = row["vin"]
            row["vout"] = _clip01(0.45 + 0.35 * (row["vin"] - 0.45))
            row["valid"] = 0.9 if row["phi2"] > 0.45 else 0.0
    assert not check_307(bad)[0]


def test_task_307_rejects_state_changes_between_phase_pairs() -> None:
    rows = _phase_pair_rows()
    assert check_307(rows)[0]

    bad = deepcopy(rows)
    for row in bad:
        if row["enable"] > 0.45 and row["phi1"] < 0.45 and row["phi2"] < 0.45:
            row["vout"] = _clip01(row["vout"] + 0.04)
    assert not check_307(bad)[0]
