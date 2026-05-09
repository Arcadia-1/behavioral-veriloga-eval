#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

def _rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return [{k.lower(): float(v) for k, v in row.items() if v not in ("", None)} for row in csv.DictReader(f)]

def check_csv(csv_path):
    rows=_rows(csv_path)
    if not rows or not {"time","lock"}.issubset(rows[0]): return {"pass":False,"score":0.0,"notes":["missing time/lock"]}
    early=[r["lock"] for r in rows if r["time"]<120e-9]
    late=[r["lock"] for r in rows if r["time"]>220e-9]
    if not early or not late: return {"pass":False,"score":0.0,"notes":["insufficient windows"]}
    early_high=sum(1 for v in early if v>0.45)/len(early); late_high=sum(1 for v in late if v>0.45)/len(late)
    ok=early_high<0.15 and late_high>0.75
    return {"pass":ok,"score":1.0 if ok else 0.0,"notes":[f"early_high={early_high:.3f} late_high={late_high:.3f}"]}

if __name__ == "__main__": print(json.dumps(check_csv(sys.argv[1]), indent=2))
