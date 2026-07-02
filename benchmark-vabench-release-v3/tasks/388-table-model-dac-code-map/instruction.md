# Table Model Dac Code Map

Implement one behavioral Verilog-A source file named `table_model_dac_code_map.va`.

## Interface

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

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use `$table_model()` as a compact DAC code transfer map. The solution must read `table-model-dac-code-map.tbl`.

Required behavior:

- treat `V(vin)` as an analog-coded DAC code coordinate;
- initialize `out_v` and `metric_v` to `0.0`;
- on each rising crossing of `clk`, reset `out_v` and `metric_v` to zero when `rst > vth`;
- otherwise set `out_v = $table_model(V(vin), "table-model-dac-code-map.tbl")`;
- set `metric_v = out_v / vhi`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `table_model_dac_code_map.va`.
