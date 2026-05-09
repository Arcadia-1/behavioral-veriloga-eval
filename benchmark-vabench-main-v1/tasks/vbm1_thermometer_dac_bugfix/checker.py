#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def _nearest(rows,t): return min(rows, key=lambda r: abs(r["time"]-t))

def check_csv(csv_path):
    rows=_rows(csv_path)
    req={"time","aout"}|{f"code_{i}" for i in range(4)}
    if not rows or not req.issubset(rows[0]): return {"pass":False,"score":0.0,"notes":["missing code/aout"]}
    vals=[]
    for idx,t in enumerate([10e-9,30e-9,50e-9,70e-9,90e-9,110e-9,130e-9,150e-9]):
        r=_nearest(rows,t)
        code=sum((1<<i) if r[f"code_{i}"]>0.45 else 0 for i in range(4))
        vals.append((code,r["aout"]))
    ordered=sorted(vals)
    mono=all(ordered[i][1] <= ordered[i+1][1]+0.04 for i in range(len(ordered)-1))
    span=max(v for _,v in vals)-min(v for _,v in vals)
    err=max(abs(v-0.9*code/15.0) for code,v in vals)
    ok=mono and span>0.65 and err<0.08
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"samples={vals} span={span:.3f} max_err={err:.3f} mono={mono}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
