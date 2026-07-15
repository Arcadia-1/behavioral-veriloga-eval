"""Task-specific checker for canonical v4 DUT 081."""
from __future__ import annotations

from ..api import Checker
import csv
import math

def _csv_header_indices(csv_path: Path) -> tuple[list[str], dict[str, int]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, [])
    return header, {name: idx for idx, name in enumerate(header)}

def _csv_required_indices(csv_path: Path, required: set[str]) -> tuple[dict[str, int] | None, list[str]]:
    header, index = _csv_header_indices(csv_path)
    missing = sorted(required - set(header))
    if missing:
        return None, missing
    return {name: index[name] for name in required}, []

def _float_at(row: list[str], index: int, default: float = 0.0) -> float:
    try:
        return float(row[index])
    except (IndexError, TypeError, ValueError):
        return default

def _stream_edge_ratio(
    csv_path: Path,
    indices: dict[str, int],
    num_signal: str,
    den_signal: str,
    t_start: float,
    t_end: float,
) -> tuple[float, str]:
    prev_num: float | None = None
    prev_den: float | None = None
    num_edges: list[float] = []
    den_edges: list[float] = []
    rows_in_window = 0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            time_s = _float_at(row, indices["time"])
            if time_s < t_start or time_s > t_end:
                continue
            rows_in_window += 1
            num = _float_at(row, indices[num_signal])
            den = _float_at(row, indices[den_signal])
            if prev_num is not None and prev_num < 0.45 <= num:
                num_edges.append(time_s)
            if prev_den is not None and prev_den < 0.45 <= den:
                den_edges.append(time_s)
            prev_num = num
            prev_den = den
    if rows_in_window < 4:
        return float("nan"), "missing_window_or_signals"
    if len(num_edges) < 3 or len(den_edges) < 3:
        return float("nan"), f"not_enough_edges num={len(num_edges)} den={len(den_edges)}"
    num_freq = (len(num_edges) - 1) / max(num_edges[-1] - num_edges[0], 1e-18)
    den_freq = (len(den_edges) - 1) / max(den_edges[-1] - den_edges[0], 1e-18)
    return num_freq / max(den_freq, 1e-18), "ok"

def _stream_weighted_high_fraction_window(
    csv_path: Path,
    indices: dict[str, int],
    signal: str,
    threshold: float,
    t_start: float,
    t_end: float,
) -> float:
    first_t: float | None = None
    last_t: float | None = None
    high_dt = 0.0
    prev_t: float | None = None
    prev_v: float | None = None
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            time_s = _float_at(row, indices["time"])
            if time_s < t_start or time_s > t_end:
                continue
            value = _float_at(row, indices[signal])
            if first_t is None:
                first_t = time_s
            if prev_t is not None and prev_v is not None:
                dt = time_s - prev_t
                if dt > 0.0 and 0.5 * (prev_v + value) > threshold:
                    high_dt += dt
            prev_t = time_s
            prev_v = value
            last_t = time_s
    if first_t is None or last_t is None or last_t <= first_t:
        return 0.0
    return high_dt / (last_t - first_t)

def _stream_adpll_ratio_hop_csv(csv_path: Path) -> tuple[float, list[str]]:
    required = {"time", "ref_clk", "ratio_ctrl", "fb_clk", "vout", "lock", "vctrl_mon"}
    indices, missing = _csv_required_indices(csv_path, required)
    if indices is None:
        return 0.0, [f"missing {'/'.join(missing)}"]
    assert indices is not None

    hop_t = float("nan")
    lock_max = float("-inf")
    vctrl_in_range = True
    prev_ratio: float | None = None
    largest_step = 0.0
    ratio_samples: list[tuple[float, float]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            time_s = _float_at(row, indices["time"])
            ratio_ctrl = _float_at(row, indices["ratio_ctrl"])
            ratio_samples.append((time_s, ratio_ctrl))
            lock = _float_at(row, indices["lock"])
            vctrl = _float_at(row, indices["vctrl_mon"])
            lock_max = max(lock_max, lock)
            if not (-1e-6 <= vctrl <= 1.2):
                vctrl_in_range = False
            if prev_ratio is not None:
                step = abs(ratio_ctrl - prev_ratio)
                if step > largest_step:
                    largest_step = step
                    hop_t = time_s
            prev_ratio = ratio_ctrl

    if (largest_step < 0.5 or not math.isfinite(hop_t)) and len(ratio_samples) >= 2:
        ratio_initial = ratio_samples[0][1]
        ratio_final = ratio_samples[-1][1]
        ratio_delta = ratio_final - ratio_initial
        if abs(ratio_delta) >= 0.5:
            hop_threshold = 0.5 * (ratio_initial + ratio_final)
            for (_prev_t, prev_v), (cur_t, cur_v) in zip(ratio_samples, ratio_samples[1:]):
                if ratio_delta > 0.0 and prev_v <= hop_threshold <= cur_v:
                    hop_t = cur_t
                    break
                if ratio_delta < 0.0 and prev_v >= hop_threshold >= cur_v:
                    hop_t = cur_t
                    break

    if not math.isfinite(hop_t):
        return 0.0, ["ratio_hop_not_detected"]

    def stream_median_signal(signal: str, start: float, stop: float) -> float | None:
        vals: list[float] = []
        with csv_path.open(newline="", encoding="utf-8") as f_inner:
            reader_inner = csv.reader(f_inner)
            next(reader_inner, None)
            for row_inner in reader_inner:
                time_s_inner = _float_at(row_inner, indices["time"])
                if start <= time_s_inner <= stop:
                    vals.append(_float_at(row_inner, indices[signal]))
        if not vals:
            return None
        vals.sort()
        return vals[len(vals) // 2]

    windows = {
        "pre": (hop_t - 1.0e-6, hop_t - 2.0e-7),
        "post": (hop_t + 1.4e-6, hop_t + 2.8e-6),
    }
    pre_target_raw = stream_median_signal("ratio_ctrl", *windows["pre"])
    post_target_raw = stream_median_signal("ratio_ctrl", *windows["post"])
    if pre_target_raw is None or post_target_raw is None:
        return 0.0, ["missing_ratio_ctrl_target_windows"]
    pre_target = max(2, min(16, int(round(pre_target_raw))))
    post_target = max(2, min(16, int(round(post_target_raw))))

    pre_ratio, pre_note = _stream_edge_ratio(csv_path, indices, "vout", "ref_clk", *windows["pre"])
    post_ratio, post_note = _stream_edge_ratio(csv_path, indices, "vout", "ref_clk", *windows["post"])
    pre_div_ratio, pre_div_note = _stream_edge_ratio(csv_path, indices, "vout", "fb_clk", *windows["pre"])
    post_div_ratio, post_div_note = _stream_edge_ratio(csv_path, indices, "vout", "fb_clk", *windows["post"])
    pre_fb_ref_ratio, pre_fb_ref_note = _stream_edge_ratio(csv_path, indices, "fb_clk", "ref_clk", *windows["pre"])
    post_fb_ref_ratio, post_fb_ref_note = _stream_edge_ratio(csv_path, indices, "fb_clk", "ref_clk", *windows["post"])
    if pre_note != "ok":
        return 0.0, [f"pre_window_{pre_note}"]
    if post_note != "ok":
        return 0.0, [f"post_window_{post_note}"]
    if pre_div_note != "ok":
        return 0.0, [f"pre_divider_window_{pre_div_note}"]
    if post_div_note != "ok":
        return 0.0, [f"post_divider_window_{post_div_note}"]
    if pre_fb_ref_note != "ok":
        return 0.0, [f"pre_feedback_window_{pre_fb_ref_note}"]
    if post_fb_ref_note != "ok":
        return 0.0, [f"post_feedback_window_{post_fb_ref_note}"]

    vth = lock_max * 0.5
    pre_lock = _stream_weighted_high_fraction_window(csv_path, indices, "lock", vth, hop_t - 4.0e-7, hop_t - 5.0e-8)
    post_lock = _stream_weighted_high_fraction_window(csv_path, indices, "lock", vth, windows["post"][0] + 3.0e-7, windows["post"][1])
    pre_tol = max(0.30, 0.06 * pre_target)
    post_tol = max(0.35, 0.06 * post_target)
    ok = (
        abs(pre_ratio - pre_target) <= pre_tol
        and abs(post_ratio - post_target) <= post_tol
        and abs(pre_div_ratio - pre_target) <= pre_tol
        and abs(post_div_ratio - post_target) <= post_tol
        and abs(pre_fb_ref_ratio - 1.0) <= 0.15
        and abs(post_fb_ref_ratio - 1.0) <= 0.15
        and pre_lock >= 0.8
        and post_lock >= 0.8
        and vctrl_in_range
    )
    return (1.0 if ok else 0.0), [
        f"hop_t={hop_t:.3e} "
        f"targets={pre_target}->{post_target} "
        f"pre_vout_ref={pre_ratio:.3f} "
        f"post_vout_ref={post_ratio:.3f} "
        f"pre_vout_fb={pre_div_ratio:.3f} "
        f"post_vout_fb={post_div_ratio:.3f} "
        f"pre_fb_ref={pre_fb_ref_ratio:.3f} "
        f"post_fb_ref={post_fb_ref_ratio:.3f} "
        f"pre_lock={pre_lock:.3f} "
        f"post_lock={post_lock:.3f} "
        f"vctrl_range_ok={vctrl_in_range}"
    ]

def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def edge_frequency_ratio(
    rows: list[dict[str, float]],
    num_signal: str,
    den_signal: str,
    t_start: float,
    t_end: float,
) -> tuple[float, str]:
    window = time_window(rows, t_start, t_end)
    if len(window) < 4 or num_signal not in window[0] or den_signal not in window[0]:
        return float("nan"), "missing_window_or_signals"

    times = [r["time"] for r in window]
    num_edges = rising_edges([r[num_signal] for r in window], times)
    den_edges = rising_edges([r[den_signal] for r in window], times)
    if len(num_edges) < 3 or len(den_edges) < 3:
        return float("nan"), f"not_enough_edges num={len(num_edges)} den={len(den_edges)}"

    num_freq = (len(num_edges) - 1) / max(num_edges[-1] - num_edges[0], 1e-18)
    den_freq = (len(den_edges) - 1) / max(den_edges[-1] - den_edges[0], 1e-18)
    return num_freq / max(den_freq, 1e-18), "ok"

def check_adpll_ratio_hop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"ref_clk", "ratio_ctrl", "fb_clk", "vout", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing ref_clk/ratio_ctrl/fb_clk/vout/lock/vctrl_mon"

    ratio_initial = rows[0]["ratio_ctrl"]
    ratio_final = rows[-1]["ratio_ctrl"]
    ratio_delta = ratio_final - ratio_initial
    hop_t = float("nan")
    if abs(ratio_delta) >= 0.5:
        hop_threshold = 0.5 * (ratio_initial + ratio_final)
        for prev, cur in zip(rows, rows[1:]):
            if ratio_delta > 0.0 and prev["ratio_ctrl"] <= hop_threshold <= cur["ratio_ctrl"]:
                hop_t = cur["time"]
                break
            if ratio_delta < 0.0 and prev["ratio_ctrl"] >= hop_threshold >= cur["ratio_ctrl"]:
                hop_t = cur["time"]
                break
    if not math.isfinite(hop_t):
        return False, "ratio_hop_not_detected"

    def median_signal(signal: str, start: float, stop: float) -> float | None:
        vals = sorted(row[signal] for row in rows if start <= row["time"] <= stop)
        if not vals:
            return None
        return vals[len(vals) // 2]

    pre_start = max(rows[0]["time"], hop_t - 1.0e-6)
    pre_stop = hop_t - 2.0e-7
    post_start = hop_t + 1.4e-6
    post_stop = min(rows[-1]["time"], hop_t + 2.8e-6)
    pre_target_raw = median_signal("ratio_ctrl", pre_start, pre_stop)
    post_target_raw = median_signal("ratio_ctrl", post_start, post_stop)
    if pre_target_raw is None or post_target_raw is None:
        return False, "missing_ratio_ctrl_target_windows"
    pre_target = max(2, min(16, int(round(pre_target_raw))))
    post_target = max(2, min(16, int(round(post_target_raw))))

    pre_ratio, pre_note = edge_frequency_ratio(rows, "vout", "ref_clk", pre_start, pre_stop)
    post_ratio, post_note = edge_frequency_ratio(rows, "vout", "ref_clk", post_start, post_stop)
    pre_div_ratio, pre_div_note = edge_frequency_ratio(rows, "vout", "fb_clk", pre_start, pre_stop)
    post_div_ratio, post_div_note = edge_frequency_ratio(rows, "vout", "fb_clk", post_start, post_stop)
    pre_fb_ref_ratio, pre_fb_ref_note = edge_frequency_ratio(rows, "fb_clk", "ref_clk", pre_start, pre_stop)
    post_fb_ref_ratio, post_fb_ref_note = edge_frequency_ratio(rows, "fb_clk", "ref_clk", post_start, post_stop)
    if pre_note != "ok":
        return False, f"pre_window_{pre_note}"
    if post_note != "ok":
        return False, f"post_window_{post_note}"
    if pre_div_note != "ok":
        return False, f"pre_divider_window_{pre_div_note}"
    if post_div_note != "ok":
        return False, f"post_divider_window_{post_div_note}"
    if pre_fb_ref_note != "ok":
        return False, f"pre_feedback_window_{pre_fb_ref_note}"
    if post_fb_ref_note != "ok":
        return False, f"post_feedback_window_{post_fb_ref_note}"

    vth = max(r["lock"] for r in rows) * 0.5 if rows else 0.45
    pre_lock = weighted_logic_high_fraction_window(rows, "lock", vth, hop_t - 4.0e-7, hop_t - 5.0e-8)
    post_lock = weighted_logic_high_fraction_window(rows, "lock", vth, post_start + 3.0e-7, post_stop)
    vctrl_vals = [r["vctrl_mon"] for r in rows]
    vctrl_in_range = all(-1e-6 <= v <= 1.2 for v in vctrl_vals)
    pre_tol = max(0.30, 0.06 * pre_target)
    post_tol = max(0.35, 0.06 * post_target)

    ok = (
        abs(pre_ratio - pre_target) <= pre_tol
        and abs(post_ratio - post_target) <= post_tol
        and abs(pre_div_ratio - pre_target) <= pre_tol
        and abs(post_div_ratio - post_target) <= post_tol
        and abs(pre_fb_ref_ratio - 1.0) <= 0.15
        and abs(post_fb_ref_ratio - 1.0) <= 0.15
        and pre_lock >= 0.8
        and post_lock >= 0.8
        and vctrl_in_range
    )
    return ok, (
        f"hop_t={hop_t:.3e} "
        f"targets={pre_target}->{post_target} "
        f"pre_vout_ref={pre_ratio:.3f} "
        f"post_vout_ref={post_ratio:.3f} "
        f"pre_vout_fb={pre_div_ratio:.3f} "
        f"post_vout_fb={post_div_ratio:.3f} "
        f"pre_fb_ref={pre_fb_ref_ratio:.3f} "
        f"post_fb_ref={post_fb_ref_ratio:.3f} "
        f"pre_lock={pre_lock:.3f} "
        f"post_lock={post_lock:.3f} "
        f"vctrl_range_ok={vctrl_in_range}"
    )

def weighted_logic_high_fraction(rows: list[dict[str, float]], signal: str, threshold: float) -> float:
    if len(rows) < 2:
        return 0.0
    total_dt = rows[-1]["time"] - rows[0]["time"]
    if total_dt <= 0.0:
        return 0.0

    high_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        v_mid = 0.5 * (rows[idx - 1][signal] + rows[idx][signal])
        if v_mid > threshold:
            high_dt += dt
    return high_dt / total_dt

def time_window(rows: list[dict[str, float]], t_start: float, t_end: float) -> list[dict[str, float]]:
    return [r for r in rows if t_start <= r["time"] <= t_end]

def weighted_logic_high_fraction_window(
    rows: list[dict[str, float]],
    signal: str,
    threshold: float,
    t_start: float,
    t_end: float,
) -> float:
    return weighted_logic_high_fraction(time_window(rows, t_start, t_end), signal, threshold)

CHECKER_ID = "v4_081_adpll_ratio_hop_timer"
CHECKER: Checker = check_adpll_ratio_hop
STREAMING_CHECKER = _stream_adpll_ratio_hop_csv
