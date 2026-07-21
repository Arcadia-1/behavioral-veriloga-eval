from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.common.issue109_factory import (
    SPAN_MAX,
    SPAN_MIN,
    VTH,
    _cont_expected,
    check_clocked_output_hold,
)
from checkers.v4.task_250 import CHECKER as CHECKER_250
from checkers.v4.task_251 import CHECKER as CHECKER_251
from checkers.v4.task_252 import CHECKER as CHECKER_252
from checkers.v4.task_253 import CHECKER as CHECKER_253
from checkers.v4.task_254 import CHECKER as CHECKER_254
from checkers.v4.task_255 import CHECKER as CHECKER_255
from checkers.v4.task_256 import CHECKER as CHECKER_256
from checkers.v4.task_257 import CHECKER as CHECKER_257
from checkers.v4.task_258 import CHECKER as CHECKER_258
from checkers.v4.task_259 import CHECKER as CHECKER_259


TASK_250_259_ROOT = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)

CONTINUOUS_FACTORY_CHECKERS = [
    (250, CHECKER_250, "gain"),
    (251, CHECKER_251, "sum"),
    (252, CHECKER_252, "window"),
    (253, CHECKER_253, "mux"),
    (254, CHECKER_254, "gain"),
    (255, CHECKER_255, "window"),
    (256, CHECKER_256, "reduction"),
    (257, CHECKER_257, "phase"),
    (258, CHECKER_258, "priority"),
    (259, CHECKER_259, "reduction"),
]


def _checker_case_id(item: object) -> str:
    if isinstance(item, int):
        return str(item)
    return getattr(item, "__name__", str(item))


def _clocked_rows(
    *,
    inter_edge_glitch: bool,
    continuous_tracking: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for step in range(1601):
        time_ns = step / 100.0
        phase = (time_ns - 0.21) % 1.0
        clk = 0.9 if phase < 0.42 else 0.0
        rst = 0.9 if time_ns < 1.25 or 9.05 <= time_ns < 10.05 else 0.0
        en = 0.0 if 6.85 <= time_ns < 7.85 else 0.9
        in0 = 0.20 if time_ns < 4.5 else 0.70
        out = in0 if continuous_tracking else 0.0
        flag = out
        metric = 0.0
        if inter_edge_glitch and rst < 0.45 and clk < 0.45:
            out = 0.9 - out
            flag = 0.9 - flag
            metric = 0.9 - metric
        rows.append({
            "time": time_ns * 1e-9,
            "clk": clk,
            "rst": rst,
            "in0": in0,
            "in1": 0.70,
            "in2": 0.42,
            "in3": 0.12,
            "ctrl0": 0.9,
            "ctrl1": 0.0,
            "vdd": 0.9,
            "vss": 0.0,
            "en": en,
            "out": out,
            "flag": flag,
            "metric": metric,
        })
    return rows


def test_clocked_outputs_hold_between_update_edges() -> None:
    assert check_clocked_output_hold(
        _clocked_rows(inter_edge_glitch=False), edge=1, task_name="test"
    )[0]


def test_clocked_outputs_reject_inter_edge_glitches() -> None:
    ok, note = check_clocked_output_hold(
        _clocked_rows(inter_edge_glitch=True), edge=1, task_name="test"
    )
    assert not ok
    assert "inter_edge_hold_error" in note


def test_clocked_outputs_reject_continuous_input_tracking() -> None:
    ok, note = check_clocked_output_hold(
        _clocked_rows(inter_edge_glitch=False, continuous_tracking=True),
        edge=1,
        task_name="test",
    )
    assert not ok
    assert "inter_edge_hold_error" in note


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


def _task_250_259_dirs() -> list[Path]:
    return sorted(TASK_250_259_ROOT.glob("25[0-9]-*"))


@pytest.mark.parametrize("task_dir", _task_250_259_dirs(), ids=lambda path: path.name)
def test_250_259_canonical_harness_matches_public_and_score_decks(
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


@pytest.mark.parametrize("task_dir", _task_250_259_dirs(), ids=lambda path: path.name)
@pytest.mark.parametrize(
    "deck_rel",
    ["public/task/feedback_tb.scs", "evaluator/score_tb.scs"],
)
def test_250_259_decks_cover_low_and_high_invalid_supply_span(
    task_dir: Path, deck_rel: str
) -> None:
    spans = _deck_span_samples(task_dir / deck_rel)

    assert any(span < SPAN_MIN for span in spans), f"missing span below {SPAN_MIN}"
    assert any(span > SPAN_MAX for span in spans), f"missing span above {SPAN_MAX}"
    assert any(SPAN_MIN <= span <= SPAN_MAX for span in spans), "missing valid span"


def _hold_value(time_ns: float, schedule: list[tuple[float, float]]) -> float:
    value = schedule[0][1]
    for start_ns, next_value in schedule:
        if time_ns < start_ns:
            break
        value = next_value
    return value


def _continuous_factory_values(time_ns: float) -> dict[str, float]:
    vss = _hold_value(
        time_ns,
        [
            (0.0, 0.03),
            (4.05, -0.06),
            (8.05, 0.02),
            (12.05, 0.05),
            (14.05, -0.08),
        ],
    )
    vdd = _hold_value(
        time_ns,
        [
            (0.0, 0.92),
            (5.05, 1.12),
            (10.05, 0.86),
            (12.05, 0.56),
            (14.05, 1.32),
        ],
    )
    return {
        "in0": _hold_value(
            time_ns,
            [(0.0, 0.18), (2.05, 0.74), (7.05, 0.36), (11.05, 0.82), (13.05, 0.28)],
        ),
        "in1": _hold_value(
            time_ns,
            [(0.0, 0.76), (3.05, 0.24), (9.05, 0.68), (12.55, 0.18), (14.55, 0.80)],
        ),
        "in2": _hold_value(
            time_ns,
            [(0.0, 0.42), (4.55, 0.86), (8.55, 0.22), (13.55, 0.62)],
        ),
        "in3": _hold_value(
            time_ns,
            [(0.0, 0.12), (6.05, 0.58), (10.55, 0.34), (15.05, 0.72)],
        ),
        "ctrl0": _hold_value(
            time_ns,
            [(0.0, 0.0), (2.55, 0.9), (7.55, 0.0), (11.55, 0.9)],
        ),
        "ctrl1": _hold_value(
            time_ns,
            [(0.0, 0.0), (4.55, 0.9), (8.05, 0.0), (12.05, 0.9)],
        ),
        "vdd": vdd,
        "vss": vss,
        "en": 0.0 if 6.85 <= time_ns < 7.85 else 0.9,
    }


def _continuous_factory_rows(
    mode: str,
    *,
    ignore_supply_span: bool,
    stop_ns: float,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for step in range(int(stop_ns / 0.05) + 1):
        time_ns = step * 0.05
        values = _continuous_factory_values(time_ns)
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


@pytest.mark.parametrize(
    "task_id, checker, mode",
    CONTINUOUS_FACTORY_CHECKERS,
    ids=_checker_case_id,
)
def test_250_259_legal_only_trace_does_not_expose_span_gate_omission(
    task_id: int,
    checker,
    mode: str,
) -> None:
    ok, note = checker(
        _continuous_factory_rows(mode, ignore_supply_span=True, stop_ns=12.0)
    )
    assert ok, f"task {task_id}: {note}"


@pytest.mark.parametrize(
    "task_id, checker, mode",
    CONTINUOUS_FACTORY_CHECKERS,
    ids=_checker_case_id,
)
def test_250_259_reject_ignore_span_outputs_after_invalid_span_coverage(
    task_id: int,
    checker,
    mode: str,
) -> None:
    ok, note = checker(
        _continuous_factory_rows(mode, ignore_supply_span=False, stop_ns=16.0)
    )
    assert ok, f"task {task_id}: {note}"

    ok, note = checker(
        _continuous_factory_rows(mode, ignore_supply_span=True, stop_ns=16.0)
    )
    assert not ok, f"task {task_id} accepted ignore-span outputs"
    assert "max_error" in note
