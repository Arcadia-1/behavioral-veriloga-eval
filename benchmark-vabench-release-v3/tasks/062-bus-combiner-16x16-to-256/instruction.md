# Bus Combiner 16x16 To 256

Implement one Verilog-A DUT file named `bus_combine_16x16_to_256.va`.

## Interface

Define module `bus_combine_16x16_to_256` with vector electrical ports in this exact order:

```verilog
module bus_combine_16x16_to_256(
    input electrical [15:0] in15,
    input electrical [15:0] in14,
    input electrical [15:0] in13,
    input electrical [15:0] in12,
    input electrical [15:0] in11,
    input electrical [15:0] in10,
    input electrical [15:0] in9,
    input electrical [15:0] in8,
    input electrical [15:0] in7,
    input electrical [15:0] in6,
    input electrical [15:0] in5,
    input electrical [15:0] in4,
    input electrical [15:0] in3,
    input electrical [15:0] in2,
    input electrical [15:0] in1,
    input electrical [15:0] in0,
    output electrical [255:0] out_bus
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat all input buses as 0/0.9 V logic using `vth`. Map input block `B` bit `K` to `out_bus[16*B+K]` without inversion or reordering. For example, `in0[0]` drives `out_bus[0]`, `in0[15]` drives `out_bus[15]`, and `in15[15]` drives `out_bus[255]`.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred; do not manually expand 256 scalar input/output ports.

## Output

Return exactly `bus_combine_16x16_to_256.va`. Do not generate a Spectre testbench.
