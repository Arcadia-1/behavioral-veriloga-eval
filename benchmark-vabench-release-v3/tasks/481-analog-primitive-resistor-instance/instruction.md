# Analog Primitive Resistor Instance

Implement one Verilog-A source file named `analog_primitive_resistor_instance.va`.

## Required Feature

Instantiate a Spectre analog resistor primitive inside a Verilog-A module.

## Required Interface

```verilog
module analog_primitive_resistor_instance(
    inout electrical p,
    inout electrical n
);
```

## Required Behavior

- Instantiate exactly one resistor-like analog primitive between `p` and `n`.
- Use Spectre-style primitive instance syntax with a parameter override, e.g. `resistor #(.r(1000.0)) rload (p, n);`.
- This is a conservative/KCL syntax-extension task: the benchmark checks parse/staging coverage, not resistor-current behavior.
- Do not replace the primitive with a behavioral voltage source or unrelated voltage-domain output.

Return exactly one source artifact named `analog_primitive_resistor_instance.va`.
