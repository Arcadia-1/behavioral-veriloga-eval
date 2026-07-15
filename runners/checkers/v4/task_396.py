"""Task-specific checker for canonical v4 DUT 396."""
from __future__ import annotations

from ..api import Checker
VTH = 0.45

def _high(row: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(row[signal]) > threshold

def _rising(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) <= threshold < float(current[signal])

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

def check_v4_396_quadrature_lo_generator_divided_clock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    properties = ["P_RESET_DISABLE_CLEAR", "P_QUADRATURE_SEQUENCE", "P_DIVIDE_BY_FOUR", "P_STATE_METRIC", "P_QUAD_OK_DELAY"]
    required = {"time", "clk_in", "rst", "enable", "lo_i", "lo_q", "div_metric", "quad_ok"}
    valid, note = _required(rows, required, "v4_396")
    if not valid:
        return False, note or "v4_396 trace_error=unknown"
    mismatches = _new_mismatches(properties)
    coverage = {"inactive_rows": 0, "clock_edges": 0, "cycles": 0, "state_transitions": 0}
    edge_count = 0
    sequence = [(1,0),(1,1),(0,1),(0,0)]
    observed_states: list[tuple[int,int]] = []
    previous = rows[0]
    for index,row in enumerate(rows):
        if not _active(row):
            coverage["inactive_rows"] += 1
            edge_count = 0
            if _inactive_settled(rows, index) and (_high(row,"lo_i") or _high(row,"lo_q") or abs(float(row["div_metric"])) > 0.04 or _high(row,"quad_ok")):
                _add(mismatches,"P_RESET_DISABLE_CLEAR",row,"lo_i=lo_q=metric=quad_ok=0",f"lo_i={int(_high(row,'lo_i'))},lo_q={int(_high(row,'lo_q'))},metric={row['div_metric']:.4g},quad_ok={int(_high(row,'quad_ok'))}",max(abs(float(row["div_metric"])),float(_high(row,"lo_i") or _high(row,"lo_q") or _high(row,"quad_ok"))))
        elif index and _rising(previous,row,"clk_in"):
            sample=_sample_after(rows,index)
            state_index=edge_count%4
            expected=sequence[state_index]
            observed=(int(_high(sample,"lo_i")),int(_high(sample,"lo_q")))
            expected_metric=0.3*state_index
            expected_ok=edge_count+1>=8
            coverage["clock_edges"]+=1
            observed_states.append(observed)
            if observed!=expected:
                _add(mismatches,"P_QUADRATURE_SEQUENCE",sample,f"state[{state_index}]={expected[0]}{expected[1]}",f"state={observed[0]}{observed[1]}",1.0)
            if abs(float(sample["div_metric"])-expected_metric)>0.045:
                _add(mismatches,"P_STATE_METRIC",sample,f"div_metric={expected_metric:.4g}",f"div_metric={sample['div_metric']:.4g}",float(sample["div_metric"])-expected_metric)
            if _high(sample,"quad_ok")!=expected_ok:
                _add(mismatches,"P_QUAD_OK_DELAY",sample,f"quad_ok={int(expected_ok)} after_edges={edge_count+1}",f"quad_ok={int(_high(sample,'quad_ok'))}",1.0)
            edge_count+=1
            coverage["cycles"]=max(coverage["cycles"],edge_count//4)
        previous=row
    coverage["state_transitions"]=len(set(observed_states))
    if coverage["cycles"]<2 or len(set(observed_states))<4:
        _add(mismatches,"P_DIVIDE_BY_FOUR",rows[-1],"two_cycles_and_four_states",f"cycles={coverage['cycles']},states={len(set(observed_states))}",max(2-coverage["cycles"],4-len(set(observed_states))))
    return _finish("v4_396_quadrature_lo_generator_divided_clock",properties,mismatches,coverage)

CHECKER_ID = "v4_396_quadrature_lo_generator_divided_clock"
CHECKER: Checker = check_v4_396_quadrature_lo_generator_divided_clock
