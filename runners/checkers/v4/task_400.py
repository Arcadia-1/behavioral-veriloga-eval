"""Task-specific checker for canonical v4 DUT 400."""
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

def check_v4_400_downconversion_mixer_lo_polarity(rows: list[dict[str, float]]) -> tuple[bool, str]:
    properties=["P_RESET_DISABLE_CENTER","P_LO_POLARITY_METRICS","P_IQ_CONVERSION","P_OUTPUT_CLAMP","P_POLARITY_QUALIFICATION"]
    required={"time","rf_in","lo_i","lo_q","rst","enable","i_out","q_out","lo_i_metric","lo_q_metric","polarity_ok"}
    valid,note=_required(rows,required,"v4_400")
    if not valid:
        return False,note or "v4_400 trace_error=unknown"
    mismatches=_new_mismatches(properties)
    coverage={"inactive_rows":0,"active_samples":0,"i_toggles":0,"q_toggles":0,"clamp_samples":0}
    i_seen=q_seen=False
    last_transition=-1e99
    previous=rows[0]
    for index,row in enumerate(rows):
        active=_active(row)
        if not active:
            i_seen=q_seen=False
            coverage["inactive_rows"]+=1
            if _inactive_settled(rows, index) and (abs(float(row["i_out"])-VCM)>0.04 or abs(float(row["q_out"])-VCM)>0.04 or abs(float(row["lo_i_metric"]))>0.04 or abs(float(row["lo_q_metric"]))>0.04 or _high(row,"polarity_ok")):
                _add(mismatches,"P_RESET_DISABLE_CENTER",row,"i_out=q_out=0.45,metrics=0,polarity_ok=0",f"i_out={row['i_out']:.4g},q_out={row['q_out']:.4g},mi={row['lo_i_metric']:.4g},mq={row['lo_q_metric']:.4g},ok={int(_high(row,'polarity_ok'))}",max(abs(float(row["i_out"])-VCM),abs(float(row["q_out"])-VCM),abs(float(row["lo_i_metric"])),abs(float(row["lo_q_metric"]))))
        else:
            if index and not _active(previous):
                last_transition=float(row["time"])
            i_toggle=index and _active(previous) and (_rising(previous,row,"lo_i") or _falling(previous,row,"lo_i"))
            q_toggle=index and _active(previous) and (_rising(previous,row,"lo_q") or _falling(previous,row,"lo_q"))
            if i_toggle:
                i_seen=True; coverage["i_toggles"]+=1; last_transition=float(row["time"])
            if q_toggle:
                q_seen=True; coverage["q_toggles"]+=1; last_transition=float(row["time"])
            if float(row["time"])-last_transition>=7e-10 and index%8==0:
                coverage["active_samples"]+=1
                si=1.0 if _high(row,"lo_i") else -1.0
                sq=1.0 if _high(row,"lo_q") else -1.0
                rf=float(row["rf_in"])-VCM
                expected_i=min(VDD,max(VSS,VCM+0.5*rf*si))
                expected_q=min(VDD,max(VSS,VCM+0.5*rf*sq))
                expected_mi=VDD if si>0 else VSS
                expected_mq=VDD if sq>0 else VSS
                if abs(float(row["lo_i_metric"])-expected_mi)>0.05 or abs(float(row["lo_q_metric"])-expected_mq)>0.05:
                    _add(mismatches,"P_LO_POLARITY_METRICS",row,f"mi={expected_mi:.3g},mq={expected_mq:.3g}",f"mi={row['lo_i_metric']:.3g},mq={row['lo_q_metric']:.3g}",max(abs(float(row["lo_i_metric"])-expected_mi),abs(float(row["lo_q_metric"])-expected_mq)))
                if abs(float(row["i_out"])-expected_i)>0.055 or abs(float(row["q_out"])-expected_q)>0.055:
                    _add(mismatches,"P_IQ_CONVERSION",row,f"i={expected_i:.4g},q={expected_q:.4g}",f"i={row['i_out']:.4g},q={row['q_out']:.4g}",max(abs(float(row["i_out"])-expected_i),abs(float(row["q_out"])-expected_q)))
                if not (-0.005<=float(row["i_out"])<=0.905 and -0.005<=float(row["q_out"])<=0.905):
                    _add(mismatches,"P_OUTPUT_CLAMP",row,"i,q in [0,0.9]",f"i={row['i_out']:.4g},q={row['q_out']:.4g}",max(0.0,-float(row["i_out"]),float(row["i_out"])-0.9,-float(row["q_out"]),float(row["q_out"])-0.9))
                if expected_i in (VSS,VDD) or expected_q in (VSS,VDD):
                    coverage["clamp_samples"]+=1
                expected_ok=i_seen and q_seen
                if _high(row,"polarity_ok")!=expected_ok:
                    _add(mismatches,"P_POLARITY_QUALIFICATION",row,f"polarity_ok={int(expected_ok)} i_seen={int(i_seen)} q_seen={int(q_seen)}",f"polarity_ok={int(_high(row,'polarity_ok'))}",1.0)
        previous=row
    if coverage["i_toggles"]<1 or coverage["q_toggles"]<1:
        _add(mismatches,"P_POLARITY_QUALIFICATION",rows[-1],"both_LOs_toggle",f"i_toggles={coverage['i_toggles']},q_toggles={coverage['q_toggles']}",1.0)
    return _finish("v4_400_downconversion_mixer_lo_polarity",properties,mismatches,coverage)

CHECKER_ID = "v4_400_downconversion_mixer_lo_polarity"
CHECKER: Checker = check_v4_400_downconversion_mixer_lo_polarity
