# Indirect Branch Ddt Balance

## Task Contract

Implement one Verilog-A source file named `indirect_branch_ddt_balance.va`. The task models a stable dynamic indirect branch equation with a `ddt()` term.

## Form-Specific Requirements

This is a DUT task. The behavior should be implemented with an indirect branch assignment, not by replacing the equation with a normal voltage contribution.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module indirect_branch_ddt_balance(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

Declare `parameter real tau = 20n from (0:inf)`. `tau` is the time constant of the dynamic balance.

## Required Behavior

Use the indirect assignment target `V(out)` with the dynamic equation `ddt(V(out)) == (V(in) - V(out)) / tau`. This gives a Spectre-solvable first-order dynamic balance with a DC operating point.

## Modeling Constraints

Keep `ddt(V(out))` in the indirect branch equation. Do not use a pure unconstrained integrator, event-only approximation, or explicit current contribution.

## Output Contract

Return exactly one source artifact named `indirect_branch_ddt_balance.va`.
