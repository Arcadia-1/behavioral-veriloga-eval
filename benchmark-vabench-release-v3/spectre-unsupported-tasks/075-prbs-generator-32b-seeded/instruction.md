# PRBS Generator 32b Seeded

## Task Contract

Implement one Verilog-A DUT file named `prbs_generator_32b.va`. The DUT is a
voltage-domain seeded PRBS/LFSR source utility for analog/mixed-signal
stimulus, converter, link, calibration, and measurement flows.

## Form-Specific Requirements

This is a DUT implementation task. Return only the Verilog-A source artifact
for the PRBS generator; do not generate a Spectre testbench or auxiliary files.

## Public Verilog-A Interface

Define module `prbs_generator_32b` with vector electrical ports in this exact
order:

```verilog
module prbs_generator_32b(
    input electrical clk,
    input electrical rst,
    input electrical load_seed,
    input electrical [0:31] seed,
    output electrical [0:31] out
);
```

Keep the `[0:31]` index direction so bit 0 maps to `seed[0]` and `out[0]`.

## Public Parameter Contract

Expose compatible real parameters named `vdd`, `vth`, and `tr`. Their default
values are `vdd=0.9`, `vth=0.45`, and `tr=20p`. `vdd` is the logic-high output
level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the
output transition rise/fall time.

## Required Behavior

On each rising `clk` threshold crossing, synchronously reset the state when
`rst` is high. The reset state is integer value 1: state bit 0 high and all
other state bits low. Otherwise, when `load_seed` is high, load the matching
`seed[0:31]` bits into the LFSR state; if the seed is all zero, use the reset
state instead. Otherwise advance the deterministic LFSR: feedback is
`state[31]` XOR `state[21]` XOR `state[1]` XOR `state[0]`, state bits shift
toward the higher index, and feedback loads into `state[0]`. Drive `out[0:31]`
with the current state bits.

## Modeling Constraints

Use `cross` on the rising `clk` threshold for state updates. Drive high outputs
near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.
Preserve the public bus bit order. Write the model so that electrical
vector-port access is legal in Cadence Spectre; constant-index expansion or
generate-time static expansion is acceptable.

## Output Contract

Return exactly one source artifact named `prbs_generator_32b.va`. Do not generate a Spectre testbench.
