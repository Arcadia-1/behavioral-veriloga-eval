# Wreal Threshold Flag

Implement one Verilog-AMS source file named `wreal_threshold_flag.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `wreal` threshold logic with a continuous `assign`.

The module must have this interface:

```verilog
module wreal_threshold_flag(a, b, sel, y);
    input a, b, sel;
    output y;
    wreal a, b, sel, y;
```

Declare:

```verilog
parameter real offset = 0.1;
parameter real threshold = 0.45;
parameter real high = 0.9;
parameter real low = 0.0;
```

Drive `y` with one continuous assignment:

1. When `sel <= threshold`, compare `a` directly against `threshold`.
2. When `sel > threshold`, compare `a + offset` against `threshold`.
3. Drive `high` when the selected value is above threshold, otherwise drive `low`.

The evaluator samples both select states with an input near the threshold.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `wreal_threshold_flag.vams`.
