# Onehot To Binary Encoder 16b

## Task Contract

Implement one Verilog-A DUT file named `onehot_to_bin_16b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Form-Specific Requirements

This is a DUT implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Define module `onehot_to_bin_16b` with electrical ports in this exact order:

```verilog
module onehot_to_bin_16b(
    input electrical [15:0] oh,
    output electrical [3:0] b,
    output electrical valid
);
```

## Public Parameter Contract

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. `vdd` is the logic-high output level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the output transition rise/fall time.

## Required Behavior

Treat `oh[15:0]` as 0/0.9 V logic using `vth`. Encode a 16-line one-hot input into binary index `b[3:0]`. Drive `valid` high only when exactly one input is high. For zero-hot or multi-hot inputs, drive `valid` low and drive `b[3:0]` to zero.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.

For Spectre compatibility, access electrical vector ports with constant indices or generate-time static expansion. Do not use runtime/procedural integer indices such as `V(bus[i])` inside analog procedural loops.

## Output Contract

Return exactly one source artifact named `onehot_to_bin_16b.va`.
