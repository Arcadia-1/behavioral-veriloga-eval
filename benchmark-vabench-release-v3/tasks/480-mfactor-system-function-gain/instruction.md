# Mfactor System Function Gain

Implement one Verilog-A source file named `mfactor_system_function_gain.va`.

## Required Feature

Use $mfactor() to scale behavioral gain.

## Required Interface

```verilog
module mfactor_system_function_gain(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Read the effective instance multiplicity using `$mfactor()`.
- Drive `out` with `$mfactor() * V(in)` using `transition(..., 0, 200p, 200p)`.
- The testbench may set the instance multiplicity; your model must not hard-code a gain.
- Use only voltage-domain behavior; do not use `I(...)`.

Return exactly one source artifact named `mfactor_system_function_gain.va`.
