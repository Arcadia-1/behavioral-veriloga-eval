# Indirect Branch Ddt Balance

Implement one Verilog-A source file named `indirect_branch_ddt_balance.va`.

## Required Feature

Use indirect branch assignment with a ddt() equation term.

## Required Interface

```verilog
module indirect_branch_ddt_balance(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Use the Verilog-A indirect branch assignment/equation form.
- Constrain `out` with the dynamic equation `V(out) : ddt(V(out)) == V(in)`.
- Do not use explicit current contributions.
- The visible and hidden testbenches drive the input node and require `out` to match the time integral implied by the indirect `ddt()` branch equation.

Return exactly one source artifact named `indirect_branch_ddt_balance.va`.
