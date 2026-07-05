# Kcl Inductor Idt Voltage

## Task Contract

Implement one Verilog-A source file named `kcl_inductor_idt_voltage.va`. This row is a conservative-current plus continuous-time-operator semantic/support task for an inductor-style branch equation.

## Form-Specific Requirements

This is a DUT task in the conservative-current support layer. It verifies that branch current `I(p,n)` can feed `idt()` in a voltage contribution.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module kcl_inductor_idt_voltage(
    inout electrical p,
    inout electrical n
);
```

## Public Parameter Contract

Declare `parameter real l = 1n`. `l` is the inductance-like scale factor multiplying the integrated branch current.

## Required Behavior

Use the conservative voltage contribution `V(p, n) <+ l * idt(I(p, n), 0.0);`. The branch voltage must accumulate according to the signed branch current and reverse when the current direction reverses.

## Modeling Constraints

Keep the branch-current `idt()` expression in the voltage contribution. Do not replace it with a voltage follower, a static source, direct waveform samples, or an event-only approximation.

## Output Contract

Return exactly one source artifact named `kcl_inductor_idt_voltage.va`.
