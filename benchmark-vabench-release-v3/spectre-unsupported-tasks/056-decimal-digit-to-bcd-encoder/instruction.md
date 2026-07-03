# Decimal Digit To BCD Encoder

Implement one Verilog-A DUT file named `decimal_to_bcd.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

Define module `decimal_to_bcd` with vector electrical ports in this exact order:

```verilog
module decimal_to_bcd(
    input electrical [9:0] d,
    output electrical [3:0] b,
    output electrical valid
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `d[9:0]` as 0/0.9 V logic using `vth`. Encode one-hot decimal digit input into BCD output `b[3:0]`. Drive `valid` high only when exactly one digit input is high. For zero-hot or multi-hot inputs, drive `valid` low and drive `b[3:0]` to zero.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred.

## Output

Return exactly one source artifact named `decimal_to_bcd.va`. Do not generate a Spectre testbench.
