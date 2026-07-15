"""Task-specific checker for canonical v4 DUT 097."""
from __future__ import annotations

from ..api import Checker
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

    ramp_count = 0
    ramp_drops = 0
    ramp_first: float | None = None
    ramp_last: float | None = None
    sine_count = 0
    sine_min = float("inf")
    sine_max = float("-inf")
    sine_sum = 0.0
    sine_prev_t: float | None = None
    sine_prev_center: float | None = None
    crossing_times: list[float] = []
    burst_count = 0
    burst_min = float("inf")
    burst_max = float("-inf")
    burst_transitions = 0
    burst_prev_out: float | None = None
    gate_low_sum = 0.0
    gate_low_count = 0
    metric_windows = {
        "ramp": (8.0e-9, 22.0e-9, 0.0, 0),
        "sine": (32.0e-9, 56.0e-9, 0.0, 0),
        "burst": (67.0e-9, 75.0e-9, 0.0, 0),
        "idle": (76.5e-9, 79.0e-9, 0.0, 0),
    }

    for row in runtime.rows():
        time_s = runtime.float(row, "time")
        rst = runtime.float(row, "rst")
        gate = runtime.float(row, "gate")
        out = runtime.float(row, "out")
        metric = runtime.float(row, "metric")
        if rst <= 0.45:
            if 6.0e-9 <= time_s <= 24.0e-9:
                ramp_count += 1
                if ramp_first is None:
                    ramp_first = out
                if ramp_last is not None and out < ramp_last - 0.02:
                    ramp_drops += 1
                ramp_last = out
            if 30.0e-9 <= time_s <= 58.0e-9:
                sine_count += 1
                sine_min = min(sine_min, out)
                sine_max = max(sine_max, out)
                sine_sum += out
                cur_center = out - 0.45
                if sine_prev_center is not None and sine_prev_t is not None:
                    if sine_prev_center == 0.0:
                        crossing_times.append(sine_prev_t)
                    elif sine_prev_center * cur_center < 0.0:
                        frac = abs(sine_prev_center) / (abs(sine_prev_center) + abs(cur_center))
                        crossing_times.append(sine_prev_t + frac * (time_s - sine_prev_t))
                sine_prev_t = time_s
                sine_prev_center = cur_center
            if 66.0e-9 <= time_s <= 88.0e-9 and gate > 0.45:
                burst_count += 1
                burst_min = min(burst_min, out)
                burst_max = max(burst_max, out)
                if burst_prev_out is not None and (
                    (burst_prev_out <= 0.45 < out) or (burst_prev_out >= 0.45 > out)
                ):
                    burst_transitions += 1
                burst_prev_out = out
            if 76.0e-9 <= time_s <= 79.5e-9 and gate <= 0.45:
                gate_low_sum += out
                gate_low_count += 1
        for label, (start, stop, total, count) in list(metric_windows.items()):
            if start <= time_s <= stop:
                metric_windows[label] = (start, stop, total + metric, count + 1)

    if min(ramp_count, sine_count, burst_count) < 6 or gate_low_count < 3:
        return 0.0, [
            "sequencer_missing_windows "
            f"ramp={ramp_count} sine={sine_count} burst={burst_count} gate_low={gate_low_count}"
        ]
    assert ramp_first is not None and ramp_last is not None
    ramp_delta = ramp_last - ramp_first
    if ramp_drops or ramp_delta < 0.16 or not (0.16 <= ramp_first <= 0.30):
        return 0.0, [
            "sequencer_ramp_not_monotonic "
            f"drops={ramp_drops} delta={ramp_delta:.3f} start={ramp_first:.3f}"
        ]
    sine_mean = sine_sum / sine_count
    center_crossings = len(crossing_times)
    if sine_min > 0.34 or sine_max < 0.56 or abs(sine_mean - 0.45) > 0.05 or center_crossings < 4:
        return 0.0, [
            "sequencer_chirp_segment_wrong "
            f"min={sine_min:.3f} max={sine_max:.3f} mean={sine_mean:.3f} crossings={center_crossings}"
        ]
    half_periods = [cur - prev for prev, cur in zip(crossing_times, crossing_times[1:])]
    if len(half_periods) < 3:
        return 0.0, [f"sequencer_chirp_missing_periods={len(half_periods)}"]
    early_half_period = sum(half_periods[:2]) / min(2, len(half_periods[:2]))
    late_half_period = sum(half_periods[-2:]) / min(2, len(half_periods[-2:]))
    if late_half_period >= early_half_period * 0.90:
        return 0.0, [
            "sequencer_chirp_frequency_not_increasing "
            f"early_half_period={early_half_period:.3e} late_half_period={late_half_period:.3e}"
        ]

    switch_times = [25.8e-9, 26.3e-9, 61.8e-9, 62.3e-9]
    switch_samples = runtime.samples_at("out", switch_times)
    if any(switch_samples[target] is None for target in switch_times):
        return 0.0, ["sequencer_missing_switch_samples"]
    switch_1_delta = abs(float(switch_samples[26.3e-9]) - float(switch_samples[25.8e-9]))
    switch_2_delta = abs(float(switch_samples[62.3e-9]) - float(switch_samples[61.8e-9]))
    if switch_1_delta > 0.12 or switch_2_delta > 0.12:
        return 0.0, [f"sequencer_mode_switch_discontinuity={switch_1_delta:.3f}/{switch_2_delta:.3f}"]

    gate_low_mean = gate_low_sum / gate_low_count
    if burst_min > 0.36 or burst_max < 0.54 or burst_transitions < 2 or abs(gate_low_mean - 0.45) > 0.08:
        return 0.0, [
            "sequencer_burst_schedule_wrong "
            f"low={burst_min:.3f} high={burst_max:.3f} transitions={burst_transitions} "
            f"gate_low_mean={gate_low_mean:.3f}"
        ]

    metric_means: dict[str, float] = {}
    for label, (_, _, total, count) in metric_windows.items():
        if count == 0:
            return 0.0, ["sequencer_missing_metric_windows"]
        metric_means[label] = total / count
    if not (0.12 <= metric_means["ramp"] <= 0.30 and 0.42 <= metric_means["sine"] <= 0.58 and metric_means["burst"] >= 0.70):
        return 0.0, [
            "sequencer_metric_does_not_mark_modes "
            f"ramp={metric_means['ramp']:.3f} sine={metric_means['sine']:.3f} burst={metric_means['burst']:.3f}"
        ]
    if metric_means["idle"] < 0.55 or metric_means["idle"] > metric_means["burst"] - 0.05:
        return 0.0, [f"sequencer_idle_metric_wrong idle={metric_means['idle']:.3f} burst={metric_means['burst']:.3f}"]

    return 1.0, [
        "programmable_stimulus_sequencer "
        f"ramp_delta={ramp_delta:.3f} sine={sine_min:.3f}/{sine_max:.3f} "
        f"chirp_half_period={early_half_period:.3e}->{late_half_period:.3e} "
        f"switch={switch_1_delta:.3f}/{switch_2_delta:.3f} "
        f"burst={burst_min:.3f}/{burst_max:.3f} transitions={burst_transitions}"
    ]

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

def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_programmable_stimulus_sequencer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "mode", "gate", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/mode/gate/out/metric"

    def window(start: float, stop: float) -> list[dict[str, float]]:
        return [r for r in rows if start <= r["time"] <= stop and r["rst"] <= 0.45]

    ramp_rows = window(6.0e-9, 24.0e-9)
    sine_rows = window(30.0e-9, 58.0e-9)
    burst_rows = [r for r in window(66.0e-9, 88.0e-9) if r["gate"] > 0.45]
    gate_low_rows = [r for r in window(76.0e-9, 79.5e-9) if r["gate"] <= 0.45]
    if min(len(ramp_rows), len(sine_rows), len(burst_rows)) < 6 or len(gate_low_rows) < 3:
        return False, (
            "sequencer_missing_windows "
            f"ramp={len(ramp_rows)} sine={len(sine_rows)} burst={len(burst_rows)} gate_low={len(gate_low_rows)}"
        )

    ramp_drops = sum(
        1 for prev, cur in zip(ramp_rows, ramp_rows[1:]) if cur["out"] < prev["out"] - 0.02
    )
    ramp_delta = ramp_rows[-1]["out"] - ramp_rows[0]["out"]
    if ramp_drops or ramp_delta < 0.16 or not (0.16 <= ramp_rows[0]["out"] <= 0.30):
        return False, (
            "sequencer_ramp_not_monotonic "
            f"drops={ramp_drops} delta={ramp_delta:.3f} start={ramp_rows[0]['out']:.3f}"
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
    center_crossings = len(crossing_times)
    if sine_min > 0.34 or sine_max < 0.56 or abs(sine_mean - 0.45) > 0.05 or center_crossings < 4:
        return False, (
            "sequencer_chirp_segment_wrong "
            f"min={sine_min:.3f} max={sine_max:.3f} mean={sine_mean:.3f} crossings={center_crossings}"
        )
    half_periods = [cur - prev for prev, cur in zip(crossing_times, crossing_times[1:])]
    if len(half_periods) < 3:
        return False, f"sequencer_chirp_missing_periods={len(half_periods)}"
    early_half_period = sum(half_periods[:2]) / min(2, len(half_periods[:2]))
    late_half_period = sum(half_periods[-2:]) / min(2, len(half_periods[-2:]))
    if late_half_period >= early_half_period * 0.90:
        return False, (
            "sequencer_chirp_frequency_not_increasing "
            f"early_half_period={early_half_period:.3e} late_half_period={late_half_period:.3e}"
        )

    switch_1_pre = sample_signal_at(rows, "out", 25.8e-9)
    switch_1_post = sample_signal_at(rows, "out", 26.3e-9)
    switch_2_pre = sample_signal_at(rows, "out", 61.8e-9)
    switch_2_post = sample_signal_at(rows, "out", 62.3e-9)
    if None in (switch_1_pre, switch_1_post, switch_2_pre, switch_2_post):
        return False, "sequencer_missing_switch_samples"
    assert switch_1_pre is not None
    assert switch_1_post is not None
    assert switch_2_pre is not None
    assert switch_2_post is not None
    switch_1_delta = abs(switch_1_post - switch_1_pre)
    switch_2_delta = abs(switch_2_post - switch_2_pre)
    if switch_1_delta > 0.12 or switch_2_delta > 0.12:
        return False, f"sequencer_mode_switch_discontinuity={switch_1_delta:.3f}/{switch_2_delta:.3f}"

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
        return False, (
            "sequencer_burst_schedule_wrong "
            f"low={burst_low:.3f} high={burst_high:.3f} transitions={burst_transitions} "
            f"gate_low_mean={gate_low_mean:.3f}"
        )

    ramp_metric = mean_in_window(rows, "metric", 8.0e-9, 22.0e-9)
    sine_metric = mean_in_window(rows, "metric", 32.0e-9, 56.0e-9)
    burst_metric = mean_in_window(rows, "metric", 67.0e-9, 75.0e-9)
    idle_metric = mean_in_window(rows, "metric", 76.5e-9, 79.0e-9)
    if None in (ramp_metric, sine_metric, burst_metric, idle_metric):
        return False, "sequencer_missing_metric_windows"
    assert ramp_metric is not None
    assert sine_metric is not None
    assert burst_metric is not None
    assert idle_metric is not None
    if not (0.12 <= ramp_metric <= 0.30 and 0.42 <= sine_metric <= 0.58 and burst_metric >= 0.70):
        return False, (
            "sequencer_metric_does_not_mark_modes "
            f"ramp={ramp_metric:.3f} sine={sine_metric:.3f} burst={burst_metric:.3f}"
        )
    if idle_metric < 0.55 or idle_metric > burst_metric - 0.05:
        return False, f"sequencer_idle_metric_wrong idle={idle_metric:.3f} burst={burst_metric:.3f}"

    return True, (
        "programmable_stimulus_sequencer "
        f"ramp_delta={ramp_delta:.3f} sine={sine_min:.3f}/{sine_max:.3f} "
        f"chirp_half_period={early_half_period:.3e}->{late_half_period:.3e} "
        f"switch={switch_1_delta:.3f}/{switch_2_delta:.3f} "
        f"burst={burst_low:.3f}/{burst_high:.3f} transitions={burst_transitions}"
    )

CHECKER_ID = "v4_097_programmable_stimulus_sequencer"
CHECKER: Checker = check_programmable_stimulus_sequencer
STREAMING_CHECKER = _stream_programmable_stimulus_sequencer_csv
