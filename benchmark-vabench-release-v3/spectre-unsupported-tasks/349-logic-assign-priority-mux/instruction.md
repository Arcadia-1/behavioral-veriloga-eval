# Logic Assign Priority Mux

Implement one Verilog-AMS source file named `logic_assign_priority_mux.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use a `logic` ternary mux with one continuous `assign`.

The module must have this interface:

```verilog
module logic_assign_priority_mux(a, b, en, y);
    input a, b, en;
    output y;
    logic a, b, en, y;
```

Drive `y` from `a` when `en` is high, otherwise drive `y` from `b`:

```verilog
assign y = en ? a : b;
```

The evaluator samples the disabled path, the enabled-high path, and the enabled-low path.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `logic_assign_priority_mux.vams`.
