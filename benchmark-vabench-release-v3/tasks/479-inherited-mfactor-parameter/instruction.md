# Inherited Mfactor Parameter

## Task Contract

Implement one Verilog-A source file named `inherited_mfactor_parameter.va`. This task exercises an inherited m-factor parameter used as a voltage gain.

## Form-Specific Requirements

This is a Verilog-A semantic/support task. Preserve the inherited-parameter attribute and use the public parameter value rather than a hard-coded gain.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module inherited_mfactor_parameter(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

Declare `(* inherited_mfactor *) parameter real m = 1.0;`. The testbench may override `m`, and the model must use the effective parameter value.

## Required Behavior

Drive `out` with `m * V(in)`.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Use only voltage-domain behavior and do not use current contributions.

## Output Contract

Return exactly one source artifact named `inherited_mfactor_parameter.va`.
