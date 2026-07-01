# Wreal Two Input Summer

Implement one Verilog-AMS source file named `wreal_two_input_summer.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `wreal` nets and a continuous `assign` for a real-valued two-input summer.

The module must have this interface:

```verilog
module wreal_two_input_summer(a, b, sel, y);
    input a, b, sel;
    output y;
    wreal a, b, sel, y;
```

Declare:

```verilog
parameter real offset = 0.1;
parameter real threshold = 0.45;
```

Drive `y` with one continuous assignment:

1. When `sel <= threshold`, drive `y = a + b`.
2. When `sel > threshold`, drive `y = a + b + offset`.

The evaluator samples both select states and checks that both wreal inputs contribute to the sum.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `wreal_two_input_summer.vams`.
