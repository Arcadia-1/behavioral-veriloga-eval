# Rtoi Conversion Quantizer

Implement one Verilog-A source file named `rtoi_conversion_quantizer.va`.

## Required Feature

Use $rtoi() to convert real-valued code to integer state.

## Required Interface

```verilog
module rtoi_conversion_quantizer(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Compute `code = $rtoi(8.0 * V(in))`.
- Saturate `code` to the integer range `[0, 7]`.
- Drive `out` with `code / 7.0` using `transition(..., 0, 200p, 200p)`.
- Use `$rtoi()` for the real-to-integer conversion; do not hand-roll the conversion with threshold-only logic.

Return exactly one source artifact named `rtoi_conversion_quantizer.va`.
