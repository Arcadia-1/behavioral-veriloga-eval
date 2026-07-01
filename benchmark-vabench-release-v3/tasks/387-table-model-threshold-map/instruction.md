# Table Model Threshold Map

Implement one behavioral Verilog-A source file named `table_model_threshold_map.va`.

## Interface

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

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use `$table_model()` to map a control voltage to a threshold state. The solution must read `table-model-threshold-map.tbl`.

Required behavior:

- initialize `out_v` and `metric_v` to `0.0`;
- on each rising crossing of `clk`, reset `out_v` and `metric_v` to zero when `rst > vth`;
- otherwise set `out_v = $table_model(V(vin), "table-model-threshold-map.tbl")`;
- use the table as a near-step threshold map, with low inputs mapped to `0.0` and high inputs mapped to `vhi`;
- set `metric_v = out_v / vhi`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `table_model_threshold_map.va`.
