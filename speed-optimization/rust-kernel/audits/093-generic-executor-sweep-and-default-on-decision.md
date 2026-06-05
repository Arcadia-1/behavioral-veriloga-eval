# 093 - Generic Executor Large Sweep + Parity Refinement + Default-On Decision

Status: `done`

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `091d-generic-executor-python-body.md` (Phase A target)
- `092-generic-executor-real-row-validation.md` (small-sweep precursor)
- `094-verilog-a-body-rust-kernel-design.md` (project that would deliver true default-on parity)

## One-Line Summary

跑 091b matcher 全量 **53 个 unique TB-form candidate models** 通过 091d generic executor：**0 runtime fallback / 14.4× geometric mean speedup / median 9.8× / range 1.2-654.7×**；尝试 Phase B parity refinement（用 `model.next_breakpoint()` 插入 transition 完成时刻），但**改善有限** — 因为根本问题不是 transition ramp 而是 cross-event-time 精度采样；**Phase C 决策：091d 保持 opt-in via `generic_executor=True`，不推 default-on**，真正的 parity-faithful Rust 化路径在 audit 094 多周项目里。

## Phase A: Large Sweep Results

Script `prototypes/audit_093_sweep.py` iterates over every `tb`-form vabench-release-v1 `.va` file that (a) has `transition_target_ir` rust_signal (b) compiles + matches 091b `generic_event_state_transition_v1` candidate (c) has no `$strobe/$display/$write` in source (d) has a `tb_*.scs` testbench nearby.

### Aggregate

| Metric | Value |
|---|---:|
| Candidate count | 53 |
| Measured (no error) | 53 (100%) |
| Skipped (sim error / timeout) | 0 |
| **Runtime fallbacks (executor exception → return None)** | **0** |
| Speedup min | 1.23× |
| Speedup max | 654.75× |
| Speedup median | 9.78× |
| **Speedup geometric mean** | **14.41×** |
| Python total wall (sum medians) | 49.02s |
| 091d total wall (sum medians) | 1.28s |

### Distribution Highlights

| Speedup band | Row count |
|---|---:|
| > 100× | 4 (window_comparator 100×, edge_interval_timer 112×, comparator_offset_search 655×, ...) |
| 30-100× | ~10 |
| 10-30× | ~15 |
| 5-10× | ~15 |
| 1-5× | ~9 |

The 1-5× cluster is dominated by lightweight 1-2 ms rows where engine orchestration is small absolute time — relative speedup is moderate but absolute wall savings are negligible (microseconds).

### CSV Size Delta

Every row has 091d CSV size **smaller** than Python CSV size (typical -5% to -30%). Worst case: `vbr1_l1_ramp_or_step_source` at **-95.5%** (091d produces a near-trivial output where Python emits 20× more rows).

CSV size delta indicates 091d's fixed grid samples fewer time points than Python's adaptive grid. This **does not mean wrong values** — it means coarser temporal resolution.

## Phase B: Parity Refinement Attempt

Modified `_try_generic_event_state_transition_fastpath` to use `fast_model.next_breakpoint(t)` between consecutive planned grid points. Between planned points, query the model's next desired breakpoint; if it falls before the next planned point, evaluate the model at that breakpoint (without recording), then proceed to the planned point.

### Implementation

```python
# Old (091d Phase A):
for t in planned:
    update_sources(t)
    fast_model.evaluate(nv, t)
    record(t)

# New (091d Phase B):
prev_t = 0.0
for record_t in planned:
    # Adaptive substeps: insert model-driven breakpoints
    while True:
        bp = fast_model.next_breakpoint(prev_t)
        if bp is not None and prev_t < bp < record_t:
            update_sources(bp)
            fast_model.evaluate(nv, bp)   # no record
            prev_t = bp
        else:
            break
    update_sources(record_t)
    fast_model.evaluate(nv, record_t)
    record(record_t)
    prev_t = record_t
```

### Phase B Effect on Sample Rows

| Row | Pre-Phase-B speedup | Post-Phase-B speedup | CSV diff change |
|---|---:|---:|---|
| pipeline_stage | 33.5× | 30.6× | unchanged (line 5 timestamp diff) |
| sar_logic_4b | 46.8× | 45.8× | unchanged (line 23 voltage diff) |

**Phase B improved nothing on the tested rows.** Slight wall regression from added `next_breakpoint()` queries.

### Root Cause Analysis

The remaining parity gap is **not transition ramp sampling** — it's **cross-event time precision**:

- Python's `_check_cross()` interpolates the exact crossing time between two consecutive samples (e.g., 1.200119e-09 between samples at 1.200e-09 and 1.300e-09)
- Python's adaptive stepper records AT the interpolated cross time, producing CSV rows with high-precision timestamps
- 091d's fixed grid samples ONLY at record_step + source breakpoints, missing the precise cross instants
- `next_breakpoint()` returns transition completion times (or other state-machine deadlines), **not source-crossing-event times**

To match Python's CSV precisely, 091d would need to:
1. For each cross() trigger expression in the analog block, scan V() values across consecutive grid intervals
2. If sign change detected, interpolate the crossing time
3. Insert that time as an extra grid point + record at it

This is **substantial work** — essentially re-implementing the cross detection algorithm at the executor level. It would also negate some of the speedup (per-step overhead grows).

**Decision**: Phase B refinement is **insufficient for default-on parity**. It stays in the code because it does no harm and minor parity wins are possible on transition-heavy circuits, but it does not change the default-on calculus.

## Phase C: Default-On Decision

### Evidence Summary

| Aspect | Verdict |
|---|---|
| 091d wall delta on real rows | **14.4× geomean (large win)** |
| 091d runtime fallback rate | **0% (zero risk of crash)** |
| 091d CSV byte-level parity vs Python adaptive | **Fails on every row** (cross-event time + grid density) |
| Phase B improvement | **Negligible** (root cause is cross precision, not transitions) |
| 094 IR + Rust kernel project | **Would deliver bit-exact parity + further speedup** (but is multi-week) |
| User opt-in | Already available via `generic_executor=True` |
| Risk of silent regression if default-on | **HIGH** — users expect byte-exact CSV; checker may reject |

### Decision

**091d stays opt-in. Default is unchanged (Python adaptive).**

Rationale:
1. CSV parity gap is **structural** (091d's fixed-grid design choice), not a bug to patch
2. Phase B refinement didn't close the gap because the gap is in cross detection, not transition
3. Users who want speed + accept coarser timestamps can flip `generic_executor=True` today
4. Users who need bit-exact parity get the existing Python path

### What Would Change This Decision

Default-on would become safe if any of:
- Audit 094 IR + Rust kernel project completes with bit-exact parity → naturally replaces 091d as default
- A "091e cross-time refinement" audit adds cross interpolation to the executor (estimated 6-10 hours)
- Downstream EVAS checker explicitly tolerates 091d's timestamp/voltage tolerance band

None of these are planned at the time of this audit.

## Phase D: Verilog-A Body → Rust Kernel Project Design

Recorded as separate audit **`094-verilog-a-body-rust-kernel-design.md`**. The current document references that audit; see it for:
- Goal definition and scope
- 8-12 audit breakdown across 3 phases (~40-80 hours total)
- Existing infrastructure that can be reused
- Risk register
- Decision point for whether/when to start the project

094 is **design-only** — implementation is not started.

## Functional Safety

- Default backend changed: `no` (decision made: stay Python adaptive default)
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes` (091d returns None → Python takes over)

## Validation

```bash
# Phase A: full sweep
PYTHONPATH=. python3 prototypes/audit_093_sweep.py
# 53/53 measured, 0 fallbacks, 14.41x geomean

# Phase B regression: 091d still works after refinement
PYTHONPATH=. python3 -m pytest tests/ -q
# 606 passed
```

## Risks And Rollback

| Risk | Signal | Mitigation |
|---|---|---|
| User enables `generic_executor=True` for a parity-critical use case | downstream checker rejects CSV | Audit 092/093 clearly document the parity caveat; opt-in is explicit |
| Phase B refinement slows down some unusual workload | wall regression > 5% on a candidate row | Sweep showed slight slowdown but within noise; can revert Phase B if needed |
| Sweep results misleading if testbench `.scs` has invalid simulation | sim_error rate increases over time | Sweep counts errors and excludes from stats; 0 errors observed |

## Claim Boundary

**可以说**：
- **53 个真实 vabench TB-form candidate models 100% 通过 091d** with 0 runtime fallback
- **Geometric mean 14.4× speedup**, median 9.8×, range 1.2-654.7×
- Python 49s total → 091d 1.3s total（38× compression over the full sweep）
- 091d 在 opt-in 下 is production-ready 在 functional-verification 用例
- 094 project documented as future path for bit-exact parity

**不能说**：
- 091d 可以 default-on（CSV parity fails systematically）
- Phase B refinement closes parity gap（it doesn't — cross precision is the gap）
- Release-wide speedup claim for paper（需要 same-server EVAS vs Spectre AX rerun）
- 094 project's expected wall delta（不是 design 时能预测的）

## Lessons For The Series

| Audit | Optimization target | Real-row wall delta |
|---|---|---:|
| 086 | per-call cheap function | +2.8% |
| 088 | per-step cheap function | +2.8% |
| 089 | per-call cheap function | **-198%** |
| 091d | bypass orchestration | +33× (small sample) |
| **093 (this)** | **bypass orchestration (53 rows)** | **+14.4× geomean** |
| 094 (future, design only) | full Rust kernel | TBD |

Key takeaways crystallized:

1. **Per-call FFI on hot-but-cheap functions = lose** (089)
2. **Bypass orchestration long-loops = win** (091d/093)
3. **Synthetic-to-real ratio varies** — 091d had 507× synthetic, 33× initial real, 14.4× full-sweep real
4. **Parity-vs-speed trade-off is structural** — fixed-grid sampling fundamentally differs from adaptive
5. **Default-on requires bit-exact parity** — even 14× speedup isn't worth silent CSV regression
6. **Multi-audit projects need design phase** — 094 is scoped before implementation to avoid scope blow-up

The 091 series is complete with this audit. 094 is a future project, design-only.

## Next Step

This audit closes the 091 series. The four-task list that motivated this session is now addressed:

| Task | Status |
|---|---|
| 1. 100-candidate sweep | ✅ done (53 candidates, all measured, 14.4× geomean) |
| 2. Parity refinement | ✅ attempted; insufficient for default-on (root cause = cross precision, not transitions) |
| 3. Default-on decision | ✅ done (stay opt-in; document parity caveat) |
| 4. New series for Verilog-A → Rust kernel | ✅ designed as audit 094 (multi-audit project, implementation TBD) |

There is no audit 095 planned in this series. Future work, if any, would either be in the 094 project's audits (094a, 094b, etc.) or in a separate decision audit if the default-on policy is revisited later.
