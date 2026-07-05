# Generic Potential Access Function

## Task Contract

Implement one Verilog-A source file named `generic_potential_access_function.va`. This row is a Verilog-A generic-access semantic/support task: it verifies reading an electrical node through `potential()`.

## Form-Specific Requirements

This is a DUT task in the language-semantic support layer. The public tests drive `in` and observe that `out` follows the generic potential access result.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module generic_potential_access_function(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This module has no public module parameters. Use a fixed `transition(..., 0, 200p, 200p)` smoothing contract for the observable output.

## Required Behavior

Read the input node potential with the generic access function `potential(in)`. Drive `out` with that value after the fixed transition smoothing so it tracks the input potential across the supplied voltage waveform.

## Modeling Constraints

Use `potential(in)` for the input read. Do not replace the generic access with a threshold detector, fixed sample table, or unrelated state machine. Use only voltage-domain output contribution; do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `generic_potential_access_function.va`.
