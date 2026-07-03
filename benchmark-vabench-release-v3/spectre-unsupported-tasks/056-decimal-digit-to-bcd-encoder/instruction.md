# Decimal Digit To BCD Encoder

## Task Contract

Implement one Verilog-A DUT file named `decimal_to_bcd.va`. The DUT is a
voltage-domain decimal-digit encoder utility for analog/mixed-signal display,
readout, and stimulus helper paths.

## Form-Specific Requirements

This is a DUT implementation task. Return only the Verilog-A source artifact
for the encoder; do not generate a Spectre testbench or auxiliary files.

## Public Verilog-A Interface

Define module `decimal_to_bcd` with vector electrical ports in this exact order:

```verilog
module decimal_to_bcd(
    input electrical [9:0] d,
    output electrical [3:0] b,
    output electrical valid
);
```

## Public Parameter Contract

Expose compatible real parameters named `vdd`, `vth`, and `tr`. Their default
values are `vdd=0.9`, `vth=0.45`, and `tr=20p`. `vdd` is the logic-high output
level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the
output transition rise/fall time.

## Required Behavior

Treat `d[9:0]` as voltage-coded logic using `vth`. Encode one-hot decimal digit
input into BCD output `b[3:0]`, with `d[i]` mapping to decimal digit `i` and
`b[0]` as the least significant output bit. Drive `valid` high only when exactly
one digit input is high. For zero-hot or multi-hot inputs, drive `valid` low and
drive `b[3:0]` to zero.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A
contributions. Preserve the public bus bit order. Write the model so that
electrical vector-port access is legal in Cadence Spectre; constant-index
expansion or generate-time static expansion is acceptable.

## Output Contract

Return exactly one source artifact named `decimal_to_bcd.va`. Do not generate a Spectre testbench.
