# Mc Trial Number Metric

## Task Contract

Implement one Verilog-A source file named `mc_trial_number_metric.va`. The task is an L0/support row for exposing the Cadence Monte Carlo trial index.

## Form-Specific Requirements

This is a DUT task for Cadence simulator-function semantics. In ordinary non-Monte-Carlo transient tests, the trial index is expected to be zero.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module mc_trial_number_metric(
    output electrical out
);
```

## Public Parameter Contract

This task has no public parameters.

## Required Behavior

In an `@(initial_step)` block, read the trial index with `$cds_get_mc_trial_number()` and store it in an integer named `trial_num`. Drive `out` with `0.25 + 0.1 * trial_num`.

## Modeling Constraints

Use `$cds_get_mc_trial_number()` only to read the simulator trial index. Drive `out` with `transition(..., 0, 200p, 200p)`. Use only voltage-domain contributions and do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `mc_trial_number_metric.va`.
