#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
PACK_ID = 'background_calibration_accumulator'

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def _nearest(rows,t): return min(rows, key=lambda r: abs(r["time"]-t))
def _avg(rows,col,a,b):
    vals=[r[col] for r in rows if a <= r["time"] <= b]
    return sum(vals)/len(vals) if vals else 0.0

def _edges(rows,col,vth=0.45):
    return [rows[i]["time"] for i in range(1,len(rows)) if rows[i-1].get(col,0.0)<vth<=rows[i].get(col,0.0)]

def check_csv(csv_path):
    rows=_rows(csv_path)
    if not rows: return {"pass":False,"score":0.0,"notes":["empty_csv"]}
    p=PACK_ID
    ok=False; note="unchecked"
    if p=="precision_rectifier":
        neg=_avg(rows,"vout",10e-9,25e-9); pos=_avg(rows,"vout",50e-9,70e-9); ok=neg<0.04 and 0.30<pos<0.40; note=f"neg={neg:.3f} pos={pos:.3f}"
    elif p=="peak_detector":
        pre=_avg(rows,"vout",70e-9,100e-9); rst=_avg(rows,"vout",123e-9,133e-9); late=_avg(rows,"vout",160e-9,175e-9); ok=pre>0.50 and rst<0.08 and late>0.65; note=f"pre={pre:.3f} rst={rst:.3f} late={late:.3f}"
    elif p=="debounce_latch":
        early=_avg(rows,"out",40e-9,60e-9); late=_avg(rows,"out",95e-9,130e-9); ok=early<0.15 and late>0.65; note=f"early={early:.3f} late={late:.3f}"
    elif p=="leaky_hold":
        high=_avg(rows,"vout",25e-9,35e-9); decayed=_avg(rows,"vout",80e-9,100e-9); rst=_avg(rows,"vout",120e-9,135e-9); ok=high>0.55 and 0.15<decayed<high and rst<0.08; note=f"high={high:.3f} decayed={decayed:.3f} rst={rst:.3f}"
    elif p=="edge_detector":
        frac=sum(1 for r in rows if r.get("pulse",0)>0.45)/len(rows); edges=len(_edges(rows,"pulse")); ok=3<=edges<=5 and 0.04<frac<0.20; note=f"pulse_edges={edges} high_frac={frac:.3f}"
    elif p=="segmented_dac":
        vals=[]
        for t in [10e-9,45e-9,75e-9,105e-9,135e-9]:
            r=_nearest(rows,t); vals.append(r["aout"])
        ok=all(vals[i] <= vals[i+1]+0.04 for i in range(len(vals)-1)) and vals[-1]-vals[0]>0.45; note=f"vals={[round(v,3) for v in vals]}"
    elif p in ("cdac_calibration","offset_calibration_fsm","background_calibration_accumulator"):
        col="accum" if p=="background_calibration_accumulator" else "trim"; first=_nearest(rows,85e-9)[col]; mid=_nearest(rows,145e-9)[col]; late=_nearest(rows,205e-9)[col]; ok=first>0.52 and mid<first-0.025 and late>mid+0.025; note=f"first={first:.3f} mid={mid:.3f} late={late:.3f}"
    elif p=="gain_trim_controller":
        first=_nearest(rows,100e-9)["gain_ctrl"]; late=_nearest(rows,170e-9)["gain_ctrl"]; ok=first>0.48 and late<first-0.12; note=f"first={first:.3f} late={late:.3f}"
    elif p in ("rotating_element_selector","element_shuffler"):
        cols=[c for c in rows[0] if c.startswith("sel") or c.startswith("out")]; highs={c:sum(1 for r in rows if r.get(c,0)>0.45) for c in cols}; ok=len(cols)==4 and all(v>5 for v in highs.values()); note=f"highs={highs}"
    elif p=="barrel_pointer_window":
        cols=["win0","win1","win2","win3"]; counts=[sum(1 for c in cols if r.get(c,0)>0.45) for r in rows if r["time"]>20e-9]; ok=counts and min(counts)>=1 and max(counts)<=2 and all(sum(1 for r in rows if r.get(c,0)>0.45)>5 for c in cols); note=f"count_range={(min(counts),max(counts)) if counts else None}"
    elif p=="thermometer_decoder_guarded":
        off=_avg(rows,"th0",5e-9,15e-9); th2=_avg(rows,"th1",65e-9,75e-9); th3=_avg(rows,"th2",90e-9,110e-9); th3off=_avg(rows,"th3",90e-9,110e-9); ok=off<0.1 and th2>0.6 and th3>0.6 and th3off<0.2; note=f"off={off:.3f} th1={th2:.3f} th2={th3:.3f} th3={th3off:.3f}"
    elif p=="first_order_lowpass":
        early=_avg(rows,"vout",30e-9,45e-9); late=_avg(rows,"vout",130e-9,155e-9); ok=0.05<early<0.55 and late>0.65; note=f"early={early:.3f} late={late:.3f}"
    elif p=="slew_rate_limiter":
        early=_avg(rows,"vout",30e-9,45e-9); late=_avg(rows,"vout",100e-9,140e-9); ok=0.05<early<0.45 and late>0.65; note=f"early={early:.3f} late={late:.3f}"
    elif p=="vco_phase_integrator":
        early=len([e for e in _edges(rows,"clk") if e<80e-9]); late=len([e for e in _edges(rows,"clk") if e>100e-9]); span=max(r["phase"] for r in rows)-min(r["phase"] for r in rows); ok=late>=early and late>=3 and span>0.7; note=f"early_edges={early} late_edges={late} phase_span={span:.3f}"
    elif p=="settling_time_measurement_tb":
        early=_avg(rows,"vout",30e-9,45e-9); late=_avg(rows,"vout",130e-9,155e-9); done=_avg(rows,"done",130e-9,155e-9); ok=early<0.45 and late>0.65 and done>0.6; note=f"early={early:.3f} late={late:.3f} done={done:.3f}"
    elif p=="file_metric_writer":
        pre=_avg(rows,"done",5e-9,25e-9); post=_avg(rows,"done",45e-9,85e-9); ok=pre<0.1 and post>0.6; note=f"pre={pre:.3f} post={post:.3f}"
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[note]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
