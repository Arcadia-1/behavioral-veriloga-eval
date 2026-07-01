# Generic Potential Access Function

Implement one Verilog-A source file named `generic_potential_access_function.va`.

## Required Feature

Use the generic potential() access function for an electrical node.

## Required Interface

```verilog
module generic_potential_access_function(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Read the input node potential using the generic access function `potential(in)`.
- Drive `out` with the value returned by `potential(in)`.
- Smooth `out` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `generic_potential_access_function.va`.
