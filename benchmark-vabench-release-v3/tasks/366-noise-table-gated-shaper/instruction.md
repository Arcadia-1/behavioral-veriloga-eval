# Noise Table Gated Shaper

## Task Contract

Implement one behavioral Verilog-A source file named `noise_table_gated_shaper.va`. This is a support/L0 Verilog-A semantics task for gating a `noise_table()` voltage contribution with an analog control threshold, not a standalone core circuit macro.

## Form-Specific Requirements

This is a DUT source task with a supplied support table named `noise_profile.tbl`. Implement only the Verilog-A source file and read the table by that exact filename; do not rename or regenerate the support table.

## Public Verilog-A Interface

```verilog
module noise_table_gated_shaper (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45`: control and clock threshold in volts.
- `vhi = 0.9`: high value reported on `metric` when the table-defined source is enabled.
- `tr = 200p`: rise/fall time for the event-updated `metric` transition.
- No additional public parameters are required; `noise_profile.tbl` is the public support artifact for the table-defined noise profile.

## Required Behavior

Contribute `noise_table("noise_profile.tbl", "profile_noise")` to `V(out)` only when `V(ctrl) > vth`; otherwise contribute zero to `out`. In ordinary transient analysis this small-signal noise contribution is not a deterministic time-domain waveform.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `vhi` when `V(ctrl) > vth`, otherwise set it to zero. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `noise_table()` directly in a voltage branch contribution. Do not assign the noise function result to a real variable, do not use current-domain `I(...)` contributions, and do not add transistor-level devices. Keep the support table dependency explicit and local to `noise_profile.tbl`.

## Output Contract

Return exactly one source artifact named `noise_table_gated_shaper.va`; the supplied `noise_profile.tbl` remains a support artifact.
