# String Config Label Select

Implement one behavioral Verilog-A source file named `string_config_label_select.va`.

## Interface

Use this exact module interface:

```verilog
module string_config_label_select (
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

Use string formatting to select and record configuration labels.

Required behavior:

- declare a string state variable such as `label_q`;
- initialize `out_v`, `metric_v`, and `count_q` at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- when `mode` is low, select configuration A: set `out_v` to `vhi` when `V(vin) > vth`, else 0.0, set `metric_v = count_q`, and format a `cfg=A` label;
- when `mode` is high, select configuration B: set `out_v` to 0.0 when `V(vin) > vth`, else `vhi`, set `metric_v = count_q + 10`, and format a `cfg=B` label;
- use `$sformat(...)` to build the selected configuration label;
- increment `count_q` after formatting the label;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `string_config_label_select.va`.
