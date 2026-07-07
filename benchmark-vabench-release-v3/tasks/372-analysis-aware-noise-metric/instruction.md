# Analysis Aware Noise Metric

## Task Contract

Implement one behavioral Verilog-A source file named `analysis_aware_noise_metric.va`. This is a support/L0 Verilog-A semantics task for combining `analysis("noise")`, `white_noise()`, and a deterministic sampled metric, not a standalone core circuit macro.

This is a DUT source task. Implement only the `analysis_aware_noise_metric` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module analysis_aware_noise_metric (
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
- `noise_power = 1.0e-12`: white-noise power spectral density parameter used when noise analysis is active.

## Required Behavior

In transient analysis, drive `out` directly from the instantaneous control voltage: `V(out) <+ V(ctrl)`. When `analysis("noise")` is true, add a voltage-domain noise contribution using `white_noise(noise_power, "metric_noise")`.

Initialize `metric_v` to zero and an integer clock counter to zero at `initial_step`. On every rising crossing of `clk` through `vth`, increment the counter by one and set `metric_v` to `count / 8.0`. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `white_noise()` directly in a voltage branch contribution and guard it with `analysis("noise")`. Do not assign the noise function result to a real variable. Do not place continuously varying branch voltages such as `V(ctrl)` inside `transition()`; drive continuous voltage behavior directly as a branch contribution.

## Output Contract

Return exactly one source artifact named `analysis_aware_noise_metric.va`.
