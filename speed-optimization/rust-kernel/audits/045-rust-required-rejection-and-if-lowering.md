# 045 - Rust Required Rejection Audit And If Lowering

Date: 2026-06-04

## Purpose

This audit answers why the current Rust static-evaluate path does not yet speed
up real top-wall vaBench models. The change adds compile-time rejection counters
for models that cannot become Rust static-linear evaluate IR, then implements a
conservative lowering for simple `if/else` statements.

## Code Changes

1. `EVAS/evas/simulator/backend.py`
   - Adds `_evaluate_ir_static_linear_rejections` metadata to compiled models.
   - Records structural rejection reasons such as event statements, dynamic
     branches, array assignment targets, unsupported binary operations,
     `transition()` calls, and self-dependent state updates.
   - Lowers only simple `if/else` forms where both branches contain matching
     static-linear targets. This is equivalent to a conditional expression:
     `target = cond ? then_linear : else_linear`.

2. `EVAS/evas/simulator/engine.py`
   - Adds `rust_static_eval_no_candidate_*` performance counters.
   - Reports why a model had no static-linear Rust candidate instead of silently
     falling back to Python.

3. `EVAS/tests/test_engine.py`
   - Adds rejection-counter tests for `transition()` and `@(cross...)`.
   - Adds Rust/Python parity tests for simple `if/else` contribution lowering.
   - Adds Rust/Python parity tests for simple `if/else` state assignment
     followed by a state-read contribution.

## Validation

Local:

```text
PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_reports_transition_rejection_reason \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_reports_event_rejection_reason \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_lowers_simple_if_else_contribution \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_lowers_if_else_state_assignment -q

4 passed
```

Remote on `thu-sui` with Linux Rust `.so`:

```text
PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_lowers_simple_if_else_contribution \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_lowers_if_else_state_assignment \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_reports_transition_rejection_reason \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_reports_event_rejection_reason -q

4 passed
```

Top-wall 10 EVAS-only A/B reports:

- `speed-optimization/reports/rust_required_topwall10_rejections_20260604.json`
- `speed-optimization/reports/rust_if_lowering_topwall10_20260604.json`

## Speed Result

Both runs compare:

- Python fast path: `profile_fast_skip_source_error_control`
- Forced Rust path: `profile_fast_rust_static` with `evas_rust_required=true`

These are EVAS-only kernel experiments, not paper-facing Spectre speed claims.

| Run | Python fast total wall (s) | Rust-required total wall (s) | Python/Rust ratio | PASS |
| --- | ---: | ---: | ---: | ---: |
| Rejection counters only | 18.2534 | 21.3040 | 0.8568 | 10/10 |
| After simple `if/else` lowering | 18.5414 | 21.3623 | 0.8679 | 10/10 |

Interpretation: forced Rust remains slower on this slice. The simple `if/else`
lowering is correct, but it does not unlock any additional complete top-wall
model for Rust execution. It only reduces rejection counts inside models that
are still blocked by arrays, events, transitions, or self-dependent state.

## Coverage Result

Before and after `if/else` lowering, the only true Rust static-evaluate
execution remains the same two small models inside
`vbr1_l2_gain_extraction_convergence_measurement_flow`.

| Case | Python fast (s) | Rust-required (s) | Python/Rust | Rust candidates/planned/ops/calls |
| --- | ---: | ---: | ---: | --- |
| weighted SAR ADC DAC loop tb | 5.5478 | 5.5947 | 0.992 | 0/0/0/0 |
| CPPLL reacquire e2e | 3.1517 | 3.0822 | 1.023 | 0/0/0/0 |
| CPPLL reacquire tb | 3.0386 | 3.0595 | 0.993 | 0/0/0/0 |
| propagation delay comparator dut | 2.2066 | 2.2109 | 0.998 | 0/0/0/0 |
| gain extraction tb | 1.4111 | 2.8684 | 0.492 | 2/2/6/32472 |
| gain extraction e2e | 1.3936 | 2.8616 | 0.487 | 2/2/6/32472 |
| LFSR PRBS generator dut | 0.5411 | 0.5686 | 0.952 | 0/0/0/0 |
| gain estimator tb | 0.5026 | 0.3864 | 1.301 | 0/0/0/0 |
| PFD up/dn logic bugfix | 0.3898 | 0.3543 | 1.100 | 0/0/0/0 |
| gain estimator e2e | 0.3584 | 0.3758 | 0.954 | 0/0/0/0 |

The two gain-extraction rows get 32,472 Rust calls each for only 6 static-linear
ops. That is exactly the bad regime: many Python/Rust boundary crossings with
too little work per call.

## Rejection Distribution

Top aggregate rejection counters before vs after `if/else` lowering:

| Reason | Before | After |
| --- | ---: | ---: |
| `expr_non_static_linear_binary` | 278 | 229 |
| `if_statement` | 100 | 88 |
| `assignment_array_target` | 90 | 66 |
| `assignment_non_static_linear_expr` | 61 | 48 |
| `expr_array_access` | 50 | 50 |
| `contribution_non_static_linear_expr` | 47 | 47 |
| `expr_function_transition` | 47 | 47 |
| `assignment_self_dependent_state` | 46 | 46 |
| `event_cross` | 36 | 36 |
| `event_statement` | 27 | 27 |

The useful signal is that `if/else` lowering reduces local rejection counts, but
the hard blockers stay unchanged: arrays, `transition()`, event statements, and
self-dependent state updates.

## Conclusion

This round improved observability and added one correct IR lowering, but it did
not create a speed win on the real top-wall slice. Current Rust static-evaluate
is still too narrow and too fragmented. It should not be presented as faster
than Python EVAS or Spectre AX.

The next meaningful optimization is not another small Python cleanup. It should
move whole evaluate/event segments to typed array/Rust execution:

1. Add fixed-range state-array IR for `arr[i]` reads/writes and array assignment
   targets. This directly targets weighted SAR and gain extraction blockers.
2. Move `transition()` target/evaluate from shadow metadata into executable Rust
   batch logic, then fuse transition output writes with array state.
3. Add event/timer/cross queue representation so event-heavy CPPLL/PFD/LFSR rows
   stop falling back to Python for the real control flow.
4. Add explicit recurrence IR for safe self-dependent state updates such as
   `x = x + linear_delta`, preserving the existing nominal-step gate.
5. Only after the above, remove per-step Python dict synchronization for Rust
   covered segments.
