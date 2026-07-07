# KCL Capacitor Ddt Current

## Task Contract

Implement one Verilog-A source file named `kcl_capacitor_ddt_current.va`. The task models a capacitor-style conservative current contribution and exposes a monitor of the contributed dynamic branch current.

This is a DUT task in the conservative-current layer. The `imon` voltage is a validation monitor for the branch current contribution.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module kcl_capacitor_ddt_current(
    inout electrical p,
    inout electrical n,
    output electrical imon
);
```

## Public Parameter Contract

Declare `parameter real c = 1p` and `parameter real tr = 200p`. `c` is the capacitance multiplying `ddt(V(p,n))`; `tr` is the monitor transition rise/fall time.

## Required Behavior

Use the conservative current contribution `I(p, n) <+ c * ddt(V(p, n));`. Drive `imon` with the probed branch current so ramping `V(p,n)` stimuli expose the derivative current sign and scale.

## Modeling Constraints

Keep `ddt(V(p,n))` in the branch current contribution. Do not replace the model with a voltage follower, static conductance, or event-only approximation. The monitor may use `transition(I(p, n), 0, tr, tr)`.

## Output Contract

Return exactly one source artifact named `kcl_capacitor_ddt_current.va`.
