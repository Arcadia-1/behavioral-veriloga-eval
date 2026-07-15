"""Task-specific checker for canonical v4 DUT 395."""
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

def check_v4_395_clock_data_valid_qualifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    properties = ["P_RESET_DISABLE_CLEAR", "P_DATA_EDGE_RESTART", "P_CLOCKED_AGE", "P_INCLUSIVE_WINDOW", "P_REGISTERED_METRIC"]
    required = {"time", "clk", "data", "rst", "enable", "valid_out", "edge_age_metric", "qualified"}
    valid, note = _required(rows, required, "v4_395")
    if not valid:
        return False, note or "v4_395 trace_error=unknown"
    mismatches = _new_mismatches(properties)
    coverage = {"inactive_rows": 0, "data_edges": 0, "clock_edges": 0, "age3_samples": 0, "expired_samples": 0}
    seen = False
    age = 4
    previous = rows[0]
    for index, row in enumerate(rows):
        if not _active(row):
            coverage["inactive_rows"] += 1
            seen = False
            age = 4
            if _inactive_settled(rows, index) and (_high(row,"valid_out") or _high(row,"qualified") or abs(float(row["edge_age_metric"])) > 0.04):
                _add(mismatches, "P_RESET_DISABLE_CLEAR", row, "valid=qualified=metric=0", f"valid={int(_high(row,'valid_out'))},qualified={int(_high(row,'qualified'))},metric={row['edge_age_metric']:.4g}", max(abs(float(row["edge_age_metric"])), float(_high(row,"valid_out") or _high(row,"qualified"))))
        else:
            data_edge = index and (_rising(previous,row,"data") or _falling(previous,row,"data"))
            if data_edge:
                seen = True
                age = 0
                coverage["data_edges"] += 1
                sample = _sample_after(rows,index,7e-10)
                if abs(float(sample["edge_age_metric"])) > 0.04:
                    _add(mismatches, "P_DATA_EDGE_RESTART", sample, "age_metric=0 after_data_edge", f"age_metric={sample['edge_age_metric']:.4g}", float(sample["edge_age_metric"]))
            if index and _rising(previous,row,"clk"):
                if seen:
                    age = min(age + 1, 4)
                sample = _sample_after(rows,index)
                coverage["clock_edges"] += 1
                expected_qualified = seen and age <= 3
                expected_metric = 0.9 * min(age,3) / 3.0 if seen else 0.9
                observed_q = _high(sample,"qualified")
                observed_v = _high(sample,"valid_out")
                if expected_qualified != observed_q:
                    property_id = "P_INCLUSIVE_WINDOW" if age == 3 else "P_CLOCKED_AGE"
                    _add(mismatches, property_id, sample, f"qualified={int(expected_qualified)} at_age={age}", f"qualified={int(observed_q)}", 1.0)
                if observed_v != observed_q:
                    _add(mismatches, "P_REGISTERED_METRIC", sample, f"valid_out={int(observed_q)}", f"valid_out={int(observed_v)}", 1.0)
                if abs(float(sample["edge_age_metric"])-expected_metric) > 0.045:
                    _add(mismatches, "P_REGISTERED_METRIC", sample, f"age_metric={expected_metric:.4g} at_age={age}", f"age_metric={sample['edge_age_metric']:.4g}", float(sample["edge_age_metric"])-expected_metric)
                if age == 3:
                    coverage["age3_samples"] += 1
                if age >= 4:
                    coverage["expired_samples"] += 1
        previous = row
    if coverage["data_edges"] < 2:
        _add(mismatches, "P_DATA_EDGE_RESTART", rows[-1], "both_data_edge_polarities", f"data_edges={coverage['data_edges']}", 2-coverage["data_edges"])
    return _finish("v4_395_clock_data_valid_qualifier", properties, mismatches, coverage)

CHECKER_ID = "v4_395_clock_data_valid_qualifier"
CHECKER: Checker = check_v4_395_clock_data_valid_qualifier
