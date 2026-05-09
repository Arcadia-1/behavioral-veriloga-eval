#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def _avg(rows,col,start,end):
    vals=[r[col] for r in rows if start<=r["time"]<=end]
    return sum(vals)/len(vals) if vals else 0.0

def check_csv(csv_path):
    rows=_rows(csv_path)
    if not rows or not {"time","rst","vin","vout"}.issubset(rows[0]): return {"pass":False,"score":0.0,"notes":["missing time/rst/vin/vout"]}
    reset_avg=_avg(rows,"vout",0,25e-9)
    mid1=_avg(rows,"vout",80e-9,100e-9)
    mid2=_avg(rows,"vout",180e-9,200e-9)
    late=_avg(rows,"vout",260e-9,300e-9)
    ok=reset_avg<0.08 and mid1>0.12 and mid2>mid1+0.08 and late<0.12
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"reset={reset_avg:.3f} mid1={mid1:.3f} mid2={mid2:.3f} late={late:.3f}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
