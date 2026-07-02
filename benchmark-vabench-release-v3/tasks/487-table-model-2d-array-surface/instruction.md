# Table Model 2d Array Surface

Implement one Verilog-A source file named `table_model_2d_array_surface.va`.

## Required Feature

Use two independent arrays and one output array in a 2D $table_model().

## Required Interface

```verilog
module table_model_2d_array_surface(
    input electrical xnode,
    input electrical ynode,
    output electrical out
);
```

## Required Behavior

- Declare real arrays `x[0:3]`, `y[0:3]`, and `z[0:3]`.
- In an `@(initial_step)` block, initialize the four surface points:
  - `(x,y,z) = (0,0,0)`
  - `(x,y,z) = (1,0,1)`
  - `(x,y,z) = (0,1,2)`
  - `(x,y,z) = (1,1,3)`
- Compute `yv = $table_model(V(xnode), V(ynode), x, y, z, "1L,1L")`.
- Drive `out` with `yv` using `transition(..., 0, 200p, 200p)`.

Return exactly one source artifact named `table_model_2d_array_surface.va`.
