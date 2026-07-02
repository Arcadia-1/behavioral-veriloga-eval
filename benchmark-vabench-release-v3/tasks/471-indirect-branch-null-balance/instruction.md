# Indirect Branch Null Balance

Implement one Verilog-A source file named `indirect_branch_null_balance.va`.

## Required Feature

Use an indirect branch assignment target/equation form.

## Required Interface

```verilog
module indirect_branch_null_balance(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Use the Verilog-A indirect branch assignment/equation form.
- Constrain `out` with the null-balance equation `V(out) : V(out) - V(in) == 0`.
- Do not use explicit current contributions.
- The visible and hidden testbenches drive the input node and require `out` to track the solved indirect-branch relationship across all PWL segments.

Return exactly one source artifact named `indirect_branch_null_balance.va`.
