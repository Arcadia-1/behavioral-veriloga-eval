# Generic Potential Contribution

Implement one Verilog-A source file named `generic_potential_contribution.va`.

## Required Feature

Use the generic potential() access function as a contribution target.

## Required Interface

```verilog
module generic_potential_contribution(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Drive the output through the generic contribution target `potential(out) <+ ...`.
- The driven output value must track the input voltage `V(in)`.
- Smooth the contribution with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain behavior; do not use `I(...)`.

Return exactly one source artifact named `generic_potential_contribution.va`.
