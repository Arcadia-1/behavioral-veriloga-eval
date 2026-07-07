# Table Model Temperature Profile

## Task Contract

Implement one behavioral Verilog-A DUT source file named `table_model_temperature_profile.va`. The DUT uses the supplied one-dimensional table file to model a temperature-dependent behavioral output sampled on clock edges.

This is a DUT task. Keep the provided module name and port list, read the public table support artifact at runtime, and do not generate a testbench or auxiliary artifacts. Keep the model voltage-domain behavioral and do not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module table_model_temperature_profile (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

The `mode` port is present for interface consistency and is not part of the table lookup.

## Public Parameter Contract

Use `vth = 0.45` as the analog logic threshold, `vhi = 0.9` as the metric normalization level, and `tr = 200p` as the transition rise/fall time. These parameters may be overridden by the testbench.

The support file `table-model-temperature-profile.tbl` is public. Treat `vin` as a temperature coordinate in degrees Celsius. The lookup must use first-degree interpolation through the cold, room, hot, and high-temperature derating points and clamp extrapolation outside the listed temperature range.

## Required Behavior

Initialize `out` and `metric` low. On each rising crossing of `clk`, reset both outputs low when `rst` is above `vth`; otherwise sample `vin` through `$table_model` using `table-model-temperature-profile.tbl`, first-degree interpolation, and clamp extrapolation on both ends. Drive `metric` as the sampled output normalized by `vhi`.

## Modeling Constraints

Use `$table_model`, `cross`, and `transition`. In Cadence control-string terms, the table lookup should express a one-dimensional linear lookup with clamp extrapolation on both bounds. Do not rely on simulator-default linear extrapolation when the public behavior requires clamp.

## Output Contract

Return exactly one source artifact named `table_model_temperature_profile.va`. Drive both `out` and `metric` with `transition(...)`.
