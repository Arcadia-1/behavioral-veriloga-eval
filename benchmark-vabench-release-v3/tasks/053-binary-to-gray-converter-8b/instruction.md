# Binary To Gray Converter 8b

Implement one Verilog-A DUT file named `bin_to_gray_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

Define module `bin_to_gray_8b` with vector electrical ports in this exact order:

```verilog
module bin_to_gray_8b(
    input electrical [7:0] b,
    output electrical [7:0] g
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `b[7:0]` as 0/0.9 V logic using `vth`. Convert binary input `b[7:0]` into Gray-code output `g[7:0]`, where `g[7] = b[7]` and each lower Gray bit is the XOR of adjacent binary bits.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred.

## Output

Return exactly one source artifact named `bin_to_gray_8b.va`. Do not generate a Spectre testbench.
