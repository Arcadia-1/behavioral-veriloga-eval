# Rtoi Conversion Quantizer

## Task Contract

Implement one Verilog-A source file named `rtoi_conversion_quantizer.va`. This task exercises `$rtoi()` as part of a voltage-domain quantizer.

## Form-Specific Requirements

This is a Verilog-A semantic/support task. The real-to-integer conversion must use `$rtoi()` rather than an equivalent hand-written threshold tree.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module rtoi_conversion_quantizer(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This task has no public Verilog-A parameters.

## Required Behavior

Compute an integer code from `8.0 * V(in)` using `$rtoi()`, clamp the code to the range from 0 through 7, and drive `out` with the normalized code value over the full output range.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Use voltage-domain behavior and do not use current contributions.

## Output Contract

Return exactly one source artifact named `rtoi_conversion_quantizer.va`.
