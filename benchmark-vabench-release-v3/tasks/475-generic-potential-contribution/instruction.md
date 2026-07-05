# Generic Potential Contribution

## Task Contract

Implement one Verilog-A source file named `generic_potential_contribution.va`. This row is a Verilog-A generic-contribution semantic/support task: it verifies using `potential()` as the output contribution target.

## Form-Specific Requirements

This is a DUT task in the language-semantic support layer. The public tests drive `in` and observe that the generic contribution target makes `out` follow the input voltage.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module generic_potential_contribution(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This module has no public module parameters. Use a fixed `transition(..., 0, 200p, 200p)` smoothing contract for the contribution target.

## Required Behavior

Drive the output through the generic contribution target `potential(out) <+ ...`. The contributed value must track `V(in)` after the fixed transition smoothing.

## Modeling Constraints

Use `potential(out)` as the contribution target. Do not replace the row with direct current contribution, threshold logic, or a fixed output table. Use only voltage-domain behavior; do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `generic_potential_contribution.va`.
