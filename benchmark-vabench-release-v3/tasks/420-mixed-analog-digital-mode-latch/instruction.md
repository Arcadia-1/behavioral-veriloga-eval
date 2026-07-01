# Mixed Analog Digital Mode Latch

Implement one behavioral Verilog-A source file named `mixed_analog_digital_mode_latch.vams`.

## Interface

Use this exact module interface:

```verilog
module mixed_analog_digital_mode_latch(vin, clk, flag);
```

The module must have scalar inputs `vin` and `clk` and scalar output `flag`. Declare `vin` as `electrical`; declare `clk` and `flag` as `logic`. Keep the model behavioral/digital and do not introduce current contributions.

## Required Behavior

Combine electrical threshold sampling with logic state output.

Required behavior:

- use `always @(posedge clk)`;
- on each rising clock edge, sample the electrical input with `V(vin)`;
- set `flag = 1'b1` when `V(vin) > 0.45` at that rising edge;
- set `flag = 1'b0` when `V(vin) <= 0.45` at that rising edge;
- hold the previous `flag` value between clock edges.

Return exactly one source artifact named `mixed_analog_digital_mode_latch.vams`.
