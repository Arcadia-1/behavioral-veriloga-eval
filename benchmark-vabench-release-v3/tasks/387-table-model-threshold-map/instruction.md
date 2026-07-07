# Table Model Threshold Map

## Task Contract

Implement one behavioral Verilog-A source file named `table_model_threshold_map.va`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module table_model_threshold_map (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use `$table_model()` to map a control voltage to a threshold state. The solution must read `table-model-threshold-map.tbl`.

Required behavior:

- initialize `out_v` and `metric_v` to `0.0`;
- on each rising crossing of `clk`, reset `out_v` and `metric_v` to zero when `rst > vth`;
- otherwise set `out_v = $table_model(V(vin), "table-model-threshold-map.tbl")`;
- use the table as a near-step threshold map, with low inputs mapped to `0.0` and high inputs mapped to `vhi`;
- set `metric_v = out_v / vhi`;
- drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `table_model_threshold_map.va`.
