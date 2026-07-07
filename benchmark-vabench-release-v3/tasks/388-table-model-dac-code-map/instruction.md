# Table Model DAC Code Map

## Task Contract

Implement one behavioral Verilog-A DUT source file named `table_model_dac_code_map.va`. The DUT uses the supplied one-dimensional table file as a compact analog-coded DAC transfer map sampled on clock edges.

This is a DUT task. Keep the provided module name and port list, read the public table support artifact at runtime, and do not generate a testbench or auxiliary artifacts. Keep the model voltage-domain behavioral and do not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module table_model_dac_code_map (
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

The support file `table-model-dac-code-map.tbl` is public. Treat `vin` as an analog-coded DAC code coordinate. The lookup must use first-degree interpolation between listed code points and clamp extrapolation outside the listed code range.

## Required Behavior

Initialize `out` and `metric` low. On each rising crossing of `clk`, reset both outputs low when `rst` is above `vth`; otherwise sample `vin` through `$table_model` using `table-model-dac-code-map.tbl`, first-degree interpolation, and clamp extrapolation on both ends. Drive `metric` as the sampled output normalized by `vhi`.

## Modeling Constraints

Use `$table_model`, `cross`, and `transition`. In Cadence control-string terms, the table lookup should express a one-dimensional linear lookup with clamp extrapolation on both bounds. Do not rely on simulator-default linear extrapolation when the public behavior requires clamp.

## Output Contract

Return exactly one source artifact named `table_model_dac_code_map.va`. Drive both `out` and `metric` with `transition(...)`.
