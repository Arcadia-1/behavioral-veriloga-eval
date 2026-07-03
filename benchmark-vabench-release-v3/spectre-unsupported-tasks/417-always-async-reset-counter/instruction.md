# Always Async Reset Counter

Implement one behavioral Verilog-A source file named `always_async_reset_counter.vams`.

## Interface

Use this exact module interface:

```verilog
module always_async_reset_counter(clk, rst, en, q);
```

The module must have scalar `input clk, rst, en` and scalar `output q`. Keep the model behavioral/digital and do not introduce current contributions.

## Required Behavior

Use an always block with asynchronous reset sensitivity.

Required behavior:

- declare `logic clk, rst, en`;
- declare scalar `logic q`;
- use `always @(posedge clk or posedge rst)`;
- if `rst` is high at a triggering event, drive `q = 1'b0`;
- otherwise, if `en` is high on a rising clock edge, toggle `q` with `q = ~q`;
- otherwise hold the previous value of `q`;
- a rising edge of `rst` must reset `q` even when there is no clock edge.

Return exactly one source artifact named `always_async_reset_counter.vams`.
