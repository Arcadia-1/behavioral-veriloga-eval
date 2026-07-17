"""Task-specific checker for canonical v4 DUT 399."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_diagnostic_contract
VTH = 0.45

def _high(row: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(row[signal]) > threshold

def _rising(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) <= threshold < float(current[signal])

def _falling(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) > threshold >= float(current[signal])

def _crossing_time(
    previous: dict[str, float],
    current: dict[str, float],
    signal: str,
    threshold: float,
) -> float:
    before = float(previous[signal])
    after = float(current[signal])
    if after == before:
        return float(current["time"])
    fraction = (threshold - before) / (after - before)
    return float(previous["time"]) + fraction * (
        float(current["time"]) - float(previous["time"])
    )

def _value_at_time(
    previous: dict[str, float],
    current: dict[str, float],
    signal: str,
    time_s: float,
) -> float:
    duration = float(current["time"]) - float(previous["time"])
    if duration <= 0.0:
        return float(current[signal])
    fraction = (time_s - float(previous["time"])) / duration
    fraction = max(0.0, min(1.0, fraction))
    return float(previous[signal]) + fraction * (
        float(current[signal]) - float(previous[signal])
    )

def _sample_after(rows: list[dict[str, float]], event_index: int, delay: float = 4e-10) -> dict[str, float] | None:
    target = float(rows[event_index]["time"]) + delay
    for sample_index, row in enumerate(rows[event_index:], start=event_index):
        if float(row["time"]) >= target:
            previous = rows[event_index]
            for current in rows[event_index + 1 : sample_index + 1]:
                controls_changed = (
                    _rising(previous, current, "clk")
                    or _falling(previous, current, "vdd_sense", 0.64)
                    or _rising(previous, current, "vdd_sense", 0.72)
                    or _rising(previous, current, "rst")
                    or _falling(previous, current, "rst")
                    or _rising(previous, current, "enable")
                    or _falling(previous, current, "enable")
                )
                if controls_changed:
                    return None
                previous = current
            return row
    return None

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

def check_v4_399_supply_supervisor_brownout_por(rows: list[dict[str, float]]) -> tuple[bool, str]:
    properties=["P_RESET_DISABLE_SAFE","P_UVLO_HYSTERESIS","P_RELEASE_DELAY","P_DIP_RESTART","P_STATE_METRICS"]
    required={"time","vdd_sense","clk","rst","enable","por_n","pgood","brownout","delay_metric","state_metric"}
    valid,note=_required(rows,required,"v4_399")
    if not valid:
        return False,note or "v4_399 trace_error=unknown"
    mismatches=_new_mismatches(properties)
    coverage={"inactive_rows":0,"clock_edges":0,"rise_crossings":0,"fall_crossings":0,"released_samples":0}
    brown=True
    count=0
    released=False
    state=0
    previous=rows[0]
    for index,row in enumerate(rows):
        active=_active(row)
        if not active:
            brown=True; count=0; released=False; state=0
            coverage["inactive_rows"]+=1
        else:
            events: list[tuple[float, str]] = []
            if index and _falling(previous,row,"vdd_sense",0.64):
                events.append((_crossing_time(previous, row, "vdd_sense", 0.64), "fall"))
            if index and _rising(previous,row,"vdd_sense",0.72):
                events.append((_crossing_time(previous, row, "vdd_sense", 0.72), "rise"))
            if index and _rising(previous,row,"clk"):
                events.append((_crossing_time(previous, row, "clk", VTH), "clock"))
            events.sort()
            for event_time, event_kind in events:
                if event_kind == "fall":
                    brown=True; count=0; released=False; state=1
                    coverage["fall_crossings"]+=1
                elif event_kind == "rise":
                    brown=False; count=0; released=False; state=2
                    coverage["rise_crossings"]+=1
                else:
                    coverage["clock_edges"]+=1
                    vdd_at_event = _value_at_time(
                        previous, row, "vdd_sense", event_time
                    )
                    if vdd_at_event < 0.64:
                        brown=True; count=0; released=False; state=1
                    elif not brown and vdd_at_event >= 0.72:
                        count=min(count+1,4)
                        released=count>=4
                        state=3 if released else 2
            event = bool(events)
            sample=_sample_after(rows,index,2.5e-10) if event else row
            if released:
                coverage["released_samples"]+=1
            if event and sample is not None:
                expected_por=released
                expected_brown=brown
                expected_delay=0.9*count/4.0
                expected_state=0.3*state
                if _high(sample,"por_n")!=expected_por or _high(sample,"pgood")!=expected_por:
                    _add(mismatches,"P_RELEASE_DELAY",sample,f"por_n=pgood={int(expected_por)} count={count}",f"por_n={int(_high(sample,'por_n'))},pgood={int(_high(sample,'pgood'))}",1.0)
                if _high(sample,"brownout")!=expected_brown:
                    pid="P_DIP_RESTART" if any(kind == "fall" for _, kind in events) else "P_UVLO_HYSTERESIS"
                    _add(mismatches,pid,sample,f"brownout={int(expected_brown)}",f"brownout={int(_high(sample,'brownout'))}",1.0)
                if any(kind == "fall" for _, kind in events) and (_high(sample,"por_n") or _high(sample,"pgood") or abs(float(sample["delay_metric"]))>0.05):
                    _add(mismatches,"P_DIP_RESTART",sample,"por_n=pgood=delay_metric=0 after_uvlo_fall",f"por_n={int(_high(sample,'por_n'))},pgood={int(_high(sample,'pgood'))},delay={sample['delay_metric']:.4g}",max(abs(float(sample["delay_metric"])),float(_high(sample,"por_n") or _high(sample,"pgood"))))
                if abs(float(sample["delay_metric"])-expected_delay)>0.05 or abs(float(sample["state_metric"])-expected_state)>0.05:
                    _add(mismatches,"P_STATE_METRICS",sample,f"delay={expected_delay:.4g},state={expected_state:.4g}",f"delay={sample['delay_metric']:.4g},state={sample['state_metric']:.4g}",max(abs(float(sample["delay_metric"])-expected_delay),abs(float(sample["state_metric"])-expected_state)))
        if not active:
            if _inactive_settled(rows, index) and (_high(row,"por_n") or _high(row,"pgood") or not _high(row,"brownout") or abs(float(row["delay_metric"]))>0.04 or abs(float(row["state_metric"]))>0.04):
                _add(mismatches,"P_RESET_DISABLE_SAFE",row,"por_n=pgood=metrics=0,brownout=1",f"por_n={int(_high(row,'por_n'))},pgood={int(_high(row,'pgood'))},brownout={int(_high(row,'brownout'))},delay={row['delay_metric']:.4g},state={row['state_metric']:.4g}",max(abs(float(row["delay_metric"])),abs(float(row["state_metric"])),float(_high(row,"por_n") or _high(row,"pgood") or not _high(row,"brownout"))))
        previous=row
    if coverage["rise_crossings"]<1:
        _add(mismatches,"P_UVLO_HYSTERESIS",rows[-1],"uvlo_rise_crossing_activated",f"crossings={coverage['rise_crossings']}",1.0)
    if coverage["fall_crossings"]<1:
        _add(mismatches,"P_DIP_RESTART",rows[-1],"uvlo_fall_crossing_activated",f"crossings={coverage['fall_crossings']}",1.0)
    return _finish("v4_399_supply_supervisor_brownout_por",properties,mismatches,coverage)

CHECKER_ID = "v4_399_supply_supervisor_brownout_por"
CHECKER: Checker = with_diagnostic_contract(check_v4_399_supply_supervisor_brownout_por)
