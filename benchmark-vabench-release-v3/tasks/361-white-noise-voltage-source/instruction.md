# White Noise Voltage Source

## Task Contract

Implement one behavioral Verilog-A source file named `white_noise_voltage_source.va`. This is a support/L0 Verilog-A semantics task for `white_noise()` in a voltage-domain behavioral source, not a standalone core circuit macro.

This is a DUT source task. Implement only the `white_noise_voltage_source` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module white_noise_voltage_source (
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
- `noise_power = 1.0e-12`: white-noise power spectral density parameter for the `white_noise()` contribution.

## Required Behavior

Contribute a voltage-domain white-noise source on `out` using `white_noise(noise_power, "white_voltage_noise")`. In ordinary transient analysis this small-signal noise contribution is not a deterministic time-domain waveform; the transient-observable behavior is carried by `metric`.

Initialize an internal real `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, sample the current control voltage and assign it to `metric_v`. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `white_noise()` directly in a branch contribution to `V(out)`. Do not assign the noise function result to a real variable, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Use `transition()` only for event-updated state such as `metric_v`, not for continuously varying branch voltages.

## Output Contract

Return exactly one source artifact named `white_noise_voltage_source.va`.
