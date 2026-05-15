# Task: vbm1_barrel_pointer_window_dut

Write a pure voltage-domain Verilog-A module named `barrel_pointer_window`.

The module implements a clocked 4-state barrel pointer with two adjacent active
window outputs. Ports are `clk`, `rst_n`, `win0`, `win1`, `win2`, and `win3`.
All ports are electrical. `rst_n` is active low. On reset, return the pointer to
state 0. On each rising edge of `clk` while reset is released, advance the state
modulo 4.

Drive the window outputs as 0/0.9 V logic levels with smoothed voltage
transitions:

- state 0: `win0` and `win1` high
- state 1: `win1` and `win2` high
- state 2: `win2` and `win3` high
- state 3: `win3` and `win0` high

Use voltage contributions only. Do not use current contributions, `ddt()`, or
`idt()`.

Return exactly one complete Verilog-A file named `barrel_pointer_window.va`.
