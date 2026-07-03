# PRBS Generator 32b Seeded

Implement `prbs_generator_32b.va` in Verilog-A.

## Interface

```verilog
module prbs_generator_32b(
    input electrical clk,
    input electrical rst,
    input electrical load_seed,
    input electrical [0:31] seed,
    output electrical [0:31] out
);
```

Inputs: `clk`, `rst`, `load_seed`, and `seed[0:31]`.
Outputs: `out[0:31]`.

The supplied Spectre harness connects the 32 seed nodes and 32 output nodes
positionally. Keep the `[0:31]` index direction so `seed0` maps to `seed[0]`
and `out0` maps to `out[0]`.

## Required Behavior

On each rising `clk`, reset state to 1 when `rst` is high; otherwise load nonzero `seed[31:0]` when `load_seed` is high; otherwise advance a deterministic LFSR: feedback = state[31] XOR state[21] XOR state[1] XOR state[0], shift state bits toward the higher index, and load feedback into state[0]. Drive `out[31:0]` with the current state bits.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
