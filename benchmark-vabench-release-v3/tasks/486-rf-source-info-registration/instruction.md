# Rf Source Info Registration

Implement one Verilog-A source file named `rf_source_info_registration.va`.

## Required Feature

Use $cds_set_rf_source_info() to register an RF source name and frequency.

## Required Interface

```verilog
module rf_source_info_registration(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Declare `parameter string fundname = "rf";`.
- Declare `parameter real freq = 1G;`.
- In an `@(initial_step)` block, call `$cds_set_rf_source_info(fundname, freq)`.
- Drive `out` with `V(in) + freq / 1.0e10` using `transition(..., 0, 200p, 200p)`.
- The output term makes the registered frequency parameter observable in ordinary transient tests.

Return exactly one source artifact named `rf_source_info_registration.va`.
