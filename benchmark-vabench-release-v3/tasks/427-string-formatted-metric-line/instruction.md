# String Formatted Metric Line

Implement one behavioral Verilog-A source file named `string_formatted_metric_line.va`.

## Interface

Use this exact module interface:

```verilog
module string_formatted_metric_line (
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

Use $swrite() to format a metric file line before writing it.

Required behavior:

- declare a string state variable such as `label_q`;
- initialize `out_v`, `metric_v`, and `count_q` at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise set `out_v` to `vhi` when `V(vin) > vth`, else 0.0;
- set `metric_v` to the current `count_q` value before incrementing it;
- call `$swrite(label_q, "mode=%0d metric=%0.3f", count_q, metric_v)` or an equivalent format that includes both count and metric;
- write the formatted label to `metric_lines.log` using `$fopen`, `$fwrite`, and `$fclose`;
- increment `count_q` after formatting/writing the label;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `string_formatted_metric_line.va`.
