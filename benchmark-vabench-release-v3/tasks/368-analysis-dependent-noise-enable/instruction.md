# Analysis Dependent Noise Enable

## Task Contract

Implement one behavioral Verilog-A source file named `analysis_dependent_noise_enable.va`. This is a support/L0 Verilog-A semantics task for combining `analysis("noise")` with a voltage-domain `white_noise()` contribution, not a standalone core circuit macro.

## Form-Specific Requirements

This is a DUT source task. Implement only the `analysis_dependent_noise_enable` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module analysis_dependent_noise_enable (
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

Do not drive a deterministic transient waveform on `out`. Add `white_noise(noise_power, "enabled_noise")` as a voltage-domain contribution only when `analysis("noise")` is true. In ordinary transient analysis this small-signal noise contribution is not a deterministic time-domain waveform.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, sample the current control voltage and assign it to `metric_v`. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `white_noise()` directly in a voltage branch contribution and guard it with `analysis("noise")`. Do not assign the noise function result to a real variable, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Use `transition()` only for event-updated state such as `metric_v`.

## Output Contract

Return exactly one source artifact named `analysis_dependent_noise_enable.va`.
