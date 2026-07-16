"""Task-specific checker for canonical v4 DUT 047."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals
import csv
import re

_INDEXED_ALIAS_TARGETS = ('dout_0',
 'dout0',
 'din_0',
 'din0',
 'ptr_0',
 'cell_en_0',
 'g0',
 'state_0',
 'div_code_0',
 'dout_1',
 'dout1',
 'din_1',
 'din1',
 'ptr_1',
 'cell_en_1',
 'g1',
 'state_1',
 'div_code_1',
 'dout_2',
 'dout2',
 'din_2',
 'din2',
 'ptr_2',
 'cell_en_2',
 'g2',
 'state_2',
 'div_code_2',
 'dout_3',
 'dout3',
 'din_3',
 'din3',
 'ptr_3',
 'cell_en_3',
 'g3',
 'state_3',
 'div_code_3',
 'dout_4',
 'dout4',
 'din_4',
 'din4',
 'ptr_4',
 'cell_en_4',
 'g4',
 'state_4',
 'div_code_4',
 'dout_5',
 'dout5',
 'din_5',
 'din5',
 'ptr_5',
 'cell_en_5',
 'g5',
 'state_5',
 'div_code_5',
 'dout_6',
 'dout6',
 'din_6',
 'din6',
 'ptr_6',
 'cell_en_6',
 'g6',
 'state_6',
 'div_code_6',
 'dout_7',
 'dout7',
 'din_7',
 'din7',
 'ptr_7',
 'cell_en_7',
 'g7',
 'state_7',
 'div_code_7',
 'dout_8',
 'dout8',
 'din_8',
 'din8',
 'ptr_8',
 'cell_en_8',
 'g8',
 'state_8',
 'div_code_8',
 'dout_9',
 'dout9',
 'din_9',
 'din9',
 'ptr_9',
 'cell_en_9',
 'g9',
 'state_9',
 'div_code_9',
 'dout_10',
 'dout10',
 'din_10',
 'din10',
 'ptr_10',
 'cell_en_10',
 'g10',
 'state_10',
 'div_code_10',
 'dout_11',
 'dout11',
 'din_11',
 'din11',
 'ptr_11',
 'cell_en_11',
 'g11',
 'state_11',
 'div_code_11',
 'dout_12',
 'dout12',
 'din_12',
 'din12',
 'ptr_12',
 'cell_en_12',
 'g12',
 'state_12',
 'div_code_12',
 'dout_13',
 'dout13',
 'din_13',
 'din13',
 'ptr_13',
 'cell_en_13',
 'g13',
 'state_13',
 'div_code_13',
 'dout_14',
 'dout14',
 'din_14',
 'din14',
 'ptr_14',
 'cell_en_14',
 'g14',
 'state_14',
 'div_code_14',
 'dout_15',
 'dout15',
 'din_15',
 'din15',
 'ptr_15',
 'cell_en_15',
 'g15',
 'state_15',
 'div_code_15')
_SCALAR_ALIAS_TARGETS = ('vin',
 'vout',
 'vin_sh',
 'rst_n',
 'clk',
 'clk_in',
 'clk_out',
 'lock',
 'ref_clk',
 'fb_clk',
 'vctrl_mon',
 'vinp',
 'vinn',
 'out_p',
 'out_n',
 'outp',
 'outn',
 'a',
 'b',
 'y',
 'd',
 'q',
 'qb',
 'rst',
 'ref',
 'div',
 'up',
 'dn',
 'serial_out',
 'dpn',
 'rstb',
 'en',
 'phase_out',
 'guard_out',
 'delay_out',
 'seen_out',
 'first_err_out',
 'max_err_out',
 'count_out',
 'metric_out',
 'mode',
 'out',
 'vin_i',
 'vout_o')
PROPERTY_IDS = (
    "P_INITIAL_WINDOW_STATE",
    "P_INSIDE_WINDOW_HIGH",
    "P_BOUNDARY_EXCLUSION",
    "P_BIDIRECTIONAL_CROSSINGS",
    "P_RAIL_SMOOTHING",
)

def _float_at(row: list[str], index: int, default: float = 0.0) -> float:
    try:
        return float(row[index])
    except (IndexError, TypeError, ValueError):
        return default

def _canonical_signal_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())

def _signal_alias_candidates(raw_key: str) -> set[str]:
    key = raw_key.strip()
    if not key:
        return set()

    candidates = {key, key.lower()}
    for sep in (":", "."):
        if sep in key:
            tail = key.split(sep)[-1]
            candidates.add(tail)
            candidates.add(tail.lower())

    vm = re.match(r"(?i)^v\(\s*([^)]+)\s*\)$", key)
    if vm:
        inner = vm.group(1).strip()
        candidates.add(inner)
        candidates.add(inner.lower())

    for cand in list(candidates):
        cm = re.match(r"^([A-Za-z_][A-Za-z0-9_$]*)\[(\d+)\]$", cand)
        if cm:
            root = cm.group(1)
            idx = cm.group(2)
            candidates.update(
                {
                    f"{root}_{idx}",
                    f"{root}{idx}",
                    f"{root.lower()}_{idx}",
                    f"{root.lower()}{idx}",
                }
            )
            # Common generated DWA/vector port names use direction suffixes
            # (`ptr_o[0]`, `cell_en_o[0]`, `code_i[0]`). The checkers use
            # scalar observable names (`ptr_0`, `cell_en_0`, `code_0`).
            stripped_root = root.lower()
            for suffix in ("_msb_i", "_lsb_i", "_o", "_i"):
                if stripped_root.endswith(suffix):
                    stripped_root = stripped_root[: -len(suffix)]
                    break
            if stripped_root in {"ptr", "cell_en", "code"}:
                candidates.update(
                    {
                        f"{stripped_root}_{idx}",
                        f"{stripped_root}{idx}",
                    }
                )

        dm = re.search(r"(dout|din|div_code|cell_en|ptr|state|code|bin_o|g|d)_?(\d+)$", cand.lower())
        if dm:
            root = dm.group(1)
            idx = dm.group(2)
            candidates.update(
                {
                    f"{root}_{idx}",
                    f"{root}{idx}",
                }
            )
            if root == "d":
                candidates.update({f"dout_{idx}", f"dout{idx}"})

    return candidates

def _add_canonical_alias_targets(alias_to_index: dict[str, int]) -> None:
    canonical_to_index: dict[str, int] = {}
    for alias, index in alias_to_index.items():
        canonical_to_index.setdefault(_canonical_signal_name(alias), index)
    for target in _INDEXED_ALIAS_TARGETS + _SCALAR_ALIAS_TARGETS:
        ckey = _canonical_signal_name(target)
        if target not in alias_to_index and ckey in canonical_to_index:
            alias_to_index[target] = canonical_to_index[ckey]

class CsvCheckerRuntime:
    """Header-indexed CSV access shared by validated streaming checkers."""

    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path
        self.header, self.index = self._load_header_index(csv_path)

    @staticmethod
    def _load_header_index(csv_path: Path) -> tuple[list[str], dict[str, int]]:
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, [])
        alias_to_index: dict[str, int] = {}
        for idx, name in enumerate(header):
            for alias in _signal_alias_candidates(name):
                alias_to_index.setdefault(alias, idx)
        _add_canonical_alias_targets(alias_to_index)
        return header, alias_to_index

    def missing(self, required: Iterable[str]) -> list[str]:
        return sorted(name for name in required if name not in self.index)

    def rows(self):
        with self.csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            yield from reader

    def require(self, required: Iterable[str]) -> tuple[bool, list[str]]:
        missing = self.missing(required)
        return not missing, missing

    def float(self, row: list[str], key: str, default: float = 0.0) -> float:
        idx = self.index.get(key)
        if idx is None:
            return default
        return _float_at(row, idx, default)

    def value_tuple(self, row: list[str], keys: Iterable[str]) -> tuple[float, ...]:
        return tuple(self.float(row, key) for key in keys)

    def mean_windows(
        self,
        windows: dict[str, tuple[float, float, str]],
    ) -> tuple[dict[str, float], list[str]]:
        accum = {label: [0.0, 0] for label in windows}
        required = {"time"} | {signal for _, _, signal in windows.values()}
        missing = self.missing(required)
        if missing:
            return {}, missing
        for row in self.rows():
            time_s = self.float(row, "time")
            for label, (start, stop, signal) in windows.items():
                if start <= time_s <= stop:
                    bucket = accum[label]
                    bucket[0] += self.float(row, signal)
                    bucket[1] += 1
        means: dict[str, float] = {}
        empty: list[str] = []
        for label, (total, count) in accum.items():
            if count:
                means[label] = total / count
            else:
                empty.append(label)
        return means, empty

    def series(self, signals: Iterable[str]) -> tuple[dict[str, list[float]], list[str]]:
        required = {"time"} | set(signals)
        missing = self.missing(required)
        if missing:
            return {}, missing
        data = {signal: [] for signal in required}
        for row in self.rows():
            for signal in required:
                data[signal].append(self.float(row, signal))
        return data, []

    @staticmethod
    def interpolate_series(times: list[float], values: list[float], target: float) -> float | None:
        if not times or len(times) != len(values):
            return None
        if target < times[0] or target > times[-1]:
            return None
        if target == times[0]:
            return values[0]
        lo = 0
        hi = len(times) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if times[mid] <= target:
                lo = mid
            else:
                hi = mid
        t0 = times[lo]
        t1 = times[hi]
        if t1 <= t0:
            return values[hi]
        alpha = (target - t0) / (t1 - t0)
        return values[lo] + alpha * (values[hi] - values[lo])

    def samples_at(
        self,
        signal: str,
        target_times: Iterable[float],
    ) -> dict[float, float | None]:
        data, missing = self.series({signal})
        targets = list(target_times)
        if missing:
            return {target: None for target in targets}
        times = data["time"]
        values = data[signal]
        return {
            target: self.interpolate_series(times, values, target)
            for target in targets
        }

    def resampled_rows(
        self,
        signals: Iterable[str],
        *,
        sample_count: int,
    ) -> tuple[list[dict[str, float]], list[str]]:
        data, missing = self.series(signals)
        if missing:
            return [], missing
        times = data["time"]
        if len(times) < 2 or sample_count < 2:
            return [], ["invalid_time_range"]
        t0 = times[0]
        t1 = times[-1]
        if t1 <= t0:
            return [], ["invalid_time_range"]
        signal_list = list(signals)
        rows: list[dict[str, float]] = []
        for idx in range(sample_count):
            target = t0 + (t1 - t0) * idx / (sample_count - 1)
            out = {"time": target}
            for signal in signal_list:
                value = self.interpolate_series(times, data[signal], target)
                if value is None:
                    return [], [f"missing_resample_{signal}"]
                out[signal] = value
            rows.append(out)
        return rows, []

def _check_true_window_comparator_resampled(eval_rows: list[dict[str, float]]) -> tuple[bool, str]:
    out_vals = [r["out"] for r in eval_rows]
    lo = min(out_vals)
    hi = max(out_vals)
    span = hi - lo
    if span < 0.3:
        return False, diagnostic(
            "P_RAIL_SMOOTHING",
            "behavior_mismatch",
            expected="out_span>=0.30",
            observed=f"out_span={span:.3f}",
            event="full_trace_resampled",
        )

    vth = lo + 0.5 * span
    t0 = eval_rows[0]["time"]
    t1 = eval_rows[-1]["time"]
    t_mid = 0.5 * (t0 + t1)

    def frac_high(selected: list[dict[str, float]]) -> float:
        if not selected:
            return 0.0
        return sum(1 for row in selected if row["out"] > vth) / len(selected)

    below = [r for r in eval_rows if r["vin"] <= 0.18]
    above = [r for r in eval_rows if r["vin"] >= 0.72]
    inside_rise = [r for r in eval_rows if r["time"] <= t_mid and 0.34 <= r["vin"] <= 0.56]
    inside_fall = [r for r in eval_rows if r["time"] > t_mid and 0.34 <= r["vin"] <= 0.56]

    if min(len(below), len(above), len(inside_rise), len(inside_fall)) < 3:
        return (
            False,
            diagnostic(
                "P_BIDIRECTIONAL_CROSSINGS",
                "insufficient_excitation",
                expected="below,above,inside_rise,inside_fall samples>=3",
                observed=(
                    f"below={len(below)},above={len(above)},"
                    f"rise={len(inside_rise)},fall={len(inside_fall)}"
                ),
                event="vin_regions_resampled",
            ),
        )

    below_hi = frac_high(below)
    above_hi = frac_high(above)
    rise_hi = frac_high(inside_rise)
    fall_hi = frac_high(inside_fall)
    ok = below_hi < 0.10 and above_hi < 0.10 and rise_hi > 0.80 and fall_hi > 0.80
    note = (
        f"below_hi={below_hi:.3f} above_hi={above_hi:.3f} "
        f"inside_rise_hi={rise_hi:.3f} inside_fall_hi={fall_hi:.3f} span={span:.3f}"
    )
    if below_hi >= 0.10 or above_hi >= 0.10:
        return False, diagnostic(
            "P_BOUNDARY_EXCLUSION",
            "behavior_mismatch",
            expected="below_hi<0.10,above_hi<0.10",
            observed=f"below_hi={below_hi:.3f},above_hi={above_hi:.3f}",
            event="outside_window_regions",
        )
    if rise_hi <= 0.80 or fall_hi <= 0.80:
        return False, diagnostic(
            "P_INSIDE_WINDOW_HIGH",
            "behavior_mismatch",
            expected="inside_rise_hi>0.80,inside_fall_hi>0.80",
            observed=f"inside_rise_hi={rise_hi:.3f},inside_fall_hi={fall_hi:.3f}",
            event="inside_window_regions",
        )
    return ok, pass_note(PROPERTY_IDS, note)

def _resample_rows_from_vectors(
    times: list[float],
    signals: dict[str, list[float]],
    *,
    sample_count: int,
) -> tuple[list[dict[str, float]], str | None]:
    if len(times) < 2 or sample_count < 2:
        return [], "invalid_time_range"
    t0 = times[0]
    t1 = times[-1]
    if t1 <= t0:
        return [], "invalid_time_range"
    rows: list[dict[str, float]] = []
    for idx in range(sample_count):
        target = t0 + (t1 - t0) * idx / (sample_count - 1)
        row = {"time": target}
        for signal, values in signals.items():
            value = CsvCheckerRuntime.interpolate_series(times, values, target)
            if value is None:
                return [], f"missing_resample_{signal}"
            row[signal] = value
        rows.append(row)
    return rows, None

def check_true_window_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "out"}
    missing = require_signals(rows, required, "P_INSIDE_WINDOW_HIGH")
    if missing:
        return False, missing

    ordered = sorted(rows, key=lambda row: row["time"])
    times = [row["time"] for row in ordered]
    eval_rows, error = _resample_rows_from_vectors(
        times,
        {
            "vin": [row["vin"] for row in ordered],
            "out": [row["out"] for row in ordered],
        },
        sample_count=361,
    )
    if error is not None:
        return False, diagnostic(
            "P_BIDIRECTIONAL_CROSSINGS",
            "invalid_trace",
            expected="resampleable_time_series",
            observed=error,
            event="full_trace",
        )
    # Spectre may save only adaptive breakpoints even when EVAS writes a dense
    # tran.csv. Judge the window function on a common time grid instead of
    # counting raw output samples.
    return _check_true_window_comparator_resampled(eval_rows)

CHECKER_ID = "v4_047_window_comparator_detector"
CHECKER: Checker = check_true_window_comparator
