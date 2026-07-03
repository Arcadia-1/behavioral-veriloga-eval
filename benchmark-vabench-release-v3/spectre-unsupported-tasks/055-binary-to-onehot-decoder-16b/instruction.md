# Binary To Onehot Decoder 16b

Implement one Verilog-A DUT file named `bin_to_onehot_16b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

Define module `bin_to_onehot_16b` with vector electrical ports in this exact order:

```verilog
module bin_to_onehot_16b(
    input electrical en,
    input electrical [3:0] b,
    output electrical [15:0] oh
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `en` and `b[3:0]` as 0/0.9 V logic using `vth`. Decode binary input `b[3:0]` into one-hot output `oh[15:0]` when `en` is high. Exactly one output, `oh[code]`, must be high. When `en` is low, all one-hot outputs must be low.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred.

## Output

Return exactly one source artifact named `bin_to_onehot_16b.va`. Do not generate a Spectre testbench.
