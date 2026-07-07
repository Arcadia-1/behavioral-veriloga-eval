# Combined White Flicker Noise

## Task Contract

Implement one behavioral Verilog-A source file named `combined_white_flicker_noise.va`. This is a support/L0 Verilog-A semantics task for combining white-noise and flicker-noise voltage contributions, not a standalone core circuit macro.

This is a DUT source task. Implement only the `combined_white_flicker_noise` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module combined_white_flicker_noise (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45`: clock crossing threshold in volts.
- `vhi = 0.9`: retained compatibility parameter for the shared source-task interface.
- `tr = 200p`: rise/fall time for the event-updated `metric` transition.
- `white_pwr = 1.0e-12`: white-noise power spectral density parameter.
- `kf = 5.0e-13`: flicker-noise coefficient.

## Required Behavior

Contribute both `white_noise(white_pwr, "white")` and `flicker_noise(kf, 1.0, "flicker")` to `V(out)` as a summed voltage-domain noise source. In ordinary transient analysis these small-signal noise contributions are not deterministic time-domain waveforms; the transient-observable behavior is carried by `metric`.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `white_pwr * 1.0e12 + kf * 1.0e12`. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use the noise functions directly in voltage branch contributions. Do not assign noise function results to real variables, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Use real-valued arithmetic for the metric scaling.

## Output Contract

Return exactly one source artifact named `combined_white_flicker_noise.va`.
