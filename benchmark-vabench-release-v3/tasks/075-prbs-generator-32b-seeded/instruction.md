# PRBS Generator 32b Seeded

Implement `prbs_generator_32b.va` in Verilog-A.

## Interface

```verilog
module prbs_generator_32b(clk, rst, load_seed, seed0, seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8, seed9, seed10, seed11, seed12, seed13, seed14, seed15, seed16, seed17, seed18, seed19, seed20, seed21, seed22, seed23, seed24, seed25, seed26, seed27, seed28, seed29, seed30, seed31, out0, out1, out2, out3, out4, out5, out6, out7, out8, out9, out10, out11, out12, out13, out14, out15, out16, out17, out18, out19, out20, out21, out22, out23, out24, out25, out26, out27, out28, out29, out30, out31);
```

Inputs: `clk, rst, load_seed, seed0, seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8, seed9, seed10, seed11, seed12, seed13, seed14, seed15, seed16, seed17, seed18, seed19, seed20, seed21, seed22, seed23, seed24, seed25, seed26, seed27, seed28, seed29, seed30, seed31`.
Outputs: `out0, out1, out2, out3, out4, out5, out6, out7, out8, out9, out10, out11, out12, out13, out14, out15, out16, out17, out18, out19, out20, out21, out22, out23, out24, out25, out26, out27, out28, out29, out30, out31`.

## Required Behavior

On each rising `clk`, reset state to 1 when `rst` is high; otherwise load nonzero `seed[31:0]` when `load_seed` is high; otherwise advance a deterministic LFSR: feedback = state[31] XOR state[21] XOR state[1] XOR state[0], shift state bits toward the higher index, and load feedback into state[0]. Drive `out[31:0]` with the current state bits.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
