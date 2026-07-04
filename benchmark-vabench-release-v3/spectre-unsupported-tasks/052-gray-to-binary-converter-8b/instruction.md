# Gray To Binary Converter 8b

## Task Contract

Implement one Verilog-A DUT file named `gray_to_bin_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Form-Specific Requirements

This is a DUT implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Define module `gray_to_bin_8b` with electrical ports in this exact order:

```verilog
module gray_to_bin_8b(
    input electrical [7:0] g,
    output electrical [7:0] b
);
```

## Public Parameter Contract

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. `vdd` is the logic-high output level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the output transition rise/fall time.

## Required Behavior

Treat `g[7:0]` as 0/0.9 V logic using `vth`. Convert Gray-code input `g[7:0]` into binary output `b[7:0]`, where `g[7]` and `b[7]` are most significant bits.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.

For Spectre compatibility, access electrical vector ports with constant indices or generate-time static expansion. Do not use runtime/procedural integer indices such as `V(bus[i])` inside analog procedural loops.

## Output Contract

Return exactly one source artifact named `gray_to_bin_8b.va`.
