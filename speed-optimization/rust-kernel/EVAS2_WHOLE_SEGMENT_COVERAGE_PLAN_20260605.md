# EVAS2 Whole-Segment Coverage Plan - 2026-06-05

Status: `active plan`

Goal: make release benchmarks run through `evas_engine=evas2`, where a row counts
only if strict whole-segment Rust executes. Python EVAS remains EVAS1.0 and is
not removed; EVAS2 should not silently fall back to Python.

## Baseline Facts

| Source | Fact | Meaning |
|---|---|---|
| 075/076 | `profile_fast_rust_55` top-wall 10 EVAS-only `13.264s -> 3.250s`, `4.08x`, `10/10` safe vs strict EVAS | This is the fastest validated operational speed state. |
| 098 | generic body IR candidates `0/348` compile-ok release `.va` | The generic body-IR path is wired but does not yet cover real release models. |
| 098 | existing whole-segment candidates `257/348` | The compiler can identify many structurally useful segments, but not all are production EVAS2 runtimes. |
| 099 | top blockers: `transition_expr` 344, `event_statement` 321, `event_cross` 272, `complex_if_write_set` 172, `$abstime` 95, `$strobe` 71, `event_timer` 70 | Real models need event, transition, time, branch write-set, and side-effect boundaries together. |
| 100 | event+transition core estimate `255/348`; ordered V1 estimate `268/348`; side-effect-boundary upper estimate `338/348` | The next big coverage jump is whole-segment event+transition, not another small primitive. |
| 101 | source-order planner accepts core `231/348`, ordered V1 `239/348`, side-effect boundary `288/348` | Actual implementation should start from planner-accepted rows, then expand source-order support. |
| 103/104 | shadow `4.52x` slower; production smoke `3.49x` slower | Per-step Rust calls are not the final runtime shape. They are correctness gates only. |

## Definition Of "EVAS2 Runnable"

A benchmark row is EVAS2 runnable only when all of these are true:

1. `evas_engine=evas2` succeeds.
2. Runtime counters show a whole-segment Rust executor was enabled and executed.
3. Python `model.evaluate()` did not own the hot path for that segment.
4. Fallback count is zero for the counted segment.
5. Strict-EVAS parity passes at waveform/checker level.
6. The row is not counted as speed-positive until wall timing beats EVAS1.0 on the same machine and mode.

This separates three concepts that were previously easy to mix:

| Concept | Meaning | Counted as EVAS2 speed? |
|---|---|---|
| Planner candidate | Static source shape looks implementable | no |
| Shadow parity | Rust recomputes while Python still runs production | no |
| Strict production | Rust owns the segment and Python fallback is disabled | yes, if parity and wall both pass |

## Workstreams

| Order | Workstream | Coverage unlocked | Required runtime shape | Acceptance gate |
|---:|---|---|---|---|
| W1 | Event+transition ordered segment core | Planner core rows: `231/348` target pool | One Rust batch owns event due/order, event body state writes, continuous transition output, breakpoint, and required trace for many steps | EVAS2 strict PASS on representative rows; no per-step Python evaluate; no Python fallback |
| W2 | `$abstime` and time-dependent expression input | Measurement, delay, timer math rows blocked by `special_identifier:$abstime` | Rust body program receives time as a typed input, not as a Python callback | Parity on rows with time-dependent state/output |
| W3 | Complex if/write-set lowering | Rows blocked by `complex_if_write_set` 172 | Rust statement IR supports ordered branch writes, partial branch writes, and same-step read-after-write rules | Differential tests for state/output write order |
| W4 | State-owned/dynamic timer queue | Rows blocked by `event_timer` 70 and source-order timer due | Rust owns timer due/reschedule and next breakpoint over a segment | No length-1 timer FFI; CPPLL/ADPLL rows show fewer Python scans |
| W5 | Array/state-machine write-set | SAR, calibration, LFSR, bus-control rows | Typed array state slots with bounded index validation and vector writes | Array parity tests plus real SAR/control rows |
| W6 | Differential/indexed output targets | Rows blocked by `differential_output_target` 65 and indexed output | Rust maps contribution target to node-id slots once, then writes arrays | `V(out, ref)` and bus output rows pass strict EVAS2 |
| W7 | Side-effect boundary | `$strobe`/file IO/string rows; upper planner pool `288/348` then estimator `338/348` | Rust owns numeric state/output; Python receives ordered side-effect events | `strobe.txt` byte/order regression tests pass |
| W8 | Sparse record/trace inside whole segment | Converts kernel speed to E2E wall | Rust returns only checker-required trace columns or sparse event trace | Checker contract preserved; CSV/write time drops without schema break |

## Execution Order

1. Start from W1, not W7. W1 is pure compute and hits the largest useful pool.
2. Use `profile_fast_evas2` to reject unsupported rows instead of silently falling back.
3. For each workstream, first run a static coverage estimate, then shadow parity, then strict production.
4. Promote a workstream only if strict production has both parity and wall evidence.
5. Keep `profile_fast_rust_55` as the fastest operational baseline until EVAS2 coverage and timing beat it.

## First Experiment Slice

The first strict EVAS2 sweep should use three row classes:

| Class | Purpose | Expected result |
|---|---|---|
| Existing whole-segment winners | Prop-delay, SAR, CPPLL, gain measurement-flow | Must continue passing and remain the speed anchor |
| Planner-core event+transition rows | Rows accepted by 101 `event_transition_core` | Should move from unsupported to strict EVAS2 runnable after W1 |
| Known non-candidates | Dynamic timer/source-order/side-effect rows | Must fail as unsupported until the matching workstream lands |

The output table should report:

- total rows;
- EVAS2 runnable rows;
- unsupported rows by blocker tag;
- strict-EVAS parity failures;
- wall speedup vs EVAS1.0 `profile_fast` and vs `profile_fast_rust_55`;
- Rust runtime counters proving no Python hot-path fallback.

## Stop Rules

- If a proposed path keeps Python in the timestep loop and calls Rust once per
  event/check/transition, it belongs in the stop-list unless a real sweep proves
  otherwise.
- If coverage increases but wall time does not improve, do not promote it to
  speed mode; keep it as correctness/coverage infrastructure.
- If a row requires task-name or model-name matching, rewrite it as a semantic
  dataflow matcher before counting it.
