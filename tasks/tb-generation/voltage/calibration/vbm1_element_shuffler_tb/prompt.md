# Task: vbm1_element_shuffler_tb

Write a Spectre testbench for a Verilog-A module named `element_shuffler` with
ports `clk rst_n out0 out1 out2 out3`.

The testbench should apply an active-low reset and then clock the DUT through at
least six observable post-reset states. Save `clk`, `rst_n`, and all four
outputs. Use a transient analysis with enough stop time and maxstep resolution
for fixed-time one-hot sequence checking.

Return exactly one Spectre testbench file named `tb_element_shuffler_ref.scs`.
