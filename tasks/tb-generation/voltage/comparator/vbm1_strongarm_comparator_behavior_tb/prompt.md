# Task: vbm1_strongarm_comparator_behavior_tb

Write a Spectre testbench for a Verilog-A module named `cmp_strongarm` with
ports `CLK VINN VINP DCMPN DCMPP LP LM VSS VDD`.

The testbench should provide 0.9 V supply rails, a 1 GHz clock, and a small
differential input around common-mode 0.45 V. The input polarity should be
positive for the first two clock decisions and negative for the next two. Save
the clock, differential inputs, and comparator outputs using plain signal names.
Use a transient stop time that is not exactly on the final input transition.

Return exactly one Spectre testbench file named `tb_cmp_strongarm_ref.scs`.
