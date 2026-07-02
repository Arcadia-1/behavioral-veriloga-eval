# Analog Primitive Isource Instance

Implement one Verilog-A source file named `analog_primitive_isource_instance.va`.

## Required Feature

Instantiate a Spectre analog current-source primitive inside a Verilog-A module.

## Required Interface

```verilog
module analog_primitive_isource_instance(
    inout electrical p,
    inout electrical n
);
```

## Required Behavior

- Declare a real parameter named `ibias` with default value `1u`.
- Instantiate exactly one Spectre-style current-source primitive between `n` and `p`, e.g. `isource #(.dc(ibias)) ib (n, p);`.
- This is a conservative/KCL syntax-extension task: the benchmark checks parse/staging coverage, not current-source circuit behavior.
- Do not replace the primitive with a behavioral voltage-domain output.

Return exactly one source artifact named `analog_primitive_isource_instance.va`.
