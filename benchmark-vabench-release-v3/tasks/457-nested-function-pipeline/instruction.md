# Nested Function Pipeline

Implement one behavioral Verilog-A/AMS source file named `nested_function_pipeline.va`.

## Interface

Use this exact module interface:

```verilog
module nested_function_pipeline(
    input electrical vin,
    output electrical out
);
```

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use nested user-defined function calls in a behavioral pipeline.

Required behavior:

- define a user function `f2` that returns `x * x`;
- define a user function `f1` that calls `f2(x)` and adds 1.0;
- drive `out` with `f1(V(vin))`;
- keep the nested function path active in the analog contribution.

Return exactly one source artifact named `nested_function_pipeline.va`.
