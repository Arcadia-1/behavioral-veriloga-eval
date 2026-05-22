# vaBench Cross-Event Threshold Audit

Date: 2026-05-16

## Decision

Normal vaBench tasks should verify circuit function, not exact threshold-point
simulator semantics. Event-body reads of the same node that triggered a
`cross(...)` event are now treated as L0 EVAS/Spectre conformance material.

## Confirmed Release Benchmark Fix

| Entry | Issue | Action |
| --- | --- | --- |
| `vbr1_l1_xor_phase_detector` | Gold/reference used a combined rising/falling `cross(V(REF/DIV)-vth, +/-1)` block and then read `V(REF/DIV) > vth` inside the event body. This couples the phase-detector function to exact crossing-point sampling. | Rewrote gold/fixed/buggy sources to use edge-directed state updates: rising edge sets the logic state to `1`, falling edge sets it to `0`. The bugfix badcase now isolates XNOR-vs-XOR behavior only. |

## New L0 Conformance Case

| Case | Axis | Purpose | Benchmark denominator |
| --- | --- | --- | --- |
| `cross_event_post_side_read` | `event-sampling` | Isolates what value an event body observes when it reads the same node that triggered a `cross(...)` event. | Excluded from L1/L2 benchmark coverage, model capability, bugfix claims, and broad parity denominators. |

## Other Cross Patterns Checked

| Pattern | Examples | Judgment |
| --- | --- | --- |
| Clock-edge sampling of other signals | ADC/DAC, sample-hold, DFF, calibration FSMs | Valid circuit behavior. The trigger node is a clock; the body samples data/reset/control nodes. |
| Rising/falling cross used as explicit state edge | burst clock, hysteresis/window comparator, PFD variants | Valid circuit behavior when state is assigned from the event direction rather than by re-reading the trigger node at the threshold. |
| Combined data-edge event using timing variables | BBPD data-edge alignment | Valid benchmark behavior. The event is a data-edge notification; the body uses clock timing/state, not the exact value of the triggering data node. |
| File metric writer | `file_metric_writer` benchmark and conformance companion | Valid as a functional benchmark when checking `metric.out` against waveform crossing time in settled tolerance; the exact event-body trigger-node voltage is not the benchmark target. |

## Rule For Future Tasks

If the circuit function can be expressed as an edge-directed state update, prefer
separate `+1` and `-1` event blocks. If a task intentionally depends on reading
the triggering node inside the event body, keep it in `conformance/evas-spectre`
and exclude it from normal benchmark scoring.
