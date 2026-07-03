# Onehot To Binary Encoder 16b

## Task Contract

Implement one Verilog-A DUT file named `onehot_to_bin_16b.va`. The DUT is a
voltage-domain one-hot encoder utility for analog/mixed-signal stimulus,
selection, and readout paths.

## Form-Specific Requirements

This is a DUT implementation task. Return only the Verilog-A source artifact
for the encoder; do not generate a Spectre testbench or auxiliary files.

## Public Verilog-A Interface

Define module `onehot_to_bin_16b` with vector electrical ports in this exact order:

```verilog
module onehot_to_bin_16b(
    input electrical [15:0] oh,
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

Treat `oh[15:0]` as voltage-coded logic using `vth`. Encode a 16-line one-hot
input into binary index `b[3:0]`, with `oh[i]` mapping to unsigned code `i` and
`b[0]` as the least significant bit. Drive `valid` high only when exactly one
input is high. For zero-hot or multi-hot inputs, drive `valid` low and drive
`b[3:0]` to zero.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A
contributions. Preserve the public bus bit order. Write the model so that
electrical vector-port access is legal in Cadence Spectre; constant-index
expansion or generate-time static expansion is acceptable.

## Output Contract

Return exactly one source artifact named `onehot_to_bin_16b.va`. Do not generate a Spectre testbench.
