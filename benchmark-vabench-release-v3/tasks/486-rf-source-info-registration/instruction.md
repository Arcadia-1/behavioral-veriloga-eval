# RF Source Info Registration

## Task Contract

Implement one Verilog-A source file named `rf_source_info_registration.va`. The task models an RF source-info registration helper with an ordinary transient-observable frequency offset.

This is a DUT task for a Cadence simulator function. The registration call is part of the public modeling contract even though the transient checker observes the frequency parameter through `out`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module rf_source_info_registration(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

Declare `parameter string fundname = "rf"` and `parameter real freq = 1G`. `fundname` is the RF source name and `freq` is the registered frequency in hertz.

## Required Behavior

Call `$cds_set_rf_source_info(fundname, freq)` in the continuous analog context. Drive `out` with `V(in) + freq / 1.0e10`.

## Modeling Constraints

Do not place `$cds_set_rf_source_info` inside `@(initial_step)`, a conditional statement, or an expression. Drive `out` as a continuous voltage-domain contribution; do not wrap the continuous input-dependent expression in `transition()`.

## Output Contract

Return exactly one source artifact named `rf_source_info_registration.va`.
