# Task: vbm1_slew_rate_limiter_e2e

Write both the Verilog-A DUT and Spectre testbench for a discrete slew-rate limiter.

The DUT module is `slew_rate_limiter` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use a 1 ns timer update and move the internal output toward `vin` by at most 0.015 V per update.
- Limit both rising and falling changes and drive `vout` with `transition()`.

Required testbench behavior:
- Apply a large upward step, hold, then a downward step.
- Save `vin` and `vout` to verify limited rising and falling slopes and eventual settling.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `slew_rate_limiter.va` and `tb_slew_rate_limiter_ref.scs`.
