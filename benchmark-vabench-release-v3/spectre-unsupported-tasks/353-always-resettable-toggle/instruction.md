# Always Resettable Toggle

Implement one Verilog-AMS source file named `always_resettable_toggle.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use edge-triggered `always` logic with asynchronous reset:

```verilog
always @(posedge clk or posedge rst)
```

When `rst` is high, clear `q` to `1'b0`. Otherwise, when both `en` and `d` are high on a positive clock edge, toggle `q` using logical `!q`; when either control is low, hold the previous value.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `always_resettable_toggle.vams`.
