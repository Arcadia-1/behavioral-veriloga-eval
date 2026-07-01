# Logic Assign Inverter

Implement one Verilog-AMS source file named `logic_assign_inverter.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `logic` nets and a continuous `assign` for inversion.

The module must have this interface:

```verilog
module logic_assign_inverter(a, b, en, y);
    input a, b, en;
    output y;
    logic a, b, en, y;
```

Drive `y` with one continuous assignment:

1. When `en` is high, drive `y = !a`.
2. When `en` is low, drive `y = b`.

The evaluator samples enabled inversion and disabled pass-through behavior.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `logic_assign_inverter.vams`.
