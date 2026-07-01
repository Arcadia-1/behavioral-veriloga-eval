# Kcl Inductor Idt Voltage

Implement one Verilog-A source file named `kcl_inductor_idt_voltage.va`.

## Required Feature

Use voltage contribution with idt() of branch current for an inductor-style model.

## Required Interface

```verilog
module kcl_inductor_idt_voltage(
    inout electrical p,
    inout electrical n
);
```

## Required Behavior

- Declare `parameter real l = 1n`.
- Use the conservative voltage contribution `V(p, n) <+ l * idt(I(p, n), 0.0);`.
- This is a conservative-current/KCL plus continuous-time operator task. It is staged for syntax and simulator-boundary coverage, not ordinary voltage-domain behavioral-event scoring.
- Do not replace the branch-current `idt()` expression with a voltage follower or event-only approximation.

Return exactly one source artifact named `kcl_inductor_idt_voltage.va`.
