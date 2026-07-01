# Above Resettable Peak Marker

Implement one behavioral Verilog-A DUT file named `above_resettable_peak_marker.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module above_resettable_peak_marker (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `above()` to arm a resettable peak marker and track the largest input level seen after the arm event.

This is a pure voltage-domain behavioral task. Do not use current-domain `I(...)` branch contributions.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- `@(above(V(vin) - vth))` arms the peak tracker
- while armed, sample `V(vin)` on `@(timer(0, 50n))`
- track `peak_q` as the largest sampled `V(vin)` since the tracker was armed
- drive `out = 0.9` once armed, otherwise `0.0`
- drive `metric = peak_q`, clamped to `0.0 ... 0.9`
- `@(cross(V(rst) - vth, +1))` clears the armed state and peak value

The hidden testbench ramps `vin` above threshold, later to a larger peak, then asserts reset and drives a smaller post-reset peak. The evaluator checks arming, peak retention, and reset clearing.

## Output

Return exactly one source artifact named `above_resettable_peak_marker.va`. Do not generate a Spectre testbench for this task.
