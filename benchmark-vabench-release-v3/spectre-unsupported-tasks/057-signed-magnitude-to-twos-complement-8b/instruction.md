# Signed Magnitude To Twos Complement 8b

## Task Contract

Implement one Verilog-A DUT file named `signmag_to_twos_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Form-Specific Requirements

This is a DUT implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Define module `signmag_to_twos_8b` with electrical ports in this exact order:

```verilog
module signmag_to_twos_8b(
    input electrical sign,
    input electrical [6:0] mag,
    output electrical [7:0] y
);
```

## Public Parameter Contract

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. `vdd` is the logic-high output level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the output transition rise/fall time.

## Required Behavior

Treat `sign` and `mag[6:0]` as 0/0.9 V logic using `vth`. Convert sign-magnitude input to 8-bit two's-complement output. `sign=0` preserves `mag[6:0]` as a positive value. `sign=1` outputs the two's-complement negative value for nonzero magnitude. Negative zero must map to output zero.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.

For Spectre compatibility, access electrical vector ports with constant indices or generate-time static expansion. Do not use runtime/procedural integer indices such as `V(bus[i])` inside analog procedural loops.

## Output Contract

Return exactly one source artifact named `signmag_to_twos_8b.va`.
