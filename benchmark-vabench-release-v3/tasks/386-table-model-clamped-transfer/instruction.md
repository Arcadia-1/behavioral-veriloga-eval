# Table Model Clamped Transfer

Implement one behavioral Verilog-A source file named `table_model_clamped_transfer.va`.

## Interface

Use this exact module interface:

```verilog
module table_model_clamped_transfer (
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

Use `$table_model()` for a clamped transfer curve lookup. The solution must read `table-model-clamped-transfer.tbl`.

Required behavior:

- initialize `out_v` and `metric_v` to `0.0`;
- on each rising crossing of `clk`, reset `out_v` and `metric_v` to zero when `rst > vth`;
- otherwise set `out_v = $table_model(V(vin), "table-model-clamped-transfer.tbl")`;
- rely on the table lookup to clamp below the first table row and above the last table row;
- set `metric_v = out_v / vhi`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `table_model_clamped_transfer.va`.
