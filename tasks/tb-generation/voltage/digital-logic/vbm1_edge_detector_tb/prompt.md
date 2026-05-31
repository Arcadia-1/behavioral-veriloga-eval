# Task: vbm1_edge_detector_tb

Write a Spectre testbench for a Verilog-A module named `edge_detector` with
ports `sig rst_n pulse`.

The testbench should apply active-low reset, then drive multiple rising and
falling transitions on `sig`. Save `sig`, `rst_n`, and `pulse`. Use a transient
analysis with enough stop time and maxstep resolution for fixed-time pulse
checks.

Return exactly one Spectre testbench file named `tb_edge_detector_ref.scs`.
