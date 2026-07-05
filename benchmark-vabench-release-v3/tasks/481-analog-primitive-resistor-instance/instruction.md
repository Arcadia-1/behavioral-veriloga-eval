# Analog Primitive Resistor Instance

## Task Contract

Implement one Verilog-A source file named `analog_primitive_resistor_instance.va`. This row is a Spectre analog-primitive instantiation semantic/support task, not a standalone resistor behavior benchmark.

## Form-Specific Requirements

This is a DUT-form structure row. The benchmark checks the public source artifact for the primitive instance contract and does not claim resistor current or full MNA/KCL behavior.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module analog_primitive_resistor_instance(
    inout electrical p,
    inout electrical n
);
```

## Public Parameter Contract

This module has no public module parameters. The primitive instance must use a fixed resistor value override of `1000.0` ohms.

## Required Behavior

Instantiate exactly one Spectre-style `resistor` primitive between `p` and `n` with `.r(1000.0)`. Use positional ports in the order `(p, n)`.

## Modeling Constraints

Do not replace the primitive with behavioral `V(...)` or `I(...)` contributions, a voltage source, or an unrelated output. This row certifies primitive-instantiation structure only.

## Output Contract

Return exactly one source artifact named `analog_primitive_resistor_instance.va`.
