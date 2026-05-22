# Task: vbm1_debounce_latch_tb

Write a Spectre testbench for a debounced latch with delayed qualification DUT.

The DUT module is `debounce_latch` with ports `sig, rst_n, out`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `debounce_latch.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use active-low reset `rst_n`; reset forces `out` low and cancels any pending qualification.
- On a rising `sig` edge while reset is released, arm a 12 ns qualification timer.
- On the timer event, set `out` high only if `sig` and `rst_n` are still high; falling `sig` clears or cancels the output.

Stimulus and observability requirements:
- Create short rejected pulses and longer accepted pulses on `sig` after reset releases.
- Run long enough to observe at least one rejected pulse and one qualified high output.
- Save `sig`, `rst_n`, and `out`.

Return exactly one Spectre testbench file named `tb_debounce_latch_ref.scs`.
