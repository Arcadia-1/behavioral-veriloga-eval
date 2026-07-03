# Logic Assign Reduction

Implement one Verilog-AMS source file named `logic_assign_reduction.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use a `logic` reduction-like combinational continuous assignment.

The module must have this interface:

```verilog
module logic_assign_reduction(a, b, en, y);
    input a, b, en;
    output y;
    logic a, b, en, y;
```

Drive `y` high only when all three inputs are high:

```verilog
assign y = a & b & en;
```

The evaluator samples the all-high case and each single-low blocking case.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `logic_assign_reduction.vams`.
