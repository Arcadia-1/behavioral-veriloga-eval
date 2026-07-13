"""Task-specific checker for canonical v4 DUT 088."""
from __future__ import annotations

from checkers.api import Checker
import csv

def _csv_fields(csv_path: Path) -> set[str]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return set(reader.fieldnames or [])

def _float_cell(row: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default

def _stream_cppll_freq_step_reacquire_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"time", "ref_clk", "fb_clk", "lock", "vctrl_mon"}
    if not required.issubset(fields):
        return 0.0, ["missing ref_clk/fb_clk/lock/vctrl_mon"]

    vth = 0.45
    ref_edges: list[float] = []
    fb_edges: list[float] = []
    lock_edges: list[float] = []
    lock_window_total_dt = 0.0
    lock_window_high_dt = 0.0
    vctrl_min = float("inf")
    vctrl_max = float("-inf")
    vctrl_in_range = True
    prev: dict[str, float] | None = None

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur = {
                "time": _float_cell(row, "time"),
                "ref_clk": _float_cell(row, "ref_clk"),
                "fb_clk": _float_cell(row, "fb_clk"),
                "lock": _float_cell(row, "lock"),
                "vctrl_mon": _float_cell(row, "vctrl_mon"),
            }
            vctrl_min = min(vctrl_min, cur["vctrl_mon"])
            vctrl_max = max(vctrl_max, cur["vctrl_mon"])
            if not (-1e-6 <= cur["vctrl_mon"] <= 0.95):
                vctrl_in_range = False
            if prev is not None:
                if prev["ref_clk"] < vth <= cur["ref_clk"]:
                    ref_edges.append(cur["time"])
                if prev["fb_clk"] < vth <= cur["fb_clk"]:
                    fb_edges.append(cur["time"])
                if prev["lock"] < vth <= cur["lock"]:
                    lock_edges.append(cur["time"])
                dt = cur["time"] - prev["time"]
                if dt > 0.0 and 2.05e-6 <= prev["time"] and cur["time"] <= 2.8e-6:
                    lock_window_total_dt += dt
                    if 0.5 * (prev["lock"] + cur["lock"]) > vth:
                        lock_window_high_dt += dt
            prev = cur

    if len(ref_edges) < 12 or len(fb_edges) < 12:
        return 0.0, [f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)}"]

    ref_late = [t for t in ref_edges if 4.5e-6 <= t <= 5.9e-6]
    fb_late = [t for t in fb_edges if 4.5e-6 <= t <= 5.9e-6]
    if len(ref_late) < 4 or len(fb_late) < 4:
        return 0.0, [
            f"not_enough_late_edges ref_late={len(ref_late)} fb_late={len(fb_late)}"
        ]

    ref_periods = [b - a for a, b in zip(ref_late, ref_late[1:])]
    fb_periods = [b - a for a, b in zip(fb_late, fb_late[1:])]
    ref_period = sum(ref_periods) / len(ref_periods)
    fb_period = sum(fb_periods) / len(fb_periods)
    if ref_period <= 0.0 or fb_period <= 0.0:
        return 0.0, ["non_positive_period"]
    freq_ratio = ref_period / fb_period

    pre_lock_edges = [t for t in lock_edges if t < 2.0e-6]
    post_lock_edges = [t for t in lock_edges if 2.2e-6 <= t <= 5.9e-6]
    relock_time = post_lock_edges[0] if post_lock_edges else float("nan")
    lock_high_frac = lock_window_high_dt / max(lock_window_total_dt, 1e-18)
    disturb_low_frac = 1.0 - lock_high_frac
    vctrl_span = vctrl_max - vctrl_min
    ok = (
        bool(pre_lock_edges)
        and disturb_low_frac >= 0.25
        and bool(post_lock_edges)
        and 0.97 <= freq_ratio <= 1.03
        and vctrl_in_range
        and vctrl_span >= 0.02
    )
    return (1.0 if ok else 0.0), [
        f"freq_ratio={freq_ratio:.4f} relock_time={relock_time:.3e} "
        f"disturb_low_frac={disturb_low_frac:.3f} "
        f"vctrl_min={vctrl_min:.3f} vctrl_max={vctrl_max:.3f} "
        f"vctrl_span={vctrl_span:.3f}"
    ]

def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

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

def check_cppll_freq_step_reacquire(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"ref_clk", "fb_clk", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing ref_clk/fb_clk/lock/vctrl_mon"

    vth = 0.45
    times = [r["time"] for r in rows]
    ref_edges = rising_edges([r["ref_clk"] for r in rows], times, threshold=vth)
    fb_edges = rising_edges([r["fb_clk"] for r in rows], times, threshold=vth)
    if len(ref_edges) < 12 or len(fb_edges) < 12:
        return False, f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)}"

    ref_late = [t for t in ref_edges if 4.5e-6 <= t <= 5.9e-6]
    fb_late = [t for t in fb_edges if 4.5e-6 <= t <= 5.9e-6]
    if len(ref_late) < 4 or len(fb_late) < 4:
        return False, (
            f"not_enough_late_edges ref_late={len(ref_late)} fb_late={len(fb_late)}"
        )

    ref_periods = [b - a for a, b in zip(ref_late, ref_late[1:])]
    fb_periods = [b - a for a, b in zip(fb_late, fb_late[1:])]
    ref_period = sum(ref_periods) / len(ref_periods)
    fb_period = sum(fb_periods) / len(fb_periods)
    if ref_period <= 0.0 or fb_period <= 0.0:
        return False, "non_positive_period"
    freq_ratio = ref_period / fb_period

    lock_edges = rising_edges([r["lock"] for r in rows], times, threshold=vth)
    pre_lock_edges = [t for t in lock_edges if t < 2.0e-6]
    post_lock_edges = [t for t in lock_edges if 2.2e-6 <= t <= 5.9e-6]
    relock_time = post_lock_edges[0] if post_lock_edges else float("nan")

    disturb_low_frac = 1.0 - weighted_logic_high_fraction_window(
        rows, "lock", vth, 2.05e-6, 2.8e-6
    )

    vctrl_vals = [r["vctrl_mon"] for r in rows]
    vctrl_min = min(vctrl_vals)
    vctrl_max = max(vctrl_vals)
    vctrl_in_range = all(-1e-6 <= v <= 0.95 for v in vctrl_vals)

    ok = (
        bool(pre_lock_edges)
        and disturb_low_frac >= 0.25
        and bool(post_lock_edges)
        and 0.97 <= freq_ratio <= 1.03
        and vctrl_in_range
    )
    return ok, (
        f"pre_lock_edges={len(pre_lock_edges)} "
        f"disturb_lock_low_frac={disturb_low_frac:.3f} "
        f"post_lock_edges={len(post_lock_edges)} "
        f"late_freq_ratio={freq_ratio:.4f} "
        f"relock_time={(relock_time if post_lock_edges else float('nan')):.3e} "
        f"vctrl_min={vctrl_min:.3f} "
        f"vctrl_max={vctrl_max:.3f}"
    )

CHECKER_ID = "v4_088_cppll_tracking_reacquire_timer"
CHECKER: Checker = check_cppll_freq_step_reacquire
STREAMING_CHECKER = _stream_cppll_freq_step_reacquire_csv
