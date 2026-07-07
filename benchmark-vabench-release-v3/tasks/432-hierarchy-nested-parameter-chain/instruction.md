# Hierarchy Nested Parameter Chain

## Task Contract

Implement one behavioral Verilog-A source file named `hierarchy_nested_parameter_chain.va`. This is a language-extension/L0 support task for hierarchical child-module reuse and parameter override propagation, not a standalone core circuit macro.

The public harness supplies a read-only support child module in `staged_gain_child.va`. Return only the parent source file and instantiate the supplied child module twice from it.

## Public Verilog-A Interface

Use this exact parent module interface:

```verilog
module hierarchy_nested_parameter_chain (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

The supplied `staged_gain_child` exposes a `gain` parameter. Override the first instance to `1.2` and the second instance to `0.5`.

## Required Behavior

- Define the top module `hierarchy_nested_parameter_chain`.
- Instantiate the supplied reusable child gain module twice using named port maps.
- Connect `vin -> gain0 -> mid -> gain1 -> out`.
- Drive `metric` directly from the intermediate node `V(mid)`.
- Preserve the two-stage gain chain so the final output reflects the 1.2 gain followed by the 0.5 gain.

## Modeling Constraints

Keep the implementation behavioral and voltage-domain only. Do not introduce current contributions or redefine the supplied support module in the returned artifact.

## Output Contract

Return exactly one source artifact named `hierarchy_nested_parameter_chain.va`.
