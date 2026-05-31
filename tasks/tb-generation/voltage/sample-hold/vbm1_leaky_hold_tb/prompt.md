# Task: vbm1_leaky_hold_tb

Write a Spectre testbench for a leaky sample-and-hold DUT.

The DUT module is `leaky_hold` with ports `sample, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `leaky_hold.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- A rising `sample` edge captures a fixed 0.75 V held level.
- A 1 ns timer applies exponential droop by multiplying the held value by 0.985 while reset is low.
- High `rst` clears the held value; drive `vout` through `transition()`.

Stimulus and observability requirements:
- Generate capture events, an observable droop interval, reset clearing, and a second capture.
- Save `sample`, `rst`, and `vout`.

Return exactly one Spectre testbench file named `tb_leaky_hold_ref.scs`.
