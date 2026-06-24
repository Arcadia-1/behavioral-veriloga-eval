# cross_event_post_side_read

## Purpose

This conformance asset isolates one EVAS/Spectre event semantic: what value is
observed when an event body reads the same node that triggered a `cross(...)`
event.

It is intentionally not a normal benchmark task. Public vaBench tasks should
verify circuit behavior such as phase-detector duty cycle, delay, settling, or
state transitions, not exact threshold-point simulator internals.

## Semantic Axis

- Axis: `event-sampling`
- Expected EVAS/Spectre relation: `waveform_equivalent`
- Scope: a rising and falling `cross(V(vin)-vth, dir)` event updates a latched
  logic state by reading `V(vin)` inside the event body.

## Gold Evidence

- `gold/cross_event_post_side_read.va`
- `gold/tb_cross_event_post_side_read.scs`

The expected Spectre-facing behavior is:

1. after the rising crossing, `state` is high;
2. after the falling crossing, `state` is low;
3. the diagnostic is judged in settled windows away from the exact threshold
   sample.

## Why This Is Not A Normal Benchmark Task

This case is about event-body sampling semantics at a crossing boundary. Normal
L1/L2 benchmark tasks should avoid depending on this detail; they should use
edge-directed state updates or settled-window checks when the circuit function
does not require exact threshold-point behavior.

## Runner Hook Needed

A conformance runner should:

1. run the included testbench on both EVAS and Spectre;
2. require both runs to compile and finish;
3. check that `state` is high in a settled post-rising window;
4. check that `state` is low in a settled post-falling window;
5. report this result outside all benchmark score/model-capability denominators.
