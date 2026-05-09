#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def _rising(rows, col, th=0.45):
    return [rows[i]["time"] for i in range(1, len(rows)) if rows[i-1][col] < th <= rows[i][col]]

def _high_frac(rows, col, th=0.45):
    hi=tot=0.0
    for i in range(1,len(rows)):
        dt=rows[i]["time"]-rows[i-1]["time"]
        if dt<=0: continue
        tot += dt
        if 0.5*(rows[i][col]+rows[i-1][col])>th: hi += dt
    return hi/max(tot,1e-18)

def check_csv(csv_path):
    rows=_rows(csv_path)
    req={"time","trig","pulse"}
    if not rows or not req.issubset(rows[0]):
        return {"pass":False,"score":0.0,"notes":["missing time/trig/pulse"]}
    trig_edges=len(_rising(rows,"trig")); pulse_edges=len(_rising(rows,"pulse")); frac=_high_frac(rows,"pulse")
    ok=trig_edges>=4 and pulse_edges>=4 and 0.015<=frac<=0.16
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"trig_edges={trig_edges} pulse_edges={pulse_edges} pulse_frac={frac:.4f}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
