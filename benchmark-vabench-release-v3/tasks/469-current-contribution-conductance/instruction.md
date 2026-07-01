# Current Contribution Conductance

Implement one Verilog-A source file named `current_contribution_conductance.va`.

## Required Feature

Use I(p,n) current contribution for a conductance-style model.

## Required Interface

```verilog
module current_contribution_conductance(
    input electrical p,
    input electrical n
);
```

## Required Behavior

- Declare `parameter real gain = 1e-3`.
- Implement a conservative conductance from `p` to `n` using exactly the current-domain contribution form `I(p, n) <+ gain * V(p, n)`.
- Do not drive voltage-domain outputs; this task is intentionally in the conservative-current/KCL layer.
- The visible and hidden testbenches instantiate the conductance with a voltage source across `p` and `n`.
- This task is not part of the ordinary behavioral-event score until EVAS has KCL/MNA behavior certification for current contributions.

Return exactly one source artifact named `current_contribution_conductance.va`.
