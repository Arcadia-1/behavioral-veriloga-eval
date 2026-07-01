# Attribute Potential Abstol Probe

Implement one Verilog-A source file named `attribute_potential_abstol_probe.va`.

## Required Feature

Access a node potential attribute through hierarchical attribute syntax.

## Required Interface

```verilog
module attribute_potential_abstol_probe(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Read the input node potential absolute tolerance with `in.potential.abstol`.
- Store the attribute value in a real variable.
- Drive `out` as `V(in) + 1e5 * in.potential.abstol`.
- Smooth `out` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `attribute_potential_abstol_probe.va`.
