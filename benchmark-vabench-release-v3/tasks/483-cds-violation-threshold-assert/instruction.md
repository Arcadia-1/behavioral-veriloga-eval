# Cds Violation Threshold Assert

## Task Contract

Implement one Verilog-A source file named `cds_violation_threshold_assert.va`. The task is an L0/support row for the Cadence `$cds_violation()` assertion system task.

## Form-Specific Requirements

This is a DUT task for Cadence simulator-function semantics. The output clamp is the transient-observable behavior used to validate the same threshold that triggers the assertion.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module cds_violation_threshold_assert(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This task has no public parameters.

## Required Behavior

Monitor `V(in)` continuously. When `V(in) > 1.0`, call `$cds_violation("va_threshold", "threshold_exceeded", V(in))` and drive `out` to `1.0`. While `V(in) <= 1.0`, drive `out` with `V(in)`.

## Modeling Constraints

Use the same `1.0` threshold for the assertion and output clamp. Drive `out` as a continuous voltage-domain contribution; do not wrap the continuous input-dependent expression in `transition()`. Do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `cds_violation_threshold_assert.va`.
