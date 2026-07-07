# Noise Table Voltage Shaper

## Task Contract

Implement one behavioral Verilog-A source file named `noise_table_voltage_shaper.va`. This is a support/L0 Verilog-A semantics task for using `noise_table()` with a supplied noise-profile file, not a standalone core circuit macro.

This is a DUT source task with a supplied support table named `noise_profile.tbl`. Implement only the Verilog-A source file and read the table by that exact filename; do not rename or regenerate the support table.

## Public Verilog-A Interface

```verilog
module noise_table_voltage_shaper (
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
- No additional public parameters are required; `noise_profile.tbl` is the public support artifact for the table-defined noise profile.

## Required Behavior

Contribute a voltage-domain table-defined noise source on `out` using `noise_table("noise_profile.tbl", "profile_noise")`. In ordinary transient analysis this small-signal noise contribution is not a deterministic time-domain waveform; the transient-observable behavior is carried by `metric`.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `0.3 + V(ctrl) * 0.2`. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `noise_table()` directly in a voltage branch contribution. Do not assign the noise function result to a real variable, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Keep the support table dependency explicit and local to `noise_profile.tbl`.

## Output Contract

Return exactly one source artifact named `noise_table_voltage_shaper.va`; the supplied `noise_profile.tbl` remains a support artifact.
