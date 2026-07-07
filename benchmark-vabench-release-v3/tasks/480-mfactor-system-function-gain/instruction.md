# Mfactor System Function Gain

## Task Contract

Implement one Verilog-A source file named `mfactor_system_function_gain.va`. This task exercises the Cadence-compatible `$mfactor` system function as a voltage gain source.

This is a Verilog-A semantic/support task. Read the effective Spectre instance multiplicity with `$mfactor` instead of using a public gain parameter or a hard-coded gain.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module mfactor_system_function_gain(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This task has no public Verilog-A parameters. Instance multiplicity is supplied by the simulator instance metadata and must be read with `$mfactor`.

## Required Behavior

Drive `out` with the effective instance multiplicity times `V(in)`.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Use only voltage-domain behavior and do not use current contributions.

## Output Contract

Return exactly one source artifact named `mfactor_system_function_gain.va`.
