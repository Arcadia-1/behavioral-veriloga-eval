# White Noise Gated Source

## Task Contract

Implement one behavioral Verilog-A source file named `white_noise_gated_source.va`. This is a support/L0 Verilog-A semantics task for gating a voltage-domain `white_noise()` contribution, not a standalone core circuit macro.

This is a DUT source task. Implement only the `white_noise_gated_source` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module white_noise_gated_source (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45`: control and clock threshold in volts.
- `vhi = 0.9`: high value reported on `metric` when the gate is enabled.
- `tr = 200p`: rise/fall time for the event-updated `metric` transition.
- `noise_power = 2.0e-12`: white-noise power spectral density parameter used when the gate is enabled.

## Required Behavior

Contribute `white_noise(noise_power, "gated_white")` to `V(out)` only when `V(ctrl) > vth`; otherwise contribute zero to `out`. In ordinary transient analysis this small-signal noise contribution is not a deterministic time-domain waveform.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `vhi` when `V(ctrl) > vth`, otherwise set it to zero. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `white_noise()` directly in a voltage branch contribution. Do not assign the noise function result to a real variable, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Use `transition()` only for event-updated state such as `metric_v`, not for continuously varying branch voltages.

## Output Contract

Return exactly one source artifact named `white_noise_gated_source.va`.
