# Analog Node Alias Initial

## Task Contract

Implement one Verilog-A source file named `analog_node_alias_initial.va`. This task exercises analog-initial node aliasing from an internal node to a named external node.

## Form-Specific Requirements

This is a Verilog-A semantic/support task. The output must depend on the alias installed by `$analog_node_alias`, not on an added ordinary input port.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module analog_node_alias_initial(
    output electrical out
);
```

Declare an internal electrical node named `aliased`.

## Public Parameter Contract

Declare `parameter string target_path = "$root.vin";`. The parameter names the external node that the internal alias should reference.

## Required Behavior

In an `analog initial` block, call `$analog_node_alias(aliased, target_path)`. Drive `out` from `V(aliased)`.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Do not add ordinary electrical input ports or bypass the alias feature.

## Output Contract

Return exactly one source artifact named `analog_node_alias_initial.va`.
