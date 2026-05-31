# Task: vbm1_one_shot_timer_e2e

Write both the Verilog-A DUT and Spectre testbench for a one-shot pulse timer.

The DUT module is `one_shot_timer` with ports `trig, rst_n, pulse`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use active-low reset to clear any active or pending pulse.
- On a rising `trig` edge while reset is released, assert `pulse` high and schedule a clear event 8 ns later.
- The public stimulus uses non-overlapping trigger pulses; implement fixed-width pulse behavior for those triggers and drive `pulse` through `transition()`.

Required testbench behavior:
- Drive multiple trigger events with reset released and include windows before, during, and after each pulse.
- Save `trig`, `rst_n`, and `pulse`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `one_shot_timer.va` and `tb_one_shot_timer_ref.scs`.
