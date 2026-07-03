# Binary To Onehot Decoder 16b

## Task Contract

Implement one Verilog-A DUT file named `bin_to_onehot_16b.va`. The DUT is a
voltage-domain binary-to-one-hot decoder utility for analog/mixed-signal
stimulus, selection, and readout paths.

## Form-Specific Requirements

This is a DUT implementation task. Return only the Verilog-A source artifact
for the decoder; do not generate a Spectre testbench or auxiliary files.

## Public Verilog-A Interface

Define module `bin_to_onehot_16b` with vector electrical ports in this exact order:

```verilog
module bin_to_onehot_16b(
    input electrical en,
    input electrical [3:0] b,
    output electrical [15:0] oh
);
```

## Public Parameter Contract

Expose compatible real parameters named `vdd`, `vth`, and `tr`. Their default
values are `vdd=0.9`, `vth=0.45`, and `tr=20p`. `vdd` is the logic-high output
level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the
output transition rise/fall time.

## Required Behavior

Treat `en` and `b[3:0]` as voltage-coded logic using `vth`. Decode unsigned
binary input `b[3:0]` into one-hot output `oh[15:0]` when `en` is high, with
`b[0]` as the least significant input bit. Exactly one output, `oh[code]`, must
be high. When `en` is low, all one-hot outputs must be low.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A
contributions. Preserve the public bus bit order. Write the model so that
electrical vector-port access is legal in Cadence Spectre; constant-index
expansion or generate-time static expansion is acceptable.

## Output Contract

Return exactly one source artifact named `bin_to_onehot_16b.va`. Do not generate a Spectre testbench.
