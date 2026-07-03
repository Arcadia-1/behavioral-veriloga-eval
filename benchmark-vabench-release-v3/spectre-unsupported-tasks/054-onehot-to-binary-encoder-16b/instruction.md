# Onehot To Binary Encoder 16b

Implement one Verilog-A DUT file named `onehot_to_bin_16b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

Define module `onehot_to_bin_16b` with vector electrical ports in this exact order:

```verilog
module onehot_to_bin_16b(
    input electrical [15:0] oh,
    output electrical [3:0] b,
    output electrical valid
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `oh[15:0]` as 0/0.9 V logic using `vth`. Encode a 16-line one-hot input into binary index `b[3:0]`. Drive `valid` high only when exactly one input is high. For zero-hot or multi-hot inputs, drive `valid` low and drive `b[3:0]` to zero.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred.

## Output

Return exactly one source artifact named `onehot_to_bin_16b.va`. Do not generate a Spectre testbench.
