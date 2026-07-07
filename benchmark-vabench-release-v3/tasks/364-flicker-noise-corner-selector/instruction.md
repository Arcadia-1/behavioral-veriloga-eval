# Flicker Noise Corner Selector

## Task Contract

Implement one behavioral Verilog-A source file named `flicker_noise_corner_selector.va`. This is a support/L0 Verilog-A semantics task for selecting a flicker-noise coefficient from an analog control level, not a standalone core circuit macro.

This is a DUT source task. Implement only the `flicker_noise_corner_selector` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module flicker_noise_corner_selector (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45`: control and clock threshold in volts.
- `vhi = 0.9`: high value reported on `metric` when the high-noise corner is selected.
- `tr = 200p`: rise/fall time for the event-updated `metric` transition.
- `kf_lo = 1.0e-13`: flicker-noise coefficient when `V(ctrl) <= vth`.
- `kf_hi = 2.0e-12`: flicker-noise coefficient when `V(ctrl) > vth`.

## Required Behavior

Contribute a voltage-domain flicker-noise source on `out` using `flicker_noise(selected_kf, 1.0, "corner_select")`, where `selected_kf` is `kf_hi` when `V(ctrl) > vth` and `kf_lo` otherwise. In ordinary transient analysis this small-signal noise contribution is not a deterministic time-domain waveform.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `vhi` when `V(ctrl) > vth`, otherwise set it to zero. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `flicker_noise()` directly in a voltage branch contribution. Do not assign the noise function result to a real variable, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Use `transition()` only for event-updated state such as `metric_v`.

## Output Contract

Return exactly one source artifact named `flicker_noise_corner_selector.va`.
