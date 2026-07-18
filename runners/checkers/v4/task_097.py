"""Task-specific checker for canonical v4 DUT 097."""
from __future__ import annotations

from ..api import Checker
import csv
import re
from .stimulus_relative import (
    crossings,
    diagnostic,
    event_label,
    mean_signal,
    pass_note,
    require_signals,
    sample_around_event,
)

PROPERTY_IDS = [
    "P_RESET_IDLE",
    "P_RAMP_MODE",
    "P_CHIRP_MODE",
    "P_BURST_GATE",
    "P_BURST_IDLE",
    "P_CONTROL_DRIVEN_SELECTION",
]

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

def _float_at(row: list[str], index: int, default: float = 0.0) -> float:
    try:
        return float(row[index])
    except (IndexError, TypeError, ValueError):
        return default

def _stream_programmable_stimulus_sequencer_csv(csv_path: Path) -> tuple[float, list[str]]:
    required = {"time", "clk", "rst", "mode", "gate", "out", "metric"}
    runtime = CsvCheckerRuntime(csv_path)
    missing = runtime.missing(required)
    if missing:
        return 0.0, [f"missing {'/'.join(missing)}"]

    sampled_rows, resample_missing = runtime.resampled_rows(required - {"time"}, sample_count=2000)
    if resample_missing:
        return 0.0, ["sequencer_resample_failed " + "/".join(resample_missing)]
    ok, message = check_programmable_stimulus_sequencer(sampled_rows)
    return (1.0 if ok else 0.0), [message]

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

def _dedupe_crossings(crossing_times: list[float], min_spacing_s: float) -> list[float]:
    filtered: list[float] = []
    for crossing in crossing_times:
        if not filtered or crossing - filtered[-1] >= min_spacing_s:
            filtered.append(crossing)
    return filtered

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

def check_programmable_stimulus_sequencer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "mode", "gate", "out", "metric"}
    missing = require_signals(rows, required, "P_CONTROL_DRIVEN_SELECTION")
    if missing:
        return False, missing

    active = [row for row in rows if row["rst"] <= 0.45]
    ramp_rows = [row for row in active if row["mode"] < 0.30]
    sine_rows = [row for row in active if 0.30 <= row["mode"] < 0.60]
    burst_rows = [row for row in active if row["mode"] >= 0.60 and row["gate"] > 0.45]
    gate_low_rows = [row for row in active if row["mode"] >= 0.60 and row["gate"] <= 0.45]
    if min(len(ramp_rows), len(sine_rows), len(burst_rows)) < 6 or len(gate_low_rows) < 3:
        return False, diagnostic(
            "P_CONTROL_DRIVEN_SELECTION",
            "missing_mode_intervals",
            expected="ramp_sine_burst_and_gate_low_intervals",
            observed=f"ramp:{len(ramp_rows)},sine:{len(sine_rows)},burst:{len(burst_rows)},gate_low:{len(gate_low_rows)}",
            event="mode_gate_intervals",
        )

    ramp_drops = sum(
        1 for prev, cur in zip(ramp_rows, ramp_rows[1:]) if cur["out"] < prev["out"] - 0.02
    )
    ramp_delta = ramp_rows[-1]["out"] - ramp_rows[0]["out"]
    # Uniform resampling can retain one boundary-interpolation sample as mode
    # crosses out of the ramp interval. Judge the ramp body, not that boundary.
    if ramp_drops > 1 or ramp_delta < 0.14 or not (0.16 <= ramp_rows[0]["out"] <= 0.30):
        return False, diagnostic(
            "P_RAMP_MODE",
            "ramp_not_monotonic",
            expected="monotonic_ramp_delta_above_0.14_with_one_boundary_sample_tolerated",
            observed=f"drops:{ramp_drops},delta:{ramp_delta:.3f},start:{ramp_rows[0]['out']:.3f}",
            event=event_label("ramp_mode", 0, ramp_rows[0]["time"]),
        )

    sine_vals = [r["out"] for r in sine_rows]
    sine_min = min(sine_vals)
    sine_max = max(sine_vals)
    sine_mean = sum(sine_vals) / len(sine_vals)
    crossing_times: list[float] = []
    for prev, cur in zip(sine_rows, sine_rows[1:]):
        prev_v = prev["out"] - 0.45
        cur_v = cur["out"] - 0.45
        if prev_v == 0.0:
            crossing_times.append(prev["time"])
        elif prev_v * cur_v < 0.0:
            frac = abs(prev_v) / (abs(prev_v) + abs(cur_v))
            crossing_times.append(prev["time"] + frac * (cur["time"] - prev["time"]))
    sine_duration = max(0.0, sine_rows[-1]["time"] - sine_rows[0]["time"])
    crossing_times = _dedupe_crossings(crossing_times, max(0.2e-9, 0.01 * sine_duration))
    center_crossings = len(crossing_times)
    if sine_min > 0.34 or sine_max < 0.56 or abs(sine_mean - 0.45) > 0.05 or center_crossings < 4:
        return False, diagnostic(
            "P_CHIRP_MODE",
            "chirp_segment_wrong",
            expected="centered_chirp_with_at_least_4_center_crossings",
            observed=f"min:{sine_min:.3f},max:{sine_max:.3f},mean:{sine_mean:.3f},crossings:{center_crossings}",
            event=event_label("sine_mode", 0, sine_rows[0]["time"]),
        )
    half_periods = [cur - prev for prev, cur in zip(crossing_times, crossing_times[1:])]
    if len(half_periods) < 3:
        return False, diagnostic(
            "P_CHIRP_MODE",
            "missing_chirp_periods",
            expected="at_least_3_half_periods",
            observed=f"half_periods:{len(half_periods)}",
            event=event_label("sine_mode", 0, sine_rows[0]["time"]),
        )
    early_half_period = sum(half_periods[:2]) / min(2, len(half_periods[:2]))
    late_half_period = sum(half_periods[-2:]) / min(2, len(half_periods[-2:]))
    if late_half_period >= early_half_period * 0.90:
        return False, diagnostic(
            "P_CHIRP_MODE",
            "frequency_not_increasing",
            expected="late_half_period_below_0.9x_early",
            observed=f"early:{early_half_period:.3e},late:{late_half_period:.3e}",
            event=event_label("sine_mode", 0, sine_rows[0]["time"]),
        )

    mode_to_sine = crossings(rows, "mode", threshold=0.30, direction="rising")
    mode_to_burst = crossings(rows, "mode", threshold=0.60, direction="rising")
    if not mode_to_sine or not mode_to_burst:
        return False, diagnostic(
            "P_CONTROL_DRIVEN_SELECTION",
            "missing_mode_crossings",
            expected="observable_mode_crossings_at_0.30_and_0.60",
            observed=f"to_sine:{len(mode_to_sine)},to_burst:{len(mode_to_burst)}",
            event="mode_crossings",
        )
    switch_1_pre, switch_1_post = sample_around_event(
        rows, "out", mode_to_sine[0], step_multiplier=1.0
    )
    switch_2_pre, switch_2_post = sample_around_event(
        rows, "out", mode_to_burst[0], step_multiplier=1.0
    )
    if None in (switch_1_pre, switch_1_post, switch_2_pre, switch_2_post):
        return False, diagnostic(
            "P_CONTROL_DRIVEN_SELECTION",
            "missing_switch_samples",
            expected="samples_around_observed_mode_crossings",
            observed="one_or_more_switch_samples_missing",
            event="mode_crossings",
        )
    assert switch_1_pre is not None
    assert switch_1_post is not None
    assert switch_2_pre is not None
    assert switch_2_post is not None
    switch_1_delta = abs(switch_1_post - switch_1_pre)
    switch_2_delta = abs(switch_2_post - switch_2_pre)
    if switch_1_delta > 0.12 or switch_2_delta > 0.12:
        return False, diagnostic(
            "P_CONTROL_DRIVEN_SELECTION",
            "mode_switch_discontinuity",
            expected="output_delta_across_mode_crossings_below_0.12",
            observed=f"switch_delta:{switch_1_delta:.3f}/{switch_2_delta:.3f}",
            event="mode_crossings",
        )

    burst_vals = [r["out"] for r in burst_rows]
    burst_low = min(burst_vals)
    burst_high = max(burst_vals)
    burst_transitions = sum(
        1
        for prev, cur in zip(burst_vals, burst_vals[1:])
        if (prev <= 0.45 < cur) or (prev >= 0.45 > cur)
    )
    gate_low_mean = sum(r["out"] for r in gate_low_rows) / len(gate_low_rows)
    if burst_low > 0.36 or burst_high < 0.54 or burst_transitions < 2 or abs(gate_low_mean - 0.45) > 0.08:
        return False, diagnostic(
            "P_BURST_GATE",
            "burst_schedule_wrong",
            expected="gated_burst_toggles_and_gate_low_idle_near_0.45",
            observed=(
                f"low:{burst_low:.3f},high:{burst_high:.3f},"
                f"transitions:{burst_transitions},gate_low_mean:{gate_low_mean:.3f}"
            ),
            event=event_label("burst_gate", 0, burst_rows[0]["time"]),
        )

    ramp_metric = mean_signal(ramp_rows, "metric")
    sine_metric = mean_signal(sine_rows, "metric")
    burst_metric = mean_signal(burst_rows, "metric")
    idle_metric = mean_signal(gate_low_rows, "metric")
    if None in (ramp_metric, sine_metric, burst_metric, idle_metric):
        return False, diagnostic(
            "P_CONTROL_DRIVEN_SELECTION",
            "missing_metric_intervals",
            expected="metric_samples_for_each_observed_mode",
            observed="one_or_more_metric_intervals_empty",
            event="mode_gate_intervals",
        )
    assert ramp_metric is not None
    assert sine_metric is not None
    assert burst_metric is not None
    assert idle_metric is not None
    if not (0.12 <= ramp_metric <= 0.30 and 0.42 <= sine_metric <= 0.58 and burst_metric >= 0.70):
        return False, diagnostic(
            "P_CONTROL_DRIVEN_SELECTION",
            "metric_does_not_mark_modes",
            expected="metric_levels_ramp_low_sine_mid_burst_high",
            observed=f"ramp:{ramp_metric:.3f},sine:{sine_metric:.3f},burst:{burst_metric:.3f}",
            event="mode_gate_intervals",
        )
    if idle_metric < 0.55 or idle_metric > burst_metric - 0.05:
        return False, diagnostic(
            "P_BURST_IDLE",
            "idle_metric_wrong",
            expected="idle_metric_between_0.55_and_below_burst_metric",
            observed=f"idle:{idle_metric:.3f},burst:{burst_metric:.3f}",
            event=event_label("gate_low", 0, gate_low_rows[0]["time"]),
        )

    return True, pass_note(
        PROPERTY_IDS,
        "programmable_stimulus_sequencer "
        f"ramp_delta={ramp_delta:.3f} sine={sine_min:.3f}/{sine_max:.3f} "
        f"chirp_half_period={early_half_period:.3e}->{late_half_period:.3e} "
        f"switch={switch_1_delta:.3f}/{switch_2_delta:.3f} "
        f"burst={burst_low:.3f}/{burst_high:.3f} transitions={burst_transitions}",
    )

CHECKER_ID = "v4_097_programmable_stimulus_sequencer"
CHECKER: Checker = check_programmable_stimulus_sequencer
STREAMING_CHECKER = _stream_programmable_stimulus_sequencer_csv
