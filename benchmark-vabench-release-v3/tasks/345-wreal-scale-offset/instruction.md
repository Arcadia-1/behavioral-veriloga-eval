# Wreal Scale Offset

Implement one Verilog-AMS source file named `wreal_scale_offset.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `wreal` affine scaling with a continuous `assign`.

The module must have this interface:

```verilog
module wreal_scale_offset(a, b, sel, y);
    input a, b, sel;
    output y;
    wreal a, b, sel, y;
```

Declare `gain = 0.75`, `offset = 0.1`, and `threshold = 0.45`.

Drive `y` with one continuous assignment:

1. When `sel <= threshold`, drive `y = gain * a + offset`.
2. When `sel > threshold`, drive `y = gain * b - offset`.

The evaluator samples both select states and checks that the affine gain and offset are applied with the correct sign.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `wreal_scale_offset.vams`.
