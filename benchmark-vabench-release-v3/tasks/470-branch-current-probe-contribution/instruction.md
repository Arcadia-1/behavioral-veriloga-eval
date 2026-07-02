# Branch Current Probe Contribution

Implement one Verilog-A source file named `branch_current_probe_contribution.va`.

## Required Feature

Use a named branch with current contribution and current probing.

## Required Interface

```verilog
module branch_current_probe_contribution(
    input electrical p,
    input electrical n,
    output electrical out
);
```

## Required Behavior

- Declare an explicit branch named `br` between `p` and `n`.
- Add a current-domain contribution on that branch with `I(br) <+ V(p,n)`.
- Probe the branch current with `I(br)` and drive `out` with `transition(I(br), 0, 200p, 200p)`.
- This task is intentionally in the conservative-current/KCL layer. It requires current contribution and branch current semantics, not just event-level voltage behavior.
- The visible and hidden testbenches instantiate the model with a driven voltage across `p` and `n` and save `p`, `n`, and `out`.

Return exactly one source artifact named `branch_current_probe_contribution.va`.
