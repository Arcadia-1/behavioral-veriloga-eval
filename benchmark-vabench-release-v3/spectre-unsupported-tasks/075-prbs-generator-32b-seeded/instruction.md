# PRBS Generator 32b Seeded

## Task Contract

Implement one Verilog-A DUT file named `prbs_generator_32b.va`.

The DUT is a voltage-domain seeded PRBS support generator for analog/mixed-signal testbenches.

## Form-Specific Requirements

This is a DUT implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Define module `prbs_generator_32b` with electrical ports in this exact order:

```verilog
module prbs_generator_32b(
    input electrical clk,
    input electrical rst,
    input electrical load_seed,
    input electrical [0:31] seed,
    output electrical [0:31] out
);
```

The supplied Spectre harness connects the 32 seed nodes and 32 output nodes positionally. Keep the `[0:31]` index direction so `seed0` maps to `seed[0]` and `out0` maps to `out[0]`.

## Public Parameter Contract

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. `vdd` is the logic-high output level, 0 V is logic low, `vth` is the input decision threshold, and `tr` is the output transition rise/fall time.

## Required Behavior

On each rising `clk`, reset state to 1 when `rst` is high; otherwise load nonzero `seed[31:0]` when `load_seed` is high; otherwise advance a deterministic LFSR: feedback is `state[31]` XOR `state[21]` XOR `state[1]` XOR `state[0]`, state bits shift toward the higher index, and feedback loads into `state[0]`. Drive `out[31:0]` with the current state bits.

## Modeling Constraints

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Use `cross` on the rising clock threshold for state updates.

For Spectre compatibility, access electrical vector ports with constant indices or generate-time static expansion. Do not use runtime/procedural integer indices such as `V(seed[i])` or `V(out[i])` inside analog procedural loops.

## Output Contract

Return exactly one source artifact named `prbs_generator_32b.va`.
