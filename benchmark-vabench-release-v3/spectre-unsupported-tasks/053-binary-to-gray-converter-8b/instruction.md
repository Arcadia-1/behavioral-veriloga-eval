# Binary To Gray Converter 8b

## Task Contract

Implement one Verilog-A DUT file named `bin_to_gray_8b.va`. The DUT is a
voltage-domain binary-to-Gray encoder utility for analog/mixed-signal test and
control paths.

## Form-Specific Requirements

This is a DUT implementation task. Return only the Verilog-A source artifact
for the converter; do not generate a Spectre testbench or auxiliary files.

## Public Verilog-A Interface

Define module `bin_to_gray_8b` with vector electrical ports in this exact order:

```verilog
module bin_to_gray_8b(
    input electrical [7:0] b,
    output electrical [7:0] g
);
```

## Public Parameter Contract

Expose compatible real parameters named `vdd`, `vth`, and `tr`. Their default
values are `vdd=0.9`, `vth=0.45`, and `tr=20p`. `vdd` is the logic-high output
level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the
output transition rise/fall time.

## Required Behavior

Treat `b[7:0]` as voltage-coded logic using `vth`. Convert binary input
`b[7:0]` into Gray-code output `g[7:0]`, where `b[7]` and `g[7]` are the most
significant bits. The Gray MSB equals the binary MSB, and each lower Gray bit is
the XOR of adjacent binary bits.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A
contributions. Preserve the public bus bit order. Write the model so that
electrical vector-port access is legal in Cadence Spectre; constant-index
expansion or generate-time static expansion is acceptable.

## Output Contract

Return exactly one source artifact named `bin_to_gray_8b.va`. Do not generate a Spectre testbench.
