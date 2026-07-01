# Inherited Mfactor Parameter

Implement one Verilog-A source file named `inherited_mfactor_parameter.va`.

## Required Feature

Declare an inherited m-factor parameter attribute.

## Required Interface

```verilog
module inherited_mfactor_parameter(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Declare a real parameter named `m` with the Verilog-A attribute `(* inherited_mfactor *)`.
- Drive `out` with `m * V(in)` using `transition(..., 0, 200p, 200p)`.
- The testbench may override `m`; your model must use the parameter value, not a hard-coded gain.
- Use only voltage-domain behavior; do not use `I(...)`.

Return exactly one source artifact named `inherited_mfactor_parameter.va`.
