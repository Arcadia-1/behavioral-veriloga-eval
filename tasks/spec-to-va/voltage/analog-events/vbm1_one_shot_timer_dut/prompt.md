# Task: vbm1_one_shot_timer_dut

Write a pure voltage-domain Verilog-A module for a one-shot pulse timer.

The DUT module is `one_shot_timer` with ports `trig, rst_n, pulse`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Use active-low reset to clear any active or pending pulse.
- On a rising `trig` edge while reset is released, assert `pulse` high and schedule a clear event 8 ns later.
- The public stimulus uses non-overlapping trigger pulses; implement fixed-width pulse behavior for those triggers and drive `pulse` through `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `one_shot_timer.va`.
