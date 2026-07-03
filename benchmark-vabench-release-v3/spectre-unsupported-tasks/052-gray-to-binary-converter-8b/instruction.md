# Gray To Binary Converter 8b

Implement one Verilog-A DUT file named `gray_to_bin_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

Define module `gray_to_bin_8b` with vector electrical ports in this exact order:

```verilog
module gray_to_bin_8b(
    input electrical [7:0] g,
    output electrical [7:0] b
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `g[7:0]` as 0/0.9 V logic using `vth`. Convert Gray-code input `g[7:0]` into binary output `b[7:0]`, where `g[7]` and `b[7]` are most significant bits.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred.

## Output

Return exactly one source artifact named `gray_to_bin_8b.va`. Do not generate a Spectre testbench.
