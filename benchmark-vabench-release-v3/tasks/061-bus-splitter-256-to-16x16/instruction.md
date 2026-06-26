# Bus Splitter 256 To 16x16

Implement one Verilog-A DUT file named `bus_split_256_to_16x16.va`.

## Interface

Define module `bus_split_256_to_16x16` with vector electrical ports in this exact order:

```verilog
module bus_split_256_to_16x16(
    input electrical [255:0] in_bus,
    output electrical [15:0] out15,
    output electrical [15:0] out14,
    output electrical [15:0] out13,
    output electrical [15:0] out12,
    output electrical [15:0] out11,
    output electrical [15:0] out10,
    output electrical [15:0] out9,
    output electrical [15:0] out8,
    output electrical [15:0] out7,
    output electrical [15:0] out6,
    output electrical [15:0] out5,
    output electrical [15:0] out4,
    output electrical [15:0] out3,
    output electrical [15:0] out2,
    output electrical [15:0] out1,
    output electrical [15:0] out0
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `in_bus[255:0]` as 0/0.9 V logic using `vth`. Map input bit `N` to output block `N/16` and bit `N%16` without inversion or reordering. For example, `in_bus[0]` drives `out0[0]`, `in_bus[15]` drives `out0[15]`, and `in_bus[255]` drives `out15[15]`.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred; do not manually expand 256 scalar input/output ports.

## Output

Return exactly `bus_split_256_to_16x16.va`. Do not generate a Spectre testbench.
