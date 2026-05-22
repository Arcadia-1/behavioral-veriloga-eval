# Task: vbm1_rotating_element_selector_e2e

Write both the Verilog-A DUT and Spectre testbench for a rotating one-hot
element selector.

The DUT module must be named `rotating_element_selector` and use electrical
ports `clk`, `rst_n`, `sel0`, `sel1`, `sel2`, and `sel3`. `rst_n` is active low.
After reset, successive rising clock edges should produce the active selector
sequence `sel1`, `sel2`, `sel3`, `sel0`, then repeat.

The testbench must stimulate reset and enough rising clock edges to observe at
least six post-reset states, save all public observables, and run a transient
analysis suitable for fixed-time sequence checks.

Return exactly two files: `rotating_element_selector.va` and `tb_rotating_element_selector_ref.scs`.
