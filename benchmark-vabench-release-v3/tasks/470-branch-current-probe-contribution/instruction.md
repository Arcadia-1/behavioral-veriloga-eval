# Branch Current Probe Contribution

## Task Contract

Implement one Verilog-A source file named `branch_current_probe_contribution.va`. This row is a conservative-current branch semantic/support task: it verifies named-branch current contribution and current probing.

This is a DUT task in the conservative-current language-semantic layer. The saved `out` voltage is a validation monitor for the contributed branch current.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module branch_current_probe_contribution(
    input electrical p,
    input electrical n,
    output electrical out
);
```

## Public Parameter Contract

This module has no public module parameters. Use a fixed `transition(..., 0, 200p, 200p)` smoothing contract for the monitor output.

## Required Behavior

Declare an explicit branch named `br` between `p` and `n`. Contribute branch current with `I(br) <+ V(p,n)`. Probe the contributed branch current with `I(br)` and drive `out` with the fixed transition smoothing so the monitor follows the current sign and scale.

## Modeling Constraints

Keep the behavior in the named branch current contribution/probe path. Do not replace it with a voltage follower, threshold detector, or event-only approximation. The monitor is voltage-domain only so the supplied tests can save the branch-current value.

## Output Contract

Return exactly one source artifact named `branch_current_probe_contribution.va`.
