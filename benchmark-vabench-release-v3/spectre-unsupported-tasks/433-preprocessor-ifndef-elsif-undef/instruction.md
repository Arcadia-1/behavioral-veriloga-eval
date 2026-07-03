# Preprocessor Ifndef Elsif Undef

Implement one behavioral Verilog-A source file named `preprocessor_ifndef_elsif_undef.va`.

## Interface

Use this exact module interface:

```verilog
module preprocessor_ifndef_elsif_undef (
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

Use `ifndef, `elsif, and `undef to select a behavioral constant.

Required behavior:

- use preprocessor control with ``ifndef``, ``elsif``, and ``undef``;
- define `V3_GAIN_VALUE` as 0.75 when `V3_GAIN_MODE` is not defined;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise drive `out_v = V3_GAIN_VALUE * V(vin)`;
- drive `metric_v = V3_GAIN_VALUE`;
- increment `count_q` after each non-reset sample;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `preprocessor_ifndef_elsif_undef.va`.
