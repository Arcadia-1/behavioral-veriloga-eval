# Macro Functionlike Clamp

Implement one behavioral Verilog-A source file named `macro_functionlike_clamp.va`.

## Interface

Use this exact module interface:

```verilog
module macro_functionlike_clamp (
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

Use a function-like preprocessor macro in analog behavior.

Required behavior:

- define and use a function-like macro named `V3_CLAMP(x)`;
- clamp macro input below `0.0` to `0.0`, above `0.9` to `0.9`, and otherwise pass the value through;
- initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and state when `rst > vth`;
- otherwise set ``out_v = `V3_CLAMP(V(vin))``;
- set `metric_v = out_v / vhi`;
- increment `count_q` after computing the outputs;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `macro_functionlike_clamp.va`.
