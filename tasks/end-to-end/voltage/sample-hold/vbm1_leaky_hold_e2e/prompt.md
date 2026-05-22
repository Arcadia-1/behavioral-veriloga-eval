# Task: vbm1_leaky_hold_e2e

Write both the Verilog-A DUT and Spectre testbench for a leaky sample-and-hold.

The DUT module is `leaky_hold` with ports `sample, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- A rising `sample` edge captures a fixed 0.75 V held level.
- A 1 ns timer applies exponential droop by multiplying the held value by 0.985 while reset is low.
- High `rst` clears the held value; drive `vout` through `transition()`.

Required testbench behavior:
- Generate capture events, an observable droop interval, reset clearing, and a second capture.
- Save `sample`, `rst`, and `vout`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `leaky_hold.va` and `tb_leaky_hold_ref.scs`.
