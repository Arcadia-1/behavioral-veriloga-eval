# Mixed Wreal To Electrical Buffer

Implement one Verilog-AMS source file named `mixed_wreal_to_electrical_buffer.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Bridge a `wreal` value into an electrical voltage output.

The module must have this interface:

```verilog
module mixed_wreal_to_electrical_buffer(vin, clk, en, sel, a, b, vout);
    input vin, clk, en, sel, a, b;
    output vout;
    electrical vin, vout;
    logic clk, en, sel;
    wreal a, b, level;
```

Continuously assign the internal `wreal` level from input `a`:

```verilog
assign level = a;
```

In the analog block, drive `V(vout)` from `level` using `transition(level, 0.0, tr, tr)`. Do not use `vin`, `b`, `sel`, or `en` to determine `vout` in this task.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `mixed_wreal_to_electrical_buffer.vams`.
