# Task: vbm1_debounce_latch_dut

Write a pure voltage-domain Verilog-A module for a debounced latch with delayed qualification.

The DUT module is `debounce_latch` with ports `sig, rst_n, out`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Use active-low reset `rst_n`; reset forces `out` low and cancels any pending qualification.
- On a rising `sig` edge while reset is released, arm a 12 ns qualification timer.
- On the timer event, set `out` high only if `sig` and `rst_n` are still high; falling `sig` clears or cancels the output.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `debounce_latch.va`.
