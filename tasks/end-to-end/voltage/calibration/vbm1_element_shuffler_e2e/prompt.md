# Task: vbm1_element_shuffler_e2e

Write both the Verilog-A DUT and Spectre testbench for a clocked one-hot
element shuffler.

The DUT module must be named `element_shuffler` and use electrical ports `clk`,
`rst_n`, `out0`, `out1`, `out2`, and `out3`. `rst_n` is active low. After reset,
successive rising clock edges should produce one-hot active outputs in the
public sequence `out1`, `out2`, `out3`, `out0`, then repeat.

The testbench must stimulate reset and enough rising clock edges to observe at
least six post-reset states, save all public observables, and run a transient
analysis suitable for fixed-time sequence checks.

Return `element_shuffler.va` and `tb_element_shuffler_ref.scs`.
