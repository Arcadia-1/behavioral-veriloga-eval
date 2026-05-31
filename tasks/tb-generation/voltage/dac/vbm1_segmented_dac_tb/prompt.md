# Task: vbm1_segmented_dac_tb

Write a Spectre testbench for a Verilog-A module named `segmented_dac` with
ports `b0 b1 t0 t1 t2 aout`.

The testbench should apply a small sequence of binary and thermometer input
codes that demonstrates monotonic output levels and the four-LSB weight of each
thermometer segment. Save all public inputs and `aout`. Use transient timing
that leaves safe sample windows away from code transitions.

Return exactly one Spectre testbench file named `tb_segmented_dac_ref.scs`.
