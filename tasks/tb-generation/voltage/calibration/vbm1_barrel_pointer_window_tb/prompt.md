# Task: vbm1_barrel_pointer_window_tb

Write a Spectre testbench for a Verilog-A module named
`barrel_pointer_window` with ports `clk rst_n win0 win1 win2 win3`.

The testbench should exercise an active-low reset followed by several rising
clock edges so the two-adjacent-window sequence can be observed. Save `clk`,
`rst_n`, and all four `win*` outputs. Use a transient stop time long enough to
observe at least six post-reset window states, with `maxstep` small enough for
stable event checking.

Return exactly one Spectre testbench file named `tb_barrel_pointer_window_ref.scs`.
