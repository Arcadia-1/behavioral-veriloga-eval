# settling_done_boundary

## Purpose

This conformance asset isolates timer-driven measurement boundary semantics from
the historical `vbm1_settling_time_measurement_tb_bugfix` main120 row. It should
not be counted as a normal bugfix benchmark task.

## Semantic Axis

- Axis: `solver-time-sampling`
- Expected EVAS/Spectre relation: `binary_outcome_equal`
- Scope: a `timer(0,1n)` first-order update, a source step, and a `done` flag
  gated by both `$abstime > 120n` and `y > 0.75`.

## Gold Evidence

- `gold/settling_time_measurement_tb.va`
- `gold/tb_settling_time_measurement_tb_ref.scs`

The internal response is already above `0.75 V` before `120 ns`; the isolated
semantic is therefore the strict time boundary. The `done` flag should remain
low at the boundary and assert only after the first timer event strictly later
than `120 ns`, modulo transition smoothing and save-grid tolerance.

## Why This Is Not A Normal Bugfix Task

This is a measurement/testbench behavior question, not a DUT repair pair. A
public bugfix task would need a bad source with one reviewed functional defect
and a fixed source that repairs it. Here the risk is whether the simulator and
checker agree on a timer/sample boundary, so it belongs in conformance.

## Runner Hook Needed

A conformance runner should:

1. run the included testbench on both EVAS and Spectre;
2. require both runs to compile and finish;
3. compare binary pass/fail from a structured done-boundary checker;
4. sample `done` away from transition knees, for example just before `120 ns`
   and safely after `121 ns`;
5. avoid final-row or raw row-count observables.
