# Logic Assign Xor Flag

Implement one Verilog-AMS source file named `logic_assign_xor_flag.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `logic` XOR with a continuous `assign`.

The module must have this interface:

```verilog
module logic_assign_xor_flag(a, b, en, y);
    input a, b, en;
    output y;
    logic a, b, en, y;
```

Drive `y` with one continuous assignment:

```verilog
assign y = en ? (a ^ b) : 1'b0;
```

The evaluator samples XOR-high, XOR-low, and enable-disabled states.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `logic_assign_xor_flag.vams`.
