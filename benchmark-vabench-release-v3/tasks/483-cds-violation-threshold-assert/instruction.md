# Cds Violation Threshold Assert

Implement one Verilog-A source file named `cds_violation_threshold_assert.va`.

## Required Feature

Use $cds_violation() to emit a Verilog-A assert violation.

## Required Interface

```verilog
module cds_violation_threshold_assert(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Monitor `V(in)` continuously.
- When `V(in) > 1.0`, call `$cds_violation("va_threshold", "threshold_exceeded", V(in))`.
- Drive `out` with `V(in)` while `V(in) <= 1.0`.
- Drive `out` with `1.0` while `V(in) > 1.0`, using the same threshold condition as the violation call.
- Smooth `out` with `transition(..., 0, 200p, 200p)`.

Return exactly one source artifact named `cds_violation_threshold_assert.va`.
