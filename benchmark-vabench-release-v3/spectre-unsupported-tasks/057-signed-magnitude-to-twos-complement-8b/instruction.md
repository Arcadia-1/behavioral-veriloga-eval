# Signed Magnitude To Twos Complement 8b

Implement one Verilog-A DUT file named `signmag_to_twos_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

Define module `signmag_to_twos_8b` with vector electrical ports in this exact order:

```verilog
module signmag_to_twos_8b(
    input electrical sign,
    input electrical [6:0] mag,
    output electrical [7:0] y
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `sign` and `mag[6:0]` as 0/0.9 V logic using `vth`. Convert sign-magnitude input to 8-bit two's-complement output. `sign=0` preserves `mag[6:0]` as a positive value. `sign=1` outputs the two's-complement negative value for nonzero magnitude. Negative zero must map to output zero.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred.

## Output

Return exactly one source artifact named `signmag_to_twos_8b.va`. Do not generate a Spectre testbench.
