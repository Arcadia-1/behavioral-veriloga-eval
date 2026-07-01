# Always Enable Hold

Implement one Verilog-AMS source file named `always_enable_hold.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use an `always @(posedge clk)` block with synchronous reset and explicit enable/hold semantics.

The module must have this interface:

```verilog
module always_enable_hold(clk, rst, d, en, q);
    input clk, rst, d, en;
    output q;
    logic clk, rst, d, en, q;
```

On each positive clock edge:

- if `rst` is high, clear `q` to `1'b0`;
- else if `en` is high, update `q` from `d`;
- else hold the previous `q`, even if `d` changes.

Use an explicit hold assignment in the disabled branch.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `always_enable_hold.vams`.
