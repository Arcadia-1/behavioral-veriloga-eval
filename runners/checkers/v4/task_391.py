"""Task-specific checker for canonical v4 DUT 391."""
from __future__ import annotations

from ..api import Checker
VCM = 0.45
VDD = 0.9
VSS = 0.0
VTH = 0.45

def _high(row: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(row[signal]) > threshold

def _rising(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) <= threshold < float(current[signal])

def _falling(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) > threshold >= float(current[signal])

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

def check_v4_391_lc_vco_behavioral_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    properties = ["P_RESET_DISABLE_CENTER", "P_CONTROL_FREQUENCY_MAP", "P_COMPLEMENTARY_AMPLITUDE", "P_METRIC_REPORTING", "P_VALID_AFTER_TWO_CYCLES"]
    required = {"time", "vctrl", "enable", "rst", "osc_p", "osc_n", "freq_metric", "amp_metric", "valid"}
    valid, note = _required(rows, required, "v4_391")
    if not valid:
        return False, note or "v4_391 trace_error=unknown"
    mismatches = _new_mismatches(properties)
    coverage = {"inactive_rows": 0, "active_samples": 0, "periods": 0, "valid_low_samples": 0, "valid_high_samples": 0}
    previous = rows[0]
    rising_edges: list[tuple[float, float]] = []
    enable_start: float | None = None
    last_osc_transition = -1e99
    last_ctrl_transition = -1e99
    half_edges = 0
    for index, row in enumerate(rows):
        if not _active(row):
            coverage["inactive_rows"] += 1
            enable_start = None
            half_edges = 0
            if _inactive_settled(rows, index) and (abs(float(row["osc_p"]) - VCM) > 0.04 or abs(float(row["osc_n"]) - VCM) > 0.04 or abs(float(row["freq_metric"])) > 0.04 or abs(float(row["amp_metric"])) > 0.04 or _high(row, "valid")):
                _add(mismatches, "P_RESET_DISABLE_CENTER", row, "osc_p=osc_n=0.45,metrics=0,valid=0", f"osc_p={row['osc_p']:.4g},osc_n={row['osc_n']:.4g},freq_metric={row['freq_metric']:.4g},amp_metric={row['amp_metric']:.4g},valid={int(_high(row,'valid'))}", max(abs(float(row["osc_p"])-VCM), abs(float(row["osc_n"])-VCM), abs(float(row["freq_metric"])), abs(float(row["amp_metric"]))))
        else:
            if enable_start is None:
                enable_start = float(row["time"])
                rising_edges = []
            if index and not _active(previous):
                last_ctrl_transition = float(row["time"])
            if abs(float(row["vctrl"]) - float(previous["vctrl"])) > 0.01:
                last_ctrl_transition = float(row["time"])
            osc_transition = _rising(previous, row, "osc_p", VCM) or _falling(previous, row, "osc_p", VCM)
            if osc_transition:
                last_osc_transition = float(row["time"])
                half_edges += 1
            if _rising(previous, row, "osc_p", VCM):
                rising_edges.append((float(row["time"]), float(row["vctrl"])))
            if len(rising_edges) >= 2:
                t0, ctrl0 = rising_edges[-2]
                t1, ctrl1 = rising_edges[-1]
                if abs(ctrl1 - ctrl0) < 0.03:
                    period = t1 - t0
                    ctrl = min(VDD, max(VSS, 0.5 * (ctrl0 + ctrl1)))
                    expected_period = 1.0 / (5e6 + 20e6 * ctrl / VDD)
                    coverage["periods"] += 1
                    if abs(period - expected_period) > max(3e-9, 0.13 * expected_period):
                        _add(mismatches, "P_CONTROL_FREQUENCY_MAP", row, f"period={expected_period:.6g}", f"period={period:.6g}", period - expected_period)
            outputs_settled = float(row["time"]) - last_osc_transition >= 7e-10
            metric_settled = outputs_settled and last_osc_transition > last_ctrl_transition
            if int(float(row["time"]) / 1e-9) % 3 == 0 and outputs_settled:
                coverage["active_samples"] += 1
                ctrl = min(VDD, max(VSS, float(row["vctrl"])))
                if metric_settled and (abs(float(row["freq_metric"]) - ctrl) > 0.04 or abs(float(row["amp_metric"]) - 0.4) > 0.04):
                    _add(mismatches, "P_METRIC_REPORTING", row, f"freq_metric={ctrl:.4g},amp_metric=0.4", f"freq_metric={row['freq_metric']:.4g},amp_metric={row['amp_metric']:.4g}", max(abs(float(row["freq_metric"])-ctrl), abs(float(row["amp_metric"])-0.4)))
                observed_amp = abs(float(row["osc_p"])-VCM)
                if observed_amp >= 0.32 and (abs((float(row["osc_p"]) + float(row["osc_n"])) - 0.9) > 0.07 or abs(observed_amp-0.4) > 0.07):
                    _add(mismatches, "P_COMPLEMENTARY_AMPLITUDE", row, "osc_p+osc_n=0.9,half_amplitude=0.4", f"sum={float(row['osc_p'])+float(row['osc_n']):.4g},amp={abs(float(row['osc_p'])-VCM):.4g}", max(abs(float(row["osc_p"])+float(row["osc_n"])-0.9), abs(abs(float(row["osc_p"])-VCM)-0.4)))
                observed = _high(row, "valid")
                expected_valid = half_edges >= 4
                if expected_valid:
                    coverage["valid_high_samples"] += 1
                else:
                    coverage["valid_low_samples"] += 1
                if observed != expected_valid:
                    _add(mismatches, "P_VALID_AFTER_TWO_CYCLES", row, f"valid={int(expected_valid)} after_half_edges={half_edges}", f"valid={int(observed)}", 1.0)
        previous = row
    if coverage["periods"] < 3:
        _add(mismatches, "P_CONTROL_FREQUENCY_MAP", rows[-1], "at_least_3_measured_periods", f"periods={coverage['periods']}", 3-coverage["periods"])
    return _finish("v4_391_lc_vco_behavioral_source", properties, mismatches, coverage)

CHECKER_ID = "v4_391_lc_vco_behavioral_source"
CHECKER: Checker = check_v4_391_lc_vco_behavioral_source
