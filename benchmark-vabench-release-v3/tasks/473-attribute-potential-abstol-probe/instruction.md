# Attribute Potential Abstol Probe

## Task Contract

Implement one Verilog-A source file named `attribute_potential_abstol_probe.va`. This row is a Verilog-A electrical-attribute semantic/support task: it verifies access to the potential abstol attribute on a public electrical input.

## Form-Specific Requirements

This is a DUT task in the language-semantic support layer. The public tests drive the input node voltage and observe the attribute-derived offset at `out`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module attribute_potential_abstol_probe(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This module has no public module parameters. Use the simulator's potential abstol value for `in` and the fixed scale factor `1e5` in the observable offset.

## Required Behavior

Read the input node potential absolute tolerance with `in.potential.abstol` and store it in a real variable. Drive `out` as the input voltage plus `1e5` times that attribute value, then smooth the observable output with `transition(..., 0, 200p, 200p)`.

## Modeling Constraints

Use the potential attribute syntax directly. Do not hard-code the final output samples or replace the attribute access with unrelated constants. Use only voltage-domain output contribution; do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `attribute_potential_abstol_probe.va`.
