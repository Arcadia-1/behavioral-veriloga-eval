# Current Contribution Conductance

## Task Contract

Implement one Verilog-A source file named `current_contribution_conductance.va`. The task models a conservative conductance current contribution and exposes a voltage-domain monitor of the contributed branch current for validation.

## Form-Specific Requirements

This is a DUT task in the conservative-current layer. The saved `imon` voltage is an observable monitor port, not a replacement for the required current contribution.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module current_contribution_conductance (
    inout electrical p,
    inout electrical n,
    output electrical imon
);
```

## Public Parameter Contract

Declare `parameter real gain = 1e-3` and `parameter real tr = 200p`. `gain` is the conductance from `p` to `n`; `tr` is the monitor transition rise/fall time.

## Required Behavior

Contribute branch current from `p` to `n` proportional to branch voltage: `I(p, n) <+ gain * V(p, n)`. Drive `imon` with the probed branch current so the supplied voltage-driven Spectre tests can observe sign and scale.

## Modeling Constraints

Keep the current contribution on the conservative branch. Do not replace the model with a voltage follower or an event-only approximation. The monitor may use `transition(I(p, n), 0, tr, tr)` to expose the branch current as a voltage-domain validation signal.

## Output Contract

Return exactly one source artifact named `current_contribution_conductance.va`.
