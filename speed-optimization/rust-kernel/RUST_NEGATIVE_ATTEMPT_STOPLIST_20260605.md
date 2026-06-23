# Rust Negative Attempt Stoplist - 2026-06-05

Status: `active guardrail`

This file marks Rust attempts that were correct, useful for parity, or useful as
diagnostics, but should not be reused as a speed route. The current fastest
validated operational state is still `profile_fast_rust_55`, not the later
per-step event/transition experiments.

## Current Fast State

| Item | Value |
|---|---|
| Fastest validated EVAS-only mode | `profile_fast_rust_55` |
| Evidence | `audits/075-gain-measurement-flow-production-rust.md`, `audits/076-current-rustification-status-after-gain-flow.md` |
| Top-wall 10 result | `profile_fast` `13.264s` -> `profile_fast_rust_55` `3.250s`, `4.08x`, `10/10` safe vs strict EVAS |
| Claim boundary | EVAS-only engineering evidence; not same-server Spectre AX paper-facing speed claim |
| EVAS2 role | `profile_fast_evas2` is a strict coverage gate: unsupported rows fail instead of silently falling back to Python |

## Do Not Repeat

| Audit / attempt | What happened | Why it failed as a speed route | Future directive |
|---|---|---|---|
| 026 static continuous model Rust eval | Functional opt-in Rust static affine evaluate, but microbench exposed slowdown from small per-model FFI calls. | Work per call was too small; Python->Rust boundary cost dominated arithmetic saved inside Rust. | Do not call Rust once per tiny model per step. Batch consecutive models or use whole-segment execution. |
| 035 state-local generated evaluate | Real top-wall profile showed `model_evaluate_s` regressed from `6.0607s` to `6.4126s`; static-branch mixed gain was only about `1%`. | Extra local state/object handling outweighed reduced lookups. | Keep state-local off by default; require real top-wall improvement before promotion. |
| 036 transition unchanged target | Reduced local `transition()` reset work, but top-wall 10 total wall had no stable gain. | Local helper savings were smaller than timestep, record, and transition bookkeeping costs. | Keep as diagnostic/off-by-default only. |
| 045 forced Rust required / simple if lowering | Top-wall forced-Rust runs were slower because coverage did not increase. | Rejection handling and mixed Rust/Python sync cost were paid without moving hot behavior to Rust. | Do not force Rust on rows without an actual production whole-segment candidate. |
| 046 fixed-index state array IR | Correctly lowered fixed array slots, but top-wall remained slower than Python fast. | Fixed-index array access was not the dominant real workload blocker. | Treat as IR coverage, not a speed milestone by itself. |
| 059 per-check timer Rust FFI | CPPLL length-1 timer path slowed down: `2.8293s -> 3.6122s` and `2.6403s -> 3.8000s`. | Tens of thousands of tiny FFI calls paid more overhead than the timer math saved. | Timer acceleration must be queue/segment-level, not per-check FFI. |
| 062 indexed-array side path alone | Fused timer/LFSR/output smoke was correct, but sidecar/indexed-array work alone was not a release-wide speed claim. | Array mirrors still require sync unless the surrounding loop is also fused. | Use indexed arrays only inside a fused runtime or whole-segment executor. |
| 089 cross/above per-call production | Handoff notes record a roughly `3x` slowdown on `cmp_delay`. | `cross()` checks are cheap; per-call ctypes marshalling dominated. | Do not implement detector acceleration as one Rust call per detector per timestep. |
| 094q opt-in full-sim wrapper | Prototype was time-aligned but slower than Python adaptive and rowwise not close enough. | It bypassed the wrong boundary without preserving production parity and amortization. | Do not wire 094q into `engine.py`; keep 091d/whole-segment route as the live base. |
| 096 `rust_transition_production` sweep | 75 real rows: 0 wins, 74 losses, total wall `81.81s -> 152.31s`, geomean `0.56x`. | Per-step transition batching still paid FFI more often than the release workloads could amortize. | Demote to experimental/off-by-default; future transition work must batch across many steps. |
| 103 event-transition shadow runtime | Shadow parity was correct, but tiny fixture wall was `0.0728s -> 0.3292s`, `4.52x` slower. | Shadow intentionally runs both Rust and Python plus array copy/compare. | Use only as correctness/parity gate, never as speed evidence. |
| 104 event-transition production gate | Correct smoke, but tiny fixture wall was `0.0906s -> 0.3157s`, `3.49x` slower. | Python still owned the outer timestep loop, packing, sync, record, and multiple per-step Rust calls. | Do not claim speed until event due/body/transition/breakpoint/record are fused into a whole-segment runtime. |

## Operational Rules

1. Speed experiments that need the fastest current EVAS Rust route should use
   `profile_fast_rust_55`.
2. `profile_fast_evas2` should be used to count strict Rust coverage and expose
   unsupported fallback, not as the current fastest release-wide mode.
3. A new Rust path must report end-to-end wall, subprocess/tran wall, fallback
   count, and strict-EVAS parity before it can be considered for promotion.
4. A new path that calls Rust every timestep must first prove that the per-call
   work is large enough to amortize Python/Rust boundary and state sync costs.
5. New coverage should be semantic/dataflow whole-segment coverage. Do not add
   task-name or model-name special cases unless they are first expressed as a
   reusable candidate family.

## EVAS2 Coverage Expansion Direction

The next useful work is not another per-step primitive. It is increasing the
number of benchmark models that can run under strict whole-segment Rust:

| Priority | Candidate family | Why it matters | Gate |
|---:|---|---|---|
| 1 | Direct static/conditional `transition()` output segment | `transition_expr` is the largest release blocker, and many rows are output-shaping models. | EVAS2 strict PASS, no Python evaluate fallback, waveform/checker parity. |
| 2 | Ordered event + transition segment with crossing-time reads | Covers common comparator, delay, state-machine, and pulse models. | Event order and interpolation parity before production. |
| 3 | State-owned timer / dynamic timer segment | Covers PLL/ADPLL/clock measurement tasks where timer scanning is hot. | Rust owns the queue across many steps, not one FFI per timer check. |
| 4 | Array/state-machine event body segment | Covers SAR, calibration, LFSR, bus/control models. | Typed array write-set parity and bounded index validation. |
| 5 | Sparse record/trace as part of whole-segment output | Converts kernel speed into E2E wall by avoiding Python trace/CSV overhead. | Checker required-signal contract preserved. |

The stop condition for any new EVAS2 candidate is simple: if it cannot skip
Python evaluate and keep the hot loop inside Rust for many events/timepoints, it
is not a speed-route candidate.
