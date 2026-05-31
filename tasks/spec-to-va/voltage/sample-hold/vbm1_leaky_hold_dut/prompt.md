# Task: vbm1_leaky_hold_dut

Write a pure voltage-domain Verilog-A module for a leaky sample-and-hold.

The DUT module is `leaky_hold` with ports `sample, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- A rising `sample` edge captures a fixed 0.75 V held level.
- A 1 ns timer applies exponential droop by multiplying the held value by 0.985 while reset is low.
- High `rst` clears the held value; drive `vout` through `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `leaky_hold.va`.
