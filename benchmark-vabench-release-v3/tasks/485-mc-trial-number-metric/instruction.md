# Mc Trial Number Metric

Implement one Verilog-A source file named `mc_trial_number_metric.va`.

## Required Feature

Use $cds_get_mc_trial_number() to expose the Monte Carlo trial index.

## Required Interface

```verilog
module mc_trial_number_metric(
    output electrical out
);
```

## Required Behavior

- In an `@(initial_step)` block, read the trial index with `$cds_get_mc_trial_number()`.
- Store the result in an integer named `trial_num`.
- Drive `out` with `0.25 + 0.1 * trial_num` using `transition(..., 0, 200p, 200p)`.
- In the default non-Monte-Carlo transient tests, `trial_num` is expected to be `0`, so `out` should settle to `0.25`.

Return exactly one source artifact named `mc_trial_number_metric.va`.
