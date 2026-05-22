# Task: vbm1_one_shot_timer_tb

Write a Spectre testbench for a one-shot pulse timer DUT.

The DUT module is `one_shot_timer` with ports `trig, rst_n, pulse`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `one_shot_timer.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use active-low reset to clear any active or pending pulse.
- On a rising `trig` edge while reset is released, assert `pulse` high and schedule a clear event 8 ns later.
- The public stimulus uses non-overlapping trigger pulses; implement fixed-width pulse behavior for those triggers and drive `pulse` through `transition()`.

Stimulus and observability requirements:
- Drive multiple trigger events with reset released and include windows before, during, and after each pulse.
- Save `trig`, `rst_n`, and `pulse`.

Return exactly one Spectre testbench file named `tb_one_shot_timer_ref.scs`.
