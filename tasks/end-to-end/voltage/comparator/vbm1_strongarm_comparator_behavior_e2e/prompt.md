# Task: vbm1_strongarm_comparator_behavior_e2e

Write both the Verilog-A DUT and Spectre testbench for a clocked StrongArm-style
comparator.

The DUT module must be named `cmp_strongarm` and use electrical ports `CLK`,
`VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, and `VDD`. On rising clock
edges, compare `VINP - VINN` with optional `voffset`; on falling clock edges,
reset both comparator outputs low. Drive `DCMPP` and `DCMPN` as complementary
0/0.9 V logic outputs.

The testbench should use 0.9 V supplies, a 1 GHz clock, and a small differential
input that produces two positive decisions followed by two negative decisions.
Save the clock, inputs, and outputs. Keep the transient stop time away from a
source transition boundary.

Return `cmp_strongarm.va` and `tb_cmp_strongarm_ref.scs`.
