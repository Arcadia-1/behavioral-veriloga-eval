# Table Model 2D Array Surface

## Task Contract

Implement one Verilog-A source file named `table_model_2d_array_surface.va`. This task exercises a 2D `$table_model()` surface backed by Verilog-A real arrays.

This is a Verilog-A semantic/support task. The surface value must come from `$table_model()` using the supplied arrays, not from a manually coded closed-form replacement.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module table_model_2d_array_surface(
    input electrical xnode,
    input electrical ynode,
    output electrical out
);
```

## Public Parameter Contract

This task has no public Verilog-A parameters.

## Required Behavior

Declare real arrays `x[0:3]`, `y[0:3]`, and `z[0:3]`. Initialize four surface points during `@(initial_step)`: `(0,0,0)`, `(1,0,1)`, `(0,1,2)`, and `(1,1,3)`. Evaluate `$table_model(V(xnode), V(ynode), x, y, z, "1L,1L")` and drive `out` with the returned value.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Use voltage-domain behavior and do not use current contributions.

## Output Contract

Return exactly one source artifact named `table_model_2d_array_surface.va`.
