# Logic Assign And Or

Implement one Verilog-AMS source file named `logic_assign_and_or.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `logic` nets and a bitwise continuous `assign`.

The module must have this interface:

```verilog
module logic_assign_and_or(a, b, en, y);
    input a, b, en;
    output y;
    logic a, b, en, y;
```

Drive `y` with one continuous assignment:

```verilog
assign y = (a & b) | en;
```

The evaluator samples all three important states: both terms low, the `a & b` term high, and the `en` term high.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `logic_assign_and_or.vams`.
