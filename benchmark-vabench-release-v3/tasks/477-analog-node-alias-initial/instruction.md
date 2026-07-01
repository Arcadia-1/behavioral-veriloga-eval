# Analog Node Alias Initial

Implement one Verilog-A source file named `analog_node_alias_initial.va`.

## Required Feature

Use $analog_node_alias inside analog initial for hierarchical node aliasing.

## Required Interface

```verilog
module analog_node_alias_initial(
    output electrical out
);
```

## Required Behavior

- Declare an internal electrical node named `aliased`.
- Declare a string parameter named `target_path` with default value `"$root.vin"`.
- In an `analog initial` block, call `$analog_node_alias(aliased, target_path)`.
- Drive `out` from `V(aliased)` using `transition(..., 0, 200p, 200p)`.
- Do not add ordinary electrical input ports to bypass the alias feature.

Return exactly one source artifact named `analog_node_alias_initial.va`.
