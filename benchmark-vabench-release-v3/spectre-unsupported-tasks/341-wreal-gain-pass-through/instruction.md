# Wreal Gain Pass Through

Implement one Verilog-AMS source file named `wreal_gain_pass_through.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `wreal` nets and a continuous `assign` for real-valued pass-through gain.

The module must have this interface:

```verilog
module wreal_gain_pass_through(a, b, sel, y);
    input a, b, sel;
    output y;
    wreal a, b, sel, y;
```

Declare these parameters:

```verilog
parameter real gain = 0.75;
parameter real offset = 0.1;
parameter real threshold = 0.45;
```

Drive `y` with one continuous assignment:

1. When `sel > threshold`, drive `y = gain * a + offset`.
2. Otherwise, drive `y = gain * b`.

The evaluator samples both select states and checks that the real-valued `wreal` continuous assignment is functional.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `wreal_gain_pass_through.vams`.
