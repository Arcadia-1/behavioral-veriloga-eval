# Binary To Onehot Decoder 16b

## Task Contract

Implement one Verilog-A DUT file named `bin_to_onehot_16b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Form-Specific Requirements

This is a DUT implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Define module `bin_to_onehot_16b` with electrical ports in this exact order:

```verilog
module bin_to_onehot_16b(
    input electrical en,
    input electrical [3:0] b,
    output electrical [15:0] oh
);
```

## Public Parameter Contract

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. `vdd` is the logic-high output level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the output transition rise/fall time.

## Required Behavior

Treat `en` and `b[3:0]` as 0/0.9 V logic using `vth`. Decode binary input `b[3:0]` into one-hot output `oh[15:0]` when `en` is high. Exactly one output, `oh[code]`, must be high. When `en` is low, all one-hot outputs must be low.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.

For Spectre compatibility, access electrical vector ports with constant indices or generate-time static expansion. Do not use runtime/procedural integer indices such as `V(bus[i])` inside analog procedural loops.

## Output Contract

Return exactly one source artifact named `bin_to_onehot_16b.va`.
