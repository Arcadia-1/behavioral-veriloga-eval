# Task: vbm1_rotating_element_selector_tb

Write a Spectre testbench for a Verilog-A module named
`rotating_element_selector` with ports `clk rst_n sel0 sel1 sel2 sel3`.

The testbench should apply an active-low reset and then clock the DUT through at
least six observable post-reset states. Save `clk`, `rst_n`, and all four
selector outputs. Use a transient analysis with enough stop time and maxstep
resolution for fixed-time one-hot sequence checking.

Return exactly one Spectre testbench file named `tb_rotating_element_selector_ref.scs`.
