# Signed Magnitude To Twos Complement 8b

## Task Contract

Implement one Verilog-A DUT file named `signmag_to_twos_8b.va`. The DUT is a
voltage-domain signed-code conversion utility for analog/mixed-signal test,
readout, and control paths.

## Form-Specific Requirements

This is a DUT implementation task. Return only the Verilog-A source artifact
for the converter; do not generate a Spectre testbench or auxiliary files.

## Public Verilog-A Interface

Define module `signmag_to_twos_8b` with vector electrical ports in this exact order:

```verilog
module signmag_to_twos_8b(
    input electrical sign,
    input electrical [6:0] mag,
    output electrical [7:0] y
);
```

## Public Parameter Contract

Expose compatible real parameters named `vdd`, `vth`, and `tr`. Their default
values are `vdd=0.9`, `vth=0.45`, and `tr=20p`. `vdd` is the logic-high output
level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the
output transition rise/fall time.

## Required Behavior

Treat `sign` and `mag[6:0]` as voltage-coded logic using `vth`, with `mag[0]`
as the least significant magnitude bit. Convert the sign-magnitude input to an
8-bit two's-complement output `y[7:0]`, with `y[0]` as the least significant
output bit. `sign=0` preserves the magnitude as a positive value. `sign=1`
outputs the two's-complement negative value for nonzero magnitude. Negative zero
must map to output zero.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A
contributions. Preserve the public bus bit order. Write the model so that
electrical vector-port access is legal in Cadence Spectre; constant-index
expansion or generate-time static expansion is acceptable.

## Output Contract

Return exactly one source artifact named `signmag_to_twos_8b.va`. Do not generate a Spectre testbench.
