from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.common.issue109_factory import SPAN_MAX, SPAN_MIN, VTH, _cont_expected
from checkers.v4.task_202 import CHECKER as CHECKER_202
from checkers.v4.task_207 import CHECKER as CHECKER_207
from checkers.v4.task_213 import CHECKER as CHECKER_213
from checkers.v4.task_219 import CHECKER as CHECKER_219
from checkers.v4.task_244 import CHECKER as CHECKER_244
from checkers.v4.task_248 import CHECKER as CHECKER_248
from checkers.v4.task_265 import CHECKER as CHECKER_265
from checkers.v4.task_266 import CHECKER as CHECKER_266
from checkers.v4.task_268 import CHECKER as CHECKER_268


TASK_ROOT = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)

CONTINUOUS_LOCAL_SUPPLY_CHECKERS = [
    (265, CHECKER_265, "translate"),
    (266, CHECKER_266, "translate"),
    (268, CHECKER_268, "mux"),
]


def _clock(time_ns: float, first_rise_ns: float, period_ns: float = 1.0) -> float:
    if time_ns < first_rise_ns:
        return 0.0
    return 0.9 if (time_ns - first_rise_ns) % period_ns < 0.30 else 0.0


def _parse_time_seconds(token: str) -> float:
    if token.endswith("n"):
        return float(token[:-1]) * 1e-9
    return float(token)


def _parse_pwl_wave(text: str, source_name: str) -> list[tuple[float, float]]:
    match = re.search(
        rf"^{re.escape(source_name)}\s+\([^)]*\)\s+vsource\s+type=pwl\s+wave=\[([^\]]+)\]",
        text,
        re.MULTILINE,
    )
    assert match, f"missing {source_name} PWL source"
    tokens = match.group(1).split()
    assert len(tokens) % 2 == 0, f"odd PWL token count for {source_name}"
    return [
        (_parse_time_seconds(tokens[idx]), float(tokens[idx + 1]))
        for idx in range(0, len(tokens), 2)
    ]


def _parse_tran_stop_seconds(text: str) -> float:
    match = re.search(r"\btran\s+tran\s+stop=([0-9.]+n?)\b", text)
    assert match, "missing tran stop"
    return _parse_time_seconds(match.group(1))


def _pwl_value_at(points: list[tuple[float, float]], time_s: float) -> float:
    if time_s <= points[0][0]:
        return points[0][1]
    for (t0, y0), (t1, y1) in zip(points, points[1:]):
        if time_s <= t1:
            if t1 == t0:
                return y1
            frac = (time_s - t0) / (t1 - t0)
            return y0 + frac * (y1 - y0)
    return points[-1][1]


def _deck_span_samples(deck: Path) -> list[float]:
    text = deck.read_text()
    vdd = _parse_pwl_wave(text, "Vvdd")
    vss = _parse_pwl_wave(text, "Vvss")
    stop = _parse_tran_stop_seconds(text)
    breakpoints = sorted(
        {0.0, stop}
        | {time for time, _ in vdd if 0.0 <= time <= stop}
        | {time for time, _ in vss if 0.0 <= time <= stop}
    )
    sample_times = set(breakpoints)
    sample_times.update(
        (left + right) / 2.0
        for left, right in zip(breakpoints, breakpoints[1:])
        if right > left
    )
    return [
        _pwl_value_at(vdd, time_s) - _pwl_value_at(vss, time_s)
        for time_s in sorted(sample_times)
    ]


def _deck_contract_fields(deck: Path) -> tuple[list[str], list[str], list[str]]:
    body_lines: list[str] = []
    analyses: list[str] = []
    save_signals: list[str] = []
    for raw_line in deck.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if line in {"simulator lang=spectre", "global 0"}:
            continue
        if line.startswith("ahdl_include"):
            continue
        if line.startswith("simulatorOptions"):
            continue
        if line.startswith("tran "):
            analyses.append(line)
            continue
        if line.startswith("save "):
            save_signals = line.split()[1:]
            continue
        body_lines.append(line)
    return body_lines, analyses, save_signals


def _continuous_local_supply_task_dirs() -> list[Path]:
    return [
        next(TASK_ROOT.glob(f"{task_id}-*"))
        for task_id, _, _ in CONTINUOUS_LOCAL_SUPPLY_CHECKERS
    ]


@pytest.mark.parametrize(
    "task_dir", _continuous_local_supply_task_dirs(), ids=lambda path: path.name
)
def test_265_266_268_canonical_harness_matches_public_and_score_decks(
    task_dir: Path,
) -> None:
    import json

    harness = json.loads((task_dir / "evaluator/harness_spec.json").read_text())
    expected = (
        harness["deck"]["body_lines"],
        harness["deck"]["analyses"],
        harness["deck"]["save_signals"],
    )

    assert _deck_contract_fields(task_dir / "evaluator/score_tb.scs") == expected
    assert _deck_contract_fields(task_dir / "public/task/feedback_tb.scs") == expected
    assert "evas_profile=balanced" in (
        task_dir / "public/task/feedback_tb.scs"
    ).read_text()
    assert "evas_profile=balanced" not in (
        task_dir / "evaluator/score_tb.scs"
    ).read_text()


def _hold_value(time_ns: float, schedule: list[tuple[float, float]]) -> float:
    value = schedule[0][1]
    for start_ns, next_value in schedule:
        if time_ns < start_ns:
            break
        value = next_value
    return value


def _local_supply_values(time_ns: float) -> dict[str, float]:
    return {
        "in0": _hold_value(
            time_ns,
            [(0.0, 0.18), (2.05, 0.74), (4.05, 0.36), (6.05, 0.90), (8.05, 0.24), (10.05, 0.68)],
        ),
        "in1": _hold_value(
            time_ns,
            [(0.0, 0.70), (2.05, 0.28), (4.05, 0.82), (6.05, 0.30), (8.05, 0.76), (10.05, 0.16)],
        ),
        "in2": _hold_value(
            time_ns,
            [(0.0, 0.42), (3.05, 0.86), (6.05, 0.20), (9.05, 0.58)],
        ),
        "in3": _hold_value(
            time_ns,
            [(0.0, 0.12), (3.05, 0.64), (6.05, 0.88), (9.05, 0.32)],
        ),
        "ctrl0": _hold_value(
            time_ns,
            [(0.0, 0.0), (3.05, 0.9), (6.05, 0.0), (9.05, 0.9)],
        ),
        "ctrl1": _hold_value(
            time_ns,
            [(0.0, 0.0), (4.55, 0.9), (8.05, 0.0), (12.05, 0.9)],
        ),
        "vss": _hold_value(
            time_ns,
            [(0.0, -0.04), (4.05, 0.07), (8.05, -0.02), (12.05, 0.05), (14.05, -0.08)],
        ),
        "vdd": _hold_value(
            time_ns,
            [(0.0, 0.94), (5.05, 1.18), (10.05, 0.88), (12.05, 0.56), (14.05, 1.32)],
        ),
        "en": 0.0 if 5.85 <= time_ns < 7.15 else 0.9,
    }


def _continuous_local_supply_rows(
    mode: str,
    *,
    ignore_supply_span: bool,
    stop_ns: float,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for step in range(int(stop_ns / 0.05) + 1):
        time_ns = step * 0.05
        values = _local_supply_values(time_ns)
        expected = _cont_expected(
            mode,
            {**values, "out": 0.0, "flag": 0.0, "metric": 0.0},
        )
        span = values["vdd"] - values["vss"]
        invalid_span = values["en"] > VTH and not (SPAN_MIN <= span <= SPAN_MAX)
        if ignore_supply_span and invalid_span:
            outputs = {"out": 0.45, "flag": 0.9, "metric": 0.45}
        else:
            outputs = expected
        rows.append({"time": time_ns * 1e-9, **values, **outputs})
    return rows


def _rows_202(*, spikes_only: bool = False) -> list[dict[str, float]]:
    windows = {
        "rst": ((0.5, 0.8),),
        "s": ((1.5, 2.5),),
        "sar": ((3.0, 5.4),),
        "clk_sar": ((3.0, 3.25), (3.6, 3.85), (4.2, 4.45)),
        "res": ((6.0, 6.6),),
        "intg": ((8.0, 8.7),),
        "zoom": ((9.2, 10.8),),
        "clk_zoom": ((9.2, 9.45), (9.8, 10.05)),
        "rst_zoom": ((11.0, 11.5),),
    }
    old_probes = {
        "rst": (0.6,),
        "s": (1.8,),
        "sar": (3.4,),
        "clk_sar": (3.1, 3.7, 4.3),
        "res": (6.3,),
        "intg": (8.3,),
        "zoom": (9.6,),
        "clk_zoom": (9.3, 9.9),
        "rst_zoom": (11.2,),
    }
    rows: list[dict[str, float]] = []
    for index in range(4501):
        time_ns = index * 0.01
        phase_ns = time_ns % 32.0
        row = {"time": time_ns * 1e-9}
        for signal, signal_windows in windows.items():
            if spikes_only:
                high = any(abs(phase_ns - probe) <= 0.01 for probe in old_probes[signal])
            else:
                high = any(start <= phase_ns < stop for start, stop in signal_windows)
            row[signal] = 1.1 if high else 0.0
        rows.append(row)
    return rows


def _restore4_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_code = 0
    for index in range(401):
        time_ns = index * 0.01
        if time_ns < 1.05:
            bits = (0, 0, 0, 0)
        elif time_ns < 2.05:
            bits = (1, 0, 1, 0)
        elif time_ns < 3.05:
            bits = (0, 1, 0, 1)
        else:
            bits = (1, 1, 1, 1)
        if any(abs(time_ns - edge) < 0.006 for edge in (0.36, 1.36, 2.36, 3.36)):
            held_code = sum(bit << bit_index for bit_index, bit in enumerate(bits))
        code = sum(bit << bit_index for bit_index, bit in enumerate(bits)) if combinational else held_code
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": _clock(time_ns, 0.36),
                **{f"d{bit_index}": 0.9 * bit for bit_index, bit in enumerate(bits)},
                "vout": (code + 0.5) * 1.8 / 16.0 - 0.9,
            }
        )
    return rows


def _signed_dac_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_total = -15.0
    for index in range(401):
        time_ns = index * 0.01
        if time_ns < 1.05:
            bits = (0, 0, 0, 0)
        elif time_ns < 2.05:
            bits = (0, 1, 0, 1)
        elif time_ns < 3.05:
            bits = (1, 0, 1, 0)
        else:
            bits = (1, 1, 1, 1)
        total = sum((1 if bit else -1) * weight for bit, weight in zip(bits, (1, 2, 4, 8)))
        if any(abs(time_ns - edge) < 0.006 for edge in (0.35, 1.35, 2.35, 3.35)):
            held_total = total
        rows.append(
            {
                "time": time_ns * 1e-9,
                "sh": 1.8 if _clock(time_ns, 0.35) > 0.45 else 0.0,
                **{f"d{bit_index}": 1.8 * bit for bit_index, bit in enumerate(bits)},
                "aout": (total if combinational else held_total) * 1.8 / 16.0,
            }
        )
    return rows


def _bin2ther_rows(*, hardcoded_rails: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(401):
        time_ns = index * 0.01
        vdd = 0.9 if time_ns < 1.65 else (1.2 if time_ns < 2.75 else 0.7)
        b1 = 0.0 if time_ns < 2.05 else 0.9
        b0 = 0.0 if time_ns < 1.05 else (0.9 if time_ns < 2.05 else (0.0 if time_ns < 3.05 else 0.4))
        if hardcoded_rails:
            high, low, threshold = 0.9, 0.0, 0.45
        else:
            high, low, threshold = vdd, 0.0, 0.5 * vdd
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vdd": vdd,
                "gnd": 0.0,
                "b1": b1,
                "b0": b0,
                "t0": high if b1 > threshold else low,
                "t1": high if b1 > threshold else low,
                "t2": high if b0 > threshold else low,
            }
        )
    return rows


def _adc3_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_code = 0
    for index in range(501):
        time_ns = index * 0.01
        vin = 0.02 if time_ns < 1.2 else (0.40 if time_ns < 2.2 else (0.70 if time_ns < 3.2 else 0.99))
        code = max(0, min(7, int(8.0 * vin)))
        if any(abs(time_ns - edge) < 0.006 for edge in (0.5, 1.5, 2.5, 3.5, 4.5)):
            held_code = code
        output_code = code if combinational else held_code
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vin": vin,
                "vclk": _clock(time_ns, 0.5),
                "vd0": 0.9 * (output_code & 1),
                "vd1": 0.9 * ((output_code >> 1) & 1),
                "vd2": 0.9 * ((output_code >> 2) & 1),
            }
        )
    return rows


def _dff_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_high = False
    for index in range(401):
        time_ns = index * 0.01
        vin = -0.4 if time_ns < 1.2 else (0.4 if time_ns < 2.2 else -0.3)
        if any(abs(time_ns - edge) < 0.006 for edge in (0.5, 1.5, 2.5, 3.5)):
            held_high = vin > 0.0
        high = vin > 0.0 if combinational else held_high
        q = 1.0 if high else -1.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vin_d": vin,
                "vclk": _clock(time_ns, 0.5),
                "vout_q": q,
                "vout_qbar": -q,
            }
        )
    return rows


def test_202_accepts_two_complete_legal_frames() -> None:
    assert CHECKER_202(_rows_202())[0]


def test_202_rejects_sparse_probe_spikes() -> None:
    assert not CHECKER_202(_rows_202(spikes_only=True))[0]


def test_207_accepts_held_restore_output_and_rejects_combinational_tracking() -> None:
    assert CHECKER_207(_restore4_rows(combinational=False))[0]
    assert not CHECKER_207(_restore4_rows(combinational=True))[0]


def test_213_accepts_sampled_dac_and_rejects_combinational_tracking() -> None:
    assert CHECKER_213(_signed_dac_rows(combinational=False))[0]
    assert not CHECKER_213(_signed_dac_rows(combinational=True))[0]


def test_219_accepts_local_rails_and_rejects_hardcoded_default_rails() -> None:
    assert CHECKER_219(_bin2ther_rows(hardcoded_rails=False))[0]
    assert not CHECKER_219(_bin2ther_rows(hardcoded_rails=True))[0]


def test_244_accepts_clocked_adc_and_rejects_combinational_tracking() -> None:
    assert CHECKER_244(_adc3_rows(combinational=False))[0]
    assert not CHECKER_244(_adc3_rows(combinational=True))[0]


def test_248_accepts_dff_hold_and_rejects_combinational_tracking() -> None:
    assert CHECKER_248(_dff_rows(combinational=False))[0]
    assert not CHECKER_248(_dff_rows(combinational=True))[0]


@pytest.mark.parametrize(
    "task_dir",
    [
        TASK_ROOT / "265-dynamic-supply-enable-driver",
        TASK_ROOT / "266-local-domain-buffer-translator",
        TASK_ROOT / "268-mode-selected-bias-driver",
    ],
    ids=lambda path: path.name,
)
@pytest.mark.parametrize(
    "deck_rel",
    ["public/task/feedback_tb.scs", "evaluator/score_tb.scs"],
)
def test_265_266_268_decks_cover_low_and_high_invalid_supply_span(
    task_dir: Path, deck_rel: str
) -> None:
    spans = _deck_span_samples(task_dir / deck_rel)

    assert any(span < SPAN_MIN for span in spans), f"missing span below {SPAN_MIN}"
    assert any(span > SPAN_MAX for span in spans), f"missing span above {SPAN_MAX}"
    assert any(SPAN_MIN <= span <= SPAN_MAX for span in spans), "missing valid span"


@pytest.mark.parametrize(
    "task_id, checker, mode",
    CONTINUOUS_LOCAL_SUPPLY_CHECKERS,
    ids=lambda item: str(item) if isinstance(item, int) else getattr(item, "__name__", str(item)),
)
def test_265_266_268_legal_only_trace_does_not_expose_span_gate_omission(
    task_id: int,
    checker,
    mode: str,
) -> None:
    ok, note = checker(
        _continuous_local_supply_rows(mode, ignore_supply_span=True, stop_ns=12.0)
    )
    assert ok, f"task {task_id}: {note}"


@pytest.mark.parametrize(
    "task_id, checker, mode",
    CONTINUOUS_LOCAL_SUPPLY_CHECKERS,
    ids=lambda item: str(item) if isinstance(item, int) else getattr(item, "__name__", str(item)),
)
def test_265_266_268_reject_ignore_span_outputs_after_invalid_span_coverage(
    task_id: int,
    checker,
    mode: str,
) -> None:
    ok, note = checker(
        _continuous_local_supply_rows(mode, ignore_supply_span=False, stop_ns=16.0)
    )
    assert ok, f"task {task_id}: {note}"

    ok, note = checker(
        _continuous_local_supply_rows(mode, ignore_supply_span=True, stop_ns=16.0)
    )
    assert not ok, f"task {task_id} accepted ignore-span outputs"
    assert "observable_mismatch" in note
