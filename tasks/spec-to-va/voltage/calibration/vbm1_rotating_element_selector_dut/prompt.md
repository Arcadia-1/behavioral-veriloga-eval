# Task: vbm1_rotating_element_selector_dut

Write a pure voltage-domain Verilog-A module named `rotating_element_selector`.

The module has electrical ports `clk`, `rst_n`, `sel0`, `sel1`, `sel2`, and
`sel3`. `rst_n` is active low. On reset, return to selector state 0. On each
rising edge of `clk` while reset is released, advance the selector modulo 4.
Exactly one selector output should be high at a time, driven as a 0/0.9 V logic
level with smoothed transitions.

The public observable sequence after reset is released is `sel1`, `sel2`,
`sel3`, `sel0`, then repeat.

Use voltage contributions only. Do not use current contributions, `ddt()`, or
`idt()`.

Return exactly one complete Verilog-A file named `rotating_element_selector.va`.
