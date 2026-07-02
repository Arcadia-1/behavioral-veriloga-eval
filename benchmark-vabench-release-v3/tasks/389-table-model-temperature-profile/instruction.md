# Table Model Temperature Profile

Implement one behavioral Verilog-A source file named `table_model_temperature_profile.va`.

## Interface

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

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use `$table_model()` for a temperature-shaped behavioral output. The solution must read `table-model-temperature-profile.tbl`.

Required behavior:

- treat `V(vin)` as a temperature coordinate in degrees Celsius;
- initialize `out_v` and `metric_v` to `0.0`;
- on each rising crossing of `clk`, reset `out_v` and `metric_v` to zero when `rst > vth`;
- otherwise set `out_v = $table_model(V(vin), "table-model-temperature-profile.tbl")`;
- use the table profile as the source of cold, room, hot, and high-temperature derating values;
- set `metric_v = out_v / vhi`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `table_model_temperature_profile.va`.
