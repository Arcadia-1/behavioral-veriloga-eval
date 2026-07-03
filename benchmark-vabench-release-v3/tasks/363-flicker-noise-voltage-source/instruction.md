# Flicker Noise Voltage Source

## Task Contract

Implement one behavioral Verilog-A source file named `flicker_noise_voltage_source.va`. This is a support/L0 Verilog-A semantics task for `flicker_noise()` in a voltage-domain behavioral source, not a standalone core circuit macro.

## Form-Specific Requirements

This is a DUT source task. Implement only the `flicker_noise_voltage_source` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module flicker_noise_voltage_source (
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
- `kf = 1.0e-12`: flicker-noise coefficient.
- `af = 1.0`: flicker-noise exponent.

## Required Behavior

Contribute a voltage-domain flicker-noise source on `out` using `flicker_noise(kf, af, "flicker_voltage_noise")`. In ordinary transient analysis this small-signal noise contribution is not a deterministic time-domain waveform; the transient-observable behavior is carried by `metric`.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `kf * 1.0e12`. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `flicker_noise()` directly in a voltage branch contribution. Do not assign the noise function result to a real variable, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Use real-valued arithmetic for the metric scaling.

## Output Contract

Return exactly one source artifact named `flicker_noise_voltage_source.va`.
