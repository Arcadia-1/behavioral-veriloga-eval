"""Task-specific checker for canonical v4 DUT 394."""
from __future__ import annotations

from ..api import Checker
VTH = 0.45

def _high(row: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(row[signal]) > threshold

def _rising(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) <= threshold < float(current[signal])

def _falling(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) > threshold >= float(current[signal])

def _sample_after(rows: list[dict[str, float]], event_index: int, delay: float = 4e-10) -> dict[str, float]:
    target = float(rows[event_index]["time"]) + delay
    for row in rows[event_index:]:
        if float(row["time"]) >= target:
            return row
    return rows[-1]

def _required(rows: list[dict[str, float]], signals: set[str], task: str) -> tuple[bool, str | None]:
    if not rows:
        return False, f"{task} trace_error=empty_trace"
    missing = sorted(signals - set(rows[0]))
    if missing:
        return False, f"{task} trace_error=missing_signals observed={','.join(missing)}"
    return True, None

def _new_mismatches(properties: list[str]) -> MismatchMap:
    return {property_id: [] for property_id in properties}

def _add(
    mismatches: MismatchMap,
    property_id: str,
    row: dict[str, float],
    expected: str,
    observed: str,
    gap: float,
) -> None:
    if len(mismatches[property_id]) < 24:
        mismatches[property_id].append((float(row["time"]), expected, observed, abs(float(gap))))

def _finish(task: str, properties: list[str], mismatches: MismatchMap, coverage: dict[str, int]) -> tuple[bool, str]:
    parts = [f"task={task}"]
    ok = True
    for property_id in properties:
        items = mismatches[property_id]
        count = len(items)
        if count:
            ok = False
            time, expected, observed, gap = items[0]
            parts.append(
                f"{property_id}:mismatch_count={count} expected={expected} "
                f"observed={observed} time={time:.6e} gap={gap:.6g}"
            )
        else:
            parts.append(
                f"{property_id}:mismatch_count=0 expected=contract_satisfied "
                "observed=contract_satisfied time=NA gap=0"
            )
    parts.append("coverage=" + ",".join(f"{key}:{value}" for key, value in sorted(coverage.items())))
    return ok, " | ".join(parts)

def _active(row: dict[str, float], reset: str = "rst", enable: str = "enable") -> bool:
    return not _high(row, reset) and _high(row, enable)

def _inactive_settled(rows: list[dict[str, float]], index: int, delay: float = 5e-10) -> bool:
    """Require controls to have remained inactive beyond output transition time."""
    target = float(rows[index]["time"]) - delay
    if target < float(rows[0]["time"]):
        return False
    for previous in reversed(rows[: index + 1]):
        if float(previous["time"]) <= target:
            return not _active(previous)
    return False

def check_v4_394_pam4_slicer_gray_decoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    properties = ["P_RESET_DISABLE_CLEAR", "P_RISING_EDGE_SAMPLE_HOLD", "P_PAM4_THRESHOLDS", "P_GRAY_MAPPING", "P_LEVEL_METRIC"]
    required = {"time", "vin", "clk", "rst", "enable", "bit_msb", "bit_lsb", "level_metric", "valid"}
    valid, note = _required(rows, required, "v4_394")
    if not valid:
        return False, note or "v4_394 trace_error=unknown"
    mismatches = _new_mismatches(properties)
    coverage = {"inactive_rows": 0, "samples": 0, "levels": 0, "hold_checks": 0}
    levels_seen: set[int] = set()
    last_sample_outputs: tuple[int, int, float, bool] | None = None
    previous = rows[0]
    for index, row in enumerate(rows):
        if not _active(row):
            coverage["inactive_rows"] += 1
            if _inactive_settled(rows, index) and (_high(row, "bit_msb") or _high(row, "bit_lsb") or abs(float(row["level_metric"])) > 0.04 or _high(row, "valid")):
                _add(mismatches, "P_RESET_DISABLE_CLEAR", row, "bits=00,metric=0,valid=0", f"bits={int(_high(row,'bit_msb'))}{int(_high(row,'bit_lsb'))},metric={row['level_metric']:.4g},valid={int(_high(row,'valid'))}", max(abs(float(row["level_metric"])), float(_high(row,"bit_msb") or _high(row,"bit_lsb") or _high(row,"valid"))))
            last_sample_outputs = None
        elif index and _rising(previous, row, "clk"):
            sample = _sample_after(rows, index)
            vin = float(row["vin"])
            level = 0 if vin < 0.225 else 1 if vin < 0.45 else 2 if vin < 0.675 else 3
            expected_bits = [(0, 0), (0, 1), (1, 1), (1, 0)][level]
            observed_bits = (int(_high(sample, "bit_msb")), int(_high(sample, "bit_lsb")))
            expected_metric = 0.3 * level
            coverage["samples"] += 1
            levels_seen.add(level)
            if observed_bits != expected_bits:
                _add(mismatches, "P_GRAY_MAPPING", sample, f"level={level},bits={expected_bits[0]}{expected_bits[1]}", f"bits={observed_bits[0]}{observed_bits[1]}", abs(2*observed_bits[0]+observed_bits[1]-(2*expected_bits[0]+expected_bits[1])))
                _add(mismatches, "P_PAM4_THRESHOLDS", sample, f"vin={vin:.4g}->level={level}", f"bits={observed_bits[0]}{observed_bits[1]}", 1.0)
            if abs(float(sample["level_metric"]) - expected_metric) > 0.045:
                _add(mismatches, "P_LEVEL_METRIC", sample, f"level_metric={expected_metric:.4g}", f"level_metric={sample['level_metric']:.4g}", float(sample["level_metric"])-expected_metric)
            if not _high(sample, "valid"):
                _add(mismatches, "P_RISING_EDGE_SAMPLE_HOLD", sample, "valid=1 after_enabled_sample", "valid=0", 1.0)
            last_sample_outputs = (*observed_bits, float(sample["level_metric"]), _high(sample, "valid"))
        elif last_sample_outputs is not None and index and (_rising(previous, row, "vin") or _falling(previous, row, "vin")):
            sample = _sample_after(rows, index)
            observed = (int(_high(sample,"bit_msb")), int(_high(sample,"bit_lsb")), float(sample["level_metric"]), _high(sample,"valid"))
            coverage["hold_checks"] += 1
            if observed[:2] != last_sample_outputs[:2] or abs(observed[2]-last_sample_outputs[2]) > 0.04:
                _add(mismatches, "P_RISING_EDGE_SAMPLE_HOLD", sample, f"held={last_sample_outputs[:3]}", f"observed={observed[:3]}", max(abs(observed[2]-last_sample_outputs[2]), float(observed[:2]!=last_sample_outputs[:2])))
        previous = row
    coverage["levels"] = len(levels_seen)
    if len(levels_seen) < 4:
        _add(mismatches, "P_PAM4_THRESHOLDS", rows[-1], "all_four_levels_activated", f"levels={sorted(levels_seen)}", 4-len(levels_seen))
    return _finish("v4_394_pam4_slicer_gray_decoder", properties, mismatches, coverage)

CHECKER_ID = "v4_394_pam4_slicer_gray_decoder"
CHECKER: Checker = check_v4_394_pam4_slicer_gray_decoder
