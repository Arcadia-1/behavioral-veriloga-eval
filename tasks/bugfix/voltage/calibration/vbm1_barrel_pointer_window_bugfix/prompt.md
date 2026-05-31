# Task: vbm1_barrel_pointer_window_bugfix

The provided voltage-domain rotating barrel-pointer window generator has a
window mapping bug: one output duplicates another adjacent window and loses the
wrap-around pair. Fix the design so exactly two adjacent window outputs are high
for each pointer position, including the wrap-around window.

The fixed module must be named `barrel_pointer_window` and use electrical ports
`clk`, `rst_n`, `win0`, `win1`, `win2`, and `win3`. Reset should return the
pointer to its initial state. While reset is released, rising clock edges should
advance the pointer through the four adjacent two-window states.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
