# Nested Function Pipeline

## Task Contract

Implement one behavioral Verilog-A source file named `nested_function_pipeline.va`. The task models a reusable nested user-defined function pipeline in an analog contribution.

## Form-Specific Requirements

This is a DUT task. Provide only the Verilog-A source file; the Spectre testbenches are supplied.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module nested_function_pipeline(
    input electrical vin,
    output electrical out
);
```

## Public Parameter Contract

This task has no public parameters.

## Required Behavior

Define a Verilog-A `analog function real` named `f2` that returns `x * x`. Define a Verilog-A `analog function real` named `f1` that calls `f2(x)` and adds `1.0`. Drive `out` continuously with `f1(V(vin))`.

## Modeling Constraints

Use Cadence-compatible `analog function` declarations with separately declared function inputs. Keep the model voltage-domain only and do not introduce current contributions.

## Output Contract

Return exactly one source artifact named `nested_function_pipeline.va`.
