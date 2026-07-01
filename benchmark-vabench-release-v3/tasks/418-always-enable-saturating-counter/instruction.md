# Always Enable Saturating Counter

Implement one behavioral Verilog-A source file named `always_enable_saturating_counter.vams`.

## Interface

Use this exact module interface:

```verilog
module always_enable_saturating_counter(clk, rst, en, q);
```

The module must have scalar `input clk, rst, en` and a two-bit `output [1:0] q`. Keep the model behavioral/digital and do not introduce current contributions.

## Required Behavior

Use an always block for enabled saturating state update.

Required behavior:

- declare `logic clk, rst, en`;
- declare `logic [1:0] q`;
- use `always @(posedge clk)`;
- when `rst` is high at a rising clock edge, set `q = 2'b00`;
- when `rst` is low and `en` is high, increment `q` by one until it reaches `2'b11`;
- once `q` is `2'b11`, further enabled clock edges must hold it at `2'b11`;
- when `en` is low, hold the previous `q` value.

Return exactly one source artifact named `always_enable_saturating_counter.vams`.
