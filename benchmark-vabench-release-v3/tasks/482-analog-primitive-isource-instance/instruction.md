# Analog Primitive Isource Instance

## Task Contract

Implement one Verilog-A source file named `analog_primitive_isource_instance.va`. This row is a Spectre analog-primitive instantiation semantic/support task, not a standalone current-source behavior benchmark.

## Form-Specific Requirements

This is a DUT-form structure row. The benchmark checks the public source artifact for the primitive instance contract and does not claim current-source circuit behavior or full MNA/KCL behavior.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module analog_primitive_isource_instance(
    inout electrical p,
    inout electrical n
);
```

## Public Parameter Contract

Declare `parameter real ibias = 1u`. The primitive dc value must reference this public parameter.

## Required Behavior

Instantiate exactly one Spectre-style `isource` primitive with `.dc(ibias)`. Connect the primitive with positional ports in the order `(n, p)`.

## Modeling Constraints

Do not replace the primitive with behavioral `V(...)` or `I(...)` contributions, a voltage-domain output, or an unrelated source model. This row certifies primitive-instantiation structure only.

## Output Contract

Return exactly one source artifact named `analog_primitive_isource_instance.va`.
