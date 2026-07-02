# Macro Ifdef Gain Select

Implement one behavioral Verilog-A source file named `macro_ifdef_gain_select.va`.

## Interface

Use this exact module interface:

```verilog
module macro_ifdef_gain_select (
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

Use conditional preprocessor selection to alter a behavioral gain constant.

Required behavior:

- define `V3_HIGH_GAIN` before the module declaration;
- use `` `ifdef V3_HIGH_GAIN`` / `` `else`` / `` `endif`` to select `selected_gain`;
- when `V3_HIGH_GAIN` is defined, set `selected_gain = 1.25`;
- otherwise set `selected_gain = 0.75`;
- initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and state when `rst > vth`;
- otherwise set `out_v = selected_gain * V(vin)`;
- set `metric_v = selected_gain`;
- increment `count_q` after computing the outputs;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `macro_ifdef_gain_select.va`.
