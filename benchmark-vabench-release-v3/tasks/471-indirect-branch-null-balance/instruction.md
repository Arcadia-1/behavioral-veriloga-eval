# Indirect Branch Null Balance

## Task Contract

Implement one Verilog-A source file named `indirect_branch_null_balance.va`. The task models a static indirect branch assignment that solves `out` from a voltage equality.

This is a DUT task. The solver should implement the indirect branch assignment form directly, not a normal `V(out) <+ ...` contribution.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module indirect_branch_null_balance(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This task has no public parameters.

## Required Behavior

Use the Cadence indirect branch assignment form to solve `out` such that `V(out) == V(in)`. The supplied PWL tests require `out` to track the input across all segments.

## Modeling Constraints

Use `V(out)` as the indirect assignment target and keep the equation left side to a valid branch quantity form. Do not use explicit current contributions.

## Output Contract

Return exactly one source artifact named `indirect_branch_null_balance.va`.
