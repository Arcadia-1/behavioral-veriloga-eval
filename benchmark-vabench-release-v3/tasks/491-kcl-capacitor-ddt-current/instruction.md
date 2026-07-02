# Kcl Capacitor Ddt Current

Implement one Verilog-A source file named `kcl_capacitor_ddt_current.va`.

## Required Feature

Use current contribution with ddt() for a capacitor-style conservative model.

## Required Interface

```verilog
module kcl_capacitor_ddt_current(
    inout electrical p,
    inout electrical n
);
```

## Required Behavior

- Declare `parameter real c = 1p`.
- Use the conservative current contribution `I(p, n) <+ c * ddt(V(p, n));`.
- This is a conservative-current/KCL-layer task, but the checker observes the contributed branch current through a harness monitor rather than requiring an unknown-node MNA solve.
- Do not replace the model with `V(...) <+ ...`, a voltage follower, or an event-only approximation.

Return exactly one source artifact named `kcl_capacitor_ddt_current.va`.
