# Always Posedged Dff

Implement one Verilog-AMS source file named `always_posedged_dff.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use `always @(posedge clk)` for a `logic` DFF with synchronous reset and enable hold.

The module must have this interface:

```verilog
module always_posedged_dff(clk, rst, d, en, q);
    input clk, rst, d, en;
    output q;
    logic clk, rst, d, en, q;
```

On each positive clock edge:

- if `rst` is high, drive `q` to `1'b0`;
- else if `en` is high, update `q` from `d`;
- else hold the previous `q`.

Use blocking assignment inside the `always` block.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `always_posedged_dff.vams`.
