# Task: vbm1_debounce_latch_e2e

Write both the Verilog-A DUT and Spectre testbench for a debounced latch with delayed qualification.

The DUT module is `debounce_latch` with ports `sig, rst_n, out`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use active-low reset `rst_n`; reset forces `out` low and cancels any pending qualification.
- On a rising `sig` edge while reset is released, arm a 12 ns qualification timer.
- On the timer event, set `out` high only if `sig` and `rst_n` are still high; falling `sig` clears or cancels the output.

Required testbench behavior:
- Create short rejected pulses and longer accepted pulses on `sig` after reset releases.
- Run long enough to observe at least one rejected pulse and one qualified high output.
- Save `sig`, `rst_n`, and `out`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `debounce_latch.va` and `tb_debounce_latch_ref.scs`.
