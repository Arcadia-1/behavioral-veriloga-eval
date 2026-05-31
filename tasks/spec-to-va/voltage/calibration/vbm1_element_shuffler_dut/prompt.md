# Task: vbm1_element_shuffler_dut

Write a pure voltage-domain Verilog-A module named `element_shuffler`.

The module has electrical ports `clk`, `rst_n`, `out0`, `out1`, `out2`, and
`out3`. `rst_n` is active low. On reset, return to the initial selection. On
each rising edge of `clk` while reset is released, advance through a deterministic
four-step shuffle order. Exactly one output is high at a time, driven as a
0/0.9 V logic level with smoothed transitions.

The public observable sequence after reset is released is:

- first sampled state: `out1` high
- then `out2`
- then `out3`
- then `out0`
- then the sequence repeats

Use voltage contributions only. Do not use current contributions, `ddt()`, or
`idt()`.

Return exactly one complete Verilog-A file named `element_shuffler.va`.
