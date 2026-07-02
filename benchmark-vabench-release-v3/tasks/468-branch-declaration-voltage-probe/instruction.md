# Branch Declaration Voltage Probe

Implement one Verilog-A source file named `branch_declaration_voltage_probe.va`.

## Required Feature

Declare an explicit branch and read its voltage.

## Required Interface

```verilog
module branch_declaration_voltage_probe(
    input electrical p,
    input electrical n,
    output electrical out
);
```

## Required Behavior

- Declare an explicit branch named `br` between `p` and `n`.
- Drive `out` with the branch voltage `V(br)`, equivalent to `V(p,n)`.
- Smooth `out` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `branch_declaration_voltage_probe.va`.
