# Wreal Clamped Mux

Implement one Verilog-AMS source file named `wreal_clamped_mux.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `wreal` select behavior with a continuous `assign`.

The module must have this interface:

```verilog
module wreal_clamped_mux(a, b, sel, y);
    input a, b, sel;
    output y;
    wreal a, b, sel, y;
```

Declare `threshold = 0.45`, `high = 0.9`, and `low = 0.0`.

Drive `y` with one continuous assignment:

1. Select `b` when `sel <= threshold`.
2. Select `a` when `sel > threshold`.
3. Clamp the selected value to `[low, high]`.

The evaluator samples both select states with one input below `low` and one input above `high`.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `wreal_clamped_mux.vams`.
