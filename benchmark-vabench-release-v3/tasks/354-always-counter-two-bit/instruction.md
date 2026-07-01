# Always Counter Two Bit

Implement one Verilog-AMS source file named `always_counter_two_bit.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use an `always @(posedge clk)` block with a small two-bit digital counter state.

The module must have this interface:

```verilog
module always_counter_two_bit(clk, rst, d, en, q);
    input clk, rst, d, en;
    output q;
    logic clk, rst, d, en, q;
    logic [1:0] count;
```

On each positive clock edge:

- if `rst` is high, set `count` to `2'b00`;
- else if both `en` and `d` are high, increment `count` by one;
- otherwise hold the previous `count`.

Continuously drive `q` from the counter MSB:

```verilog
assign q = count[1];
```

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `always_counter_two_bit.vams`.
