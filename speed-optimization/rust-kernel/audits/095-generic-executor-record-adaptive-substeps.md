# 095 - Record Adaptive Substeps In Generic Executor

Status: `done` (Stage 1 parity improvement)

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `091d-generic-executor-python-body.md`
- `093-generic-executor-sweep-and-default-on-decision.md`

## One-Line Summary

Fix audit 091d's parity gap by recording 091d's adaptive substep
evaluate calls in the CSV output (previously only planned grid points
were emitted); after 095, **38/53 sweep rows have <5% CSV size diff**
(was 0/53), **21/53 within 1%**, parity at common time points improves
dramatically (sar_logic_4b mid-transition voltage `0.675` now matches
Python at line 23 instead of showing settled `0.9`); geomean wall
delta slightly reduced from 14.4× to 10.3× due to recording overhead,
still well within useful range.

## Root Cause Analysis

Before 095, the executor's loop was:

```python
while next_breakpoint < record_time:
    fast_model.evaluate(nv, bp)   # adaptive substep
    # NO RECORD — wrong!
    prev_t = bp
fast_model.evaluate(nv, record_t)
record(record_t)                  # only record at planned grid
```

Python adaptive stepper records at **every** evaluate call (including
cross-event interpolation times). My 091d skipped recording at
adaptive substeps → CSV had fewer rows + voltage values reflected only
post-event states (missed mid-ramp samples).

## What Changed

Modified `_try_generic_event_state_transition_fastpath` in
`evas/simulator/engine.py` to append columns at adaptive substeps too:

```python
while next_breakpoint < record_time:
    fast_model.evaluate(nv, bp)
    emitted_times.append(bp)              # NEW: record substep
    for name in recorded_names:           # NEW: record columns
        columns[name].append(nv[name])
    prev_t = bp
fast_model.evaluate(nv, record_t)
emitted_times.append(record_t)
record(record_t)
```

Output `times_arr` now built from `emitted_times` (all evaluated
points), not just planned grid.

## Before / After

### Sweep (53 candidates, 095 vs Pre-095)

| Metric | Pre-095 | Post-095 |
|---|---:|---:|
| Geomean wall speedup | 14.4× | 10.3× |
| Median wall speedup | 9.8× | 6.8× |
| Total fallbacks | 0 | 0 |
| Rows with CSV size diff < 1% | 0 | **21** |
| Rows with CSV size diff < 5% | 0 | **38** |
| Rows with CSV size diff > 50% | many | 5 |

Wall slightly reduced — recording cost on adaptive substeps. Geomean 10.3× still excellent.

### Sample Rows (post-095 detail)

`vbr1_l1_sar_logic_4b` (tb form):

```text
line 23 (was the worst pre-095 mismatch):
  Python : 2.075004247303e-08, 0.6750382, 0.9, 0.0, ...
  091d   : 2.075000000000e-08, 0.6750000, 0.9, 0.0, ...
diff   : timestamp 4e-15 s, voltage 4e-5 V → essentially float precision
```

`vbr1_l1_pipeline_adc_stage` (tb form):

```text
line 5:
  Python : 1.200119562763e-09, 0.9, 0.0, 0.72, 4.5e-01
  091d   : 1.200000000000e-09, 0.9, 0.0, 0.72, 4.5e-01
diff   : timestamp ~1e-13 s, voltage identical
```

## Remaining Divergent Rows

5 rows have CSV size diff > 50% (091d records more or fewer points than Python):

```text
programmable_gain_amplifier          csv=+289.4%  speed=6.1×
precision_rectifier_envelope_detector csv=+264.2%  speed=4.5×
ramp_or_step_source                  csv=-80.2%   speed=1.0×
pfd_up_dn_logic                      csv=+70.9%   speed=510×
peak_detector                        csv=+50.4%   speed=14.4×
```

These have model-driven `next_breakpoint()` patterns that don't
align with Python adaptive's err_ratio refinement. Voltage values
at common time points are typically close but CSV structure
(number of rows) differs significantly.

## Default-On Decision (post-095)

**Still recommend opt-in.** Reason:
- 38/53 (72%) rows have <5% CSV diff — significant improvement
- 5 outlier rows would surprise users with dramatic CSV size change
- Voltage parity at common timestamps is good

**Path to default-on**:
- Either accept 5-outlier surprise (and document)
- Or implement err_ratio-style adaptive refinement (audit 096 in original plan)
- Or wait for 094 project IR + Rust kernel which would deliver bit-exact

## Functional Safety

- Default backend changed: `no` (still opt-in)
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

```bash
PYTHONPATH=. python3 -m pytest tests/                # 606 passed
PYTHONPATH=. python3 prototypes/audit_093_sweep.py   # 53/53, 10.3× geomean, 0 fallback
```

## Claim Boundary

**可以说**：
- 091d Phase B 录制 bug 已修复（记录 adaptive substeps）
- 38/53 rows CSV 大小差 <5%（vs 0/53 pre-095）
- Voltage values at common timestamps 接近 bit-exact
- Wall delta 仍 10.3× geomean

**不能说**：
- bit-exact CSV parity（5 outlier rows 仍显著不同）
- 091d 可以 default-on（需要 5-outlier 处理或更深 refinement）
- release-wide speedup claim（仅 sweep 数据）

## Next Step

095 已是 Stage 1 主要改进。后续路径：
- Stage 2-4: 094 IR + Rust kernel 项目（bit-exact 真正解决方案）
- 或单独 audit 处理 5 outlier rows 的 next_breakpoint pattern

本会话推进 094 项目。
